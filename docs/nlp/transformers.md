# Modèle NLP : Transformers (CamemBERT)

## Vue d'ensemble

Le modèle Transformers utilise la bibliothèque Hugging Face Transformers avec CamemBERT (modèle français pré-entraîné) pour l'extraction d'entités nommées (NER). C'est le modèle le plus précis mais aussi le plus gourmand en ressources.

## Caractéristiques

- **Précision** : ⭐⭐⭐⭐⭐ (Excellente)
- **Vitesse** : ⭐⭐⭐ (Moyenne)
- **Fine-tuning** : ✅ (Supporté)
- **GPU requis** : Recommandé (fonctionne sur CPU mais plus lent)
- **Modèle de base** : `camembert-base`

## Installation

```bash
pip install transformers torch accelerate
```

**Note** : `accelerate` est requis pour l'entraînement avec le Trainer.

## Configuration

### Modèle de base

```yaml
# configs/nlp/transformers_base.yaml
nlp:
  model_name: camembert-base
  device: cpu  # ou "cuda" si GPU disponible
```

### Modèle fine-tuné

```yaml
# configs/nlp/transformers_finetuned.yaml
nlp:
  model_name: camembert-base
  custom_model_path: models/nlp/transformers_finetuned/model
  device: cpu
```

### Paramètres d'entraînement

```yaml
nlp:
  model_name: camembert-base
  n_epochs: 3           # Nombre d'époques
  learning_rate: 2e-5   # Taux d'apprentissage
  batch_size: 16        # Taille du batch
```

## Utilisation

### Via CLI

```bash
# Extraction simple
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model transformers

# Avec configuration
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model transformers \
    --config configs/nlp/transformers_base.yaml

# Évaluation
python -m src.cli.nlp evaluate \
    --model transformers \
    --dataset data/splits/test/test_nlp.jsonl
```

### Via Python

```python
from src.nlp.models.transformers_ner import TransformersNERModel

# Modèle de base
model = TransformersNERModel({
    "model_name": "camembert-base",
    "device": "cpu"
})

# Modèle fine-tuné
model = TransformersNERModel({
    "model_name": "camembert-base",
    "custom_model_path": "models/nlp/transformers_finetuned/model",
    "device": "cuda"  # Si GPU disponible
})

# Extraction
result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}")
print(f"Destination: {result.destination}")
print(f"Confiance: {result.confidence}")
```

## Méthode d'extraction

Le modèle utilise :

1. **Token Classification** : CamemBERT tokenise le texte et classe chaque token
2. **NER Pipeline** : Utilise le pipeline Hugging Face pour l'extraction d'entités
3. **Patterns regex** : Combine avec des patterns pour déterminer origine/destination

### Labels utilisés

- **O** : Token non-pertinent
- **B-ORIGIN** : Début d'une entité origine
- **I-ORIGIN** : Intérieur d'une entité origine
- **B-DESTINATION** : Début d'une entité destination
- **I-DESTINATION** : Intérieur d'une entité destination

## Fine-tuning

Le modèle Transformers peut être fine-tuné sur des données personnalisées pour une précision maximale.

### Préparation des données

Format JSONL avec annotations (même format que spaCy) :

```jsonl
{"text": "Je veux aller à Paris depuis Lyon", "origin": "Lyon", "destination": "Paris", "is_valid": true}
{"text": "Bonjour, comment allez-vous ?", "origin": null, "destination": null, "is_valid": false}
```

### Entraînement

```bash
python -m src.cli.nlp train \
    --model transformers \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --output-dir models/nlp/transformers_finetuned
```

### Paramètres d'entraînement

- **n_epochs** : Nombre d'époques (défaut: 3)
- **learning_rate** : Taux d'apprentissage (défaut: 2e-5)
- **batch_size** : Taille du batch (défaut: 16)

**Note** : L'entraînement peut prendre du temps, surtout sur CPU. Un GPU est fortement recommandé.

### Utilisation du modèle fine-tuné

Après l'entraînement, utilisez le modèle fine-tuné :

```yaml
nlp:
  model_name: camembert-base
  custom_model_path: models/nlp/transformers_finetuned/model
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
        "model": "transformers-camembert-base",
        "locations_found": ["Lyon", "Paris"],
        "extraction_method": "transformers_ner_patterns"
    }
)
```

## Calcul de confiance

La confiance est calculée selon :

- **Base** : 0.5
- **Origine + Destination** : +0.3
- **Entités détectées** : +0.1
- **Noms bien formés** : +0.05 chacun

Maximum : 1.0

## Performance

### Exemple de latence

| Périphérique | Longueur texte | Temps traitement |
|--------------|----------------|------------------|
| CPU | 10 mots | ~0.1s |
| CPU | 50 mots | ~0.5s |
| GPU | 10 mots | ~0.02s |
| GPU | 50 mots | ~0.1s |

### Précision (sur dataset de test)

| Métrique | Modèle de base | Modèle fine-tuné |
|----------|----------------|------------------|
| F1-Score | ~0.40 | ~0.65+ |
| Precision | ~0.45 | ~0.70+ |
| Recall | ~0.38 | ~0.60+ |

**Note** : Les performances varient selon le dataset et le fine-tuning.

## Avantages

1. **Précision maximale** : Meilleur modèle disponible
2. **Fine-tuning avancé** : Excellent pour l'adaptation à des données spécifiques
3. **Modèle de pointe** : Utilise les dernières techniques de NLP
4. **Flexible** : Peut être adapté à différents domaines

## Inconvénients

1. **Lent** : Plus lent que spaCy, surtout sur CPU
2. **Ressources** : Nécessite beaucoup de RAM et de stockage
3. **GPU recommandé** : L'entraînement est très lent sur CPU
4. **Complexité** : Plus complexe à configurer et utiliser

## Recommandations

- **Production (GPU)** : Idéal pour une précision maximale
- **Production (CPU)** : Utilisez spaCy pour de meilleures performances
- **Fine-tuning** : Nécessite un GPU pour un entraînement raisonnable
- **Développement** : Le modèle de base peut être utilisé pour tester

## Dépannage

### Erreur : "transformers and torch are required"
```bash
pip install transformers torch accelerate
```

### Erreur : "accelerate>=0.26.0 required"
```bash
pip install accelerate>=0.26.0
```

### Performance lente
- Utilisez un GPU si disponible (`device: cuda`)
- Réduisez la taille du batch
- Utilisez un modèle plus petit (mais moins précis)

### Erreur lors du chargement
Le modèle utilise `camembert-base` par défaut pour éviter les problèmes avec certains modèles NER pré-entraînés. Si vous rencontrez des erreurs, vérifiez que le modèle est bien téléchargé.

## Références

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [CamemBERT](https://huggingface.co/camembert-base)
- [Fine-tuning NER](https://huggingface.co/docs/transformers/tasks/token_classification)
