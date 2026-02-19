# Documentation Complète de la Pipeline THOR

**Version**: 1.0  
**Date**: Janvier 2026  
**Auteur**: THOR Team - EPITECH

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture de la Pipeline](#architecture-de-la-pipeline)
3. [Modèle STT (Speech-to-Text)](#modèle-stt-speech-to-text)
4. [Modèle NLP (Natural Language Processing)](#modèle-nlp-natural-language-processing)
5. [Modèle Pathfinding](#modèle-pathfinding)
6. [Utilisation de la Pipeline](#utilisation-de-la-pipeline)
7. [Exemples de Commandes](#exemples-de-commandes)
8. [Exemples de Résultats](#exemples-de-résultats)
9. [API REST](#api-rest)
10. [Interface Web](#interface-web)

---

## Vue d'ensemble

La pipeline THOR est un système complet de traitement de commandes vocales pour la recherche d'itinéraires ferroviaires. Elle combine trois modèles d'intelligence artificielle pour transformer une commande vocale en itinéraire détaillé.

### Flux de traitement

```
Audio (WAV/WebM) 
    ↓
[STT - Whisper]
    ↓
Texte transcrit
    ↓
[NLP - spaCy]
    ↓
Origine + Destination
    ↓
[Pathfinding - Dijkstra]
    ↓
Itinéraire complet avec détails
```

### Technologies utilisées

- **STT**: OpenAI Whisper (reconnaissance vocale)
- **NLP**: spaCy (extraction d'entités nommées)
- **Pathfinding**: Algorithme de Dijkstra (recherche de chemin optimal)
- **Données**: GTFS SNCF (horaires réels, géométries de voies)

---

## Architecture de la Pipeline

### Composants principaux

1. **Orchestrateur** (`src/pipeline/orchestrator.py`)
   - Coordonne les trois modèles
   - Gère le flux de données
   - Gère les erreurs

2. **Modèles STT**
   - `WhisperModel`: Transcription avec OpenAI Whisper
   - `VoskModel`: Alternative légère (optionnel)

3. **Modèles NLP**
   - `SpacyFRModel`: Extraction d'entités avec spaCy
   - Support des modèles fine-tunés

4. **Modèles Pathfinding**
   - `DijkstraPathfindingModel`: Recherche de chemin optimal
   - Utilise les temps de trajet réels

### Structure des données

#### Entrée
- Fichier audio (WAV, WebM, MP3)
- Format: 16kHz, mono, PCM

#### Sortie
```json
{
  "transcript": "Je veux aller de Paris à Lyon",
  "origin": "Paris",
  "destination": "Lyon",
  "is_valid": true,
  "confidence": 0.85,
  "route": {
    "steps": ["Paris Gare de Lyon", "Lyon Part Dieu"],
    "total_time": 117.0,
    "total_distance": 390.79,
    "metadata": {
      "segments": [
        {
          "from": "Paris Gare de Lyon",
          "to": "Lyon Part Dieu",
          "temps_min": 117.0,
          "distance_km": 390.79,
          "type_train": "TGV",
          "nb_trains_jour": 120
        }
      ]
    }
  }
}
```

---

## Modèle STT (Speech-to-Text)

### OpenAI Whisper

Whisper est un modèle de transcription vocale développé par OpenAI, capable de transcrire la parole en texte avec une grande précision, même dans des conditions difficiles.

#### Caractéristiques

- **Modèles disponibles**: `tiny`, `base`, `small`, `medium`, `large`
- **Langue**: Français (configurable)
- **Précision**: Très élevée pour le français
- **Temps de traitement**: ~1-5 secondes selon le modèle

#### Configuration

```python
from src.stt.models.whisper import WhisperModel

model = WhisperModel({
    "model_size": "small",  # tiny, base, small, medium, large
    "language": "fr",
    "device": "cpu"  # ou "cuda" pour GPU
})
model.initialize()
```

#### Utilisation

```python
result = model.transcribe("audio.wav")
print(result.text)  # "Je veux aller de Paris à Lyon"
print(result.metadata)  # {"model": "whisper-small", "segments": 1}
```

#### Traitement interne

1. **Chargement audio**
   - Utilise `librosa` pour charger l'audio
   - Conversion automatique en 16kHz mono
   - Format: float32 array

2. **Transcription**
   - Whisper analyse l'audio
   - Détection automatique de la langue
   - Génération du texte transcrit

3. **Post-traitement**
   - Nettoyage du texte
   - Suppression des espaces superflus
   - Normalisation

#### Exemple de sortie

```python
STTResult(
    text="Je veux aller de Paris à Lyon",
    confidence=None,  # Whisper ne fournit pas de score global
    language="fr",
    processing_time=2.3,
    metadata={
        "model": "whisper-small",
        "segments": 1,
        "detected_language": "fr"
    }
)
```

---

## Modèle NLP (Natural Language Processing)

### spaCy pour l'extraction d'entités

Le modèle NLP utilise spaCy pour extraire les villes (origine et destination) depuis le texte transcrit.

#### Caractéristiques

- **Modèle de base**: `fr_core_news_md` (spaCy)
- **Fine-tuning**: Support des modèles entraînés sur données spécifiques
- **Extraction**: NER (Named Entity Recognition) + patterns regex
- **Confiance**: Score calculé basé sur plusieurs facteurs

#### Méthodes d'extraction

##### 1. NER (Named Entity Recognition)

Détection automatique des entités de type `LOC` (location):

```python
doc = nlp("Je veux aller de Paris à Lyon")
for ent in doc.ents:
    if ent.label_ == "LOC":
        print(ent.text)  # "Paris", "Lyon"
```

##### 2. Patterns regex

Détection basée sur des patterns linguistiques:

- `"de X à Y"` → origine: X, destination: Y
- `"depuis X"` → origine: X
- `"aller à Y"` → destination: Y
- `"partir de X"` → origine: X

##### 3. Modèles fine-tunés

Si un modèle fine-tuné est utilisé, il peut détecter directement:
- `ORIGIN`: Ville de départ
- `DESTINATION`: Ville d'arrivée

#### Configuration

```python
from src.nlp.models.spacy_fr import SpacyFRModel

# Modèle de base
model = SpacyFRModel({
    "model_name": "fr_core_news_md"
})

# Modèle fine-tuné
model = SpacyFRModel({
    "model_name": "fr_core_news_md",
    "custom_model_path": "models/nlp/spacy_finetuned"
})
```

#### Calcul de la confiance

Le score de confiance (0.0 à 1.0) est calculé selon:

- **+0.2**: Au moins une ville détectée
- **+0.4**: Modèle fine-tuné utilisé
- **+0.2**: Les deux villes détectées directement
- **+0.2**: Origine ET destination trouvées
- **+0.1**: Demande valide (mots-clés de trajet présents)
- **×0.5**: Pénalité si villes détectées mais pas d'extraction

#### Exemple de sortie

```python
NLPExtraction(
    origin="Paris",
    destination="Lyon",
    is_valid=True,
    confidence=0.85,
    entities=[
        {"text": "Paris", "label": "LOC"},
        {"text": "Lyon", "label": "LOC"}
    ],
    metadata={
        "model": "spacy-fr_core_news_md",
        "locations_found": ["Paris", "Lyon"],
        "extraction_method": "ner_patterns"
    }
)
```

---

## Modèle Pathfinding

### Algorithme de Dijkstra

Le pathfinding utilise l'algorithme de Dijkstra pour trouver le chemin optimal entre deux gares, en optimisant le **temps de trajet** plutôt que la distance géographique.

#### Caractéristiques

- **Algorithme**: Dijkstra (plus court chemin)
- **Poids**: Temps de trajet réel (en minutes)
- **Données**: GTFS SNCF (horaires réels)
- **Optimisation**: Priorité aux TGV/OUIGO
- **Multi-source**: Teste plusieurs gares pour grandes villes

#### Données utilisées

##### 1. Gares (`dataset_gares.json`)

```json
{
  "nom_gare": "Paris Gare de Lyon",
  "uic": ["87686006", "87686030"],
  "position_geographique": {
    "lat": 48.8445,
    "lon": 2.3732
  },
  "ville": {
    "nom_commune": "Paris",
    "id_commune": "75056"
  }
}
```

##### 2. Liaisons enrichies (`dataset_liaisons_enhanced.json`)

```json
{
  "depart": "87686006",
  "arrivee": "87723197",
  "depart_nom": "Paris Gare de Lyon",
  "arrivee_nom": "Lyon Part Dieu",
  "temps_moyen_min": 117.0,
  "temps_min_min": 105.0,
  "temps_max_min": 130.0,
  "nb_trains": 120,
  "distance_km": 390.79,
  "type_train": "TGV",
  "types_details": {
    "TGV": 120
  }
}
```

#### Algorithme de Dijkstra

##### 1. Construction du graphe

```python
graph = {
    "87686006": [  # Paris Gare de Lyon
        ("87723197", 117.0),  # → Lyon Part Dieu (117 min)
        ("87686030", 5.0)     # → Paris Gare de Lyon (autre UIC)
    ],
    "87723197": [  # Lyon Part Dieu
        ("87686006", 117.0)   # → Paris Gare de Lyon (117 min)
    ]
}
```

##### 2. Pondération par type de train

Les temps sont pondérés pour favoriser les trains rapides:

```python
TRAIN_TYPE_PENALTY = {
    'TGV': 1.0,           # Priorité maximale
    'OUIGO': 1.0,         # Même priorité que TGV
    'Lyria': 1.0,         # TGV international
    'Eurostar': 1.0,      # TGV international
    'Intercités': 1.3,    # Légère pénalité
    'Train de nuit': 1.5, # Pénalité modérée
    'TER': 2.0,           # Pénalité importante
    'Navette': 2.0,       # Pénalité importante
    'Auto-train': 2.5,    # Forte pénalité
    'Autre': 2.0,         # Pénalité par défaut
    'Correspondance': 1.0 # Pas de pénalité (transfert inter-gare nécessaire)
}

temps_pondere = temps_moyen * TRAIN_TYPE_PENALTY[type_train]

# Exemple de calcul:
# Liaison TGV Paris → Lyon : 117 min
# Poids = 117 × 1.0 = 117 minutes

# Liaison TER : 180 min
# Poids = 180 × 2.0 = 360 minutes

# L'algorithme choisit TOUJOURS le chemin avec le PLUS PETIT poids total
```

**Note importante** : Ce système de **pénalités intelligentes** permet à Dijkstra de :
- Favoriser les TGV sans les prioriser absolument
- Accepter un TER court + TGV long si c'est mieux qu'un TER direct
- Ne pas pénaliser les correspondances inter-gare (métro entre gares parisiennes)

##### 3. Sélection intelligente des villes

Le système utilise un **scoring avancé** pour éviter de choisir les mauvaises gares, notamment en cas d'homonymes.

**Problématique :** 
- Recherche: `"marseille"` 
- ❌ Sans système intelligent → `Marseille-en-Beauvaisis` (60, village de 800 habitants, plus proche de Paris)
- ✅ Avec système intelligent → `Marseille Saint-Charles` (13, 2ème ville de France, 870 000 habitants)

**Système de scoring :**

| Critère | Score | Exemple |
|---------|-------|---------|
| Nom exact de gare | +200 | "Paris Gare de Lyon" → 87686006 |
| Grande ville majeure | +100 | Marseille, Lyon, Toulouse, Nice, Bordeaux, Lille... (29 villes) |
| Gare principale reconnue | +50 | Saint-Charles, Part-Dieu, Saint-Jean, Montparnasse... |
| Gare TGV/centrale | +30 | Contient "TGV", "Central", "Centre" dans le nom |
| Nombre de connexions | +2×N | N = nombre de liaisons depuis cette gare |
| Gare secondaire | -20 | Aéroport, Banlieue, RER, etc. |

**Exclusion automatique des homonymes :**

Pour les recherches simples (sans tiret), le système exclut automatiquement les homonymes indésirables :

```python
EXCLUDED_WHEN_SIMPLE = {
    'marseille': ['marseille-en-beauvaisis'],
    'lyon': ['lyon-dagneux'],
    'paris': ['paris-plage']
}

# Si recherche = "marseille" (sans tiret)
# → Exclut Marseille-en-Beauvaisis AVANT le scoring

# Si recherche = "marseille-en-beauvaisis" (avec tiret)
# → Ne fait AUCUNE exclusion, trouve bien le village
```

**Exemple de calcul complet :**

```python
# Recherche: "marseille"

# Candidate 1: Marseille Saint-Charles (87756353)
score = 0
score += 80   # ville_nom == "marseille"
score += 100  # "marseille" in MAJOR_CITIES
score += 50   # "saint-charles" in gare_nom
score += 2 * 60  # 60 connexions dans le graphe
→ Score total = 350

# Candidate 2: Marseille-en-Beauvaisis (87474411)
# → EXCLU automatiquement (homonyme indésirable)

# Résultat: Marseille Saint-Charles ✅
```

##### 4. Correspondances inter-gare

Le système supporte les **transferts métro** entre grandes gares parisiennes :

```python
# Correspondances automatiques ajoutées au graphe
correspondances_paris = [
    {
        "depart": "87391102",  # Paris Montparnasse
        "arrivee": "87686006",  # Paris Gare de Lyon
        "temps_min": 5,
        "type_train": "Correspondance"
    },
    {
        "depart": "87391102",  # Paris Montparnasse
        "arrivee": "87271031",  # Paris Nord
        "temps_min": 5,
        "type_train": "Correspondance"
    },
    {
        "depart": "87686006",  # Paris Gare de Lyon
        "arrivee": "87271031",  # Paris Nord
        "temps_min": 5,
        "type_train": "Correspondance"
    }
]
```

**Affichage sur la carte web** : Les correspondances sont affichées en **lignes jaunes pointillées** reliant visuellement les deux gares.

**Exemple de trajet avec correspondance** : Biarritz → Marseille
- Biarritz → Paris Montparnasse (TGV, 274 min)
- Paris Montparnasse → Paris Gare de Lyon (**Correspondance métro**, 5 min)
- Paris Gare de Lyon → Marseille (TGV, 189 min)
- **Total : 468 min** (au lieu d'un détour par Massy/Marne-la-Vallée)

##### 5. Recherche du chemin

```python
def find_shortest_path(graph, start_uic, end_uic):
    queue = [(0, start_uic, [])]  # (coût, nœud, chemin)
    visited = set()
    min_dist = {start_uic: 0}
    
    while queue:
        cost, current, path = heappop(queue)
        
        if current in visited:
            continue
        
        visited.add(current)
        path = path + [current]
        
        if current == end_uic:
            return cost, path  # Chemin trouvé!
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
            
            new_cost = cost + weight
            if new_cost < min_dist.get(neighbor, float('inf')):
                min_dist[neighbor] = new_cost
                heappush(queue, (new_cost, neighbor, path))
    
    return None, None  # Pas de chemin
```

#### Sélection des gares

##### Pour les grandes villes (Paris, Lyon, Marseille...)

Le système teste **toutes les gares** de la ville et choisit le meilleur trajet:

```python
# Paris a plusieurs gares:
paris_gares = [
    "Paris Gare de Lyon",      # UIC: 87686006
    "Paris Montparnasse",       # UIC: 87391003
    "Paris Gare du Nord",       # UIC: 87271031
    "Paris Est",                # UIC: 87113001
    # ...
]

# Teste toutes les combinaisons:
for origin_uic in paris_gares:
    for destination_uic in lyon_gares:
        weight, path = find_shortest_path(graph, origin_uic, destination_uic)
        # Garde le meilleur
```

##### Exclusion des aéroports

Les gares d'aéroport sont exclues pour les destinations:

```python
exclude_terms = [
    'aéroport', 'exupéry', 'cdg', 
    'charles de gaulle', 'rer', 'banlieue'
]
```

#### Exemple de sortie

```python
Route(
    origin="Paris",
    destination="Lyon",
    steps=["Paris Gare de Lyon", "Lyon Part Dieu"],
    total_distance=390.79,
    total_time=117.0,
    metadata={
        "origin_uic": "87686006",
        "destination_uic": "87723197",
        "path_uic": ["87686006", "87723197"],
        "num_stations": 2,
        "mode": "temps_reel",
        "segments": [
            {
                "from": "Paris Gare de Lyon",
                "to": "Lyon Part Dieu",
                "temps_min": 117.0,
                "distance_km": 390.79,
                "nb_trains_jour": 120,
                "type_train": "TGV",
                "types_details": {"TGV": 120}
            }
        ]
    }
)
```

---

## Utilisation de la Pipeline

### Via CLI (ligne de commande)

#### Commande de base

```bash
python3 -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --pathfinding-model dijkstra
```

#### Options disponibles

- `--audio`: Chemin vers le fichier audio (requis)
- `--stt-model`: Modèle STT (`whisper`, `vosk`)
- `--nlp-model`: Modèle NLP (`spacy`)
- `--pathfinding-model`: Modèle Pathfinding (`dijkstra`, optionnel)
- `--config`: Fichier de configuration (optionnel)
- `--output`: Chemin de sortie pour le JSON (optionnel)

### Via API REST

#### Endpoint: `/api/pipeline`

```bash
curl -X POST http://localhost:8000/api/pipeline \
    -H "Content-Type: application/json" \
    -d '{
        "audio": "base64_encoded_audio",
        "format": "wav"
    }'
```

#### Endpoint: `/api/search`

```bash
curl -X POST http://localhost:8000/api/search \
    -H "Content-Type: application/json" \
    -d '{
        "text": "Je veux aller de Paris à Lyon"
    }'
```

### Via Interface Web

1. Ouvrir `http://localhost:3000`
2. Cliquer sur le bouton micro
3. Parler la demande
4. L'itinéraire s'affiche automatiquement

---

## Exemples de Commandes

### Exemple 1: Trajet simple

```bash
python3 -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --pathfinding-model dijkstra
```

**Résultat attendu:**
```
=== Configuration ===
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
📏 Distance totale: 209.5 km
🛤️  Nombre d'étapes: 2

📊 Détails du trajet:
   🚄 [TGV        ] Toulouse Matabiau → Bordeaux Saint-Jean
      ⏱️ 143 min | 📏 209.5 km | 🚂 17 trains/jour
```

### Exemple 2: Trajet avec correspondance

```bash
python3 -m src.cli.pipeline \
    --audio data/raw/audio/sample_000193.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --pathfinding-model dijkstra
```

**Résultat attendu:**
```
=== Itinéraire ===
⏱️  Temps de trajet: 5h47 (348 min)
📏 Distance totale: 1186.0 km
🛤️  Nombre d'étapes: 6

📊 Détails du trajet:
   🚄 [TGV        ] Bordeaux Saint-Jean → Massy TGV
      ⏱️ 8.9 min | 📏 13.55 km | 🚂 143 trains/jour
   🚄 [TGV        ] Massy TGV → Marne-la-Vallée Chessy
      ⏱️ 15.2 min | 📏 25.3 km | 🚂 89 trains/jour
   🚄 [TGV        ] Marne-la-Vallée Chessy → Lyon Saint-Exupéry TGV
      ⏱️ 120.5 min | 📏 412.8 km | 🚂 45 trains/jour
   🚄 [TGV        ] Lyon Saint-Exupéry TGV → Aix-en-Provence TGV
      ⏱️ 95.3 min | 📏 298.2 km | 🚂 38 trains/jour
   🚄 [TGV        ] Aix-en-Provence TGV → Marseille Saint-Charles
      ⏱️ 15.1 min | 📏 31.2 km | 🚂 67 trains/jour
```

### Exemple 3: Sans pathfinding

```bash
python3 -m src.cli.pipeline \
    --audio data/raw/audio/sample.wav \
    --stt-model whisper \
    --nlp-model spacy
```

**Résultat:**
```
=== Résultats ===
Transcription: Je veux aller à Paris.
Origine: None
Destination: Paris
Valide: True
Confidence: 0.60
```

---

## Exemples de Résultats

### Résultat JSON complet

```json
{
  "audio_path": "data/raw/audio/sample_000160.wav",
  "transcript": "Je veux voyager de Toulouse à Bordeaux.",
  "origin": "Toulouse",
  "destination": "Bordeaux",
  "is_valid": true,
  "confidence": 0.70,
  "route": {
    "steps": [
      "Toulouse Matabiau",
      "Bordeaux Saint-Jean"
    ],
    "total_distance": 209.5,
    "total_time": 143.0,
    "metadata": {
      "origin_uic": "87611004",
      "destination_uic": "87581009",
      "path_uic": ["87611004", "87581009"],
      "num_stations": 2,
      "mode": "temps_reel",
      "segments": [
        {
          "from": "Toulouse Matabiau",
          "to": "Bordeaux Saint-Jean",
          "temps_min": 143.0,
          "distance_km": 209.5,
          "nb_trains_jour": 17,
          "type_train": "TGV",
          "types_details": {
            "TGV": 17
          },
          "geometry": {
            "type": "LineString",
            "coordinates": [
              [1.453616, 43.611206],
              [1.452123, 43.612345],
              ...
            ]
          }
        }
      ]
    }
  },
  "stt_metadata": {
    "model": "whisper-small",
    "segments": 1,
    "detected_language": "fr"
  },
  "nlp_metadata": {
    "model": "spacy-fr_core_news_md",
    "locations_found": ["Toulouse", "Bordeaux"],
    "extraction_method": "ner_patterns"
  }
}
```

### Rapport Markdown généré

Voir `results/pipeline/sample_000160_whisper_spacy_dijkstra_result.md` pour un exemple complet.

---

## API REST

### Démarrer l'API

```bash
cd /Users/antoinegourgue/Desktop/THOR
python3 api/app.py --preload
```

L'API démarre sur `http://localhost:8000`

### Endpoints disponibles

#### 1. `/api/health` (GET)

Vérifie l'état de l'API et des modèles.

```bash
curl http://localhost:8000/api/health
```

**Réponse:**
```json
{
  "status": "ok",
  "message": "THOR API is running",
  "models": {
    "stt": "not_loaded",
    "nlp": "loaded",
    "pathfinding": "loaded"
  }
}
```

#### 2. `/api/search` (POST)

Analyse un texte et trouve un itinéraire.

```bash
curl -X POST http://localhost:8000/api/search \
    -H "Content-Type: application/json" \
    -d '{"text": "Je veux aller de Paris à Lyon"}'
```

#### 3. `/api/pipeline` (POST)

Pipeline complète depuis un audio.

```bash
curl -X POST http://localhost:8000/api/pipeline \
    -H "Content-Type: application/json" \
    -d '{
        "audio": "base64_encoded_audio_here",
        "format": "wav"
    }'
```

#### 4. `/api/route` (POST)

Trouve un itinéraire entre deux villes.

```bash
curl -X POST http://localhost:8000/api/route \
    -H "Content-Type: application/json" \
    -d '{
        "origin": "Paris",
        "destination": "Lyon"
    }'
```

#### 5. `/api/preload` (POST)

Précharge tous les modèles.

```bash
curl -X POST http://localhost:8000/api/preload
```

---

## Interface Web

### Démarrage

```bash
cd web
npm install
npm run dev
```

L'interface démarre sur `http://localhost:3000`

### Fonctionnalités

1. **Recherche textuelle**
   - Saisie manuelle de la demande
   - Suggestions de trajets populaires

2. **Recherche vocale**
   - Enregistrement audio via microphone
   - Conversion automatique WebM → WAV
   - Pipeline complète: Audio → STT → NLP → Pathfinding

3. **Affichage des résultats**
   - Transcription de la demande
   - Détails de l'itinéraire (temps, distance, étapes)
   - Types de trains avec badges colorés (TGV, OUIGO, Intercités, TER)
   - **Correspondances inter-gare** affichées en jaune
   - **Carte interactive Leaflet** avec fonctionnalités avancées :
     - Tracés ferroviaires réels (géométries SNCF précises)
     - Filtrage intelligent des points aberrants (>50km)
     - Correspondances en lignes jaunes pointillées
     - Tracés incomplets en lignes pointillées (<80% valide)
     - Popups détaillées au clic
     - Restriction géographique à la France
     - Markers précis aux extrémités des segments

### Architecture frontend

- **Framework**: Next.js 14 (React) avec App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS (dark mode)
- **Cartes**: Leaflet.js + React Leaflet
- **Icônes**: Lucide React
- **API**: Proxy Next.js → Flask backend
- **Composants clés**:
  - `SearchInput`: Recherche vocale/textuelle
  - `RouteMapClient`: Carte interactive avec géométries
  - `RouteDetails`: Affichage détaillé des segments
  - `CodeBlock`: Documentation avec coloration syntaxique

---

## Conclusion

La pipeline THOR est un système complet et performant pour la recherche d'itinéraires ferroviaires via commande vocale. Elle combine les meilleures technologies d'IA (Whisper, spaCy) avec des algorithmes classiques optimisés (Dijkstra) pour offrir une expérience utilisateur fluide et précise.

### Points forts

- ✅ **Précision élevée** : Whisper (STT) + spaCy (NLP) avec validation robuste
- ✅ **Temps de trajet réels** : Données SNCF enrichies (11382+ liaisons)
- ✅ **Pénalités intelligentes** : Favorise TGV sans exclure alternatives
- ✅ **Correspondances inter-gare** : Support transferts métro Paris (×1.0 pas de pénalité)
- ✅ **Géométries précises** : Tracés ferroviaires réels avec filtrage intelligent
- ✅ **Interface web moderne** : Next.js 14 + Leaflet avec dark mode
- ✅ **API REST complète** : Flask avec lazy loading des modèles
- ✅ **Support multi-gares** : Gestion intelligente grandes villes
- ✅ **Visualisation avancée** : Correspondances en jaune, tracés incomplets détectés
- ✅ **Documentation interactive** : Guide complet accessible depuis l'interface

### Améliorations futures

#### Court terme
- Support correspondances Lyon, Marseille, Lille, Bordeaux
- Optimisation multi-critère (temps vs prix vs confort)
- Complétion géométries manquantes via OpenStreetMap
- Intégration API SNCF temps réel pour horaires dynamiques

#### Moyen terme
- Support de plusieurs langues (EN, ES, IT, DE)
- Prédiction des retards via machine learning
- Suggestions d'alternatives (Top-K chemins)
- Historique des recherches utilisateur
- Export PDF des itinéraires avec QR codes

#### Long terme
- Intégration multimodale (bus, avion, covoiturage)
- Optimisation CO2 et affichage empreinte carbone
- Personnalisation avancée (fenêtre, couloir, 1ère classe)
- Réservation intégrée avec systèmes SNCF
- Analytics et recommandations basées sur l'historique

---

**Document généré automatiquement par THOR Pipeline**  
**Pour plus d'informations**: https://github.com/THOR-EPITECH/THOR
