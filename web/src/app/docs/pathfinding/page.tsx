import { ArrowRight, Route, Zap, Timer, Map, Train, Plane, Settings, CheckCircle2, AlertCircle } from 'lucide-react';

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

export default function DocsPathfinding() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Pipeline</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Pathfinding</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Pathfinding (Dijkstra)</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Algorithme de recherche du plus court chemin optimisé pour le réseau ferroviaire français, 
          avec priorisation des TGV et temps de trajet réels.
        </p>
      </div>

      {/* Algorithm */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">L'algorithme de Dijkstra</h2>
        <div className="prose prose-invert max-w-none mb-6">
          <p className="text-neutral-400">
            L'algorithme de Dijkstra est un algorithme de recherche du plus court chemin dans un graphe pondéré. 
            Il explore progressivement les nœuds du graphe en commençant par celui ayant le coût le plus faible, 
            garantissant ainsi de trouver le chemin optimal.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
          <h3 className="font-semibold text-green-400 mb-3">Complexité</h3>
          <div className="flex items-center gap-8 text-sm">
            <div>
              <span className="text-neutral-400">Temps :</span>
              <code className="ml-2 text-green-400">O((V + E) log V)</code>
            </div>
            <div>
              <span className="text-neutral-400">Espace :</span>
              <code className="ml-2 text-green-400">O(V)</code>
            </div>
          </div>
        </div>
      </div>

      {/* Weighting */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Système de pondération</h2>
        <div className="prose prose-invert max-w-none mb-6">
          <p className="text-neutral-400">
            Le poids de chaque arête est basé sur le temps de trajet réel extrait des données GTFS, 
            avec un système de pénalités pour privilégier les trains rapides.
          </p>
        </div>

        <div className="rounded-xl border border-white/10 overflow-hidden mb-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Type de train</th>
                <th className="text-left p-4 font-medium">Pénalité</th>
                <th className="text-left p-4 font-medium">Effet</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr className="bg-green-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-green-400" />
                  <span className="text-green-400 font-medium">TGV / OUIGO</span>
                </td>
                <td className="p-4"><code className="text-green-400">×1.0</code></td>
                <td className="p-4 text-neutral-400">Priorité maximale</td>
              </tr>
              <tr className="bg-green-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">Lyria / Eurostar</span>
                </td>
                <td className="p-4"><code className="text-green-400">×1.0</code></td>
                <td className="p-4 text-neutral-400">TGV internationaux</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-yellow-400" />
                  <span className="text-yellow-400">Intercités</span>
                </td>
                <td className="p-4"><code className="text-yellow-400">×1.3</code></td>
                <td className="p-4 text-neutral-400">Légère pénalité</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-orange-400" />
                  <span className="text-orange-400">Train de nuit</span>
                </td>
                <td className="p-4"><code className="text-orange-400">×1.5</code></td>
                <td className="p-4 text-neutral-400">Pénalité modérée</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-red-400" />
                  <span className="text-red-400">TER</span>
                </td>
                <td className="p-4"><code className="text-red-400">×2.0</code></td>
                <td className="p-4 text-neutral-400">Pénalité importante</td>
              </tr>
            </tbody>
          </table>
        </div>

        <CodeBlock title="Calcul du poids">{`# Le poids pondéré est calculé ainsi :
temps_pondere = temps_reel × penalite_type_train

# Exemple Paris → Lyon en TGV (117 min)
poids = 117 × 1.0 = 117

# Exemple avec TER (supposons 180 min)
poids = 180 × 2.0 = 360  # Défavorisé`}</CodeBlock>
      </div>

      {/* Multi-source */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Zap className="w-6 h-6 text-yellow-400" />
          Dijkstra Multi-source
        </h2>
        <div className="prose prose-invert max-w-none mb-6">
          <p className="text-neutral-400">
            Pour les grandes villes avec plusieurs gares (Paris, Lyon, Marseille...), 
            le système explore toutes les gares possibles et sélectionne l'itinéraire global optimal.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-4">Exemple : Paris → Lyon</h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-4 h-4 text-green-400" />
              <span className="text-neutral-300">Paris Gare de Lyon → Lyon Part Dieu</span>
              <span className="ml-auto text-green-400">117 min ✓</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full border border-neutral-600" />
              <span className="text-neutral-500">Paris Montparnasse → Lyon Perrache</span>
              <span className="ml-auto text-neutral-500">145 min</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded-full border border-neutral-600" />
              <span className="text-neutral-500">Paris Bercy → Lyon Part Dieu</span>
              <span className="ml-auto text-neutral-500">135 min</span>
            </div>
          </div>
        </div>
      </div>

      {/* Airport exclusion */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Plane className="w-6 h-6 text-red-400" />
          Exclusion des aéroports
        </h2>
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 mb-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-red-400 mt-0.5" />
            <div className="text-sm">
              <p className="text-red-300 font-medium">Gares d'aéroport exclues par défaut</p>
              <p className="text-red-200/70">
                Les gares comme "Lyon Saint-Exupéry TGV" ou "Paris CDG" sont exclues des 
                origines/destinations par défaut pour privilégier les gares centrales.
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {['Aéroport', 'CDG', 'Saint-Exupéry', 'Orly'].map((term) => (
            <span key={term} className="px-3 py-1 rounded-full bg-red-500/10 text-red-400 text-xs">
              {term}
            </span>
          ))}
        </div>
      </div>

      {/* Configuration */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Settings className="w-6 h-6 text-neutral-400" />
          Configuration
        </h2>
        
        <CodeBlock title="Paramètres du pathfinding">{`{
  "pathfinding": {
    "path_gares": "data/train_station/dataset_gares.json",
    "path_liaisons": "data/train_station/dataset_liaisons_enhanced.json",
    "path_shapes": "data/train_station/dataset_liaisons_with_shapes.json",
    "mode": "time",
    "prioritize_tgv": true,
    "exclude_airports": true
  }
}`}</CodeBlock>
      </div>

      {/* Usage */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Utilisation</h2>
        
        <h3 className="font-semibold mb-3">Via la CLI</h3>
        <CodeBlock title="Terminal">{`python3 -m src.cli.pathfinding \\
  --origin "Paris" \\
  --destination "Marseille" \\
  --model dijkstra`}</CodeBlock>

        <h3 className="font-semibold mb-3 mt-6">Via Python</h3>
        <CodeBlock title="Python">{`from src.pathfinding.models.dijkstra import DijkstraPathfinder

# Initialiser le pathfinder
pathfinder = DijkstraPathfinder()

# Trouver un itinéraire
route = pathfinder.find_route("Paris", "Lyon")

print(route.steps)         # ['Paris Gare de Lyon', 'Lyon Part Dieu']
print(route.total_time)    # 117
print(route.total_distance)# 390.79
print(route.metadata)      # Détails des segments, géométries, etc.`}</CodeBlock>
      </div>

      {/* Output example */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Exemple de résultat</h2>
        <CodeBlock title="Route Paris → Lyon">{`{
  "origin": "Paris",
  "destination": "Lyon",
  "steps": ["Paris Gare de Lyon", "Lyon Part Dieu"],
  "total_time": 117,
  "total_distance": 390.79,
  "metadata": {
    "origin_uic": "87686006",
    "destination_uic": "87723197",
    "path_uic": ["87686006", "87723197"],
    "segments": [
      {
        "from": "Paris Gare de Lyon",
        "to": "Lyon Part Dieu",
        "temps_min": 117,
        "distance_km": 390.79,
        "nb_trains_jour": 120,
        "type_train": "TGV",
        "geometry": {
          "type": "LineString",
          "coordinates": [[2.37396, 48.8447], ...]
        }
      }
    ]
  }
}`}</CodeBlock>
      </div>

      {/* Geometry */}
      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Map className="w-5 h-5 text-neutral-400" />
          Géométries des voies
        </h2>
        <p className="text-sm text-neutral-400 mb-4">
          Chaque segment inclut sa géométrie GeoJSON pour tracer le parcours réel sur une carte. 
          Les coordonnées suivent le format LineString avec des points détaillés le long de la voie ferrée.
        </p>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-white mb-1">3000+</div>
            <div className="text-neutral-500">Segments avec géométrie</div>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-white mb-1">~300</div>
            <div className="text-neutral-500">Points par segment (moy.)</div>
          </div>
        </div>
      </div>
    </div>
  );
}
