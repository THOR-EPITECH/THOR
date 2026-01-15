# Modèle NLP : Regex Advanced

## Vue d'ensemble

Le modèle Regex Advanced utilise des patterns regex sophistiqués et une liste de villes françaises connues pour extraire l'origine et la destination. C'est un modèle rapide et léger, idéal pour les applications nécessitant une faible latence.

## Caractéristiques

- **Précision** : ⭐⭐⭐ (Bonne)
- **Vitesse** : ⭐⭐⭐⭐⭐ (Très rapide)
- **Fine-tuning** : ❌ (Pas supporté)
- **GPU requis** : ❌ (Fonctionne sur CPU)
- **Dépendances** : Aucune dépendance lourde

## Installation

Aucune installation spéciale requise. Le modèle utilise uniquement la bibliothèque standard Python (`re`).

## Configuration

```yaml
# configs/nlp/regex_advanced.yaml
nlp:
  model_name: regex_advanced
```

Le modèle n'a pas de paramètres de configuration spécifiques.

## Utilisation

### Via CLI

```bash
# Extraction simple
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model regex_advanced

# Avec configuration
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon" \
    --model regex_advanced \
    --config configs/nlp/regex_advanced.yaml

# Évaluation
python -m src.cli.nlp evaluate \
    --model regex_advanced \
    --dataset data/splits/test/test_nlp.jsonl
```

### Via Python

```python
from src.nlp.models.regex_advanced import RegexAdvancedModel

model = RegexAdvancedModel()

result = model.extract("Je veux aller à Paris depuis Lyon")
print(f"Origine: {result.origin}")        # Lyon
print(f"Destination: {result.destination}")  # Paris
print(f"Confiance: {result.confidence}")     # 0.7-1.0
```

## Méthode d'extraction

Le modèle utilise :

1. **Patterns regex avancés** : Détecte les patterns de trajet dans le texte
2. **Liste de villes** : Vérifie si les entités extraites sont des villes connues
3. **Validation** : Vérifie si c'est une demande de trajet valide

### Patterns supportés

#### Origine
- **"depuis X"** : "aller à Paris depuis Lyon"
- **"de X"** : "de Lyon à Paris"
- **"partir de X"** : "partir de Lyon"
- **"venant de X"** : "venant de Lyon"
- **"je suis à X"** : "je suis à Lyon"

#### Destination
- **"à X"** : "aller à Paris"
- **"vers X"** : "aller vers Paris"
- **"pour X"** : "aller pour Paris"
- **"destination X"** : "destination Paris"
- **"arrivée X"** : "arrivée à Paris"

### Liste de villes

Le modèle contient une liste de ~100 villes françaises communes pour valider les extractions :
- Paris, Lyon, Marseille, Toulouse, Nice, Nantes, etc.

## Résultat

Le modèle retourne un objet `NLPExtraction` :

```python
NLPExtraction(
    origin="Lyon",
    destination="Paris",
    is_valid=True,
    confidence=0.8,
    metadata={
        "model": "regex_advanced",
        "extraction_method": "advanced_patterns"
    }
)
```

## Calcul de confiance

La confiance est calculée selon :

- **Base** : 0.4
- **Origine + Destination** : +0.3
- **Ville dans liste connue** : +0.1 chacun
- **Noms bien formés** : +0.05 chacun

Maximum : 1.0

## Performance

### Exemple de latence

| Longueur texte | Temps traitement |
|----------------|------------------|
| 10 mots | ~0.001s |
| 50 mots | ~0.005s |
| 100 mots | ~0.01s |

**Note** : Le modèle est très rapide car il n'utilise que des regex.

### Précision (sur dataset de test)

| Métrique | Score |
|----------|-------|
| F1-Score | ~0.43 |
| Precision | ~0.45 |
| Recall | ~0.40 |

**Note** : La précision est limitée par la nature des patterns regex.

## Avantages

1. **Très rapide** : Traitement quasi-instantané
2. **Léger** : Aucune dépendance lourde
3. **Simple** : Facile à comprendre et modifier
4. **Offline** : Fonctionne sans connexion
5. **CPU uniquement** : Pas besoin de GPU

## Inconvénients

1. **Précision limitée** : Moins flexible que les modèles ML
2. **Maintenance** : Nécessite d'ajouter manuellement de nouveaux patterns
3. **Villes limitées** : Liste de villes limitée (peut être étendue)
4. **Pas de fine-tuning** : Ne peut pas apprendre de nouvelles données

## Recommandations

- **Applications temps réel** : Idéal pour la faible latence
- **Ressources limitées** : Parfait pour les environnements contraints
- **Prototypage rapide** : Excellent pour tester rapidement
- **Production simple** : Suffisant si les patterns sont bien couverts

## Extensibilité

Le modèle peut être étendu en :

1. **Ajoutant des patterns** : Modifiez les listes `origin_patterns` et `dest_patterns`
2. **Ajoutant des villes** : Étendez la liste `FRENCH_CITIES`
3. **Améliorant la validation** : Modifiez `_is_likely_city()` pour mieux détecter les villes

## Dépannage

### Extraction incorrecte
- Vérifiez que le pattern est bien couvert
- Ajoutez le pattern manquant dans le code
- Vérifiez que la ville est dans la liste ou ressemble à une ville

### Performance dégradée
- Le modèle est normalement très rapide
- Vérifiez qu'il n'y a pas de regex trop complexes

## Code source

Le modèle est défini dans `src/nlp/models/regex_advanced.py`. Vous pouvez le modifier directement pour ajouter des patterns ou des villes.
