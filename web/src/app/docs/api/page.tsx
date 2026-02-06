import { ArrowRight, Server, CheckCircle2, AlertCircle, Lock, Zap } from 'lucide-react';

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

function Badge({ method }: { method: 'GET' | 'POST' }) {
  const colors = {
    GET: 'bg-green-500/20 text-green-400',
    POST: 'bg-blue-500/20 text-blue-400',
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-mono font-medium ${colors[method]}`}>
      {method}
    </span>
  );
}

function Endpoint({ method, path, description, children }: { 
  method: 'GET' | 'POST'; 
  path: string; 
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
      <div className="flex items-center gap-3 mb-3">
        <Badge method={method} />
        <code className="text-sm font-mono">{path}</code>
      </div>
      <p className="text-sm text-neutral-400 mb-4">{description}</p>
      {children}
    </div>
  );
}

export default function DocsAPI() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">API REST</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">API REST</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Documentation complète de l'API Flask exposant les fonctionnalités de la pipeline THOR.
        </p>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Configuration</h2>
        <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-neutral-400">Base URL</span>
            <code className="text-green-400">http://localhost:8000</code>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-neutral-400">Content-Type</span>
            <code className="text-neutral-300">application/json</code>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Endpoints</h2>

        <Endpoint 
          method="GET" 
          path="/api/health"
          description="Vérifie l'état de l'API et des modèles chargés."
        >
          <h4 className="text-sm font-medium mb-2">Réponse</h4>
          <CodeBlock title="200 OK">{`{
  "status": "ok",
  "models": {
    "stt": "whisper",
    "nlp": "spacy",
    "pathfinding": "dijkstra"
  },
  "stations_count": 3247,
  "connections_count": 5842
}`}</CodeBlock>
        </Endpoint>

        <Endpoint 
          method="POST" 
          path="/api/pipeline"
          description="Pipeline complète : Audio → STT → NLP → Pathfinding. Traite un fichier audio et retourne l'itinéraire."
        >
          <h4 className="text-sm font-medium mb-2">Corps de la requête</h4>
          <CodeBlock title="Request Body">{`{
  "audio": "base64_encoded_audio_data",
  "format": "wav"
}`}</CodeBlock>
          
          <h4 className="text-sm font-medium mb-2 mt-4">Paramètres</h4>
          <div className="space-y-2 mb-4">
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
              <code className="text-blue-400">audio</code>
              <span className="text-neutral-400">string (base64) — requis</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
              <code className="text-blue-400">format</code>
              <span className="text-neutral-400">string (wav, mp3, webm) — requis</span>
            </div>
          </div>

          <h4 className="text-sm font-medium mb-2">Réponse</h4>
          <CodeBlock title="200 OK">{`{
  "transcript": "Je veux aller de Paris à Lyon",
  "origin": "Paris",
  "destination": "Lyon",
  "is_valid": true,
  "confidence": 0.85,
  "route": {
    "steps": ["Paris Gare de Lyon", "Lyon Part Dieu"],
    "total_time": 117,
    "total_distance": 390.79,
    "metadata": { ... }
  }
}`}</CodeBlock>
        </Endpoint>

        <Endpoint 
          method="POST" 
          path="/api/search"
          description="Analyse un texte en langage naturel et trouve l'itinéraire correspondant."
        >
          <h4 className="text-sm font-medium mb-2">Corps de la requête</h4>
          <CodeBlock title="Request Body">{`{
  "text": "Je voudrais aller de Bordeaux à Marseille"
}`}</CodeBlock>
          
          <h4 className="text-sm font-medium mb-2 mt-4">Exemple curl</h4>
          <CodeBlock title="Terminal">{`curl -X POST http://localhost:8000/api/search \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Je veux aller de Paris à Lyon"}'`}</CodeBlock>
        </Endpoint>

        <Endpoint 
          method="POST" 
          path="/api/route"
          description="Trouve un itinéraire entre deux villes spécifiées directement."
        >
          <h4 className="text-sm font-medium mb-2">Corps de la requête</h4>
          <CodeBlock title="Request Body">{`{
  "origin": "Paris",
  "destination": "Lyon"
}`}</CodeBlock>
          
          <h4 className="text-sm font-medium mb-2 mt-4">Réponse</h4>
          <CodeBlock title="200 OK">{`{
  "success": true,
  "route": {
    "origin": "Paris",
    "destination": "Lyon",
    "steps": ["Paris Gare de Lyon", "Lyon Part Dieu"],
    "total_time": 117,
    "total_distance": 390.79,
    "metadata": {
      "origin_uic": "87686006",
      "destination_uic": "87723197",
      "segments": [
        {
          "from": "Paris Gare de Lyon",
          "to": "Lyon Part Dieu",
          "temps_min": 117,
          "distance_km": 390.79,
          "type_train": "TGV",
          "geometry": { "type": "LineString", "coordinates": [...] }
        }
      ]
    }
  }
}`}</CodeBlock>
        </Endpoint>

        <Endpoint 
          method="GET" 
          path="/api/stations"
          description="Liste toutes les gares disponibles avec leurs informations."
        >
          <h4 className="text-sm font-medium mb-2">Paramètres de requête</h4>
          <div className="space-y-2 mb-4">
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
              <code className="text-green-400">search</code>
              <span className="text-neutral-400">string — optionnel (filtre par nom)</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 text-sm">
              <code className="text-green-400">limit</code>
              <span className="text-neutral-400">int — optionnel (défaut: 100)</span>
            </div>
          </div>
          
          <h4 className="text-sm font-medium mb-2">Exemple</h4>
          <CodeBlock title="Terminal">{`curl "http://localhost:8000/api/stations?search=paris&limit=10"`}</CodeBlock>
        </Endpoint>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Gestion des erreurs</h2>
        <div className="space-y-4">
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20">
            <div className="flex items-center gap-3 mb-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <code className="text-sm text-red-400">400 Bad Request</code>
            </div>
            <p className="text-sm text-neutral-400">Paramètres manquants ou invalides</p>
          </div>
          
          <div className="p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
            <div className="flex items-center gap-3 mb-2">
              <AlertCircle className="w-4 h-4 text-yellow-400" />
              <code className="text-sm text-yellow-400">404 Not Found</code>
            </div>
            <p className="text-sm text-neutral-400">Gare ou itinéraire non trouvé</p>
          </div>
          
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20">
            <div className="flex items-center gap-3 mb-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <code className="text-sm text-red-400">500 Internal Server Error</code>
            </div>
            <p className="text-sm text-neutral-400">Erreur interne du serveur</p>
          </div>
        </div>

        <CodeBlock title="Format d'erreur">{`{
  "error": "Message d'erreur descriptif",
  "code": "ERROR_CODE",
  "details": { ... }
}`}</CodeBlock>
      </div>

      <div className="p-6 rounded-xl bg-blue-500/5 border border-blue-500/20">
        <h3 className="font-semibold text-blue-400 mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5" />
          Conseils d'utilisation
        </h3>
        <ul className="space-y-3 text-sm text-neutral-400">
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
            <span>Utilisez l'option <code className="px-1.5 py-0.5 bg-blue-500/10 rounded">--preload</code> au lancement pour précharger les modèles</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
            <span>Pour l'audio, préférez le format WAV 16kHz mono pour de meilleurs résultats</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
            <span>L'endpoint /api/search est idéal pour les interfaces utilisateur avec saisie libre</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
            <span>Les géométries des segments permettent d'afficher le tracé réel des voies sur une carte</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
