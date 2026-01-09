# Module Speech-to-Text

## Vue d'ensemble

Le module STT convertit la parole en texte. Il supporte plusieurs modèles et permet de les comparer via un système de benchmark.

## Modèles disponibles

### 1. Whisper (OpenAI)

**Fichier**: `src/stt/models/whisper.py`

**Caractéristiques**:
- Modèles: tiny, base, small, medium, large
- Multilingue (détection automatique)
- Très précis
- Nécessite GPU pour les gros modèles

**Configuration**:
```yaml
model: whisper
model_size: small
language: fr
device: cpu  # ou "cuda"
```

**Utilisation**:
```python
from src.stt.models.whisper import WhisperModel

model = WhisperModel({"model_size": "small", "language": "fr"})
result = model.transcribe("audio.wav")
print(result.text)
```

### 2. Vosk

**Fichier**: `src/stt/models/vosk.py`

**Caractéristiques**:
- Offline (pas besoin d'internet)
- Rapide et léger
- Modèles français pré-entraînés
- Moins précis que Whisper

**Configuration**:
```yaml
model: vosk
model_path: models/vosk-fr
sample_rate: 16000
```

**Utilisation**:
```python
from src.stt.models.vosk import VoskModel

model = VoskModel({"model_path": "models/vosk-fr"})
result = model.transcribe("audio.wav")
print(result.text)
```

### 3. Dummy (baseline)

**Fichier**: `src/stt/models/dummy.py`

**Usage**: Tests et baseline pour valider le pipeline.

## Métriques

### Word Error Rate (WER)
Taux d'erreur au niveau des mots. 0.0 = parfait, 1.0+ = erreurs.

### Character Error Rate (CER)
Taux d'erreur au niveau des caractères.

### Latency
Temps de traitement en secondes.

### Real-Time Factor (RTF)
Ratio temps de traitement / durée audio. RTF < 1.0 signifie traitement plus rapide que la durée audio.

## Évaluation

### Via CLI
```bash
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --output-dir results/stt/whisper_test \
    --analyze-errors
```

### Via Python
```python
from src.stt.eval.evaluate import evaluate_model
from src.stt.models.whisper import WhisperModel

model = WhisperModel({"model_size": "small"})
metrics = evaluate_model(
    model,
    "data/splits/test/test.jsonl",
    "results/stt/whisper_test"
)
```

## Format du dataset

Le dataset doit être au format JSONL avec une ligne par échantillon :

```json
{"id": "sample_001", "audio_path": "data/raw/audio/sample_001.wav", "transcript": "Je veux aller à Paris"}
{"id": "sample_002", "audio_path": "data/raw/audio/sample_002.wav", "transcript": "Depuis Lyon, je voudrais me rendre à Marseille"}
```

## Ajouter un nouveau modèle

1. Créez un fichier dans `src/stt/models/` (ex: `my_model.py`)
2. Implémentez l'interface `STTModel` :
```python
from src.stt.interfaces import STTModel
from src.common.types import STTResult

class MyModel(STTModel):
    def transcribe(self, audio_path: str) -> STTResult:
        # Votre implémentation
        return STTResult(text="...", processing_time=0.5)
```

3. Créez une configuration dans `configs/stt/my_model.yaml`
4. Ajoutez le modèle dans `src/cli/stt.py` si nécessaire

Voir `src/stt/models/dummy.py` pour un exemple minimal.

