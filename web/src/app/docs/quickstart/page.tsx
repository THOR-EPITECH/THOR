import { ArrowRight, Play, Mic, Type, Terminal } from 'lucide-react';
import Link from 'next/link';

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

export default function DocsQuickstart() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Démarrage rapide</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Démarrage rapide</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Apprenez à utiliser THOR en quelques minutes avec ces exemples pratiques.
        </p>
      </div>

      {/* Web Interface */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Play className="w-5 h-5 text-blue-400" />
          </div>
          Interface Web
        </h2>
        
        <div className="space-y-6">
          <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Type className="w-4 h-4 text-neutral-400" />
              Recherche textuelle
            </h3>
            <ol className="space-y-3 text-sm text-neutral-400">
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">1</span>
                <span>Accédez à <code className="px-2 py-0.5 bg-white/5 rounded">http://localhost:3000</code></span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">2</span>
                <span>Tapez votre recherche en langage naturel, par exemple : <code className="px-2 py-0.5 bg-white/5 rounded">"Je veux aller de Paris à Lyon"</code></span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">3</span>
                <span>Appuyez sur Entrée ou cliquez sur la flèche</span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">4</span>
                <span>Visualisez l'itinéraire optimal sur la carte avec les détails du trajet</span>
              </li>
            </ol>
          </div>

          <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Mic className="w-4 h-4 text-neutral-400" />
              Recherche vocale
            </h3>
            <ol className="space-y-3 text-sm text-neutral-400">
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">1</span>
                <span>Cliquez sur l'icône microphone dans la barre de recherche</span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">2</span>
                <span>Autorisez l'accès au microphone si demandé</span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">3</span>
                <span>Parlez naturellement : <em>"Comment aller de Bordeaux à Marseille ?"</em></span>
              </li>
              <li className="flex gap-3">
                <span className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-xs flex-shrink-0">4</span>
                <span>Cliquez à nouveau sur le micro pour arrêter l'enregistrement</span>
              </li>
            </ol>
            <div className="mt-4 p-4 rounded-lg bg-purple-500/10 border border-purple-500/20">
              <p className="text-sm text-purple-200/70">
                La recherche vocale utilise la pipeline complète : Whisper transcrit votre voix, 
                spaCy analyse le texte, et Dijkstra trouve l'itinéraire optimal.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CLI Examples */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Terminal className="w-5 h-5 text-green-400" />
          </div>
          Ligne de commande
        </h2>

        <div className="space-y-6">
          <div>
            <h3 className="font-semibold mb-3">Pipeline complète (audio)</h3>
            <CodeBlock title="Terminal">{`python3 -m src.cli.pipeline \\
  --audio data/raw/audio/sample_000160.wav \\
  --stt-model whisper \\
  --nlp-model spacy \\
  --pathfinding-model dijkstra`}</CodeBlock>
          </div>

          <div>
            <h3 className="font-semibold mb-3">Recherche de route directe</h3>
            <CodeBlock title="Terminal">{`python3 -m src.cli.pathfinding \\
  --origin "Paris" \\
  --destination "Bordeaux" \\
  --model dijkstra`}</CodeBlock>
          </div>

          <div>
            <h3 className="font-semibold mb-3">Analyse NLP seule</h3>
            <CodeBlock title="Terminal">{`python3 -m src.cli.nlp \\
  --text "Je voudrais partir de Lyon pour aller à Nice" \\
  --model spacy`}</CodeBlock>
          </div>
        </div>
      </div>

      {/* Example output */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Exemple de résultat</h2>
        <CodeBlock title="Résultat pipeline Toulouse → Bordeaux">{`=== Résultats ===
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
      </div>

      {/* Next steps */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-white/5 to-white/[0.02] border border-white/10">
        <h3 className="font-semibold mb-4">Prochaines étapes</h3>
        <div className="grid gap-3">
          <Link 
            href="/docs/pipeline"
            className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors group"
          >
            <span className="text-sm text-neutral-300">Comprendre la pipeline en détail</span>
            <ArrowRight className="w-4 h-4 text-neutral-500 group-hover:text-white transition-colors" />
          </Link>
          <Link 
            href="/docs/api"
            className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors group"
          >
            <span className="text-sm text-neutral-300">Explorer l'API REST</span>
            <ArrowRight className="w-4 h-4 text-neutral-500 group-hover:text-white transition-colors" />
          </Link>
          <Link 
            href="/docs/pathfinding"
            className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors group"
          >
            <span className="text-sm text-neutral-300">Découvrir l'algorithme de pathfinding</span>
            <ArrowRight className="w-4 h-4 text-neutral-500 group-hover:text-white transition-colors" />
          </Link>
        </div>
      </div>
    </div>
  );
}
