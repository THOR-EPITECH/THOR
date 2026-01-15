# Documentation des Modèles STT (Speech-to-Text)

## Vue d'ensemble

Le module STT (Speech-to-Text) convertit les fichiers audio en texte. Il supporte plusieurs modèles avec différentes caractéristiques de performance, précision et ressources nécessaires.

## Modèles disponibles

### 1. [Whisper](./whisper.md)
- **Recommandé pour** : Précision maximale, multilingue
- **Avantages** : Très précis, support multilingue, modèle open-source d'OpenAI
- **Inconvénients** : Plus lent, nécessite plus de ressources (GPU recommandé pour les gros modèles)
- **Fichier** : `src/stt/models/whisper.py`

### 2. [Vosk](./vosk.md)
- **Recommandé pour** : Traitement offline, rapidité
- **Avantages** : Rapide, léger, fonctionne offline, pas besoin de GPU
- **Inconvénients** : Moins précis que Whisper, nécessite téléchargement de modèle
- **Fichier** : `src/stt/models/vosk.py`

### 3. [Dummy](./dummy.md)
- **Recommandé pour** : Tests et baseline
- **Avantages** : Aucune dépendance, instantané
- **Inconvénients** : Ne fait pas de vraie transcription
- **Fichier** : `src/stt/models/dummy.py`

## Métriques d'évaluation

Les modèles STT sont évalués selon plusieurs métriques :

- **WER (Word Error Rate)** : Taux d'erreur de mots (plus bas = mieux)
- **CER (Character Error Rate)** : Taux d'erreur de caractères (plus bas = mieux)
- **Latency** : Temps de traitement (plus bas = mieux)
- **RTF (Real-time Factor)** : Ratio temps traitement / durée audio (RTF < 1 = temps réel)

## Utilisation

### Via CLI

```bash
# Transcrire un fichier audio
python -m src.cli.stt transcribe \
    --model whisper \
    --audio path/to/audio.wav

# Évaluer un modèle
python -m src.cli.stt evaluate \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --dataset data/splits/stt/test/test.jsonl
```

### Via Python

```python
from src.stt.models.whisper import WhisperModel

model = WhisperModel({
    "model_size": "small",
    "language": "fr",
    "device": "cpu"
})
result = model.transcribe("audio.wav")
print(result.text)
```

## Interface standard

Tous les modèles STT implémentent l'interface `STTModel` :

```python
class STTModel(ABC):
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """Transcrit un fichier audio en texte."""
        pass
```

## Résultat de transcription

Tous les modèles retournent un objet `STTResult` :

```python
@dataclass
class STTResult:
    text: str                    # Texte transcrit
    confidence: Optional[float]  # Confiance (si disponible)
    language: str                # Langue détectée
    processing_time: float       # Temps de traitement (secondes)
    metadata: Dict[str, Any]     # Métadonnées supplémentaires
```

## Comparaison rapide

| Modèle | Précision | Vitesse | Offline | GPU requis | Multilingue |
|--------|-----------|---------|---------|------------|-------------|
| Whisper | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Recommandé | ✅ |
| Vosk | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ❌ | ❌ (FR) |
| Dummy | ❌ | ⭐⭐⭐⭐⭐ | ✅ | ❌ | ❌ |

## Configuration

Chaque modèle peut être configuré via un fichier YAML dans `configs/stt/` :

```yaml
# configs/stt/whisper_small.yaml
model: whisper
model_size: small
language: fr
device: cpu
```

## Ajouter un nouveau modèle

Pour ajouter un nouveau modèle STT :

1. Créer un fichier dans `src/stt/models/` (ex: `my_model.py`)
2. Implémenter la classe héritant de `STTModel`
3. Implémenter la méthode `transcribe()`
4. Enregistrer le modèle dans le registre (voir `src/common/registry.py`)
