# Guide d'utilisation - Génération de dataset STT

## Workflow complet

### Étape 1 : Générer le dataset JSONL

```bash
# Depuis la racine du projet
PYTHONPATH=. python3 scripts/generate_stt_dataset.py \
    --output-dir data/splits \
    --num-samples 1000 \
    --audio-dir data/raw/audio \
    --seed 42
```

Cela génère :
- `data/splits/train/train.jsonl` (70% des données)
- `data/splits/valid/valid.jsonl` (15% des données)
- `data/splits/test/test.jsonl` (15% des données)
- `data/splits/full_dataset.jsonl` (dataset complet)

### Étape 2 : Générer les fichiers audio

#### Option A : Avec gTTS (recommandé pour qualité)

```bash
# Installer gTTS
pip install gtts

# Générer les audios
PYTHONPATH=. python3 scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine gtts
```

**Note** : gTTS nécessite une connexion internet et peut avoir des limites de requêtes.

#### Option B : Avec pyttsx3 (offline)

```bash
# Installer pyttsx3
pip install pyttsx3

# Générer les audios
PYTHONPATH=. python3 scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine pyttsx3
```

### Étape 3 : Vérifier

```bash
# Vérifier les fichiers audio générés
ls -lh data/raw/audio/ | head -20

# Vérifier le dataset
wc -l data/splits/train/train.jsonl
wc -l data/splits/test/test.jsonl
wc -l data/splits/valid/valid.jsonl
```

## Diversité du dataset

Le script génère automatiquement :

### ✅ Demandes de trajet complètes (30%)
- "Je veux aller à Paris depuis Lyon"
- "Comment me rendre à Marseille ?"

### ✅ Demandes sans destination (5%)
- "Je veux partir de Lyon"
- "Comment partir de Paris ?"

### ✅ Demandes sans origine (10%)
- "Je veux aller à Paris"
- "Comment me rendre à Marseille ?"

### ✅ Phrases avec villes mais PAS trajet (15%)
- "Paris est la capitale de la France"
- "J'ai visité Lyon l'année dernière"
- "Mon ami habite à Bordeaux"

### ✅ Phrases de la vie quotidienne (15%)
- "Quel temps fait-il aujourd'hui ?"
- "J'ai faim, on va manger ?"
- "Quelle heure est-il ?"

### ✅ Tournures de phrases différentes (10%)
- "Serait-il possible d'aller à Paris depuis Lyon ?"
- "Auriez-vous l'amabilité de me dire comment me rendre à Marseille ?"

### ✅ Variations de ponctuation (5%)
- "Je veux aller à Paris depuis Lyon."
- "Je veux aller à Paris depuis Lyon !"
- "Je veux aller à Paris... depuis Lyon"

### ✅ Phrases en anglais (5%)
- "I want to go to Paris from Lyon"
- "How can I get to Marseille?"

### ✅ Phrases en espagnol (2%)
- "Quiero ir a París desde Lyon"
- "¿Cómo puedo llegar a Marsella?"

### ✅ Hésitations (2%)
- "Euh... je veux aller à Paris... depuis Lyon"
- "Je veux... aller à Paris... depuis Lyon"

### ✅ Niveaux de formalité (1%)
- "Je souhaiterais me rendre à Paris en partant de Lyon" (formel)
- "J'veux aller à Paris depuis Lyon" (familier)

## Personnalisation

Pour modifier les phrases ou les proportions, éditez `scripts/generate_stt_dataset.py` :

```python
# Modifier les proportions
categories = [
    (TRAVEL_REQUESTS_COMPLETE, 0.30),  # Changez 0.30 pour modifier la proportion
    # ...
]

# Ajouter vos propres phrases
MY_CUSTOM_PHRASES = [
    "Votre phrase personnalisée ici",
    # ...
]
```

## Notes importantes

1. **Format audio** : Les fichiers générés sont en WAV/MP3. Le code convertira automatiquement en 16kHz mono si nécessaire.

2. **Détection de langue** : Le script détecte automatiquement la langue (fr/en/es) pour utiliser la bonne voix TTS.

3. **Reproductibilité** : Utilisez `--seed 42` pour obtenir le même dataset à chaque fois.

4. **Taille** : Pour 1000 échantillons, comptez environ :
   - ~50-100 MB de fichiers audio (selon la durée)
   - Quelques minutes de génération avec gTTS

5. **Limites gTTS** : Google TTS peut avoir des limites de requêtes. Si vous générez beaucoup d'audios, utilisez pyttsx3 ou un service cloud.

