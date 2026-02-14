# Modèle Pathfinding : Dijkstra Optimisé

## Vue d'ensemble

Le modèle Dijkstra utilise l'algorithme de Dijkstra pour trouver le chemin optimal entre deux gares dans un graphe ferroviaire. La version optimisée de THOR privilégie le **temps de trajet** plutôt que la distance, et utilise des **pénalités intelligentes** pour favoriser les trains rapides (TGV, OUIGO) sans les prioriser absolument.

## Caractéristiques

- **Algorithme** : Dijkstra avec pénalités par type de train
- **Critère d'optimisation** : Temps de trajet (minutes)
- **Pénalités intelligentes** : Multiplicateurs adaptés par type de train
- **Correspondances inter-gare** : Support des transferts métro entre gares parisiennes
- **Graphe** : Non-orienté (liaisons dans les deux sens)
- **Performance** : ⭐⭐⭐⭐⭐ (Optimisé pour trajets réels)
- **Précision** : ⭐⭐⭐⭐⭐ (Trouve le chemin optimal selon critères définis)

## Fonctionnement

### 1. Chargement des données

Le modèle charge deux fichiers JSON enrichis :

- **`dataset_gares.json`** : Liste des gares avec :
  - Code UIC (identifiant unique)
  - Nom de la gare
  - Coordonnées géographiques (latitude, longitude)
  - Informations sur la ville (code INSEE, nom)

- **`dataset_liaisons_enhanced.json`** : Liste des liaisons enrichies avec :
  - Code UIC de la gare de départ et d'arrivée
  - **Temps de trajet** (temps_min) - données réelles SNCF
  - Distance (distance_km)
  - Nombre de trains par jour (nb_trains_jour)
  - **Type de train** (type_train) : TGV, OUIGO, Intercités, TER, Correspondance
  - Types détaillés (types_details) : Distribution des trains par type
  - **Géométrie** (geometry) : Tracé précis de la voie ferrée (GeoJSON LineString)

### 2. Construction du graphe

Le modèle construit un graphe non-orienté où :
- **Nœuds** : Gares (identifiées par leur code UIC)
- **Arêtes** : Liaisons ferroviaires + correspondances inter-gare
- **Poids** : Temps de trajet × multiplicateur de pénalité par type de train

### 3. Système de pénalités par type de train

Le modèle utilise des **pénalités intelligentes** pour favoriser les trains rapides tout en permettant des alternatives :

| Type de train | Multiplicateur | Justification |
|---------------|----------------|---------------|
| **TGV** | ×1.0 | Priorité maximale (rapide, confortable) |
| **OUIGO** | ×1.0 | Même priorité que TGV (TGV low-cost) |
| **Lyria** | ×1.0 | TGV international (Suisse) |
| **Eurostar** | ×1.0 | TGV international (UK, Belgique) |
| **Intercités** | ×1.3 | Légère pénalité (plus lent) |
| **Train de nuit** | ×1.5 | Pénalité modérée (très lent mais utile) |
| **TER** | ×2.0 | Pénalité importante (régional, nombreux arrêts) |
| **Navette** | ×2.0 | Pénalité importante (courte distance) |
| **Auto-train** | ×2.5 | Forte pénalité (très lent) |
| **Autre** | ×2.0 | Pénalité par défaut |
| **Correspondance** | ×1.0 | Pas de pénalité (transfert inter-gare nécessaire) |

**Exemple de calcul :**
```
# Liaison TGV Paris → Lyon : 120 min
Poids = 120 × 1.0 = 120 minutes

# Liaison TER : 180 min
Poids = 180 × 2.0 = 360 minutes

# L'algorithme choisit la liaison avec le poids le PLUS PETIT
```

Ce système permet à Dijkstra de trouver des trajets intelligents :
- Prendre un TER court + TGV long peut être mieux qu'un TER direct
- Les correspondances inter-gare ne sont pas pénalisées injustement

### 4. Correspondances inter-gare

Le modèle supporte les **transferts métro** entre grandes gares parisiennes :

- **Paris Montparnasse ↔ Paris Gare de Lyon** : 5-10 min (métro ligne 14)
- **Paris Montparnasse ↔ Paris Nord** : 5-10 min (métro ligne 4)
- **Paris Gare de Lyon ↔ Paris Nord** : 5-10 min (métro ligne 5)

Ces correspondances sont représentées comme des liaisons spéciales de type `"Correspondance"` avec :
- Temps de transfert réaliste (5-10 min)
- Distance à vol d'oiseau entre gares
- Pénalité ×1.0 (neutre)

**Sur la carte web :** Les correspondances sont affichées en **lignes jaunes pointillées** entre les gares.

### 5. Recherche de ville

Pour chaque ville demandée (origine/destination), le modèle :
1. Recherche dans la base de données des gares
2. Trouve le code INSEE de la ville
3. Trouve le code UIC de la gare correspondante
4. Si plusieurs gares, prend en compte toutes les combinaisons possibles

**Note** : Les grandes villes avec plusieurs gares (Paris, Lyon, etc.) sont gérées intelligemment.

### 6. Algorithme de Dijkstra optimisé

