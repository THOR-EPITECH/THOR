import { ArrowRight, Mic, Brain, Route, Zap, FileAudio, FileText, Map } from 'lucide-react';

function FlowStep({ icon: Icon, title, description, color, isLast = false }: { 
  icon: any; 
  title: string; 
  description: string; 
  color: string;
  isLast?: boolean;
}) {
  const colorClasses: Record<string, { bg: string; text: string; border: string }> = {
    blue: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
    purple: { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/20' },
    green: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
    orange: { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20' },
  };
  const c = colorClasses[color] || colorClasses.blue;

  return (
    <div className="flex items-start gap-4">
      <div className="flex flex-col items-center">
        <div className={`w-12 h-12 rounded-xl ${c.bg} flex items-center justify-center`}>
          <Icon className={`w-6 h-6 ${c.text}`} />
        </div>
        {!isLast && <div className="w-px h-8 bg-white/10 my-2" />}
      </div>
      <div className="pt-2">
        <h3 className="font-semibold mb-1">{title}</h3>
        <p className="text-sm text-neutral-400">{description}</p>
      </div>
    </div>
  );
}

export default function DocsPipeline() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Pipeline</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Vue d'ensemble</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Vue d'ensemble de la Pipeline</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Découvrez comment les différents modules de THOR s'enchaînent pour transformer 
          une requête vocale en itinéraire optimisé.
        </p>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Flux de données</h2>
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <FlowStep 
            icon={FileAudio}
            title="1. Entrée Audio"
            description="L'utilisateur enregistre sa demande via le microphone. L'audio est capturé en format WAV pour une compatibilité optimale."
            color="blue"
          />
          <FlowStep 
            icon={Mic}
            title="2. Speech-to-Text (Whisper)"
            description="Le modèle Whisper d'OpenAI transcrit l'audio en texte avec une précision remarquable pour le français."
            color="blue"
          />
          <FlowStep 
            icon={FileText}
            title="3. Texte transcrit"
            description="La transcription brute est transmise au module NLP pour analyse sémantique."
            color="purple"
          />
          <FlowStep 
            icon={Brain}
            title="4. Natural Language Processing (spaCy)"
            description="spaCy analyse le texte pour identifier et extraire l'origine et la destination du voyage."
            color="purple"
          />
          <FlowStep 
            icon={Route}
            title="5. Pathfinding (Dijkstra)"
            description="L'algorithme de Dijkstra calcule l'itinéraire optimal en utilisant les temps de trajet réels et en privilégiant les TGV."
            color="green"
          />
          <FlowStep 
            icon={Map}
            title="6. Résultat"
            description="L'itinéraire complet est retourné avec les détails de chaque segment, les temps, distances et géométries des voies."
            color="green"
            isLast
          />
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Les modules</h2>
        <div className="grid gap-4">
          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-blue-500/10">
                <Mic className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="font-semibold text-lg">STT - Speech-to-Text</h3>
            </div>
            <p className="text-neutral-400 text-sm mb-4">
              Convertit l'audio en texte en utilisant le modèle Whisper d'OpenAI. 
              Supporte plusieurs tailles de modèle (tiny, base, small, medium, large) 
              pour équilibrer précision et performance.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs">Whisper</span>
              <span className="px-3 py-1 rounded-full bg-white/5 text-neutral-400 text-xs">Vosk (alternatif)</span>
            </div>
          </div>

          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <Brain className="w-5 h-5 text-purple-400" />
              </div>
              <h3 className="font-semibold text-lg">NLP - Natural Language Processing</h3>
            </div>
            <p className="text-neutral-400 text-sm mb-4">
              Analyse le texte transcrit pour en extraire les informations pertinentes : 
              ville de départ, ville d'arrivée. Utilise la reconnaissance d'entités nommées 
              et des patterns regex avancés.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 rounded-full bg-purple-500/10 text-purple-400 text-xs">spaCy</span>
              <span className="px-3 py-1 rounded-full bg-white/5 text-neutral-400 text-xs">Transformers (finetuné)</span>
              <span className="px-3 py-1 rounded-full bg-white/5 text-neutral-400 text-xs">Regex avancé</span>
            </div>
          </div>

          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-green-500/10">
                <Route className="w-5 h-5 text-green-400" />
              </div>
              <h3 className="font-semibold text-lg">Pathfinding</h3>
            </div>
            <p className="text-neutral-400 text-sm mb-4">
              Trouve l'itinéraire optimal entre deux gares en utilisant l'algorithme de Dijkstra. 
              Les poids sont basés sur les temps de trajet réels, avec une priorisation des TGV 
              et l'exclusion automatique des gares d'aéroport.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 text-xs">Dijkstra</span>
              <span className="px-3 py-1 rounded-full bg-white/5 text-neutral-400 text-xs">Multi-source</span>
              <span className="px-3 py-1 rounded-full bg-white/5 text-neutral-400 text-xs">TGV prioritaire</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
        <h2 className="text-xl font-bold mb-4">Sources de données</h2>
        <div className="grid gap-3 text-sm">
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
            <span className="text-neutral-300">Gares SNCF</span>
            <code className="text-xs text-neutral-500">dataset_gares.json</code>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
            <span className="text-neutral-300">Liaisons avec temps réels</span>
            <code className="text-xs text-neutral-500">dataset_liaisons_enhanced.json</code>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
            <span className="text-neutral-300">Géométries des voies</span>
            <code className="text-xs text-neutral-500">dataset_liaisons_with_shapes.json</code>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
            <span className="text-neutral-300">Données GTFS SNCF</span>
            <code className="text-xs text-neutral-500">stop_times.txt, trips.txt, etc.</code>
          </div>
        </div>
      </div>
    </div>
  );
}
