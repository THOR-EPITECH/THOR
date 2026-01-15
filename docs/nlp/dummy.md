# Modèle NLP : Dummy

## Vue d'ensemble

Le modèle Dummy est un modèle baseline utilisé pour les tests et le développement. Il utilise des patterns regex simples pour extraire l'origine et la destination.

## Caractéristiques

- **Précision** : ⭐⭐ (Limitée)
- **Vitesse** : ⭐⭐⭐⭐⭐ (Très rapide)
- **Fine-tuning** : ❌ (Pas supporté)
- **GPU requis** : ❌
- **Dépendances** : Aucune

## Utilisation

Le modèle Dummy est principalement utilisé pour :
- **Tests unitaires** : Valider le pipeline sans dépendances externes
- **Baseline** : Comparer les performances des vrais modèles
- **Développement** : Tester rapidement sans attendre le chargement d'un modèle

## Configuration

```yaml
# Pas de configuration spécifique nécessaire
model: dummy
```

## Utilisation

### Via CLI

```bash
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model dummy
```

### Via Python

```python
from src.nlp.models.dummy import DummyNLPModel

model = DummyNLPModel()
result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}")
print(f"Destination: {result.destination}")
```

## Méthode d'extraction

Le modèle utilise des patterns regex simples :

- **"depuis X"** : "aller à Paris depuis Lyon" → origine: Lyon
- **"de X à Y"** : "de Lyon à Paris" → origine: Lyon, destination: Paris
- **"aller à X"** : "aller à Paris" → destination: Paris
- **"partir de X"** : "partir de Lyon" → origine: Lyon

## Liste de villes

Le modèle contient une liste limitée de ~20 villes françaises communes :
- Paris, Lyon, Marseille, Toulouse, Nice, Nantes, etc.

## Résultat

Le modèle retourne un objet `NLPExtraction` :

```python
NLPExtraction(
    origin="Lyon",
    destination="Paris",
    is_valid=True,
    confidence=0.5,  # Fixe à 0.5 si extraction réussie
    metadata={
        "model": "dummy",
        "extraction_method": "regex_patterns"
    }
)
```

## Calcul de confiance

- **Extraction réussie** : 0.5
- **Aucune extraction** : 0.0

## Performance

### Exemple de latence

| Longueur texte | Temps traitement |
|----------------|------------------|
| 10 mots | ~0.001s |
| 50 mots | ~0.001s |
| 100 mots | ~0.001s |

### Précision (sur dataset de test)

| Métrique | Score |
|----------|-------|
| F1-Score | ~0.23 |
| Precision | ~0.25 |
| Recall | ~0.21 |

**Note** : La précision est limitée par la simplicité des patterns.

## Avantages

1. **Très rapide** : Traitement instantané
2. **Aucune dépendance** : Fonctionne sans installation
3. **Simple** : Facile à comprendre
4. **Baseline** : Utile pour comparer les performances

## Inconvénients

1. **Précision très limitée** : Patterns très simples
2. **Liste de villes limitée** : Seulement ~20 villes
3. **Pas de fine-tuning** : Ne peut pas être amélioré
4. **Ne peut pas être utilisé en production** : Trop basique

## Cas d'usage

1. **Tests de pipeline** : Valider que le pipeline fonctionne
2. **Tests NLP** : Tester l'extraction avec un modèle simple
3. **Benchmark** : Utiliser comme baseline pour comparer

## Limitations

- Ne gère pas bien les variations de formulation
- Liste de villes très limitée
- Patterns très basiques
- Ne peut pas être utilisé en production
