# Module NLP (Natural Language Processing)

## Vue d'ensemble

Ce module extrait l'origine et la destination depuis un texte transcrit. Il utilise des techniques de NLP pour identifier les villes et déterminer leur rôle (origine vs destination).

## Architecture

```
nlp/
  interfaces.py      # Interface NLPModel
  models/            # Implémentations des modèles
  eval/              # Métriques et évaluation
```

## Interface standard

Tous les modèles NLP implémentent l'interface `NLPModel` :

```python
class NLPModel(ABC):
    @abstractmethod
    def extract(self, text: str) -> NLPExtraction:
        """Extrait origine/destination depuis un texte."""
        pass
```

## Modèles disponibles

### 1. spaCy (recommandé)

**Fichier**: `models/spacy_fr.py`

**Caractéristiques**:
- Utilise NER (Named Entity Recognition) pour identifier les lieux
- Patterns regex pour déterminer origine/destination
- Gère les variations (minuscules, accents)
- Détecte les demandes de trajet valides

**Configuration**:
```yaml
model: spacy
model_name: fr_core_news_md
```

**Installation**:
```bash
pip install spacy
python -m spacy download fr_core_news_md
```

**Utilisation**:
```python
from src.nlp.models.spacy_fr import SpacyFRModel

model = SpacyFRModel({"model_name": "fr_core_news_md"})
result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}, Destination: {result.destination}")
```

### 2. Dummy (baseline)

**Fichier**: `models/dummy.py`

**Usage**: Tests et baseline pour valider le pipeline.

## Métriques

- **Precision** : Proportion d'entités extraites correctement
- **Recall** : Proportion d'entités de référence trouvées
- **F1-Score** : Moyenne harmonique de Precision et Recall
- **Origin Accuracy** : Précision sur l'origine
- **Destination Accuracy** : Précision sur la destination
- **Validation Accuracy** : Précision sur is_valid

## Utilisation

### Via CLI
```bash
# Extraire depuis un texte
python -m src.cli.nlp extract --text "Je veux aller à Paris depuis Lyon" --model spacy

# Évaluer sur un dataset
python -m src.cli.nlp evaluate \
    --dataset data/splits/test/test_nlp.jsonl \
    --model spacy \
    --output-dir results/nlp/spacy_test
```

### Via Pipeline complet
```bash
# Audio → STT → NLP
python -m src.cli.pipeline \
    --audio audio.wav \
    --stt-model whisper \
    --nlp-model spacy
```

## Format du dataset

Le dataset doit être au format JSONL :

```json
{
  "id": "sample_001",
  "sentence": "Je veux aller à Paris depuis Lyon",
  "origin": "Lyon",
  "destination": "Paris",
  "is_valid": true
}
```

## Ajouter un nouveau modèle

1. Créez un fichier dans `models/` (ex: `my_model.py`)
2. Implémentez l'interface `NLPModel` :
```python
from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction

class MyModel(NLPModel):
    def extract(self, text: str) -> NLPExtraction:
        # Votre implémentation
        return NLPExtraction(origin="...", destination="...")
```

3. Créez une configuration dans `configs/nlp/`
4. Ajoutez le modèle dans `src/cli/nlp.py` si nécessaire

