# Module Speech-to-Text

Module de reconnaissance vocale (speech-to-text) utilisant Whisper pour le projet THOR.

## Table des matières

1. [Installation](#installation)
2. [Utilisation rapide](#utilisation-rapide)
3. [Architecture](#architecture)
4. [API](#api)
5. [Modèles disponibles](#modèles-disponibles)
6. [Exemples](#exemples)
7. [Intégration avec NLP](#intégration-avec-nlp)
8. [Tests](#tests)

---

## Installation

### Dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :
- `openai-whisper` : Modèle Whisper pour la transcription
- `torch` : Framework PyTorch
- `numpy` : Calculs numériques
- `sounddevice` : Capture audio depuis le microphone

---

## Utilisation rapide

### Transcription depuis le microphone

```python
from src.speech_to_text.factory import SpeechToTextFactory

# Créer un modèle
model = SpeechToTextFactory.create("whisper-base")

# Transcrire depuis le microphone
result = model.transcribe_from_microphone(duration=5.0, language="fr")

if result.is_valid:
    print(f"Texte transcrit: {result.text}")
    print(f"Confiance: {result.confidence:.2%}")
```

### Transcription d'un fichier audio

```python
from pathlib import Path

# Transcrire un fichier
audio_path = Path("data/audio/commande.wav")
result = model.transcribe(audio_path, language="fr")

print(result.text)
```

---

## Architecture

Le module suit l'architecture définie dans la documentation du projet :

```
src/speech_to_text/
├── base/
│   └── model_interface.py      # Interface commune (SpeechToTextInterface)
├── models/
│   └── whisper_model.py        # Implémentation Whisper
├── factory.py                   # Factory pour créer les modèles
└── README.md                    # Cette documentation
```

### Principes

- **Interface commune** : Tous les modèles implémentent `SpeechToTextInterface`
- **Factory Pattern** : Création simple via `SpeechToTextFactory`
- **Extensibilité** : Facile d'ajouter d'autres modèles (Wav2Vec2, etc.)

---

## API

### SpeechToTextFactory

Factory pour créer des instances de modèles.

#### Méthodes

##### `create(model_type: str, **kwargs) -> SpeechToTextInterface`

Crée une instance d'un modèle speech-to-text.

**Paramètres :**
- `model_type` (str) : Type de modèle (`whisper-tiny`, `whisper-base`, etc.)
- `**kwargs` : Arguments additionnels (ex: `model_size`, `device`)

**Retourne :**
- Instance du modèle implémentant `SpeechToTextInterface`

**Exemple :**
```python
model = SpeechToTextFactory.create("whisper-base")
model = SpeechToTextFactory.create("whisper-small", device="cuda")
```

##### `list_available_models() -> list[str]`

Liste tous les modèles disponibles.

**Retourne :**
- Liste des noms de modèles disponibles

**Exemple :**
```python
models = SpeechToTextFactory.list_available_models()
# ['whisper-tiny', 'whisper-base', 'whisper-small', ...]
```

### SpeechToTextInterface

Interface commune pour tous les modèles de reconnaissance vocale.

#### Méthodes

##### `transcribe(audio_path: str | Path, language: Optional[str] = None) -> TranscriptionResult`

Transcrit un fichier audio en texte.

**Paramètres :**
- `audio_path` : Chemin vers le fichier audio
- `language` : Code langue ISO (ex: `"fr"`, `"en"`). Si `None`, détection automatique.

**Retourne :**
- `TranscriptionResult` : Résultat de la transcription

##### `transcribe_from_bytes(audio_bytes: bytes, sample_rate: int = 16000, language: Optional[str] = None) -> TranscriptionResult`

Transcrit des données audio brutes en texte.

**Paramètres :**
- `audio_bytes` : Données audio brutes (format PCM 16-bit)
- `sample_rate` : Taux d'échantillonnage en Hz (défaut: 16000)
- `language` : Code langue ISO (optionnel)

**Retourne :**
- `TranscriptionResult` : Résultat de la transcription

##### `transcribe_from_microphone(duration: float = 5.0, sample_rate: int = 16000, language: Optional[str] = None) -> TranscriptionResult`

Transcrit l'audio capturé depuis le microphone en temps réel.

**Paramètres :**
- `duration` : Durée d'enregistrement en secondes (défaut: 5.0)
- `sample_rate` : Taux d'échantillonnage en Hz (défaut: 16000)
- `language` : Code langue ISO (optionnel)

**Retourne :**
- `TranscriptionResult` : Résultat de la transcription

### TranscriptionResult

Résultat de transcription audio en texte.

**Attributs :**
- `text` (str) : Texte transcrit
- `language` (Optional[str]) : Langue détectée (code ISO)
- `confidence` (float) : Score de confiance (0.0 à 1.0)
- `segments` (Optional[list[dict]]) : Segments temporels si disponibles
- `is_valid` (bool) : True si la transcription est valide
- `error_message` (Optional[str]) : Message d'erreur si échec

**Exemple :**
```python
result = model.transcribe("audio.wav")

if result.is_valid:
    print(f"Texte: {result.text}")
    print(f"Langue: {result.language}")
    print(f"Confiance: {result.confidence:.2%}")
else:
    print(f"Erreur: {result.error_message}")
```

---

## Modèles disponibles

### Whisper

Modèle transformer open-source développé par OpenAI, spécialisé dans la transcription multilingue.

| Modèle | Vitesse | Précision | Taille | Usage recommandé |
|--------|---------|-----------|--------|-------------------|
| `whisper-tiny` | ⚡⚡⚡ | ⭐⭐ | 39 MB | Tests rapides |
| `whisper-base` | ⚡⚡ | ⭐⭐⭐ | 74 MB | **Usage général (recommandé)** |
| `whisper-small` | ⚡ | ⭐⭐⭐⭐ | 244 MB | Précision importante |
| `whisper-medium` | 🐌 | ⭐⭐⭐⭐⭐ | 769 MB | Précision maximale |
| `whisper-large` | 🐌🐌 | ⭐⭐⭐⭐⭐ | 1550 MB | Recherche/Production |

### Caractéristiques

- **Multilingue** : Supporte 99 langues dont le français
- **Précision élevée** : Excellent pour le français avec accents
- **Open-source** : Gratuit et libre d'utilisation
- **Optimisé** : Paramètres optimisés pour améliorer la précision

### Paramètres optimisés

Le modèle Whisper utilise des paramètres optimisés pour améliorer la précision :

- `temperature=0.0` : Déterminisme maximal
- `beam_size=5` : Beam search pour explorer plusieurs hypothèses
- `best_of=5` : Sélection du meilleur résultat parmi 5 tentatives
- `condition_on_previous_text=True` : Utilise le contexte pour la cohérence

### Preprocessing audio

Le module applique automatiquement un preprocessing pour améliorer la qualité :

- **Normalisation du volume** : Peak normalization à 0.95
- **Réduction du bruit** : Filtre passe-bas léger
- **Suppression du silence** : Retrait automatique du silence au début/fin

---

## Exemples

### Exemple 1 : Transcription simple

```python
from src.speech_to_text.factory import SpeechToTextFactory
from pathlib import Path

# Créer le modèle
model = SpeechToTextFactory.create("whisper-base")

# Transcrire un fichier
result = model.transcribe(Path("audio.wav"), language="fr")

print(f"Texte: {result.text}")
```

### Exemple 2 : Transcription depuis le microphone

```python
from src.speech_to_text.factory import SpeechToTextFactory

model = SpeechToTextFactory.create("whisper-base")

# Enregistrer et transcrire
result = model.transcribe_from_microphone(
    duration=5.0,
    language="fr"
)

if result.is_valid:
    print(f"Vous avez dit: {result.text}")
```

### Exemple 3 : Comparaison de modèles

```python
from src.speech_to_text.factory import SpeechToTextFactory

audio_path = "commande.wav"

# Tester différents modèles
for model_type in ["whisper-tiny", "whisper-base", "whisper-small"]:
    model = SpeechToTextFactory.create(model_type)
    result = model.transcribe(audio_path, language="fr")
    
    print(f"{model_type}: {result.text}")
    print(f"  Confiance: {result.confidence:.2%}")
```

### Exemple 4 : Gestion des erreurs

```python
from src.speech_to_text.factory import SpeechToTextFactory

model = SpeechToTextFactory.create("whisper-base")
result = model.transcribe("fichier_inexistant.wav")

if not result.is_valid:
    print(f"Erreur: {result.error_message}")
    # Erreur: Fichier audio non trouvé: fichier_inexistant.wav
```

---

## Intégration avec NLP

Le texte transcrit peut être directement passé au module NLP pour extraire les villes :

```python
from src.speech_to_text.factory import SpeechToTextFactory
from src.nlp.factory import NLPModelFactory

# 1. Transcrire l'audio
stt_model = SpeechToTextFactory.create("whisper-base")
audio_result = stt_model.transcribe_from_microphone(
    duration=5.0,
    language="fr"
)

if not audio_result.is_valid:
    print(f"Erreur de transcription: {audio_result.error_message}")
    exit(1)

# 2. Extraire les villes depuis le texte transcrit
nlp_model = NLPModelFactory.create("camembert")
nlp_result = nlp_model.extract(audio_result.text)

if nlp_result.is_valid:
    print(f"Départ: {nlp_result.departure}")
    print(f"Destination: {nlp_result.destination}")
else:
    print(f"Erreur d'extraction: {nlp_result.error_message}")
```

### Pipeline complet

```python
# Pipeline complet : Audio -> Texte -> Extraction villes
def process_voice_command(audio_path: str):
    # Étape 1: Speech-to-Text
    stt = SpeechToTextFactory.create("whisper-base")
    transcription = stt.transcribe(audio_path, language="fr")
    
    if not transcription.is_valid:
        return None
    
    # Étape 2: NLP
    nlp = NLPModelFactory.create("camembert")
    extraction = nlp.extract(transcription.text)
    
    return extraction
```

---

## Tests

### Tests unitaires

Voir `tests/speech_to_text/test_speech_to_text.py` pour les tests complets.

### Exécution des tests

```bash
# Test basique
python tests/speech_to_text/test_speech_to_text.py --basic

# Test avec microphone
python tests/speech_to_text/test_speech_to_text.py --mic

# Test avec fichier audio
python tests/speech_to_text/test_speech_to_text.py --file audio.wav

# Test en boucle
python tests/speech_to_text/test_speech_to_text.py --mic-loop

# Voir toutes les options
python tests/speech_to_text/test_speech_to_text.py --help
```

### Options de test

- `--basic` : Test basique (vérification du module)
- `--models` : Test de création des modèles
- `--list` : Liste les modèles disponibles
- `--mic` : Test avec le microphone
- `--mic-loop` : Test microphone en boucle
- `--file <chemin>` : Test avec un fichier audio
- `--duration <sec>` : Durée d'enregistrement
- `--language <lang>` : Langue (fr/en)
- `--model <size>` : Taille du modèle (tiny/base/small)

---

## Conseils d'utilisation

### Pour améliorer la précision

1. **Utilisez un modèle plus grand** : `whisper-small` ou `whisper-medium`
2. **Parlez clairement** : Articulez bien les mots
3. **Environnement calme** : Réduisez le bruit de fond
4. **Microphone de qualité** : Utilisez un bon microphone
5. **Durée appropriée** : 3-10 secondes est optimal
6. **Spécifiez la langue** : Toujours utiliser `language="fr"` pour le français

### Pour améliorer la vitesse

1. **Utilisez un modèle plus petit** : `whisper-tiny` ou `whisper-base`
2. **Réduisez la durée** : Enregistrements plus courts
3. **Utilisez un GPU** : Si disponible, Whisper sera beaucoup plus rapide

### Formats audio supportés

- `.wav` (recommandé)
- `.mp3`
- `.m4a`
- `.flac`
- `.ogg`

### Langues supportées

Whisper supporte 99 langues, notamment :
- Français (`fr`)
- Anglais (`en`)
- Espagnol (`es`)
- Allemand (`de`)
- Italien (`it`)
- Et bien d'autres...

---

## Résolution de problèmes

### Erreur : "sounddevice n'est pas installé"

```bash
pip install sounddevice
```

### Erreur : "ModuleNotFoundError: No module named 'whisper'"

```bash
pip install -r requirements.txt
```

### Erreur SSL lors du téléchargement du modèle

Le module gère automatiquement les problèmes SSL. Si le problème persiste :

1. Vérifiez votre connexion internet
2. Si vous êtes derrière un proxy, configurez-le :
   ```bash
   export https_proxy=http://proxy:port
   ```

### Transcription peu précise

- Utilisez un modèle plus grand (`whisper-small` ou `whisper-medium`)
- Vérifiez la qualité audio (volume, bruit)
- Parlez plus clairement et plus lentement
- Spécifiez explicitement `language="fr"`

### Transcription trop lente

- Utilisez un modèle plus petit (`whisper-tiny` ou `whisper-base`)
- Réduisez la durée d'enregistrement
- Utilisez un GPU si disponible

---

## Architecture technique

### Flux de traitement

```
Audio Input
    ↓
Preprocessing (normalisation, réduction bruit)
    ↓
Whisper Model (transcription)
    ↓
Post-processing (extraction métadonnées)
    ↓
TranscriptionResult
```

### Interface commune

Tous les modèles implémentent `SpeechToTextInterface` pour permettre :
- Le remplacement facile d'un modèle par un autre
- La comparaison équitable entre modèles
- Le benchmarking automatisé
- L'ajout de nouveaux modèles sans modifier le code existant

### Extensibilité

Pour ajouter un nouveau modèle (ex: Wav2Vec2) :

1. Créer une classe qui hérite de `SpeechToTextInterface`
2. Implémenter toutes les méthodes abstraites
3. Ajouter le modèle dans `SpeechToTextFactory._models`

Voir la documentation du projet pour plus de détails sur l'architecture.

---

## Références

- [Documentation Whisper](https://github.com/openai/whisper)
- [Documentation du projet THOR](../docs/DOCUMENTATION.md)
- [Tests](../tests/README.md)

