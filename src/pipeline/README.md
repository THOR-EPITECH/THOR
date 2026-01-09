# Pipeline complet Audio → STT → NLP

## Vue d'ensemble

Le pipeline orchestre le flux complet :
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte

## Utilisation

### Via CLI

```bash
# Pipeline complet avec Whisper + spaCy
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000001.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --output results/pipeline_result.json
```

### Options

- `--audio` : Chemin vers le fichier audio (requis)
- `--stt-model` : Modèle STT à utiliser (`whisper`, `vosk`) - défaut: `whisper`
- `--nlp-model` : Modèle NLP à utiliser (`spacy`) - défaut: `spacy`
- `--config` : Fichier de configuration YAML (optionnel)
- `--output` : Chemin pour sauvegarder les résultats JSON (optionnel)

### Exemple de résultat

```json
{
  "audio_path": "data/raw/audio/sample_000001.wav",
  "transcript": "Je voudrais bien aller à Paris.",
  "origin": null,
  "destination": "Paris",
  "is_valid": true,
  "confidence": 0.7,
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
Result: {origin, destination, is_valid}
```

## Modèles supportés

### STT
- **Whisper** : Recommandé, très précis
- **Vosk** : Offline, rapide

### NLP
- **spaCy** : Utilise NER (Named Entity Recognition) + patterns

## Via Python

```python
from src.pipeline.orchestrator import Pipeline
from src.stt.models.whisper import WhisperModel
from src.nlp.models.spacy_fr import SpacyFRModel

# Initialise les modèles
stt_model = WhisperModel({"model_size": "small", "language": "fr"})
nlp_model = SpacyFRModel({"model_name": "fr_core_news_md"})

# Crée le pipeline
pipeline = Pipeline(stt_model, nlp_model)

# Traite un audio
result = pipeline.process("audio.wav")

print(f"Origine: {result['origin']}")
print(f"Destination: {result['destination']}")
```

