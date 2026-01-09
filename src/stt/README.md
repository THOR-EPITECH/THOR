# Module Speech-to-Text (STT)

## Vue d'ensemble

Ce module gère la conversion de la parole en texte. Il supporte plusieurs modèles (Whisper, Vosk, Google STT) et permet de les comparer via un système de benchmark.

## Architecture

```
stt/
  interfaces.py      # Interface STTModel
  models/            # Implémentations des modèles
  eval/              # Métriques et évaluation
```

## Interface standard

Tous les modèles STT implémentent l'interface `STTModel` :

```python
class STTModel(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> STTResult:
        """Transcrit un fichier audio en texte."""
        pass
```

## Modèles disponibles

### 1. Whisper (OpenAI)
- **Fichier**: `models/whisper.py`
- **Modèles**: tiny, base, small, medium, large
- **Avantages**: Très précis, multilingue
- **Inconvénients**: Plus lent, nécessite GPU pour les gros modèles

### 2. Vosk
- **Fichier**: `models/vosk.py`
- **Modèles**: Modèles français pré-entraînés
- **Avantages**: Rapide, léger, fonctionne offline
- **Inconvénients**: Moins précis que Whisper

### 3. Google Speech-to-Text
- **Fichier**: `models/google_stt.py`
- **Avantages**: Très précis, API cloud
- **Inconvénients**: Nécessite connexion internet, coût

### 4. Dummy (baseline)
- **Fichier**: `models/dummy.py`
- **Usage**: Tests et baseline

## Métriques

- **WER** (Word Error Rate) : Taux d'erreur de mots
- **CER** (Character Error Rate) : Taux d'erreur de caractères
- **Latency** : Temps de traitement
- **Real-time Factor (RTF)** : Ratio temps traitement / durée audio

## Utilisation

### Via CLI
```bash
python -m src.cli.stt transcribe --model whisper --audio path/to/audio.wav
python -m src.cli.stt evaluate --model whisper --config configs/stt/whisper_small.yaml
```

### Via Python
```python
from src.stt.models.whisper import WhisperModel

model = WhisperModel(model_size="small")
result = model.transcribe("audio.wav")
print(result.text)
```

## Ajouter un nouveau modèle

1. Créer un fichier dans `models/` (ex: `my_model.py`)
2. Implémenter `STTModel`
3. Enregistrer dans `models/__init__.py`
4. Créer une config dans `configs/stt/`

Voir `models/dummy.py` pour un exemple minimal.

