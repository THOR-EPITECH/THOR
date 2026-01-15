# Modèle NLP : spaCy

## Vue d'ensemble

spaCy est un modèle NLP utilisant la bibliothèque spaCy pour l'extraction d'entités nommées (NER) et des patterns regex pour déterminer l'origine et la destination. C'est le modèle recommandé pour la production, offrant un excellent compromis entre précision et performance.

## Caractéristiques

- **Précision** : ⭐⭐⭐⭐ (Très bonne)
- **Vitesse** : ⭐⭐⭐⭐ (Rapide)
- **Fine-tuning** : ✅ (Supporté)
- **GPU requis** : ❌ (Fonctionne sur CPU)
- **Modèle de base** : `fr_core_news_md` (modèle français moyen)

## Installation

```bash
# Installer spaCy
pip install spacy

# Télécharger le modèle français
python -m spacy download fr_core_news_md
```

## Modèles spaCy disponibles

| Modèle | Taille | Précision | Vitesse |
|--------|--------|-----------|---------|
| fr_core_news_sm | ~20 MB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| fr_core_news_md | ~40 MB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| fr_core_news_lg | ~500 MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**Recommandation** : `fr_core_news_md` pour un bon compromis.

## Configuration

### Modèle de base

```yaml
# configs/nlp/spacy_base.yaml
nlp:
  model_name: fr_core_news_md
```

### Modèle fine-tuné

```yaml
# configs/nlp/spacy_finetuned.yaml
nlp:
  model_name: fr_core_news_md
  custom_model_path: models/nlp/spacy_finetuned/model
```

### Paramètres d'entraînement

```yaml
nlp:
  model_name: fr_core_news_md
  n_iter: 20        # Nombre d'itérations d'entraînement
  dropout: 0.1      # Taux de dropout
```

## Utilisation

### Via CLI

```bash
# Extraction simple
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model spacy

# Avec configuration
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model spacy \
    --config configs/nlp/spacy_base.yaml

# Évaluation
python -m src.cli.nlp evaluate \
    --model spacy \
    --dataset data/splits/test/test_nlp.jsonl
```

### Via Python

```python
from src.nlp.models.spacy_fr import SpacyFRModel

# Modèle de base
model = SpacyFRModel({
    "model_name": "fr_core_news_md"
})

# Modèle fine-tuné
model = SpacyFRModel({
    "model_name": "fr_core_news_md",
    "custom_model_path": "models/nlp/spacy_finetuned/model"
})

# Extraction
result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}")        # Lyon
print(f"Destination: {result.destination}")  # Paris
print(f"Confiance: {result.confidence}")     # 0.7-1.0
print(f"Valide: {result.is_valid}")         # True
```

## Méthode d'extraction

Le modèle utilise une approche hybride :

1. **NER (Named Entity Recognition)** : Détecte les entités de type `LOC` (location)
2. **Patterns regex** : Analyse les patterns pour déterminer origine/destination
3. **Fine-tuning** : Si un modèle fine-tuné est utilisé, détecte directement `ORIGIN` et `DESTINATION`

### Patterns supportés

- **"depuis X"** : "aller à Paris depuis Lyon" → origine: Lyon
- **"de X à Y"** : "de Lyon à Paris" → origine: Lyon, destination: Paris
- **"aller à X"** : "aller à Paris" → destination: Paris
- **"partir de X"** : "partir de Lyon" → origine: Lyon

## Fine-tuning

Le modèle spaCy peut être fine-tuné sur des données personnalisées pour améliorer la précision.

### Préparation des données

Format JSONL avec annotations :

```jsonl
{"text": "Je veux aller à Paris depuis Lyon", "origin": "Lyon", "destination": "Paris", "is_valid": true}
{"text": "Bonjour, comment allez-vous ?", "origin": null, "destination": null, "is_valid": false}
```

### Entraînement

```bash
python -m src.cli.nlp train \
    --model spacy \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --output-dir models/nlp/spacy_finetuned
```

### Paramètres d'entraînement

- **n_iter** : Nombre d'itérations (défaut: 20)
- **dropout** : Taux de dropout (défaut: 0.1)

### Utilisation du modèle fine-tuné

Après l'entraînement, utilisez le modèle fine-tuné en spécifiant `custom_model_path` :

```yaml
nlp:
  model_name: fr_core_news_md
  custom_model_path: models/nlp/spacy_finetuned/model
```

## Résultat

Le modèle retourne un objet `NLPExtraction` :

```python
NLPExtraction(
    origin="Lyon",
    destination="Paris",
    is_valid=True,
    confidence=0.85,
    entities=[
        {"text": "Lyon", "label": "LOC"},
        {"text": "Paris", "label": "LOC"}
    ],
    metadata={
        "model": "spacy-fr_core_news_md",
        "locations_found": ["Lyon", "Paris"],
        "extraction_method": "ner_patterns"  # ou "fine_tuned_ner"
    }
)
```

## Calcul de confiance

La confiance est calculée dynamiquement selon :

- **Modèle de base** :
  - Origine + Destination : 0.7
  - Origine ou Destination : 0.5
  - Villes détectées mais pas d'extraction : 0.2
  - Aucune ville : 0.0

- **Modèle fine-tuné** :
  - Origine + Destination : 1.0
  - Origine ou Destination : 0.8
  - Villes détectées mais pas de trajet clair : 0.5
  - Aucune ville : 0.2

## Performance

### Exemple de latence (CPU)

| Longueur texte | Temps traitement |
|----------------|------------------|
| 10 mots | ~0.01s |
| 50 mots | ~0.05s |
| 100 mots | ~0.1s |

### Précision (sur dataset de test)

| Métrique | Modèle de base | Modèle fine-tuné |
|----------|----------------|------------------|
| F1-Score | ~0.41 | ~0.62 |
| Precision | ~0.45 | ~0.65 |
| Recall | ~0.38 | ~0.60 |

## Avantages

1. **Précision élevée** : Excellent compromis précision/vitesse
2. **Fine-tuning** : Peut être adapté à des données spécifiques
3. **Rapide** : Traitement en temps réel
4. **Robuste** : Gère bien les variations de formulation
5. **CPU uniquement** : Pas besoin de GPU

## Inconvénients

1. **Modèle à télécharger** : Nécessite téléchargement du modèle français
2. **Précision limitée** : Moins précis que Transformers pour certains cas
3. **Fine-tuning nécessaire** : Pour de meilleures performances, nécessite fine-tuning

## Recommandations

- **Production** : Utilisez le modèle fine-tuné pour de meilleures performances
- **Développement** : Le modèle de base suffit pour tester
- **Performance** : `fr_core_news_md` est le meilleur compromis

## Dépannage

### Erreur : "Model not found"
```bash
# Téléchargez le modèle français
python -m spacy download fr_core_news_md
```

### Performance dégradée
- Utilisez un modèle plus grand (`fr_core_news_lg`)
- Fine-tunez le modèle sur vos données
- Vérifiez que le texte est bien formaté

## Références

- [Documentation spaCy](https://spacy.io/)
- [Modèles français spaCy](https://spacy.io/models/fr)
- [Fine-tuning spaCy NER](https://spacy.io/usage/training#ner)
