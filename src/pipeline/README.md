# Pipeline complet Audio → STT → NLP → Pathfinding

## Vue d'ensemble

Le pipeline orchestre le flux complet :
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte
3. **Pathfinding** : Recherche d'itinéraire optimal entre les gares (optionnel)

## Utilisation

### Via CLI

```bash
# Pipeline complet avec Whisper + spaCy (sans pathfinding)
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000001.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --output results/pipeline_result.json

# Pipeline complet avec pathfinding
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --pathfinding-model dijkstra
```

### Options

- `--audio` : Chemin vers le fichier audio (requis)
- `--stt-model` : Modèle STT à utiliser (`whisper`, `vosk`) - défaut: `whisper`
- `--nlp-model` : Modèle NLP à utiliser (`spacy`) - défaut: `spacy`
- `--pathfinding-model` : Modèle Pathfinding à utiliser (`dijkstra`) - optionnel
- `--config` : Fichier de configuration YAML (optionnel)
- `--output` : Chemin pour sauvegarder les résultats JSON (optionnel)

### Exemple de résultat (sans pathfinding)

```json
{
  "audio_path": "data/raw/audio/sample_000001.wav",
  "transcript": "Je voudrais bien aller à Paris.",
  "origin": null,
  "destination": "Paris",
  "is_valid": true,
  "confidence": 0.7,
  "stt_metadata": {...},
  "nlp_metadata": {...},
  "route": null
}
```

### Exemple de résultat (avec pathfinding)

```json
{
  "audio_path": "data/raw/audio/sample_000160.wav",
  "transcript": "Je veux voyager de Toulouse à Bordeaux.",
  "origin": "Toulouse",
  "destination": "Bordeaux",
  "is_valid": true,
  "confidence": 0.7,
  "route": {
    "steps": ["Toulouse Matabiau", "Bordeaux Saint-Jean"],
    "total_distance": 216.83,
    "total_time": null,
    "metadata": {
      "origin_uic": "87611000",
      "destination_uic": "87581000",
      "num_stations": 2
    }
  },
  "stt_metadata": {...},
  "nlp_metadata": {...}
}
```

## Architecture

```
Audio File
    ↓
[STT Model] → Transcription textuelle
    ↓
[NLP Model] → Extraction origine/destination
    ↓
[Pathfinding Model] → Recherche d'itinéraire (optionnel)
    ↓
Result: {origin, destination, is_valid, route}
```

## Modèles supportés

### STT
- **Whisper** : Recommandé, très précis
- **Vosk** : Offline, rapide

### NLP
- **spaCy** : Utilise NER (Named Entity Recognition) + patterns

### Pathfinding
- **Dijkstra** : Algorithme de recherche du chemin le plus court entre gares

## Via Python

```python
from src.pipeline.orchestrator import Pipeline
from src.stt.models.whisper import WhisperModel
from src.nlp.models.spacy_fr import SpacyFRModel
from src.pathfinding.models.dijkstra import DijkstraPathfindingModel

# Initialise les modèles
stt_model = WhisperModel({"model_size": "small", "language": "fr"})
nlp_model = SpacyFRModel({"model_name": "fr_core_news_md"})
pathfinding_model = DijkstraPathfindingModel({
    "path_gares": "data/train_station/dataset_gares.json",
    "path_liaisons": "data/train_station/dataset_liaisons.json"
})

# Crée le pipeline avec pathfinding
pipeline = Pipeline(stt_model, nlp_model, pathfinding_model)

# Traite un audio
result = pipeline.process("audio.wav")

print(f"Origine: {result['origin']}")
print(f"Destination: {result['destination']}")

# Affiche l'itinéraire si disponible
if result.get('route') and result['route'].get('steps'):
    route = result['route']
    print(f"Distance: {route['total_distance']:.2f} km")
    print(f"Étapes: {', '.join(route['steps'])}")
```

