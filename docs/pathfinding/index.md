# Documentation des Modèles Pathfinding

## Vue d'ensemble

Le module Pathfinding trouve des itinéraires ferroviaires entre deux villes en utilisant un graphe de gares et de liaisons. Il utilise des algorithmes de recherche de chemin pour déterminer le trajet optimal.

## Modèles disponibles

### 1. [Dijkstra](./dijkstra.md)
- **Recommandé pour** : Recherche de chemin optimal
- **Avantages** : Trouve le chemin le plus court, algorithme classique et fiable
- **Inconvénients** : Nécessite un graphe complet des liaisons
- **Fichier** : `src/pathfinding/models/dijkstra.py`

## Fonctionnement

Le pathfinding fonctionne en plusieurs étapes :

1. **Chargement des données** : Charge les gares et les liaisons ferroviaires depuis des fichiers JSON
2. **Construction du graphe** : Crée un graphe non-orienté avec les distances entre gares
3. **Recherche de ville** : Trouve les gares correspondant aux villes demandées
4. **Calcul du chemin** : Utilise un algorithme de recherche (Dijkstra) pour trouver le chemin optimal
5. **Retour du résultat** : Retourne l'itinéraire avec les étapes, la distance et les métadonnées

## Métriques d'évaluation

Les modèles Pathfinding sont évalués selon plusieurs métriques :

- **Origin Accuracy** : Précision sur l'identification de la ville de départ
- **Destination Accuracy** : Précision sur l'identification de la ville d'arrivée
- **Route Found Rate** : Taux d'itinéraires trouvés avec succès
- **Path Accuracy** : Précision du chemin (comparaison avec étapes de référence)
- **Distance Error** : Erreur de distance par rapport à la référence
- **Num Steps** : Nombre moyen d'étapes dans l'itinéraire

## Utilisation

### Via CLI

```bash
# Trouver un itinéraire
python -m src.cli.pathfinding find-route \
    --origin Toulouse \
    --destination Bordeaux \
    --model dijkstra

# Évaluer un modèle
python -m src.cli.pathfinding evaluate \
    --dataset data/splits/test/test_pathfinding.jsonl \
    --model dijkstra \
    --output-dir results/pathfinding/dijkstra_test
```

### Via Python

```python
from src.pathfinding.models.dijkstra import DijkstraPathfindingModel

model = DijkstraPathfindingModel({
    "path_gares": "data/train_station/dataset_gares.json",
    "path_liaisons": "data/train_station/dataset_liaisons.json"
})
result = model.find_route("Toulouse", "Bordeaux")
print(f"Distance: {result.total_distance} km")
print(f"Étapes: {result.steps}")
```

## Interface standard

Tous les modèles Pathfinding implémentent l'interface `PathfindingModel` :

```python
class PathfindingModel(ABC):
    def find_route(self, origin: str, destination: str) -> Route:
        """Trouve un itinéraire entre deux villes."""
        pass
```

## Résultat de recherche

Tous les modèles retournent un objet `Route` :

```python
@dataclass
class Route:
    origin: str                    # Ville de départ
    destination: str                # Ville d'arrivée
    steps: List[str]               # Liste des gares/étapes
    total_distance: Optional[float] # Distance totale en km
    total_time: Optional[float]    # Temps estimé en minutes
    metadata: Dict[str, Any]        # Métadonnées supplémentaires
```

## Données requises

Le pathfinding nécessite deux fichiers JSON :

1. **Dataset des gares** (`dataset_gares.json`) :
   - Liste des gares avec leurs coordonnées géographiques
   - Informations sur les villes (code INSEE, nom)
   - Codes UIC des gares

2. **Dataset des liaisons** (`dataset_liaisons.json`) :
   - Liste des liaisons ferroviaires entre gares
   - Codes UIC de départ et d'arrivée

## Configuration

Chaque modèle peut être configuré via un fichier YAML dans `configs/pathfinding/` :

```yaml
# configs/pathfinding/dijkstra.yaml
pathfinding:
  path_gares: data/train_station/dataset_gares.json
  path_liaisons: data/train_station/dataset_liaisons.json
```

## Limitations

- **Villes non trouvées** : Si une ville n'est pas dans la base de données, aucun itinéraire ne sera trouvé
- **Pas de connexion** : Si deux villes ne sont pas connectées dans le graphe, aucun chemin ne sera trouvé
- **Distance géographique** : La distance est calculée à vol d'oiseau (Haversine), pas la distance réelle du trajet ferroviaire

## Ajouter un nouveau modèle

Pour ajouter un nouveau modèle Pathfinding :

1. Créer un fichier dans `src/pathfinding/models/` (ex: `my_model.py`)
2. Implémenter la classe héritant de `PathfindingModel`
3. Implémenter la méthode `find_route()`
4. Enregistrer le modèle dans le registre (voir `src/common/registry.py`)
