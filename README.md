# 🚂 THOR - Travel Order Resolver

> Système intelligent de traitement du langage naturel pour extraire des commandes de voyage depuis la parole ou le texte, et identifier les itinéraires de train optimaux.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)


## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Démarrage rapide](#-démarrage-rapide)
- [Architecture](#-architecture)
- [Modèles disponibles](#-modèles-disponibles)
- [Documentation](#-documentation)
- [Développement](#-développement)

## 🎯 Vue d'ensemble

THOR est un système complet de traitement du langage naturel conçu pour :

1. **Transcrire la parole en texte** (Speech-to-Text) avec plusieurs modèles
2. **Extraire les informations de voyage** (origine, destination) depuis le texte
3. **Trouver des itinéraires optimaux** (Pathfinding) - *en développement*

Le système est modulaire, extensible et supporte le fine-tuning des modèles pour améliorer les performances sur des données spécifiques.

## ✨ Fonctionnalités

### 🎤 Speech-to-Text (STT)
- **Multi-modèles** : Whisper, Vosk, Dummy
- **Évaluation complète** : WER, CER, Latency, RTF
- **Benchmark** : Comparaison de plusieurs modèles
- **Support multilingue** : Français, Anglais, et plus (via Whisper)

### 🧠 Natural Language Processing (NLP)
- **Multi-modèles** : spaCy, Transformers (CamemBERT), Regex Advanced, Dummy
- **Extraction intelligente** : Origine et destination depuis le texte
- **Fine-tuning** : Support pour entraîner les modèles sur des données personnalisées
- **Benchmark** : Comparaison de plusieurs modèles NLP
- **Confiance dynamique** : Score de confiance calculé selon la qualité de l'extraction

### 🔄 Pipeline complet
- **End-to-end** : Audio → Transcription → Extraction → Résultat
- **Rapports automatiques** : Génération de rapports Markdown détaillés
- **Gestion d'erreurs** : Messages d'erreur spécifiques pour les informations manquantes

## 📦 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip
- (Optionnel) GPU pour de meilleures performances avec les modèles Transformers

### Installation de base

```bash
# Clone le repository
git clone https://github.com/THOR-EPITECH/THOR.git
cd THOR

# Crée un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installe les dépendances de base
pip install -e .
```

### Installation des modules optionnels

```bash
# Pour Speech-to-Text
pip install -e ".[stt]"

# Pour NLP
pip install -e ".[nlp]"

# Pour Pathfinding (en développement)
pip install -e ".[pathfinding]"

# Pour le développement
pip install -e ".[dev]"
```

### Installation des modèles

```bash
# Modèle spaCy français
python -m spacy download fr_core_news_md

# Modèle Vosk (optionnel, téléchargement manuel requis)
# Voir docs/stt/vosk.md pour les instructions
```

### Installation multi-plateforme

THOR est compatible avec **Linux Ubuntu** et **Windows**. Voici les instructions spécifiques pour chaque plateforme :

#### 🐧 Linux Ubuntu

**Prérequis système :**

```bash
# Mettre à jour les paquets
sudo apt update

# Installer Python 3.9+ et pip si nécessaire
sudo apt install python3 python3-pip python3-venv

# Installer les dépendances système pour audio (si vous utilisez STT)
sudo apt install ffmpeg portaudio19-dev python3-dev

# Installer les dépendances pour les modèles Transformers (optionnel, pour GPU)
sudo apt install build-essential
```

**Installation du projet :**

```bash
# Clone le repository
git clone https://github.com/THOR-EPITECH/THOR.git
cd THOR

# Crée un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installe les dépendances de base
pip install --upgrade pip
pip install -e .

# Installe les modules optionnels selon vos besoins
pip install -e ".[stt]"      # Pour Speech-to-Text
pip install -e ".[nlp]"      # Pour NLP
pip install -e ".[dev]"      # Pour le développement

# Télécharge le modèle spaCy français
python -m spacy download fr_core_news_md
```

**Note pour GPU (CUDA) :** Si vous avez une carte graphique NVIDIA et souhaitez utiliser le GPU pour les modèles Transformers :

```bash
# Installer PyTorch avec support CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 🪟 Windows

**Prérequis système :**

1. **Installer Python 3.9+** :
   - Téléchargez depuis [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important** : Cochez "Add Python to PATH" lors de l'installation
   - Vérifiez l'installation : `python --version` dans PowerShell ou CMD

2. **Installer Git** (si nécessaire) :
   - Téléchargez depuis [git-scm.com](https://git-scm.com/download/win)

3. **Installer FFmpeg** (pour le traitement audio avec STT) :
   - Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extrayez et ajoutez le dossier `bin` au PATH système
   - Vérifiez : `ffmpeg -version` dans PowerShell

**Installation du projet :**

```powershell
# Ouvrir PowerShell ou CMD en tant qu'administrateur (recommandé)

# Clone le repository
git clone https://github.com/THOR-EPITECH/THOR.git
cd THOR

# Crée un environnement virtuel
python -m venv venv

# Active l'environnement virtuel
.\venv\Scripts\activate

# Installe les dépendances de base
python -m pip install --upgrade pip
pip install -e .

# Installe les modules optionnels selon vos besoins
pip install -e ".[stt]"      # Pour Speech-to-Text
pip install -e ".[nlp]"      # Pour NLP
pip install -e ".[dev]"      # Pour le développement

# Télécharge le modèle spaCy français
python -m spacy download fr_core_news_md
```

**Note pour GPU (CUDA) :** Si vous avez une carte graphique NVIDIA :

1. Installez [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
2. Installez PyTorch avec support CUDA :
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Dépannage Windows :**

- **Erreur "python n'est pas reconnu"** : Vérifiez que Python est dans le PATH ou utilisez `py` au lieu de `python`
- **Erreur lors de l'activation du venv** : Exécutez PowerShell en tant qu'administrateur ou changez la politique d'exécution :
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Erreur avec FFmpeg** : Vérifiez que FFmpeg est dans le PATH système

#### ✅ Vérification de l'installation

Après l'installation sur n'importe quelle plateforme, vérifiez que tout fonctionne :

```bash
# Vérifier l'installation
python -m src.cli.nlp extract --text "Je veux aller à Paris depuis Lyon" --model dummy

# Devrait afficher :
# {
#   "origin": "Lyon",
#   "destination": "Paris",
#   ...
# }
```

## 🚀 Démarrage rapide

### Transcription audio (STT)

```bash
# Transcription simple avec Whisper
python -m src.cli.stt transcribe \
    --audio data/raw/audio/sample_000001.wav \
    --model whisper
```

### Extraction NLP

```bash
# Extraction depuis un texte
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model spacy
```

### Pipeline complet

```bash
# Traitement complet : Audio → STT → NLP
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000001.wav \
    --stt-model whisper \
    --nlp-model spacy
```

### Entraînement d'un modèle NLP

```bash
# Entraîner le modèle spaCy
python -m src.cli.nlp train \
    --model spacy \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --output-dir models/nlp/spacy_finetuned
```

### Benchmark de modèles

```bash
# Comparer plusieurs modèles NLP
python -m src.cli.nlp benchmark \
    --dataset data/splits/test/test_nlp.jsonl \
    --models spacy transformers regex_advanced
```

## 🏗️ Architecture

```
THOR/
├── src/
│   ├── stt/              # Module Speech-to-Text
│   │   ├── models/       # Modèles STT (Whisper, Vosk, Dummy)
│   │   └── eval/         # Évaluation et métriques
│   ├── nlp/              # Module Natural Language Processing
│   │   ├── models/       # Modèles NLP (spaCy, Transformers, Regex, Dummy)
│   │   ├── eval/         # Évaluation et benchmark
│   │   └── training/     # Fine-tuning des modèles
│   ├── pipeline/         # Pipeline complet Audio → STT → NLP
│   ├── cli/              # Interfaces en ligne de commande
│   └── common/           # Modules communs (types, config, logging)
├── configs/              # Fichiers de configuration YAML
├── data/                 # Données (raw, processed, splits)
├── models/               # Modèles entraînés
├── results/              # Résultats des expériences
├── docs/                 # Documentation complète
│   ├── stt/             # Documentation des modèles STT
│   ├── nlp/             # Documentation des modèles NLP
│   ├── COMMANDES.md     # Guide complet des commandes
│   └── ARCHITECTURE.md  # Architecture détaillée
└── scripts/             # Scripts utilitaires
```

## 🤖 Modèles disponibles

### Modèles STT

| Modèle | Précision | Vitesse | Offline | GPU | Documentation |
|--------|-----------|---------|---------|-----|---------------|
| **Whisper** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Recommandé | [docs/stt/whisper.md](docs/stt/whisper.md) |
| **Vosk** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ❌ | [docs/stt/vosk.md](docs/stt/vosk.md) |
| **Dummy** | ❌ | ⭐⭐⭐⭐⭐ | ✅ | ❌ | [docs/stt/dummy.md](docs/stt/dummy.md) |

### Modèles NLP

| Modèle | Précision | Vitesse | Fine-tuning | GPU | Documentation |
|--------|-----------|---------|-------------|-----|---------------|
| **spaCy** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ | [docs/nlp/spacy.md](docs/nlp/spacy.md) |
| **Transformers** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Recommandé | [docs/nlp/transformers.md](docs/nlp/transformers.md) |
| **Regex Advanced** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ❌ | [docs/nlp/regex_advanced.md](docs/nlp/regex_advanced.md) |
| **Dummy** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ❌ | [docs/nlp/dummy.md](docs/nlp/dummy.md) |

## 📊 Métriques

### Métriques STT
- **WER** (Word Error Rate) : Taux d'erreur de mots
- **CER** (Character Error Rate) : Taux d'erreur de caractères
- **Latency** : Temps de traitement
- **RTF** (Real-time Factor) : Ratio temps traitement / durée audio

### Métriques NLP
- **Precision** : Proportion d'entités extraites correctement
- **Recall** : Proportion d'entités de référence trouvées
- **F1-Score** : Moyenne harmonique de Precision et Recall
- **Origin/Destination Accuracy** : Précision sur l'extraction spécifique
- **Validation Accuracy** : Précision sur la détection de demande valide

## 📚 Documentation

### Documentation principale

- **[📚 Guide complet des commandes](docs/COMMANDES.md)** - Toutes les commandes disponibles avec exemples
- **[🏗️ Architecture détaillée](docs/ARCHITECTURE.md)** - Architecture complète du système

### Documentation des modèles

#### STT
- **[Index STT](docs/stt/index.md)** - Vue d'ensemble des modèles STT
- **[Whisper](docs/stt/whisper.md)** - Documentation complète du modèle Whisper
- **[Vosk](docs/stt/vosk.md)** - Documentation complète du modèle Vosk
- **[Dummy STT](docs/stt/dummy.md)** - Modèle baseline pour tests

#### NLP
- **[Index NLP](docs/nlp/index.md)** - Vue d'ensemble des modèles NLP
- **[spaCy](docs/nlp/spacy.md)** - Documentation complète du modèle spaCy
- **[Transformers](docs/nlp/transformers.md)** - Documentation complète du modèle Transformers
- **[Regex Advanced](docs/nlp/regex_advanced.md)** - Documentation du modèle Regex
- **[Dummy NLP](docs/nlp/dummy.md)** - Modèle baseline pour tests

### Documentation des modules

- **[Module STT](src/stt/README.md)** - Documentation du module Speech-to-Text
- **[Module NLP](src/nlp/README.md)** - Documentation du module NLP
- **[Module Pipeline](src/pipeline/README.md)** - Documentation du pipeline complet

## 🔧 Développement

### Configuration de l'environnement de développement

```bash
# Installe les dépendances de développement
pip install -e ".[dev]"

# Configure les outils de formatage
black src/ tests/
ruff check src/ tests/
```

### Ajouter un nouveau modèle

#### Modèle STT

1. Créez un fichier dans `src/stt/models/` (ex: `my_model.py`)
2. Implémentez l'interface `STTModel` :
```python
from src.stt.interfaces import STTModel
from src.common.types import STTResult

class MySTTModel(STTModel):
    def transcribe(self, audio_path: str | Path) -> STTResult:
        # Votre implémentation
        return STTResult(text="...", ...)
```
3. Créez une configuration dans `configs/stt/my_model.yaml`
4. Ajoutez le modèle dans `src/cli/stt.py`

#### Modèle NLP

1. Créez un fichier dans `src/nlp/models/` (ex: `my_model.py`)
2. Implémentez l'interface `NLPModel` :
```python
from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction

class MyNLPModel(NLPModel):
    def extract(self, text: str) -> NLPExtraction:
        # Votre implémentation
        return NLPExtraction(origin="...", destination="...", ...)
```
3. Créez une configuration dans `configs/nlp/my_model.yaml`
4. Ajoutez le modèle dans `src/cli/nlp.py`

### Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=src tests/

# Tests d'un module spécifique
pytest tests/test_stt.py
```

### Workflow de développement

```bash
# 1. Test STT
python -m src.cli.stt evaluate \
    --model whisper \
    --dataset data/splits/test/test.jsonl \
    --output-dir results/stt/whisper_test

# 2. Test NLP
python -m src.cli.nlp evaluate \
    --model spacy \
    --dataset data/splits/test/test_nlp.jsonl \
    --output-dir results/nlp/spacy_test

# 3. Test Pipeline
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000001.wav \
    --stt-model whisper \
    --nlp-model spacy
```

---

## 🔗 Liens utiles

- [Documentation complète](docs/)
- [Guide des commandes](docs/COMMANDES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Issues](https://github.com/THOR-EPITECH/THOR/issues)
- [Pull Requests](https://github.com/THOR-EPITECH/THOR/pulls)

---

**Note** : Le module Pathfinding est en cours de développement et sera disponible dans une future version.