L'algorithme de Dijkstra trouve le chemin avec le **temps de trajet minimal** :

1. Initialise une file de priorité avec la gare de départ (coût = 0)
2. Tant que la file n'est pas vide :
   - Extrait le nœud avec le coût minimal (temps accumulé)
   - Si c'est la destination, retourne le chemin
   - Sinon, explore les voisins :
     - Calcule : `nouveau_coût = coût_actuel + (temps_liaison × pénalité_type_train)`
     - Si meilleur que le coût connu, met à jour
3. Retourne le chemin avec temps total et étapes

**Gestion multi-gare :**
- Si origine/destination ont plusieurs gares, teste toutes les combinaisons
- Conserve le meilleur chemin global

### 7. Formatage du résultat

Le modèle convertit les codes UIC en noms de gares et retourne un objet `Route` avec :

**Segments détaillés** :
- Gare de départ et d'arrivée
- Temps de trajet (temps_min)
- Distance (distance_km)
- Type de train (type_train)
- Nombre de trains par jour
- **Géométrie GeoJSON** : Tracé précis de la voie ferrée
- Coordonnées exactes des gares (from_lat, from_lon, to_lat, to_lon)

**Métadonnées** :
- Codes UIC des gares
- Chemin complet (path_uic)
- Nombre de stations
- Mode de calcul (temps_reel)
- Gares d'origine/destination UIC

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
  path_liaisons_enhanced: data/train_station/dataset_liaisons_enhanced.json
  path_shapes: data/raw/shapes.json
```

### Configuration personnalisée

```yaml
pathfinding:
  path_gares: /chemin/vers/dataset_gares.json
  path_liaisons_enhanced: /chemin/vers/dataset_liaisons_enhanced.json
  path_shapes: /chemin/vers/shapes.json
```

**Fichiers requis :**
- `dataset_gares.json` : Informations des gares (2782 gares)
- `dataset_liaisons_enhanced.json` : Liaisons enrichies avec temps, types, géométries (11382+ liaisons)
- `shapes.json` : Tracés géométriques complets des voies ferrées (fallback)

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

### Format des liaisons enrichies

```json
{
  "depart": "87497461",
  "arrivee": "87581000",
  "distance_km": 216.83,
  "temps_min": 135.5,
  "nb_trains_jour": 42,
  "type_train": "TGV",
  "types_details": {
    "TGV": 38,
    "OUIGO": 4
  },
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [1.4542, 43.6111],
      [1.456, 43.612],
      ...
      [-0.5569, 44.8378]
    ]
  }
}
```

### Format des correspondances inter-gare

```json
{
  "depart": "87391102",
  "arrivee": "87686006",
  "distance_km": 5,
  "temps_min": 5,
  "nb_trains_jour": 999,
  "type_train": "Correspondance",
  "types_details": {
    "Correspondance": 1
  },
  "geometry": {
    "type": "LineString",
    "coordinates": [
      [2.320514, 48.841172],
      [2.37352, 48.844888]
    ]
  }
}
```

## Calcul de temps et distance

### Temps de trajet

Le modèle utilise les **temps réels** issus des données SNCF :
- Temps moyens calculés à partir des horaires de trains
- Prise en compte des arrêts intermédiaires
- Temps de correspondance réalistes (5-10 min pour inter-gare)

### Distance géographique

Le modèle utilise la **formule de Haversine** pour les distances à vol d'oiseau :

```python
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convertir en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Différences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Formule de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c  # Rayon de la Terre en km
    
    return distance

