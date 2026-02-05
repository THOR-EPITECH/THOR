import { 
  ArrowRight, 
  Database, 
  FileAudio, 
  FileText, 
  Train, 
  Map, 
  Folder, 
  FileJson, 
  Download,
  ExternalLink,
  Clock,
  MapPin,
  Route,
  Mic,
  Brain
} from 'lucide-react';

function DatasetCard({ 
  icon: Icon, 
  title, 
  description, 
  path,
  stats,
  usage,
  color = 'blue'
}: { 
  icon: any;
  title: string;
  description: string;
  path: string;
  stats: { label: string; value: string }[];
  usage: string[];
  color?: string;
}) {
  const colorClasses: Record<string, { bg: string; text: string; border: string }> = {
    blue: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
    green: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
    purple: { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/20' },
    orange: { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20' },
    yellow: { bg: 'bg-yellow-500/10', text: 'text-yellow-400', border: 'border-yellow-500/20' },
  };
  const c = colorClasses[color];

  return (
    <div className={`p-6 rounded-xl bg-white/[0.02] border ${c.border}`}>
      <div className="flex items-start gap-4 mb-4">
        <div className={`p-3 rounded-lg ${c.bg}`}>
          <Icon className={`w-5 h-5 ${c.text}`} />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-lg mb-1">{title}</h3>
          <code className="text-xs text-neutral-500 bg-white/5 px-2 py-0.5 rounded">{path}</code>
        </div>
      </div>
      
      <p className="text-sm text-neutral-400 mb-4">{description}</p>
      
      <div className="grid grid-cols-2 gap-2 mb-4">
        {stats.map((stat, i) => (
          <div key={i} className="p-2 rounded-lg bg-white/5 text-center">
            <div className="text-sm font-mono text-white">{stat.value}</div>
            <div className="text-xs text-neutral-500">{stat.label}</div>
          </div>
        ))}
      </div>
      
      <div>
        <div className="text-xs text-neutral-500 mb-2">Utilisé pour :</div>
        <div className="flex flex-wrap gap-1">
          {usage.map((u, i) => (
            <span key={i} className={`px-2 py-0.5 rounded text-xs ${c.bg} ${c.text}`}>
              {u}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

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

export default function DocsDatasets() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Recherche</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Datasets</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Datasets & Données</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Documentation complète des données utilisées par THOR : sources, formats, 
          et utilisation dans chaque module de la pipeline.
        </p>
      </div>

      {/* Overview */}
      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-12">
        <div className="flex items-center gap-3 mb-4">
          <Database className="w-5 h-5 text-neutral-400" />
          <h3 className="font-semibold">Vue d'ensemble</h3>
        </div>
        <div className="grid md:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-blue-400">200</div>
            <div className="text-xs text-neutral-500">Fichiers audio</div>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-purple-400">5,836</div>
            <div className="text-xs text-neutral-500">Phrases NLP</div>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-green-400">2,782</div>
            <div className="text-xs text-neutral-500">Gares SNCF</div>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-orange-400">7,852</div>
            <div className="text-xs text-neutral-500">Liaisons</div>
          </div>
        </div>
      </div>

      {/* Data structure */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Structure des données</h2>
        <CodeBlock title="Arborescence">{`data/
├── raw/                    # Données brutes sources
│   ├── audio/              # 200 fichiers WAV pour STT
│   ├── stop_times.txt      # 367k horaires GTFS SNCF
│   ├── trips.txt           # Trajets GTFS
│   ├── routes.txt          # Lignes GTFS
│   ├── stops.txt           # Arrêts GTFS
│   └── shapes.json         # 3,348 géométries de voies
│
├── splits/                 # Datasets annotés
│   ├── train/              # Entraînement (70%)
│   ├── valid/              # Validation (15%)
│   └── test/               # Test (15%)
│
└── train_station/          # Données traitées
    ├── dataset_gares.json           # 2,782 gares
    ├── dataset_liaisons.json        # Liaisons basiques
    ├── dataset_liaisons_enhanced.json  # + temps réels
    └── dataset_liaisons_with_shapes.json  # + géométries`}</CodeBlock>
      </section>

      {/* Audio data */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Mic className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold">Données Audio (STT)</h2>
        </div>

        <DatasetCard
          icon={FileAudio}
          title="Fichiers Audio"
          description="Enregistrements vocaux de demandes de trajets en français, utilisés pour entraîner et évaluer le module Speech-to-Text."
          path="data/raw/audio/"
          color="blue"
          stats={[
            { label: 'Fichiers', value: '200' },
            { label: 'Format', value: 'WAV 16kHz' },
            { label: 'Durée moy.', value: '~3s' },
            { label: 'Total', value: '~10 min' },
          ]}
          usage={['Évaluation Whisper', 'Évaluation Vosk', 'Tests pipeline']}
        />

        <div className="mt-4 p-4 rounded-lg bg-white/5">
          <h4 className="text-sm font-medium mb-3">Exemple d'échantillon</h4>
          <CodeBlock title="data/splits/train/train.jsonl">{`{
  "id": "sample_000160",
  "audio_path": "data/raw/audio/sample_000160.wav",
  "transcript": "Je veux voyager de Toulouse à Bordeaux"
}`}</CodeBlock>
        </div>
      </section>

      {/* NLP data */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-purple-500/10">
            <Brain className="w-5 h-5 text-purple-400" />
          </div>
          <h2 className="text-2xl font-bold">Données NLP</h2>
        </div>

        <div className="grid gap-4">
          <DatasetCard
            icon={FileText}
            title="Dataset d'entraînement NLP"
            description="Phrases annotées avec origine et destination pour entraîner le modèle spaCy. Inclut des exemples positifs (demandes de trajet) et négatifs."
            path="data/splits/train/train_nlp.jsonl"
            color="purple"
            stats={[
              { label: 'Échantillons', value: '4,085' },
              { label: 'Format', value: 'JSONL' },
              { label: 'Split', value: '70%' },
              { label: 'Villes uniques', value: '~150' },
            ]}
            usage={['Fine-tuning spaCy', 'Entraînement NER']}
          />

          <div className="grid md:grid-cols-2 gap-4">
            <DatasetCard
              icon={FileText}
              title="Dataset de validation"
              description="Utilisé pendant l'entraînement pour ajuster les hyperparamètres et éviter le surapprentissage."
              path="data/splits/valid/valid_nlp.jsonl"
              color="purple"
              stats={[
                { label: 'Échantillons', value: '875' },
                { label: 'Split', value: '15%' },
              ]}
              usage={['Validation', 'Early stopping']}
            />

            <DatasetCard
              icon={FileText}
              title="Dataset de test"
              description="Évaluation finale des modèles NLP. Non utilisé pendant l'entraînement."
              path="data/splits/test/test_nlp.jsonl"
              color="purple"
              stats={[
                { label: 'Échantillons', value: '876' },
                { label: 'Split', value: '15%' },
              ]}
              usage={['Benchmark', 'Métriques finales']}
            />
          </div>
        </div>

        <div className="mt-4 p-4 rounded-lg bg-white/5">
          <h4 className="text-sm font-medium mb-3">Format des annotations NLP</h4>
          <CodeBlock title="Exemples">{`// Demande valide avec origine et destination
{
  "id": "nlp_001",
  "sentence": "Je veux aller de Paris à Lyon",
  "origin": "Paris",
  "destination": "Lyon",
  "is_valid": true
}

// Demande partielle (destination seule)
{
  "id": "nlp_002",
  "sentence": "Je veux voyager jusqu'à Lille",
  "origin": null,
  "destination": "Lille",
  "is_valid": true
}

// Phrase non pertinente
{
  "id": "nlp_003",
  "sentence": "Mon ami habite à Strasbourg",
  "origin": null,
  "destination": null,
  "is_valid": false
}`}</CodeBlock>
        </div>
      </section>

      {/* GTFS data */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-orange-500/10">
            <Train className="w-5 h-5 text-orange-400" />
          </div>
          <h2 className="text-2xl font-bold">Données GTFS (SNCF)</h2>
        </div>

        <div className="p-4 rounded-lg bg-orange-500/5 border border-orange-500/20 mb-6">
          <div className="flex items-start gap-3">
            <ExternalLink className="w-4 h-4 text-orange-400 mt-1" />
            <div>
              <h4 className="font-medium text-orange-400 mb-1">Source officielle</h4>
              <p className="text-sm text-neutral-400 mb-3">
                Données ouvertes SNCF au format GTFS (General Transit Feed Specification).
                Téléchargées depuis <code className="px-1 bg-white/10 rounded">data.sncf.com</code>
              </p>
              <div className="text-xs text-neutral-500">
                <strong className="text-orange-300">GTFS</strong> = Standard Google pour les données de transport en commun. 
                Utilisé par Google Maps, Citymapper, et des milliers d'applications.
              </div>
            </div>
          </div>
        </div>

        {/* What we extract */}
        <div className="p-4 rounded-lg bg-white/5 border border-white/10 mb-6">
          <h4 className="text-sm font-medium mb-4">Données exploitées par THOR</h4>
          <div className="grid md:grid-cols-3 gap-4 text-xs">
            <div className="p-3 rounded-lg bg-green-500/10">
              <div className="font-medium text-green-400 mb-2">✓ Utilisé</div>
              <ul className="space-y-1 text-neutral-400">
                <li>• Temps de trajet entre gares</li>
                <li>• Codes UIC des gares</li>
                <li>• Type de train (TGV, TER...)</li>
                <li>• Fréquence des trains</li>
                <li>• Noms des gares</li>
              </ul>
            </div>
            <div className="p-3 rounded-lg bg-yellow-500/10">
              <div className="font-medium text-yellow-400 mb-2">◐ Partiellement</div>
              <ul className="space-y-1 text-neutral-400">
                <li>• Coordonnées GPS</li>
                <li>• Identifiants de ligne</li>
                <li>• Direction du trajet</li>
              </ul>
            </div>
            <div className="p-3 rounded-lg bg-neutral-500/10">
              <div className="font-medium text-neutral-400 mb-2">✗ Non utilisé</div>
              <ul className="space-y-1 text-neutral-500">
                <li>• Horaires exacts</li>
                <li>• Calendrier (dates)</li>
                <li>• Prix / tarifs</li>
                <li>• Correspondances</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="grid gap-4">
          <DatasetCard
            icon={Clock}
            title="stop_times.txt"
            description="Horaires de passage à chaque arrêt pour tous les trajets. Source principale pour extraire les temps de trajet réels entre gares."
            path="data/raw/stop_times.txt"
            color="orange"
            stats={[
              { label: 'Lignes', value: '367,639' },
              { label: 'Format', value: 'CSV (GTFS)' },
              { label: 'Colonnes', value: '9' },
              { label: 'Taille', value: '~35 MB' },
            ]}
            usage={['Temps de trajet', 'Fréquence trains', 'Type de train']}
          />

          <div className="grid md:grid-cols-2 gap-4">
            <DatasetCard
              icon={Route}
              title="trips.txt"
              description="Définition des trajets avec identifiants, lignes associées et directions."
              path="data/raw/trips.txt"
              color="orange"
              stats={[
                { label: 'Trajets', value: '~15,000' },
                { label: 'Types', value: 'TGV, TER, IC...' },
              ]}
              usage={['Mapping trajet → ligne', 'Type de train']}
            />

            <DatasetCard
              icon={MapPin}
              title="stops.txt"
              description="Liste des arrêts avec codes UIC, noms et coordonnées GPS."
              path="data/raw/stops.txt"
              color="orange"
              stats={[
                { label: 'Arrêts', value: '~4,000' },
                { label: 'Avec GPS', value: 'Oui' },
              ]}
              usage={['Géolocalisation', 'Codes UIC']}
            />
          </div>
        </div>

        <div className="mt-4 space-y-4">
          {/* stop_times.txt */}
          <div className="p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">stop_times.txt — Horaires de passage</h4>
            <CodeBlock title="stop_times.txt">{`trip_id,arrival_time,departure_time,stop_id,stop_sequence,...
OCETGV...,08:15:00,08:15:00,StopPoint:OCE87686006,0,...
OCETGV...,10:12:00,10:12:00,StopPoint:OCE87723197,1,...`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-orange-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Exploité ?</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-orange-300">trip_id</td>
                    <td className="p-2 text-neutral-400">Identifiant unique du trajet (encode le type de train)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">arrival_time</td>
                    <td className="p-2 text-neutral-400">Heure d'arrivée à l'arrêt (HH:MM:SS)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">departure_time</td>
                    <td className="p-2 text-neutral-400">Heure de départ de l'arrêt</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_id</td>
                    <td className="p-2 text-neutral-400">Identifiant de l'arrêt (contient code UIC)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_sequence</td>
                    <td className="p-2 text-neutral-400">Ordre de l'arrêt dans le trajet (0, 1, 2...)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 p-2 rounded bg-green-500/10 text-xs text-green-300">
              <strong>Calcul :</strong> Temps trajet = arrival_time[stop N+1] - departure_time[stop N]
            </div>
          </div>

          {/* stops.txt */}
          <div className="p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">stops.txt — Liste des arrêts</h4>
            <CodeBlock title="stops.txt">{`stop_id,stop_name,stop_lat,stop_lon,location_type,parent_station
StopArea:OCE87686006,PARIS GARE DE LYON,48.8447,2.3739,1,
StopPoint:OCETGV-87686006,PARIS GARE DE LYON,48.8447,2.3739,0,StopArea:OCE87686006`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-orange-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Exploité ?</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_id</td>
                    <td className="p-2 text-neutral-400">ID unique (contient code UIC : 87686006)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_name</td>
                    <td className="p-2 text-neutral-400">Nom de la gare en majuscules</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_lat</td>
                    <td className="p-2 text-neutral-400">Latitude GPS</td>
                    <td className="p-2 text-yellow-400">◐ Backup</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">stop_lon</td>
                    <td className="p-2 text-neutral-400">Longitude GPS</td>
                    <td className="p-2 text-yellow-400">◐ Backup</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">location_type</td>
                    <td className="p-2 text-neutral-400">0 = Quai, 1 = Station</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">parent_station</td>
                    <td className="p-2 text-neutral-400">Station parente (pour les quais)</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 p-2 rounded bg-blue-500/10 text-xs text-blue-300">
              <strong>Note :</strong> Le code UIC (87686006) est extrait du stop_id via regex
            </div>
          </div>

          {/* trips.txt */}
          <div className="p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">trips.txt — Définition des trajets</h4>
            <CodeBlock title="trips.txt">{`route_id,service_id,trip_id,trip_headsign,direction_id
FR:Line::abc123,000001,OCETGV-6789-Paris-Lyon,6789,0
FR:Line::def456,000002,OCEOUIGO-1234-Paris-Lyon,1234,0`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-orange-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Exploité ?</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-orange-300">route_id</td>
                    <td className="p-2 text-neutral-400">Identifiant de la ligne</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">service_id</td>
                    <td className="p-2 text-neutral-400">Jour de service (lié au calendrier)</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">trip_id</td>
                    <td className="p-2 text-neutral-400">ID unique du trajet (préfixe = type train)</td>
                    <td className="p-2 text-green-400">✓ Oui</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">trip_headsign</td>
                    <td className="p-2 text-neutral-400">Numéro du train affiché</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-orange-300">direction_id</td>
                    <td className="p-2 text-neutral-400">Direction (0 = aller, 1 = retour)</td>
                    <td className="p-2 text-neutral-500">✗ Non</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 p-2 rounded bg-orange-500/10 text-xs text-orange-300">
              <strong>Clé :</strong> Le préfixe du trip_id (OCETGV, OCEOUIGO...) permet d'identifier le type de train
            </div>
          </div>

          <div className="p-4 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <h4 className="text-sm font-medium text-orange-400 mb-3">Extraction du type de train</h4>
            <CodeBlock title="Parsing trip_id">{`// Le trip_id GTFS encode le type de train
"OCETGV..."       → TGV         (pénalité ×1.0)
"OCEOUIGO..."     → OUIGO       (pénalité ×1.0)
"OCEINTERCITES..."→ Intercités  (pénalité ×1.3)
"OCETER..."       → TER         (pénalité ×2.0)
"OCESN..."        → Navette     (pénalité ×2.0)
"OCEEA..."        → Eurostar    (pénalité ×1.0)
"OCELO..."        → Train nuit  (pénalité ×1.5)
"OCEL..."         → Lyria       (pénalité ×1.0)`}</CodeBlock>
          </div>
        </div>
      </section>

      {/* Processed data */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Database className="w-5 h-5 text-green-400" />
          </div>
          <h2 className="text-2xl font-bold">Données Traitées</h2>
        </div>

        {/* dataset_gares.json */}
        <div className="mb-8">
          <DatasetCard
            icon={Train}
            title="dataset_gares.json"
            description="Référentiel des gares SNCF avec codes UIC, coordonnées GPS, communes et noms normalisés. Généré à partir des données SNCF ouvertes."
            path="data/train_station/dataset_gares.json"
            color="green"
            stats={[
              { label: 'Gares', value: '2,782' },
              { label: 'Avec GPS', value: '100%' },
              { label: 'Multi-UIC', value: 'Oui' },
              { label: 'Taille', value: '~2.5 MB' },
            ]}
            usage={['Résolution ville → gare', 'Pathfinding', 'Affichage carte']}
          />

          <div className="mt-4 p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">Structure d'une gare (exemple réel)</h4>
            <CodeBlock title="dataset_gares.json">{`{
  "uic": ["87686006"],
  "nom_gare": "Paris Gare de Lyon",
  "trigramme": "PLY",
  "position_geographique": { "lat": 48.8447, "lon": 2.3739 },
  "ville": { "id_commune": "75056", "nom_commune": "PARIS" }
}`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-green-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Type</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Utilisé pour</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-green-300">uic</td>
                    <td className="p-2 text-neutral-500">string[]</td>
                    <td className="p-2 text-neutral-400">Code(s) UIC international (ex: 87686006)</td>
                    <td className="p-2 text-blue-300">Clé du graphe Dijkstra</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">nom_gare</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Nom officiel de la gare</td>
                    <td className="p-2 text-blue-300">Affichage UI</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">trigramme</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Code 3 lettres SNCF (PLY, LPD...)</td>
                    <td className="p-2 text-neutral-500">Non utilisé</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">position_geographique.lat</td>
                    <td className="p-2 text-neutral-500">float</td>
                    <td className="p-2 text-neutral-400">Latitude GPS (WGS84)</td>
                    <td className="p-2 text-blue-300">Marqueurs carte</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">position_geographique.lon</td>
                    <td className="p-2 text-neutral-500">float</td>
                    <td className="p-2 text-neutral-400">Longitude GPS (WGS84)</td>
                    <td className="p-2 text-blue-300">Marqueurs carte</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">ville.id_commune</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Code INSEE de la commune</td>
                    <td className="p-2 text-blue-300">Résolution ville → gare</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">ville.nom_commune</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Nom de la commune (majuscules)</td>
                    <td className="p-2 text-blue-300">Recherche fuzzy</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 p-2 rounded bg-green-500/10 text-xs text-green-300">
              <strong>Multi-UIC :</strong> Une gare peut avoir plusieurs codes UIC (ex: Paris Gare de Lyon a des UIC différents pour TGV et TER)
            </div>
          </div>
        </div>

        {/* dataset_liaisons_enhanced.json */}
        <div className="mb-8">
          <DatasetCard
            icon={Route}
            title="dataset_liaisons_enhanced.json"
            description="Graphe des connexions entre gares avec temps de trajet moyens, distances, fréquences et types de train. Généré depuis stop_times.txt."
            path="data/train_station/dataset_liaisons_enhanced.json"
            color="green"
            stats={[
              { label: 'Liaisons', value: '7,852' },
              { label: 'Avec temps', value: '100%' },
              { label: 'Avec type train', value: '100%' },
              { label: 'Taille', value: '~5 MB' },
            ]}
            usage={['Dijkstra', 'Pondération TGV', 'Stats trajets']}
          />

          <div className="mt-4 p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">Structure d'une liaison (exemple réel)</h4>
            <CodeBlock title="dataset_liaisons_enhanced.json">{`{
  "depart": "87271494",
  "arrivee": "87111849",
  "depart_nom": "Aéroport CDG 2 TGV",
  "arrivee_nom": "Marne-la-Vallée Chessy",
  "temps_moyen_min": 11.1,
  "temps_min_min": 9,
  "temps_max_min": 18,
  "nb_trains": 638,
  "distance_km": 21.46,
  "type_train": "TGV",
  "types_details": { "TGV": 563, "OUIGO": 75 }
}`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-green-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Type</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Utilisé pour</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-green-300">depart</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Code UIC de la gare de départ</td>
                    <td className="p-2 text-blue-300">Nœud source (graphe)</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">arrivee</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Code UIC de la gare d'arrivée</td>
                    <td className="p-2 text-blue-300">Nœud destination (graphe)</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">depart_nom</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Nom lisible de la gare de départ</td>
                    <td className="p-2 text-blue-300">Affichage UI</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">arrivee_nom</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Nom lisible de la gare d'arrivée</td>
                    <td className="p-2 text-blue-300">Affichage UI</td>
                  </tr>
                  <tr className="bg-green-500/5">
                    <td className="p-2 font-mono text-green-300">temps_moyen_min</td>
                    <td className="p-2 text-neutral-500">float</td>
                    <td className="p-2 text-neutral-400">Temps de trajet moyen en minutes</td>
                    <td className="p-2 text-green-400 font-medium">⭐ Poids Dijkstra</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">temps_min_min</td>
                    <td className="p-2 text-neutral-500">int</td>
                    <td className="p-2 text-neutral-400">Temps minimum observé (train le plus rapide)</td>
                    <td className="p-2 text-neutral-500">Info seulement</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">temps_max_min</td>
                    <td className="p-2 text-neutral-500">int</td>
                    <td className="p-2 text-neutral-400">Temps maximum observé (train le plus lent)</td>
                    <td className="p-2 text-neutral-500">Info seulement</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">nb_trains</td>
                    <td className="p-2 text-neutral-500">int</td>
                    <td className="p-2 text-neutral-400">Nombre de trains par jour sur cette liaison</td>
                    <td className="p-2 text-blue-300">Affichage fréquence</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">distance_km</td>
                    <td className="p-2 text-neutral-500">float</td>
                    <td className="p-2 text-neutral-400">Distance en km (calculée via Haversine)</td>
                    <td className="p-2 text-blue-300">Affichage distance</td>
                  </tr>
                  <tr className="bg-green-500/5">
                    <td className="p-2 font-mono text-green-300">type_train</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Type de train majoritaire (TGV, TER, IC...)</td>
                    <td className="p-2 text-green-400 font-medium">⭐ Pénalité Dijkstra</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">types_details</td>
                    <td className="p-2 text-neutral-500">object</td>
                    <td className="p-2 text-neutral-400">Répartition par type {"{ TGV: 563, OUIGO: 75 }"}</td>
                    <td className="p-2 text-blue-300">Stats détaillées</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 p-2 rounded bg-green-500/10 text-xs text-green-300">
              <strong>Calcul poids :</strong> temps_pondere = temps_moyen_min × pénalité(type_train) — TGV ×1.0, TER ×2.0
            </div>
          </div>
        </div>

        {/* dataset_liaisons_with_shapes.json */}
        <div className="mb-8">
          <DatasetCard
            icon={Map}
            title="dataset_liaisons_with_shapes.json"
            description="Liaisons enrichies avec les géométries GeoJSON des voies ferrées pour l'affichage cartographique des trajets réels."
            path="data/train_station/dataset_liaisons_with_shapes.json"
            color="green"
            stats={[
              { label: 'Liaisons', value: '7,852' },
              { label: 'Avec géométrie', value: '~60%' },
              { label: 'Points/segment', value: '~300 moy' },
              { label: 'Taille', value: '~50 MB' },
            ]}
            usage={['Tracé carte', 'Visualisation routes']}
          />

          <div className="mt-4 p-4 rounded-lg bg-white/5">
            <h4 className="text-sm font-medium mb-3">Structure avec géométrie (exemple réel)</h4>
            <CodeBlock title="dataset_liaisons_with_shapes.json">{`{
  "depart": "87271494",
  "arrivee": "87111849",
  "depart_nom": "Aéroport CDG 2 TGV",
  "arrivee_nom": "Marne-la-Vallée Chessy",
  "temps_moyen_min": 11.1,
  "type_train": "TGV",
  "geometry": {
    "type": "LineString",
    "coordinates": [[2.570892, 49.003652], ..., [2.782720, 48.869856]]
  },
  "ligne_code": 226310,
  "ligne_nom": "Raccordement interconnexion LGV"
}`}</CodeBlock>
            <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-white/5">
                    <th className="text-left p-2 font-medium text-green-400">Propriété</th>
                    <th className="text-left p-2 font-medium">Type</th>
                    <th className="text-left p-2 font-medium">Description</th>
                    <th className="text-left p-2 font-medium">Utilisé pour</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  <tr>
                    <td className="p-2 font-mono text-neutral-400" colSpan={4}>
                      <em>... tous les champs de dataset_liaisons_enhanced.json ...</em>
                    </td>
                  </tr>
                  <tr className="bg-green-500/5">
                    <td className="p-2 font-mono text-green-300">geometry</td>
                    <td className="p-2 text-neutral-500">object</td>
                    <td className="p-2 text-neutral-400">Objet GeoJSON LineString</td>
                    <td className="p-2 text-green-400 font-medium">⭐ Tracé carte</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">geometry.type</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Toujours "LineString"</td>
                    <td className="p-2 text-blue-300">Validation GeoJSON</td>
                  </tr>
                  <tr className="bg-green-500/5">
                    <td className="p-2 font-mono text-green-300">geometry.coordinates</td>
                    <td className="p-2 text-neutral-500">number[][]</td>
                    <td className="p-2 text-neutral-400">Liste de points [lon, lat] (ordre GeoJSON)</td>
                    <td className="p-2 text-green-400 font-medium">⭐ Polyline Leaflet</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">ligne_code</td>
                    <td className="p-2 text-neutral-500">int</td>
                    <td className="p-2 text-neutral-400">Code numérique de la ligne RFN</td>
                    <td className="p-2 text-neutral-500">Référence</td>
                  </tr>
                  <tr>
                    <td className="p-2 font-mono text-green-300">ligne_nom</td>
                    <td className="p-2 text-neutral-500">string</td>
                    <td className="p-2 text-neutral-400">Nom officiel de la ligne ferroviaire</td>
                    <td className="p-2 text-blue-300">Info popup</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-3 grid md:grid-cols-2 gap-3">
              <div className="p-2 rounded bg-yellow-500/10 text-xs text-yellow-300">
                <strong>⚠️ Ordre GeoJSON :</strong> [longitude, latitude] — Leaflet attend [lat, lon], donc le frontend inverse
              </div>
              <div className="p-2 rounded bg-blue-500/10 text-xs text-blue-300">
                <strong>Couverture :</strong> ~60% des liaisons ont une géométrie, les autres affichent une ligne droite
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Shapes data */}
      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-yellow-500/10">
            <Map className="w-5 h-5 text-yellow-400" />
          </div>
          <h2 className="text-2xl font-bold">Géométries des Voies</h2>
        </div>

        <DatasetCard
          icon={Map}
          title="shapes.json"
          description="Tracés géographiques détaillés des lignes ferroviaires françaises au format GeoJSON. Source : Réseau Ferré National (RFN)."
          path="data/raw/shapes.json"
          color="yellow"
          stats={[
            { label: 'Lignes', value: '3,348' },
            { label: 'Format', value: 'GeoJSON' },
            { label: 'Type', value: 'LineString' },
            { label: 'Taille', value: '~100 MB' },
          ]}
          usage={['Tracé routes sur carte', 'Association liaisons', 'Visualisation']}
        />

        <div className="mt-4 p-4 rounded-lg bg-white/5">
          <h4 className="text-sm font-medium mb-3">Structure d'une ligne ferroviaire (exemple réel)</h4>
          <CodeBlock title="shapes.json">{`{
  "licence": "ODBL",
  "source": "Portail Open Data SNCF",
  "codeLigne": 1000,
  "idGaia": "79e6edd0-e28c...",
  "nomLigne": "Ligne de Paris-Est à Mulhouse-Ville",
  "pkDebut": 0.052,
  "pkFin": 491.081,
  "statut": "Exploitée",
  "geometry": {
    "type": "LineString",
    "coordinates": [[2.358926, 48.877370], ..., [7.344862, 47.742907]]
  },
  "electrifications": [{ "detail": "25000V alternatif", "from": 0, "to": 39 }],
  "regimeExploitation": [{ "detail": "Double voie", "from": 0, "to": 491 }]
}`}</CodeBlock>
          <div className="mt-4 rounded-lg border border-white/10 overflow-hidden">
            <table className="w-full text-xs">
              <thead>
                <tr className="bg-white/5">
                  <th className="text-left p-2 font-medium text-yellow-400">Propriété</th>
                  <th className="text-left p-2 font-medium">Type</th>
                  <th className="text-left p-2 font-medium">Description</th>
                  <th className="text-left p-2 font-medium">Utilisé pour</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <tr>
                  <td className="p-2 font-mono text-yellow-300">licence</td>
                  <td className="p-2 text-neutral-500">string</td>
                  <td className="p-2 text-neutral-400">Licence des données (ODBL)</td>
                  <td className="p-2 text-neutral-500">Métadonnée</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">source</td>
                  <td className="p-2 text-neutral-500">string</td>
                  <td className="p-2 text-neutral-400">Origine des données</td>
                  <td className="p-2 text-neutral-500">Métadonnée</td>
                </tr>
                <tr className="bg-yellow-500/5">
                  <td className="p-2 font-mono text-yellow-300">codeLigne</td>
                  <td className="p-2 text-neutral-500">int</td>
                  <td className="p-2 text-neutral-400">Code numérique RFN de la ligne (ex: 1000)</td>
                  <td className="p-2 text-yellow-400 font-medium">⭐ Matching liaisons</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">idGaia</td>
                  <td className="p-2 text-neutral-500">string</td>
                  <td className="p-2 text-neutral-400">UUID interne SNCF</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
                <tr className="bg-yellow-500/5">
                  <td className="p-2 font-mono text-yellow-300">nomLigne</td>
                  <td className="p-2 text-neutral-500">string</td>
                  <td className="p-2 text-neutral-400">Nom officiel (ex: "Paris-Est à Mulhouse")</td>
                  <td className="p-2 text-yellow-400 font-medium">⭐ Info affichée</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">pkDebut</td>
                  <td className="p-2 text-neutral-500">float</td>
                  <td className="p-2 text-neutral-400">Point kilométrique de début</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">pkFin</td>
                  <td className="p-2 text-neutral-500">float</td>
                  <td className="p-2 text-neutral-400">Point kilométrique de fin</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">statut</td>
                  <td className="p-2 text-neutral-500">string</td>
                  <td className="p-2 text-neutral-400">État de la ligne (Exploitée, Fermée...)</td>
                  <td className="p-2 text-neutral-500">Filtrage potentiel</td>
                </tr>
                <tr className="bg-yellow-500/5">
                  <td className="p-2 font-mono text-yellow-300">geometry</td>
                  <td className="p-2 text-neutral-500">object</td>
                  <td className="p-2 text-neutral-400">Objet GeoJSON LineString</td>
                  <td className="p-2 text-yellow-400 font-medium">⭐ Tracé carte</td>
                </tr>
                <tr className="bg-yellow-500/5">
                  <td className="p-2 font-mono text-yellow-300">geometry.coordinates</td>
                  <td className="p-2 text-neutral-500">number[][]</td>
                  <td className="p-2 text-neutral-400">Points [lon, lat] de la voie (~100-2000 pts)</td>
                  <td className="p-2 text-yellow-400 font-medium">⭐ Polyline</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">electrifications</td>
                  <td className="p-2 text-neutral-500">array</td>
                  <td className="p-2 text-neutral-400">Tronçons électrifiés (25kV, 1500V...)</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">regimeExploitation</td>
                  <td className="p-2 text-neutral-500">array</td>
                  <td className="p-2 text-neutral-400">Double/simple voie, VU...</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
                <tr>
                  <td className="p-2 font-mono text-yellow-300">vitesses</td>
                  <td className="p-2 text-neutral-500">array</td>
                  <td className="p-2 text-neutral-400">Limites de vitesse par tronçon</td>
                  <td className="p-2 text-neutral-500">Non utilisé</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-3 p-2 rounded bg-yellow-500/10 text-xs text-yellow-300">
            <strong>Algorithme matching :</strong> Pour chaque liaison, on cherche la ligne dont geometry passe le plus près des deux gares (Haversine &lt; 5km)
          </div>
        </div>
      </section>

      {/* Data flow */}
      <section>
        <h2 className="text-2xl font-bold mb-6">Flux de données</h2>
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-orange-500/20 flex items-center justify-center text-sm font-mono text-orange-400">1</div>
              <div className="flex-1">
                <div className="font-medium">Données GTFS brutes</div>
                <div className="text-sm text-neutral-500">stop_times.txt, trips.txt, routes.txt → Téléchargées de data.sncf.com</div>
              </div>
            </div>
            
            <div className="ml-4 border-l-2 border-white/10 h-6" />
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-sm font-mono text-green-400">2</div>
              <div className="flex-1">
                <div className="font-medium">Script de génération</div>
                <div className="text-sm text-neutral-500">generate_enhanced_graph.py → Parse GTFS et calcule temps moyens</div>
              </div>
            </div>
            
            <div className="ml-4 border-l-2 border-white/10 h-6" />
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-sm font-mono text-blue-400">3</div>
              <div className="flex-1">
                <div className="font-medium">Datasets traités</div>
                <div className="text-sm text-neutral-500">dataset_liaisons_enhanced.json → Prêt pour Dijkstra</div>
              </div>
            </div>
            
            <div className="ml-4 border-l-2 border-white/10 h-6" />
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center text-sm font-mono text-yellow-400">4</div>
              <div className="flex-1">
                <div className="font-medium">Enrichissement géométries</div>
                <div className="text-sm text-neutral-500">generate_railway_shapes.py → Ajoute tracés GeoJSON</div>
              </div>
            </div>
            
            <div className="ml-4 border-l-2 border-white/10 h-6" />
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center text-sm font-mono text-purple-400">5</div>
              <div className="flex-1">
                <div className="font-medium">API & Frontend</div>
                <div className="text-sm text-neutral-500">Chargé par Flask → Servi à Next.js → Affiché sur Leaflet</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
