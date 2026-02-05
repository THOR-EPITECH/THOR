import { ArrowRight, Brain, Target, Lightbulb, Code, Settings, CheckCircle2 } from 'lucide-react';

function CodeBlock({ children, title }: { children: string; title?: string }) {
  return (
    <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0d0d0d]">
      {title && (
        <div className="px-4 py-2 bg-white/5 border-b border-white/5 text-xs text-neutral-400">
          {title}
        </div>
      )}
      <pre className="p-4 overflow-x-auto">
        <code className="text-sm text-neutral-300">{children}</code>
      </pre>
    </div>
  );
}

export default function DocsNLP() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Pipeline</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">NLP (spaCy)</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Natural Language Processing</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Module d'analyse du langage naturel utilisant spaCy pour extraire 
          l'origine et la destination des requêtes de voyage.
        </p>
      </div>

      {/* How it works */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Comment ça fonctionne ?</h2>
        <div className="prose prose-invert max-w-none mb-6">
          <p className="text-neutral-400">
            Le module NLP analyse le texte transcrit pour identifier les entités géographiques 
            (villes, gares) et déterminer leur rôle dans la requête (origine ou destination). 
            Il combine plusieurs techniques pour une extraction robuste.
          </p>
        </div>

        <div className="space-y-4">
          <div className="p-5 rounded-xl bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <Target className="w-4 h-4 text-purple-400" />
              </div>
              <h3 className="font-semibold">1. Reconnaissance d'entités (NER)</h3>
            </div>
            <p className="text-sm text-neutral-400">
              spaCy identifie les entités de type <code className="px-1.5 py-0.5 bg-white/10 rounded">LOC</code> (locations) 
              dans le texte. Ces entités correspondent généralement aux noms de villes ou de gares.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <Code className="w-4 h-4 text-purple-400" />
              </div>
              <h3 className="font-semibold">2. Patterns regex</h3>
            </div>
            <p className="text-sm text-neutral-400">
              Des expressions régulières identifient les structures syntaxiques comme 
              "de X à Y", "depuis X vers Y", "partir de X pour Y", etc.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <Lightbulb className="w-4 h-4 text-purple-400" />
              </div>
              <h3 className="font-semibold">3. Résolution contextuelle</h3>
            </div>
            <p className="text-sm text-neutral-400">
              Les entités sont associées à leur rôle (origine/destination) en fonction 
              de leur position relative aux mots-clés identifiés par les patterns.
            </p>
          </div>
        </div>
      </div>

      {/* Extraction patterns */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Patterns d'extraction</h2>
        
        <div className="rounded-xl border border-white/10 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Pattern</th>
                <th className="text-left p-4 font-medium">Exemple</th>
                <th className="text-left p-4 font-medium">Origine</th>
                <th className="text-left p-4 font-medium">Destination</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr>
                <td className="p-4"><code className="text-purple-400">de X à Y</code></td>
                <td className="p-4 text-neutral-400">"de Paris à Lyon"</td>
                <td className="p-4 text-green-400">Paris</td>
                <td className="p-4 text-blue-400">Lyon</td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-purple-400">depuis X vers Y</code></td>
                <td className="p-4 text-neutral-400">"depuis Marseille vers Nice"</td>
                <td className="p-4 text-green-400">Marseille</td>
                <td className="p-4 text-blue-400">Nice</td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-purple-400">partir de X pour Y</code></td>
                <td className="p-4 text-neutral-400">"partir de Bordeaux pour Toulouse"</td>
                <td className="p-4 text-green-400">Bordeaux</td>
                <td className="p-4 text-blue-400">Toulouse</td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-purple-400">aller à Y</code></td>
                <td className="p-4 text-neutral-400">"aller à Strasbourg"</td>
                <td className="p-4 text-neutral-500">—</td>
                <td className="p-4 text-blue-400">Strasbourg</td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-purple-400">X - Y</code></td>
                <td className="p-4 text-neutral-400">"Paris - Bordeaux"</td>
                <td className="p-4 text-green-400">Paris</td>
                <td className="p-4 text-blue-400">Bordeaux</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Configuration */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Settings className="w-6 h-6 text-neutral-400" />
          Configuration
        </h2>
        
        <CodeBlock title="configs/nlp/spacy_base.yaml">{`name: spacy
model_name: fr_core_news_md
use_gpu: false
confidence_threshold: 0.5`}</CodeBlock>

        <div className="mt-6 space-y-4">
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center justify-between mb-2">
              <code className="text-sm text-purple-400">model_name</code>
              <span className="text-xs text-neutral-500">string</span>
            </div>
            <p className="text-sm text-neutral-400">
              Modèle spaCy à utiliser. Options : fr_core_news_sm, fr_core_news_md, fr_core_news_lg.
            </p>
          </div>
          
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center justify-between mb-2">
              <code className="text-sm text-purple-400">confidence_threshold</code>
              <span className="text-xs text-neutral-500">float</span>
            </div>
            <p className="text-sm text-neutral-400">
              Seuil minimum de confiance pour valider l'extraction. Entre 0 et 1.
            </p>
          </div>
        </div>
      </div>

      {/* Usage */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Utilisation</h2>
        
        <h3 className="font-semibold mb-3">Via la CLI</h3>
        <CodeBlock title="Terminal">{`python3 -m src.cli.nlp \\
  --text "Je voudrais aller de Paris à Marseille" \\
  --model spacy`}</CodeBlock>

        <h3 className="font-semibold mb-3 mt-6">Via Python</h3>
        <CodeBlock title="Python">{`from src.nlp.models.spacy_fr import SpacyNLP

# Initialiser le modèle
nlp = SpacyNLP(model_name="fr_core_news_md")

# Analyser un texte
result = nlp.extract_route("Je veux aller de Lyon à Nice")

print(result.origin)      # "Lyon"
print(result.destination) # "Nice"
print(result.confidence)  # 0.85
print(result.is_valid)    # True`}</CodeBlock>
      </div>

      {/* Output example */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Exemple de sortie</h2>
        <CodeBlock title="Résultat JSON">{`{
  "origin": "Lyon",
  "destination": "Nice",
  "is_valid": true,
  "confidence": 0.85,
  "entities": [
    { "text": "Lyon", "label": "LOC", "start": 21, "end": 25 },
    { "text": "Nice", "label": "LOC", "start": 28, "end": 32 }
  ],
  "method": "pattern_de_a"
}`}</CodeBlock>
      </div>

      {/* Models comparison */}
      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
        <h2 className="text-xl font-bold mb-4">Modèles disponibles</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 rounded-lg bg-green-500/5 border border-green-500/10">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-4 h-4 text-green-400" />
              <div>
                <span className="font-medium">spaCy</span>
                <span className="ml-2 px-2 py-0.5 rounded text-xs bg-green-500/20 text-green-400">recommandé</span>
              </div>
            </div>
            <span className="text-sm text-neutral-400">Rapide et précis</span>
          </div>
          <div className="flex items-center justify-between p-4 rounded-lg bg-white/5">
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full border border-neutral-500" />
              <span className="font-medium text-neutral-300">Transformers (finetuné)</span>
            </div>
            <span className="text-sm text-neutral-500">Plus précis, plus lent</span>
          </div>
          <div className="flex items-center justify-between p-4 rounded-lg bg-white/5">
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full border border-neutral-500" />
              <span className="font-medium text-neutral-300">Regex avancé</span>
            </div>
            <span className="text-sm text-neutral-500">Léger, moins flexible</span>
          </div>
        </div>
      </div>
    </div>
  );
}
