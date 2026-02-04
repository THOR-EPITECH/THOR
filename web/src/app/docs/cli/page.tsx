import { ArrowRight, Terminal, Play, Settings, FileText, Mic, Brain, Route } from 'lucide-react';

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

function CLICommand({ title, description, icon: Icon, color, children }: {
  title: string;
  description: string;
  icon: any;
  color: string;
  children: React.ReactNode;
}) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-500/10 text-blue-400',
    purple: 'bg-purple-500/10 text-purple-400',
    green: 'bg-green-500/10 text-green-400',
    orange: 'bg-orange-500/10 text-orange-400',
  };

  return (
    <div className="mb-10">
      <div className="flex items-center gap-3 mb-4">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-semibold text-lg">{title}</h3>
          <p className="text-sm text-neutral-400">{description}</p>
        </div>
      </div>
      {children}
    </div>
  );
}

export default function DocsCLI() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Commandes CLI</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Commandes CLI</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Interface en ligne de commande pour tester et utiliser chaque module de THOR individuellement.
        </p>
      </div>

      {/* Pipeline */}
      <CLICommand
        title="Pipeline complète"
        description="Exécute la chaîne complète : Audio → STT → NLP → Pathfinding"
        icon={Play}
        color="orange"
      >
        <CodeBlock title="Syntaxe">{`python3 -m src.cli.pipeline [OPTIONS]`}</CodeBlock>
        
        <h4 className="font-medium mt-6 mb-3">Options</h4>
        <div className="rounded-xl border border-white/10 overflow-hidden mb-4">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-3 font-medium">Option</th>
                <th className="text-left p-3 font-medium">Description</th>
                <th className="text-left p-3 font-medium">Défaut</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr>
                <td className="p-3"><code className="text-orange-400">--audio</code></td>
                <td className="p-3 text-neutral-400">Chemin vers le fichier audio</td>
                <td className="p-3 text-neutral-500">requis</td>
              </tr>
              <tr>
                <td className="p-3"><code className="text-orange-400">--stt-model</code></td>
                <td className="p-3 text-neutral-400">Modèle STT à utiliser</td>
                <td className="p-3 text-neutral-500">whisper</td>
              </tr>
              <tr>
                <td className="p-3"><code className="text-orange-400">--nlp-model</code></td>
                <td className="p-3 text-neutral-400">Modèle NLP à utiliser</td>
                <td className="p-3 text-neutral-500">spacy</td>
              </tr>
              <tr>
                <td className="p-3"><code className="text-orange-400">--pathfinding-model</code></td>
                <td className="p-3 text-neutral-400">Modèle de pathfinding</td>
                <td className="p-3 text-neutral-500">dijkstra</td>
              </tr>
              <tr>
                <td className="p-3"><code className="text-orange-400">--output</code></td>
                <td className="p-3 text-neutral-400">Dossier de sortie des résultats</td>
                <td className="p-3 text-neutral-500">results/pipeline/</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h4 className="font-medium mt-4 mb-3">Exemple</h4>
        <CodeBlock title="Terminal">{`python3 -m src.cli.pipeline \\
  --audio data/raw/audio/sample_000160.wav \\
  --stt-model whisper \\
  --nlp-model spacy \\
  --pathfinding-model dijkstra`}</CodeBlock>

        <h4 className="font-medium mt-4 mb-3">Sortie</h4>
        <CodeBlock title="Résultat">{`=== Configuration ===
Modèle STT: whisper
Modèle NLP: spacy
Modèle Pathfinding: dijkstra

=== Résultats ===
Transcription: Je veux voyager de Toulouse à Bordeaux.
Origine: Toulouse
Destination: Bordeaux
Valide: True
Confidence: 0.70

=== Itinéraire ===
⏱️  Temps de trajet: 2h23 (143 min)
📏  Distance totale: 209.5 km
🛤️  Nombre d'étapes: 2

📊 Détails du trajet:
   🚄 [TGV] Toulouse Matabiau → Bordeaux Saint-Jean
      ⏱️ 143 min | 📏 209.5 km | 🚂 17 trains/jour`}</CodeBlock>
      </CLICommand>

      {/* STT */}
      <CLICommand
        title="Speech-to-Text"
        description="Transcrit un fichier audio en texte"
        icon={Mic}
        color="blue"
      >
        <CodeBlock title="Syntaxe">{`python3 -m src.cli.stt [OPTIONS]`}</CodeBlock>
        
        <h4 className="font-medium mt-6 mb-3">Options</h4>
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-blue-400">--audio</code>
            <span className="text-neutral-400">Fichier audio à transcrire</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-blue-400">--model</code>
            <span className="text-neutral-400">Modèle (whisper, vosk)</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-blue-400">--output</code>
            <span className="text-neutral-400">Dossier de sortie</span>
          </div>
        </div>

        <h4 className="font-medium mt-4 mb-3">Exemple</h4>
        <CodeBlock title="Terminal">{`python3 -m src.cli.stt \\
  --audio data/raw/audio/sample.wav \\
  --model whisper \\
  --output results/stt/`}</CodeBlock>
      </CLICommand>

      {/* NLP */}
      <CLICommand
        title="Natural Language Processing"
        description="Analyse un texte pour extraire origine et destination"
        icon={Brain}
        color="purple"
      >
        <CodeBlock title="Syntaxe">{`python3 -m src.cli.nlp [OPTIONS]`}</CodeBlock>
        
        <h4 className="font-medium mt-6 mb-3">Options</h4>
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-purple-400">--text</code>
            <span className="text-neutral-400">Texte à analyser</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-purple-400">--model</code>
            <span className="text-neutral-400">Modèle (spacy, transformers, regex)</span>
          </div>
        </div>

        <h4 className="font-medium mt-4 mb-3">Exemple</h4>
        <CodeBlock title="Terminal">{`python3 -m src.cli.nlp \\
  --text "Je voudrais aller de Lyon à Nice" \\
  --model spacy`}</CodeBlock>
      </CLICommand>

      {/* Pathfinding */}
      <CLICommand
        title="Pathfinding"
        description="Trouve l'itinéraire optimal entre deux villes"
        icon={Route}
        color="green"
      >
        <CodeBlock title="Syntaxe">{`python3 -m src.cli.pathfinding [OPTIONS]`}</CodeBlock>
        
        <h4 className="font-medium mt-6 mb-3">Options</h4>
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-green-400">--origin</code>
            <span className="text-neutral-400">Ville de départ</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-green-400">--destination</code>
            <span className="text-neutral-400">Ville d'arrivée</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
            <code className="text-green-400">--model</code>
            <span className="text-neutral-400">Algorithme (dijkstra)</span>
          </div>
        </div>

        <h4 className="font-medium mt-4 mb-3">Exemple</h4>
        <CodeBlock title="Terminal">{`python3 -m src.cli.pathfinding \\
  --origin "Paris" \\
  --destination "Marseille" \\
  --model dijkstra`}</CodeBlock>
      </CLICommand>

      {/* Scripts */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6">Scripts utilitaires</h2>
        
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-neutral-400" />
              <code className="text-sm text-white">generate_enhanced_graph.py</code>
            </div>
            <p className="text-sm text-neutral-400 mb-3">
              Génère le graphe des liaisons avec temps de trajet réels à partir des données GTFS.
            </p>
            <CodeBlock>{`python3 scripts/generate_enhanced_graph.py`}</CodeBlock>
          </div>

          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-neutral-400" />
              <code className="text-sm text-white">generate_railway_shapes.py</code>
            </div>
            <p className="text-sm text-neutral-400 mb-3">
              Associe les géométries des voies ferrées aux liaisons pour l'affichage cartographique.
            </p>
            <CodeBlock>{`python3 scripts/generate_railway_shapes.py`}</CodeBlock>
          </div>

          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-neutral-400" />
              <code className="text-sm text-white">train_all_nlp_models.py</code>
            </div>
            <p className="text-sm text-neutral-400 mb-3">
              Entraîne tous les modèles NLP sur le dataset annoté.
            </p>
            <CodeBlock>{`python3 scripts/train_all_nlp_models.py`}</CodeBlock>
          </div>
        </div>
      </div>
    </div>
  );
}
