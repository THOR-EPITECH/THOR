# Modèle STT : Whisper

## Vue d'ensemble

Whisper est un modèle de transcription automatique développé par OpenAI. Il est très précis, multilingue et open-source. Il supporte plusieurs tailles de modèles avec un compromis entre précision et vitesse.

## Caractéristiques

- **Précision** : ⭐⭐⭐⭐⭐ (Excellente)
- **Vitesse** : ⭐⭐⭐ (Moyenne à lente selon la taille)
- **Multilingue** : ✅ (99 langues supportées)
- **Offline** : ✅ (Fonctionne sans connexion internet)
- **GPU requis** : Recommandé pour les gros modèles (medium, large)

## Tailles de modèles disponibles

| Taille | Paramètres | Taille disque | Vitesse (RTF) | Précision |
|--------|------------|---------------|---------------|-----------|
| tiny | 39M | ~75 MB | ~0.1x | ⭐⭐ |
| base | 74M | ~150 MB | ~0.2x | ⭐⭐⭐ |
| small | 244M | ~500 MB | ~0.5x | ⭐⭐⭐⭐ |
| medium | 769M | ~1.5 GB | ~1.5x | ⭐⭐⭐⭐⭐ |
| large | 1550M | ~3 GB | ~3x | ⭐⭐⭐⭐⭐ |

**Note** : RTF (Real-time Factor) < 1 signifie traitement plus rapide que le temps réel.

## Installation

```bash
pip install openai-whisper
```

**Dépendances optionnelles** (recommandées) :
```bash
pip install soundfile librosa
```

Ces bibliothèques permettent de charger l'audio sans nécessiter `ffmpeg`.

## Configuration

### Fichier de configuration

```yaml
# configs/stt/whisper_small.yaml
model: whisper
model_size: small      # tiny, base, small, medium, large
language: fr          # Code langue ISO (fr, en, etc.)
device: cpu           # cpu ou cuda
```

### Paramètres

- **model_size** : Taille du modèle (`tiny`, `base`, `small`, `medium`, `large`)
- **language** : Langue du modèle (code ISO, ex: `fr`, `en`)
- **device** : Périphérique (`cpu` ou `cuda` pour GPU)

## Utilisation

### Via CLI

```bash
# Transcription simple
python -m src.cli.stt transcribe \
    --model whisper \
    --audio data/raw/audio/sample.wav

# Avec configuration personnalisée
python -m src.cli.stt transcribe \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --audio data/raw/audio/sample.wav
```

### Via Python

```python
from src.stt.models.whisper import WhisperModel

# Initialisation
model = WhisperModel({
    "model_size": "small",
    "language": "fr",
    "device": "cpu"
})

# Transcription
result = model.transcribe("audio.wav")
print(f"Texte: {result.text}")
print(f"Langue détectée: {result.language}")
print(f"Temps de traitement: {result.processing_time:.2f}s")
```

## Format audio supporté

Whisper accepte tous les formats audio supportés par `ffmpeg` ou `librosa` :
- WAV, MP3, FLAC, OGG, M4A, etc.

**Recommandation** : WAV 16kHz mono pour de meilleures performances.

## Résultat

Le modèle retourne un objet `STTResult` :

```python
STTResult(
    text="Je voudrais aller à Paris depuis Lyon",
    confidence=None,  # Whisper ne retourne pas de confidence globale
    language="fr",
    processing_time=2.5,
    metadata={
        "model": "whisper-small",
        "segments": 1,
        "detected_language": "fr"
    }
)
```

## Performance

### Exemple de latence (CPU, Intel i7)

| Taille | Durée audio | Temps traitement | RTF |
|--------|-------------|------------------|-----|
| tiny | 5s | 0.5s | 0.1x |
| base | 5s | 1.0s | 0.2x |
| small | 5s | 2.5s | 0.5x |
| medium | 5s | 7.5s | 1.5x |
| large | 5s | 15s | 3.0x |

**Note** : Les performances varient selon le matériel. Un GPU peut réduire significativement le temps de traitement.

## Avantages

1. **Précision exceptionnelle** : Meilleur modèle open-source disponible
2. **Multilingue** : Supporte 99 langues
3. **Robuste** : Gère bien les accents, bruit, différents locuteurs
4. **Open-source** : Pas de limitation d'utilisation

## Inconvénients

1. **Lent** : Les gros modèles peuvent être lents sur CPU
2. **Ressources** : Nécessite beaucoup de RAM et de stockage pour les gros modèles
3. **GPU recommandé** : Les modèles medium/large sont beaucoup plus rapides sur GPU

## Recommandations

- **Développement/Test** : `tiny` ou `base` (rapide, suffisant pour tester)
- **Production (CPU)** : `small` (bon compromis précision/vitesse)
- **Production (GPU)** : `medium` ou `large` (meilleure précision)

## Dépannage

### Erreur : "Model not found"
```bash
# Le modèle sera téléchargé automatiquement au premier usage
# Ou téléchargez manuellement :
python -c "import whisper; whisper.load_model('small')"
```

### Erreur : "ffmpeg not found"
```bash
# Installez ffmpeg ou utilisez soundfile/librosa :
pip install soundfile librosa
```

### Performance lente
- Utilisez un modèle plus petit (`tiny`, `base`)
- Utilisez un GPU si disponible (`device: cuda`)
- Réduisez la qualité audio (16kHz mono suffit)

## Références

- [Documentation Whisper](https://github.com/openai/whisper)
- [Paper Whisper](https://arxiv.org/abs/2212.04356)
