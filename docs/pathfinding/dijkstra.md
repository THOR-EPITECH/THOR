# Modèle Pathfinding : Dijkstra

## Vue d'ensemble

Le modèle Dijkstra utilise l'algorithme de Dijkstra pour trouver le chemin le plus court entre deux gares dans un graphe ferroviaire. C'est un algorithme classique et fiable qui garantit de trouver le chemin optimal en termes de distance.

## Caractéristiques

- **Algorithme** : Dijkstra (recherche du plus court chemin)
- **Distance** : Calculée avec la formule de Haversine (distance à vol d'oiseau)
- **Graphe** : Non-orienté (liaisons dans les deux sens)
- **Performance** : ⭐⭐⭐⭐ (Rapide pour des graphes de taille moyenne)
- **Précision** : ⭐⭐⭐⭐⭐ (Trouve toujours le chemin optimal)

## Fonctionnement

### 1. Chargement des données

Le modèle charge deux fichiers JSON :

- **`dataset_gares.json`** : Liste des gares avec :
  - Code UIC (identifiant unique)
  - Nom de la gare
  - Coordonnées géographiques (latitude, longitude)
  - Informations sur la ville (code INSEE, nom)

- **`dataset_liaisons.json`** : Liste des liaisons avec :
  - Code UIC de la gare de départ
  - Code UIC de la gare d'arrivée

### 2. Construction du graphe

Le modèle construit un graphe non-orienté où :
- **Nœuds** : Gares (identifiées par leur code UIC)
- **Arêtes** : Liaisons ferroviaires
- **Poids** : Distance géographique calculée avec la formule de Haversine

### 3. Recherche de ville

Pour chaque ville demandée (origine/destination), le modèle :
1. Recherche dans la base de données des gares
2. Trouve le code INSEE de la ville
3. Trouve le code UIC de la gare correspondante

**Note** : Si une ville a plusieurs gares, seule la dernière trouvée dans la base est utilisée.

### 4. Algorithme de Dijkstra

L'algorithme de Dijkstra trouve le chemin le plus court :

1. Initialise une file de priorité avec la gare de départ (coût = 0)
2. Tant que la file n'est pas vide :
   - Extrait le nœud avec le coût minimal
   - Si c'est la destination, retourne le chemin
   - Sinon, explore les voisins et met à jour les coûts
3. Retourne le chemin et la distance totale

### 5. Formatage du résultat

Le modèle convertit les codes UIC en noms de gares et retourne un objet `Route` avec :
- Liste des étapes (noms de gares)
- Distance totale en kilomètres
- Métadonnées (codes UIC, nombre d'étapes)

## Installation

Aucune dépendance supplémentaire requise. Le modèle utilise uniquement la bibliothèque standard Python :
- `heapq` : Pour la file de priorité
- `math` : Pour les calculs de distance
- `json` : Pour le chargement des données

## Configuration

### Configuration par défaut

```yaml
# configs/pathfinding/dijkstra.yaml
pathfinding:
  path_gares: data/train_station/dataset_gares.json
  path_liaisons: data/train_station/dataset_liaisons.json
```

### Configuration personnalisée

```yaml
pathfinding:
  path_gares: /chemin/vers/dataset_gares.json
  path_liaisons: /chemin/vers/dataset_liaisons.json
```

## Utilisation

### Via CLI

```bash
# Recherche d'itinéraire simple
python -m src.cli.pathfinding find-route \
    --origin Toulouse \
    --destination Bordeaux \
    --model dijkstra

# Avec configuration
python -m src.cli.pathfinding find-route \
    --origin Paris \
    --destination Lyon \
    --model dijkstra \
    --config configs/pathfinding/dijkstra.yaml

# Évaluation
python -m src.cli.pathfinding evaluate \
    --dataset data/splits/test/test_pathfinding.jsonl \
    --model dijkstra \
    --output-dir results/pathfinding/dijkstra_test
```

### Via Python

```python
from src.pathfinding.models.dijkstra import DijkstraPathfindingModel

# Initialisation
model = DijkstraPathfindingModel({
    "path_gares": "data/train_station/dataset_gares.json",
    "path_liaisons": "data/train_station/dataset_liaisons.json"
})

# Recherche d'itinéraire
result = model.find_route("Toulouse", "Bordeaux")

if result.steps:
    print(f"Distance: {result.total_distance:.2f} km")
    print(f"Étapes: {len(result.steps)}")
    for i, step in enumerate(result.steps, 1):
        print(f"  {i}. {step}")
else:
    print(f"Erreur: {result.metadata.get('error', 'Inconnue')}")
```

## Format des données

### Format des gares

```json
{
  "uic": ["87497461"],
  "nom_gare": "Toulouse Matabiau",
  "trigramme": "TLS",
  "position_geographique": {
    "lat": 43.6111,
    "lon": 1.4542
  },
  "ville": {
    "id_commune": "31555",
    "nom_commune": "TOULOUSE"
  }
}
```

### Format des liaisons

```json
{
  "depart": "87497461",
  "arrivee": "87581000"
}
```

## Calcul de distance

Le modèle utilise la **formule de Haversine** pour calculer la distance entre deux points géographiques :

```
distance = 2 × R × atan2(√a, √(1-a))

où:
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
R = 6371 km (rayon de la Terre)
```

**Note** : Cette distance est à vol d'oiseau, pas la distance réelle du trajet ferroviaire.

## Gestion des erreurs

Le modèle gère plusieurs cas d'erreur :

1. **Ville non trouvée** : Si la ville n'existe pas dans la base de données
   ```python
   Route(
       origin="VilleInexistante",
       destination="Bordeaux",
       steps=[],
       metadata={"error": "Ville de départ 'VilleInexistante' non trouvée"}
   )
   ```

2. **Aucune gare** : Si la ville n'a pas de gare associée
   ```python
   metadata={"error": "Aucune gare trouvée pour 'Ville'"}
   ```

3. **Pas de chemin** : Si les deux villes ne sont pas connectées
   ```python
   metadata={"error": "Aucun chemin trouvé entre ces deux villes"}
   ```

## Exemples de résultats

### Itinéraire trouvé

```python
Route(
    origin="Toulouse",
    destination="Bordeaux",
    steps=[
        "Toulouse Matabiau",
        "Bordeaux Saint-Jean",
        "Mérignac Arlac",
        "Caudéran Mérignac"
    ],
    total_distance=216.83,
    metadata={
        "origin_uic": "87497461",
        "destination_uic": "87581000",
        "path_uic": ["87497461", "87581000", "...", "..."],
        "num_stations": 4
    }
)
```

### Erreur : ville non trouvée

```python
Route(
    origin="VilleInexistante",
    destination="Bordeaux",
    steps=[],
    metadata={"error": "Ville de départ 'VilleInexistante' non trouvée"}
)
```

## Performance

- **Temps de chargement** : ~1-2 secondes (2782 gares, 2381 nœuds)
- **Temps de recherche** : < 0.1 seconde pour la plupart des cas
- **Complexité** : O((V + E) log V) où V = nombre de gares, E = nombre de liaisons

## Limitations

1. **Distance géographique** : La distance est calculée à vol d'oiseau, pas la distance réelle du trajet
2. **Une seule gare par ville** : Si une ville a plusieurs gares, seule la dernière dans la base est utilisée
3. **Pas de temps de trajet** : Le modèle ne calcule que la distance, pas le temps
4. **Graphe statique** : Le graphe ne change pas dynamiquement (pas de prise en compte des horaires)

## Améliorations possibles

- **A* Algorithm** : Utiliser une heuristique pour accélérer la recherche
- **Multi-gare par ville** : Gérer plusieurs gares pour une même ville
- **Temps de trajet** : Ajouter le calcul du temps basé sur les vitesses moyennes
- **Pondération** : Utiliser d'autres critères que la distance (temps, nombre de correspondances)

## Dépannage

### Erreur : "Gares file not found"

Vérifiez que le fichier existe :
```bash
ls -la data/train_station/dataset_gares.json
```

### Erreur : "Ville non trouvée"

Vérifiez que la ville existe dans la base de données :
```python
import json
data = json.load(open('data/train_station/dataset_gares.json'))
toulouse = [g for g in data if 'toulouse' in str(g).lower()]
print(len(toulouse))  # Doit être > 0
```

### Pas de chemin trouvé

Cela peut signifier :
- Les deux villes ne sont pas connectées dans le graphe
- Une des villes n'a pas de gare
- Le graphe est incomplet

Vérifiez les liaisons :
```python
import json
liaisons = json.load(open('data/train_station/dataset_liaisons.json'))
print(f"Nombre de liaisons: {len(liaisons)}")
```