# Exemple : Paris → Lyon
distance = calculate_distance(48.8566, 2.3522, 45.7640, 4.8357)
# Résultat : ~392 km (à vol d'oiseau, trajet réel ~465 km)
```

**Note** : La distance Haversine est utilisée uniquement pour :
- Les correspondances inter-gare (courte distance)
- Le fallback si distance_km n'est pas disponible
- L'affichage sur la carte (géométries précises disponibles)

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

### Itinéraire simple (Toulouse → Bordeaux)

```python
Route(
    origin="Toulouse",
    destination="Bordeaux",
    segments=[
        {
            "from": "Toulouse Matabiau",
            "to": "Bordeaux Saint-Jean",
            "from_lat": 43.6111,
            "from_lon": 1.4542,
            "to_lat": 44.8378,
            "to_lon": -0.5569,
            "temps_min": 135.5,
            "distance_km": 216.83,
            "nb_trains_jour": 42,
            "type_train": "TGV",
            "types_details": {
                "TGV": 38,
                "OUIGO": 4
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[1.4542, 43.6111], ..., [-0.5569, 44.8378]]
            }
        }
    ],
    metadata={
        "origin_uic": "87497461",
        "destination_uic": "87581000",
        "path_uic": ["87497461", "87581000"],
        "num_stations": 2,
        "mode": "temps_reel"
    }
)
```

### Itinéraire avec correspondance inter-gare (Biarritz → Marseille)

```python
Route(
    origin="Biarritz",
    destination="Marseille",
    segments=[
        {
            "from": "Biarritz",
            "to": "Paris Montparnasse",
            "temps_min": 274.2,
            "distance_km": 758.66,
            "type_train": "TGV",
            "geometry": { ... }
        },
        {
            "from": "Paris Montparnasse",
            "to": "Paris Gare de Lyon",
            "temps_min": 5,
            "distance_km": 5,
            "type_train": "Correspondance",  # Ligne jaune pointillée sur la carte
            "geometry": {
                "type": "LineString",
                "coordinates": [[2.320514, 48.841172], [2.37352, 48.844888]]
            }
        },
        {
            "from": "Paris Gare de Lyon",
            "to": "Marseille Saint-Charles",
            "temps_min": 189.3,
            "distance_km": 660.48,
            "type_train": "TGV",
            "geometry": { ... }
        }
    ],
    metadata={
        "num_stations": 4,
        "mode": "temps_reel"
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

- **Temps de chargement** : ~2-3 secondes (2782 gares, 11382+ liaisons avec géométries)
- **Temps de recherche** : < 0.2 seconde pour la plupart des cas (avec multi-gare)
- **Complexité** : O((V + E) log V) où V = nombre de gares, E = nombre de liaisons
- **Mémoire** : ~150 MB (avec géométries chargées en lazy loading)

## Limitations

1. **Horaires fixes** : Temps moyens utilisés, pas les horaires en temps réel
2. **Graphe statique** : Pas de prise en compte des retards ou annulations
3. **Correspondances limitées** : Seules les correspondances inter-gare Paris sont implémentées
4. **Géométries incomplètes** : Certaines liaisons ont des tracés partiels (<80% de points valides)
5. **Pas d'optimisation multi-critère** : Optimise uniquement le temps (pas prix, confort, etc.)

## Améliorations possibles

### Court terme
- **Correspondances étendues** : Ajouter Lyon, Marseille, Lille, Bordeaux inter-gare
- **Optimisation multi-critère** : Pareto-optimal (temps vs prix vs confort)
- **Géométries complètes** : Compléter les tracés manquants via OpenStreetMap
- **Horaires dynamiques** : Intégration API SNCF temps réel

### Moyen terme
- **A* Algorithm** : Heuristique avec distance géographique pour accélérer
- **Prédiction retards** : Machine learning sur historique des retards
- **Alternatives multiples** : Top-K chemins au lieu d'un seul optimal
- **Optimisation CO2** : Calcul et affichage de l'empreinte carbone

### Long terme
- **Intégration multimodale** : Bus, avion, covoiturage en complément
- **Personnalisation** : Préférences utilisateur (fenêtre, couloir, 1ère classe)
- **Réservation intégrée** : API directe avec systèmes de réservation
- **Historique et analytics** : Suggestions basées sur trajets précédents

## Dépannage

### Erreur : "Gares file not found"

Vérifiez que les fichiers existent :
```bash
ls -la data/train_station/dataset_gares.json
ls -la data/train_station/dataset_liaisons_enhanced.json
ls -la data/raw/shapes.json
```

### Erreur : "Ville non trouvée"

Le système utilise une validation avec normalisation. Vérifiez que la ville existe :
```python
import json
data = json.load(open('data/train_station/dataset_gares.json'))
toulouse = [g for g in data if 'toulouse' in str(g).lower()]
print(len(toulouse))  # Doit être > 0
print([g['nom_gare'] for g in toulouse])
```

**Astuce** : Le validateur normalise automatiquement :
- Casse ignorée : "Paris" = "paris" = "PARIS"
- Hyphens ignorés : "Saint-Jean-Pied-de-Port" = "Saint Jean Pied de Port"
- Accents gérés : "Béziers" = "Beziers"

### Pas de chemin trouvé

Causes possibles :
- Les deux villes ne sont pas connectées dans le graphe ferroviaire français
- Une des villes n'a pas de gare SNCF
- Le graphe est incomplet pour cette liaison spécifique

Vérifiez les liaisons :
```python
import json
liaisons = json.load(open('data/train_station/dataset_liaisons_enhanced.json'))
print(f"Nombre de liaisons: {len(liaisons)}")

# Vérifier liaisons depuis une gare spécifique
uic = "87497461"  # Toulouse
from_toulouse = [l for l in liaisons if l['depart'] == uic]
print(f"Liaisons depuis Toulouse: {len(from_toulouse)}")
```

### Géométries manquantes sur la carte

Si les lignes n'apparaissent pas sur la carte :
1. Vérifiez que `geometry` existe dans la réponse API
2. Vérifiez que Leaflet CSS est chargé : `import 'leaflet/dist/leaflet.css'`
3. Ouvrez la console navigateur pour voir les erreurs
4. Certaines liaisons ont des géométries incomplètes → ligne pointillée affichée

### Correspondances pas affichées

Les correspondances inter-gare doivent :
- Avoir `type_train: "Correspondance"`
- Avoir une géométrie simple 2 points (début/fin)
- Être affichées en jaune pointillé

Vérifiez dans l'API :
```bash
curl -X POST http://localhost:8000/api/route \
  -H "Content-Type: application/json" \
  -d '{"origin": "Biarritz", "destination": "Marseille"}' | jq '.segments[] | select(.type_train == "Correspondance")'
```
