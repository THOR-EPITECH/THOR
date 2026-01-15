# Modèle STT : Vosk

## Vue d'ensemble

Vosk est un moteur de reconnaissance vocale offline, open-source et léger. Il est optimisé pour le français et fonctionne sans connexion internet. Idéal pour les applications nécessitant une faible latence et un traitement local.

## Caractéristiques

- **Précision** : ⭐⭐⭐ (Bonne)
- **Vitesse** : ⭐⭐⭐⭐⭐ (Très rapide)
- **Multilingue** : ❌ (Spécialisé français)
- **Offline** : ✅ (Fonctionne sans connexion)
- **GPU requis** : ❌ (Fonctionne sur CPU)

## Installation

```bash
pip install vosk
```

## Téléchargement du modèle

Vosk nécessite un modèle pré-entraîné téléchargé séparément. Plusieurs modèles sont disponibles :

| Modèle | Taille | Précision | Vitesse |
|--------|--------|-----------|---------|
| vosk-model-small-fr-0.22 | ~45 MB | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| vosk-model-fr-0.22 | ~1.5 GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| vosk-model-fr-0.6 | ~1.8 GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**Téléchargement** :
```bash
# Créez le dossier models
mkdir -p models/vosk-fr

# Téléchargez un modèle depuis :
# https://alphacephei.com/vosk/models
# Exemple pour le modèle français :
wget https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip
unzip vosk-model-fr-0.22.zip -d models/vosk-fr
```

## Configuration

### Fichier de configuration

```yaml
# configs/stt/vosk.yaml
model: vosk
model_path: models/vosk-fr/vosk-model-fr-0.22
sample_rate: 16000
```

### Paramètres

- **model_path** : Chemin vers le dossier du modèle Vosk téléchargé
- **sample_rate** : Taux d'échantillonnage (généralement 16000 Hz)

## Utilisation

### Via CLI

```bash
# Transcription simple
python -m src.cli.stt transcribe \
    --model vosk \
    --audio data/raw/audio/sample.wav

# Avec configuration personnalisée
python -m src.cli.stt transcribe \
    --model vosk \
    --config configs/stt/vosk.yaml \
    --audio data/raw/audio/sample.wav
```

### Via Python

```python
from src.stt.models.vosk import VoskModel

# Initialisation
model = VoskModel({
    "model_path": "models/vosk-fr/vosk-model-fr-0.22",
    "sample_rate": 16000
})

# Transcription
result = model.transcribe("audio.wav")
print(f"Texte: {result.text}")
print(f"Temps de traitement: {result.processing_time:.2f}s")
```

## Format audio requis

Vosk nécessite un fichier audio au format **WAV** avec les spécifications suivantes :
- **Format** : WAV (non compressé)
- **Sample rate** : 16000 Hz
- **Channels** : Mono (1 canal)
- **Bit depth** : 16-bit

**Conversion audio** :
```bash
# Avec ffmpeg
ffmpeg -i input.mp3 -ar 16000 -ac 1 -sample_fmt s16 output.wav
```

## Résultat

Le modèle retourne un objet `STTResult` :

```python
STTResult(
    text="Je voudrais aller à Paris depuis Lyon",
    confidence=None,  # Vosk ne retourne pas de confidence globale
    language="fr",
    processing_time=0.5,
    metadata={
        "model": "vosk",
        "model_path": "models/vosk-fr/vosk-model-fr-0.22"
    }
)
```

## Performance

### Exemple de latence (CPU)

| Durée audio | Temps traitement | RTF |
|-------------|------------------|-----|
| 1s | 0.05s | 0.05x |
| 5s | 0.25s | 0.05x |
| 10s | 0.5s | 0.05x |

**Note** : Vosk est généralement 5-10x plus rapide que Whisper sur CPU.

## Avantages

1. **Très rapide** : Traitement en temps réel ou plus rapide
2. **Léger** : Modèles petits disponibles (45 MB pour small)
3. **Offline** : Aucune connexion internet requise
4. **Faible latence** : Idéal pour applications temps réel
5. **CPU uniquement** : Pas besoin de GPU

## Inconvénients

1. **Précision inférieure** : Moins précis que Whisper
2. **Format audio strict** : Nécessite WAV 16kHz mono
3. **Unilingue** : Spécialisé français uniquement
4. **Modèle à télécharger** : Nécessite téléchargement séparé

## Recommandations

- **Applications temps réel** : Vosk est idéal pour la reconnaissance vocale en direct
- **Ressources limitées** : Utilisez le modèle small pour les environnements contraints
- **Précision maximale** : Utilisez le modèle large (vosk-model-fr-0.6)

## Dépannage

### Erreur : "Vosk model not found"
```bash
# Vérifiez que le chemin du modèle est correct
# Le dossier doit contenir les fichiers du modèle Vosk
ls models/vosk-fr/
```

### Erreur : "Audio format not supported"
- Vosk nécessite WAV 16kHz mono
- Convertissez votre audio avec ffmpeg :
```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 -sample_fmt s16 output.wav
```

### Performance dégradée
- Vérifiez que l'audio est bien en 16kHz mono
- Utilisez un modèle plus grand pour plus de précision

## Références

- [Site officiel Vosk](https://alphacephei.com/vosk/)
- [Modèles disponibles](https://alphacephei.com/vosk/models)
- [Documentation Vosk](https://github.com/alphacep/vosk-api)
