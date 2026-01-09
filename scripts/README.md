# Scripts utilitaires

## Génération de dataset STT

### 1. Générer le dataset JSONL

Crée un dataset JSONL avec une grande variété de phrases :

```bash
python scripts/generate_stt_dataset.py \
    --output-dir data/splits \
    --num-samples 1000 \
    --audio-dir data/raw/audio \
    --seed 42
```

**Caractéristiques du dataset généré** :
- ✅ Demandes de trajet complètes (30%)
- ✅ Demandes sans destination (5%)
- ✅ Demandes sans origine (10%)
- ✅ Phrases avec villes mais pas trajet (15%)
- ✅ Phrases de la vie quotidienne (15%)
- ✅ Tournures de phrases différentes (10%)
- ✅ Variations de ponctuation (5%)
- ✅ Phrases en anglais (5%)
- ✅ Phrases en espagnol (2%)
- ✅ Hésitations (2%)
- ✅ Niveaux de formalité différents (1%)

Le script génère automatiquement les splits train/valid/test (70/15/15).

### 2. Générer les fichiers audio

Une fois le dataset JSONL créé, générez les fichiers audio :

#### Option A : Avec gTTS (Google Text-to-Speech) - Nécessite internet

```bash
# Installe gTTS
pip install gtts

# Génère les audios
python scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine gtts
```

**Avantages** : Qualité élevée, plusieurs langues, gratuit
**Inconvénients** : Nécessite internet, limite de requêtes

#### Option B : Avec pyttsx3 (offline)

```bash
# Installe pyttsx3
pip install pyttsx3

# Génère les audios
python scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine pyttsx3
```

**Avantages** : Offline, pas de limite
**Inconvénients** : Qualité variable selon le système

#### Option C : Avec un service cloud (Azure, AWS, etc.)

Pour une meilleure qualité, vous pouvez utiliser :
- Azure Cognitive Services Speech
- AWS Polly
- Google Cloud Text-to-Speech

Il faudra adapter le script `generate_audio.py` pour utiliser ces services.

### 3. Workflow complet

```bash
# 1. Génère le dataset JSONL
python scripts/generate_stt_dataset.py \
    --output-dir data/splits \
    --num-samples 1000

# 2. Génère les fichiers audio
python scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine gtts

# 3. Vérifie que tout est OK
ls -la data/raw/audio/ | head -10
wc -l data/splits/train/train.jsonl
```

## Préparation des splits

Pour diviser un dataset existant en train/test/valid :

```bash
python scripts/prepare_splits.py \
    --input data/raw/sentences/all.jsonl \
    --output data/splits \
    --train-ratio 0.7 \
    --valid-ratio 0.15 \
    --test-ratio 0.15 \
    --seed 42
```

## Notes importantes

### Format des fichiers audio

Les fichiers audio générés doivent être :
- Format : WAV (recommandé) ou MP3
- Sample rate : 16 kHz (sera converti automatiquement si nécessaire)
- Channels : Mono
- Bit depth : 16-bit

### Diversité du dataset

Le script `generate_stt_dataset.py` génère automatiquement :
- Différentes intonations (via variations de ponctuation)
- Différentes langues (français, anglais, espagnol)
- Phrases avec villes mais pas trajets
- Demandes incomplètes (sans origine ou destination)
- Tournures variées
- Phrases quotidiennes

### Personnalisation

Vous pouvez modifier `scripts/generate_stt_dataset.py` pour :
- Ajouter vos propres phrases
- Ajuster les proportions de chaque catégorie
- Ajouter d'autres langues
- Modifier les variations

