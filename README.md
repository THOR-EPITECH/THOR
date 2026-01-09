# THOR - Travel Order Resolver

Système de traitement du langage naturel pour extraire des commandes de voyage depuis du texte ou de la parole, et trouver des itinéraires de train optimaux.

## 🏗️ Architecture

Le projet se concentre actuellement sur le module **Speech-to-Text (STT)** : Conversion audio → texte.

Les modules NLP et Pathfinding seront ajoutés ultérieurement.

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour plus de détails.

## 📦 Installation

### Prérequis

- Python 3.9+
- pip

### Installation de base

```bash
# Clone le repository
git clone <repo-url>
cd THOR

# Crée un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installe les dépendances de base
pip install -e .

# Installe les dépendances optionnelles selon vos besoins
pip install -e ".[stt]"      # Pour Speech-to-Text
pip install -e ".[nlp]"       # Pour NLP
pip install -e ".[pathfinding]"  # Pour Pathfinding
pip install -e ".[dev]"       # Pour le développement
```

### Configuration

1. Copiez `.env.example` vers `.env` :
```bash
cp .env.example .env
```

2. Modifiez `.env` selon vos besoins (chemins, clés API, etc.)

## 🚀 Utilisation

### Speech-to-Text

#### Transcrire un fichier audio
```bash
python -m src.cli.stt transcribe --audio path/to/audio.wav --model whisper
```

#### Évaluer un modèle
```bash
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --output-dir results/stt/whisper_test \
    --analyze-errors
```


## 📊 Structure du projet

```
thor/
  src/
    common/          # Modules communs (types, config, logging, etc.)
    stt/             # Module Speech-to-Text
      models/        # Implémentations des modèles STT
      eval/          # Métriques et évaluation
    cli/             # Interfaces en ligne de commande
  configs/           # Fichiers de configuration YAML
  data/              # Données (raw, processed, splits)
  results/           # Résultats des expériences
  tests/             # Tests unitaires
  docs/              # Documentation
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=src tests/
```

## 📝 Documentation

- **[📚 Guide complet des commandes](COMMANDES.md)** - Toutes les commandes disponibles
- [Architecture complète](ARCHITECTURE.md)
- [Documentation STT](src/stt/README.md)
- [Documentation NLP](src/nlp/README.md)
- [Documentation Pipeline](src/pipeline/README.md)

## 🔧 Développement

### Ajouter un nouveau modèle STT

1. Créez un fichier dans `src/stt/models/` (ex: `my_model.py`)
2. Implémentez l'interface `STTModel` :
```python
from src.stt.interfaces import STTModel
from src.common.types import STTResult

class MyModel(STTModel):
    def transcribe(self, audio_path: str) -> STTResult:
        # Votre implémentation
        return STTResult(text="...")
```

3. Créez une configuration dans `configs/stt/my_model.yaml`
4. Ajoutez le modèle dans `src/cli/stt.py` si nécessaire

Voir `src/stt/models/dummy.py` pour un exemple minimal.

### Workflow de test

```bash
# Test STT
python -m src.cli.stt evaluate \
    --model whisper \
    --dataset data/splits/test/test.jsonl \
    --output-dir results/stt/whisper_test
```

## 📈 Métriques

Le module STT expose des métriques standardisées :

- **WER** (Word Error Rate) : Taux d'erreur de mots
- **CER** (Character Error Rate) : Taux d'erreur de caractères
- **Latency** : Temps de traitement
- **Real-time Factor (RTF)** : Ratio temps traitement / durée audio

Les résultats sont sauvegardés dans `results/runs/<timestamp>_stt_<model>/`

## 🤝 Contribution

1. Créez une branche pour votre fonctionnalité
2. Ajoutez des tests
3. Assurez-vous que tous les tests passent
4. Créez une pull request

## 📄 Licence

MIT

## 👥 Auteurs

THOR Team

