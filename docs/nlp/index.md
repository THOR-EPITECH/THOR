# Documentation des Modèles NLP (Natural Language Processing)

## Vue d'ensemble

Le module NLP (Natural Language Processing) extrait l'origine et la destination depuis un texte transcrit. Il utilise différentes techniques de traitement du langage naturel pour identifier les villes et déterminer leur rôle (origine vs destination).

## Modèles disponibles

### 1. [spaCy](./spacy.md)
- **Recommandé pour** : Production, précision élevée
- **Avantages** : Très précis, supporte le fine-tuning, NER intégré
- **Inconvénients** : Nécessite téléchargement du modèle français
- **Fichier** : `src/nlp/models/spacy_fr.py`

### 2. [Transformers (CamemBERT)](./transformers.md)
- **Recommandé pour** : Précision maximale, fine-tuning avancé
- **Avantages** : Modèle de pointe, excellent pour le fine-tuning
- **Inconvénients** : Plus lent, nécessite GPU pour de meilleures performances
- **Fichier** : `src/nlp/models/transformers_ner.py`

### 3. [Regex Advanced](./regex_advanced.md)
- **Recommandé pour** : Rapidité, simplicité
- **Avantages** : Très rapide, aucune dépendance lourde, patterns sophistiqués
- **Inconvénients** : Moins flexible que les modèles ML
- **Fichier** : `src/nlp/models/regex_advanced.py`

### 4. [Dummy](./dummy.md)
- **Recommandé pour** : Tests et baseline
- **Avantages** : Aucune dépendance, patterns simples
- **Inconvénients** : Précision limitée
- **Fichier** : `src/nlp/models/dummy.py`

## Métriques d'évaluation

Les modèles NLP sont évalués selon plusieurs métriques :

- **Precision** : Proportion d'entités extraites correctement
- **Recall** : Proportion d'entités de référence trouvées
- **F1-Score** : Moyenne harmonique de Precision et Recall
- **Origin Accuracy** : Précision sur l'extraction de l'origine
- **Destination Accuracy** : Précision sur l'extraction de la destination
- **Validation Accuracy** : Précision sur la détection de demande valide

## Utilisation

### Via CLI

```bash
# Extraire depuis un texte
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model spacy

# Évaluer un modèle
python -m src.cli.nlp evaluate \
    --model spacy \
    --config configs/nlp/spacy_base.yaml \
    --dataset data/splits/nlp/test/test.jsonl

# Entraîner un modèle
python -m src.cli.nlp train \
    --model spacy \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --output-dir models/nlp/spacy_finetuned

# Benchmarker plusieurs modèles
python -m src.cli.nlp benchmark \
    --dataset data/splits/test/test_nlp.jsonl \
    --models spacy transformers regex_advanced
```

### Via Python

```python
from src.nlp.models.spacy_fr import SpacyFRModel

model = SpacyFRModel({
    "model_name": "fr_core_news_md"
})
result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}")
print(f"Destination: {result.destination}")
print(f"Confiance: {result.confidence}")
```

## Interface standard

Tous les modèles NLP implémentent l'interface `NLPModel` :

```python
class NLPModel(ABC):
    def extract(self, text: str) -> NLPExtraction:
        """Extrait l'origine et la destination depuis un texte."""
        pass
    
    def train(self, train_dataset: str | Path, valid_dataset: str | Path = None, 
              output_dir: str | Path = None):
        """Entraîne le modèle sur un dataset."""
        pass
```

## Résultat d'extraction

Tous les modèles retournent un objet `NLPExtraction` :

```python
@dataclass
class NLPExtraction:
    origin: Optional[str]        # Ville de départ
    destination: Optional[str]    # Ville d'arrivée
    is_valid: bool               # Si c'est une demande de trajet valide
    confidence: float            # Score de confiance (0.0-1.0)
    entities: List[Dict]         # Entités détectées
    metadata: Dict[str, Any]      # Métadonnées supplémentaires
```

## Comparaison rapide

| Modèle | Précision | Vitesse | Fine-tuning | GPU requis |
|--------|-----------|---------|-------------|------------|
| spaCy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ |
| Transformers | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Recommandé |
| Regex Advanced | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ❌ |
| Dummy | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ❌ |

## Fine-tuning

Les modèles **spaCy** et **Transformers** supportent le fine-tuning sur des données personnalisées :

1. **Préparer un dataset** au format JSONL avec annotations
2. **Entraîner le modèle** avec `train` command
3. **Utiliser le modèle fine-tuné** en spécifiant `custom_model_path` dans la config

Voir la documentation de chaque modèle pour plus de détails.

## Configuration

Chaque modèle peut être configuré via un fichier YAML dans `configs/nlp/` :

```yaml
# configs/nlp/spacy_base.yaml
nlp:
  model_name: fr_core_news_md
  # custom_model_path: models/nlp/spacy_finetuned/model  # Pour modèle fine-tuné
```

## Patterns de texte supportés

Les modèles reconnaissent différents patterns pour extraire origine/destination :

- **"depuis X"** : "Je veux aller à Paris depuis Lyon" → origine: Lyon
- **"de X à Y"** : "Je veux aller de Lyon à Paris" → origine: Lyon, destination: Paris
- **"aller à X"** : "Je veux aller à Paris" → destination: Paris
- **"partir de X"** : "Je veux partir de Lyon" → origine: Lyon

Et bien d'autres variations...

## Ajouter un nouveau modèle

Pour ajouter un nouveau modèle NLP :

1. Créer un fichier dans `src/nlp/models/` (ex: `my_model.py`)
2. Implémenter la classe héritant de `NLPModel`
3. Implémenter la méthode `extract()`
4. Optionnellement implémenter `train()` pour le fine-tuning
5. Enregistrer le modèle dans le registre (voir `src/common/registry.py`)
