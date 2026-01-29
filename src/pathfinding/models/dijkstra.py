"""
Algorithme de Dijkstra pour le pathfinding ferroviaire.

Version consolidée utilisant les temps de trajet réels extraits des données GTFS.
"""

import math
import json
from heapq import heappop, heappush
from pathlib import Path
from typing import Optional

from src.pathfinding.interfaces import PathfindingModel
from src.common.types import Route
from src.common.logging import setup_logging

logger = setup_logging(module="pathfinding.dijkstra")


# --- Fonctions utilitaires ---

def haversine(pos1: dict, pos2: dict) -> float:
    """Calcule la distance en km entre deux positions GPS."""
    R = 6371  # Rayon de la Terre en km
    lat1, lon1 = pos1['lat'], pos1['lon']
    lat2, lon2 = pos2['lat'], pos2['lon']
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_data_legacy(path_gares: str, path_liaisons: str) -> tuple[dict, dict, dict]:
    """
    Chargement legacy utilisant la distance géographique comme poids.
    Gardé pour rétrocompatibilité.
    """
    with open(path_gares, 'r', encoding='utf-8') as f:
        data_gares = json.load(f)
    with open(path_liaisons, 'r', encoding='utf-8') as f:
        data_liaisons = json.load(f)

    stations_by_uic = {}
    commune_to_uic = {}

    for g in data_gares:
        uic = str(g['uic'][0])
        code_insee = str(g['ville']['id_commune'])
        stations_by_uic[uic] = g
        commune_to_uic[code_insee] = uic
    
    graph = {}
    for l in data_liaisons:
        uic_dep, uic_arr = str(l['depart']), str(l['arrivee'])
        if uic_dep in stations_by_uic and uic_arr in stations_by_uic:
            dist = haversine(
                stations_by_uic[uic_dep]['position_geographique'], 
                stations_by_uic[uic_arr]['position_geographique']
            )
            graph.setdefault(uic_dep, []).append((uic_arr, dist))
            graph.setdefault(uic_arr, []).append((uic_dep, dist))
            
    return stations_by_uic, commune_to_uic, graph


def load_data_enhanced(path_gares: str, path_liaisons_enhanced: str) -> tuple[dict, dict, dict, dict]:
    """
    Chargement utilisant le fichier enrichi avec temps de trajet réels.
    
    Returns:
        stations_by_uic: Dict des gares indexées par UIC
        commune_to_uic: Dict code INSEE -> UIC
        graph: Dict du graphe avec temps de trajet comme poids
        edge_info: Dict (uic_from, uic_to) -> infos détaillées de la liaison
    """
    with open(path_gares, 'r', encoding='utf-8') as f:
        data_gares = json.load(f)
    with open(path_liaisons_enhanced, 'r', encoding='utf-8') as f:
        data_enhanced = json.load(f)

    stations_by_uic = {}
    commune_to_uic = {}

    for g in data_gares:
        code_insee = str(g['ville']['id_commune'])
        # Indexer par TOUS les codes UIC de la gare
        for uic in g['uic']:
            uic_str = str(uic)
            stations_by_uic[uic_str] = g
            commune_to_uic[code_insee] = uic_str
    
    graph = {}
    edge_info = {}
    
    liaisons = data_enhanced.get('liaisons', data_enhanced)
    if isinstance(liaisons, dict):
        liaisons = data_enhanced
    
    # Coefficients de pénalité par type de train
    # Plus le coefficient est bas, plus le train est favorisé
    TRAIN_TYPE_PENALTY = {
        'TGV': 1.0,           # Priorité maximale
        'OUIGO': 1.0,         # Même priorité que TGV
        'Lyria': 1.0,         # TGV international
        'Eurostar': 1.0,      # TGV international
        'Intercités': 1.3,    # Légère pénalité
        'Train de nuit': 1.5, # Pénalité modérée
        'TER': 2.0,           # Pénalité importante
        'Navette': 2.0,       # Pénalité importante
        'Auto-train': 2.5,    # Forte pénalité
        'Autre': 2.0,         # Pénalité par défaut
    }
    
    for l in liaisons:
        uic_dep = str(l['depart'])
        uic_arr = str(l['arrivee'])
        
        if uic_dep not in stations_by_uic or uic_arr not in stations_by_uic:
            continue
        
        # Utiliser le temps de trajet moyen comme poids principal
        temps = l.get('temps_moyen_min', 0)
        
        # Si pas de temps disponible, fallback sur la distance
        if temps <= 0:
            temps = haversine(
                stations_by_uic[uic_dep]['position_geographique'],
                stations_by_uic[uic_arr]['position_geographique']
            )
        
        # Appliquer la pénalité selon le type de train
        train_type = l.get('type_train', 'Autre')
        penalty = TRAIN_TYPE_PENALTY.get(train_type, 2.0)
        temps_pondere = temps * penalty
        
        graph.setdefault(uic_dep, []).append((uic_arr, temps_pondere))
        
        # Stocker les infos détaillées
        edge_info[(uic_dep, uic_arr)] = {
            'temps_moyen': l.get('temps_moyen_min', 0),
            'temps_min': l.get('temps_min_min', 0),
            'temps_max': l.get('temps_max_min', 0),
            'nb_trains': l.get('nb_trains', 0),
            'distance_km': l.get('distance_km', 0),
            'type_train': l.get('type_train', 'Autre'),
            'types_details': l.get('types_details', {})
        }
    
    return stations_by_uic, commune_to_uic, graph, edge_info


def find_shortest_path(graph: dict, start_uic: str, end_uic: str) -> tuple[float | None, list | None]:
    """
    Algorithme de Dijkstra pour trouver le chemin le plus court.
    
    Args:
        graph: Graphe du réseau {uic: [(voisin_uic, poids), ...]}
        start_uic: UIC de départ
        end_uic: UIC d'arrivée
    
    Returns:
        (coût_total, liste_uic) ou (None, None) si pas de chemin
    """
    if start_uic not in graph:
        return None, None
    
    queue = [(0, start_uic, [])]
    visited = set()
    min_dist = {start_uic: 0}

    while queue:
        cost, current, path = heappop(queue)

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]

        if current == end_uic:
            return cost, path

        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
                
            new_cost = cost + weight
            if new_cost < min_dist.get(neighbor, float('inf')):
                min_dist[neighbor] = new_cost
                heappush(queue, (new_cost, neighbor, path))

    return None, None


# --- Classe principale ---

class DijkstraPathfindingModel(PathfindingModel):
    """
    Modèle de pathfinding utilisant Dijkstra avec temps de trajet réels.
    
    Ce modèle peut utiliser:
    - Le fichier enrichi avec temps de trajet réels (par défaut)
    - Le fichier legacy avec distances géographiques (fallback)
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        
        self.path_gares = self.config.get(
            "path_gares",
            "data/train_station/dataset_gares.json"
        )
        self.path_liaisons_enhanced = self.config.get(
            "path_liaisons_enhanced",
            "data/train_station/dataset_liaisons_enhanced.json"
        )
        self.path_liaisons_legacy = self.config.get(
            "path_liaisons",
            "data/train_station/dataset_liaisons.json"
        )
        
        # Mode: "time" (temps de trajet) ou "distance" (distance géo)
        self.mode = self.config.get("mode", "time")
        
        self._stations_by_uic = {}
        self._commune_to_uic = {}
        self._graph = {}
        self._edge_info = {}
        self._use_enhanced = False
    
    def _load_model(self):
        """Charge les données des gares et construit le graphe."""
        path_gares = Path(self.path_gares)
        path_liaisons_enhanced = Path(self.path_liaisons_enhanced)
        path_liaisons_legacy = Path(self.path_liaisons_legacy)
        
        if not path_gares.exists():
            raise FileNotFoundError(f"Gares file not found: {path_gares}")
        
        # Essayer le fichier enrichi d'abord
        if self.mode == "time" and path_liaisons_enhanced.exists():
            logger.info(f"Loading enhanced data (temps de trajet réels)")
            logger.info(f"  Gares: {path_gares}")
            logger.info(f"  Liaisons: {path_liaisons_enhanced}")
            
            self._stations_by_uic, self._commune_to_uic, self._graph, self._edge_info = load_data_enhanced(
                str(path_gares),
                str(path_liaisons_enhanced)
            )
            self._use_enhanced = True
            
        elif path_liaisons_legacy.exists():
            logger.info(f"Loading legacy data (distances géographiques)")
            logger.info(f"  Gares: {path_gares}")
            logger.info(f"  Liaisons: {path_liaisons_legacy}")
            
            self._stations_by_uic, self._commune_to_uic, self._graph = load_data_legacy(
                str(path_gares),
                str(path_liaisons_legacy)
            )
            self._use_enhanced = False
            
        else:
            raise FileNotFoundError(
                f"Aucun fichier de liaisons trouvé: {path_liaisons_enhanced} ou {path_liaisons_legacy}"
            )
        
        logger.info(f"Loaded {len(self._stations_by_uic)} stations and {len(self._graph)} graph nodes")
        logger.info(f"Mode: {'temps de trajet' if self._use_enhanced else 'distance géographique'}")
    
    def _find_uic_for_city(self, city_name: str) -> Optional[str]:
        """
        Trouve l'UIC de la meilleure gare pour une ville donnée.
        
        Pour les grandes villes avec plusieurs gares, on privilégie:
        1. La gare principale (souvent la plus connectée dans le graphe)
        2. Une gare TGV ou grande ligne
        """
        city_name_lower = city_name.lower().strip()
        candidates = []
        
        # Étape 1: Chercher les gares dont le nom COMMENCE par la ville ou
        # dont la commune correspond
        for uic, station in self._stations_by_uic.items():
            gare_nom = station.get('nom_gare', '').lower()
            ville_nom = station.get('ville', {}).get('nom_commune', '').lower()
            
            # Correspondance exacte du nom de gare
            if gare_nom == city_name_lower:
                candidates.append((uic, station, 200))
                continue
            
            # Le nom de gare COMMENCE par la ville (ex: "Lyon Part Dieu", pas "Paris Gare de Lyon")
            if gare_nom.startswith(city_name_lower + ' ') or gare_nom.startswith(city_name_lower + '-'):
                score = 100
                # Bonus pour les grandes gares principales
                if any(term in gare_nom for term in ['part-dieu', 'part dieu', 'saint-jean', 
                                                       'saint-charles', 'perrache', 'montparnasse']):
                    score += 50
                if any(term in gare_nom for term in ['tgv', 'central', 'centre']):
                    score += 30
                # Pénalité pour les gares secondaires
                if any(term in gare_nom for term in ['aéroport', 'banlieue', 'rer', 'gorge', 'vaise', 'saint-paul']):
                    score -= 20
                candidates.append((uic, station, score))
                continue
            
            # Correspondance exacte sur le nom de commune
            if ville_nom == city_name_lower:
                score = 80
                candidates.append((uic, station, score))
            elif city_name_lower in ville_nom and not ville_nom.startswith('paris'):
                # Éviter de matcher les arrondissements parisiens pour d'autres villes
                candidates.append((uic, station, 40))
        
        if not candidates:
            # Fallback: recherche plus permissive pour les noms composés
            for uic, station in self._stations_by_uic.items():
                gare_nom = station.get('nom_gare', '').lower()
                # Ex: "Saint-Étienne" dans "Saint-Étienne Châteaucreux"
                if city_name_lower in gare_nom and not 'gare de' in gare_nom:
                    candidates.append((uic, station, 30))
        
        if not candidates:
            return None
        
        # Filtrer les candidats qui sont dans le graphe
        candidates_in_graph = [(uic, s, score) for uic, s, score in candidates if uic in self._graph]
        
        if candidates_in_graph:
            # Bonus significatif pour les gares bien connectées
            for i, (uic, s, score) in enumerate(candidates_in_graph):
                nb_connections = len(self._graph.get(uic, []))
                # Les gares très connectées sont généralement les gares principales
                candidates_in_graph[i] = (uic, s, score + nb_connections * 2)
            
            # Trier par score et retourner le meilleur
            candidates_in_graph.sort(key=lambda x: -x[2])
            return candidates_in_graph[0][0]
        
        # Sinon, retourner le meilleur candidat même hors graphe
        candidates.sort(key=lambda x: -x[2])
        return candidates[0][0]
    
    def _find_uic_by_name(self, name: str) -> Optional[str]:
        """Trouve l'UIC d'une gare à partir de son nom exact ou partiel."""
        name_lower = name.lower().strip()
        
        # Recherche exacte
        for uic, station in self._stations_by_uic.items():
            if station.get('nom_gare', '').lower() == name_lower:
                if uic in self._graph:
                    return uic
        
        # Recherche partielle, priorité aux gares dans le graphe
        matches = []
        for uic, station in self._stations_by_uic.items():
            gare_nom = station.get('nom_gare', '').lower()
            if name_lower in gare_nom or gare_nom in name_lower:
                in_graph = uic in self._graph
                matches.append((uic, in_graph))
        
        # Priorité aux gares dans le graphe
        matches.sort(key=lambda x: -x[1])
        return matches[0][0] if matches else None
    
    def find_route(self, origin: str, destination: str) -> Route:
        """
        Trouve un itinéraire entre deux villes.
        
        L'algorithme optimise maintenant le temps de trajet total plutôt
        que la distance géographique.
        """
        if not self._initialized:
            self.initialize()
        
        # Chercher les UIC avec la méthode améliorée
        origin_uic = self._find_uic_for_city(origin)
        destination_uic = self._find_uic_for_city(destination)
        
        # Fallback: chercher par nom de gare exact
        if not origin_uic:
            origin_uic = self._find_uic_by_name(origin)
        if not destination_uic:
            destination_uic = self._find_uic_by_name(destination)
        
        if not origin_uic:
            logger.warning(f"Origin '{origin}' not found")
            return Route(origin=origin, destination=destination, steps=[], 
                       metadata={"error": f"Ville/gare de départ '{origin}' non trouvée"})
        
        if not destination_uic:
            logger.warning(f"Destination '{destination}' not found")
            return Route(origin=origin, destination=destination, steps=[],
                       metadata={"error": f"Ville/gare d'arrivée '{destination}' non trouvée"})
        
        # Recherche du chemin optimal
        total_weight, chemin_uic = find_shortest_path(self._graph, origin_uic, destination_uic)
        
        if not chemin_uic:
            return Route(origin=origin, destination=destination, steps=[],
                       metadata={"error": "Aucun chemin trouvé"})
        
        # Construire les étapes détaillées
        steps = [self._stations_by_uic[uic]['nom_gare'] for uic in chemin_uic]
        
        # Calculer les statistiques du trajet
        total_time = 0
        total_distance = 0
        segment_details = []
        
        for i in range(len(chemin_uic) - 1):
            uic_from = chemin_uic[i]
            uic_to = chemin_uic[i + 1]
            
            edge = self._edge_info.get((uic_from, uic_to), {})
            
            temps = edge.get('temps_moyen', 0)
            distance = edge.get('distance_km', 0)
            
            # Si pas d'info enrichie, calculer la distance
            if distance == 0:
                distance = haversine(
                    self._stations_by_uic[uic_from]['position_geographique'],
                    self._stations_by_uic[uic_to]['position_geographique']
                )
            
            total_time += temps
            total_distance += distance
            
            segment_details.append({
                "from": self._stations_by_uic[uic_from]['nom_gare'],
                "to": self._stations_by_uic[uic_to]['nom_gare'],
                "temps_min": edge.get('temps_moyen', 0),
                "distance_km": round(distance, 2),
                "nb_trains_jour": edge.get('nb_trains', 0),
                "type_train": edge.get('type_train', 'Autre'),
                "types_details": edge.get('types_details', {})
            })
        
        logger.info(f"Found route: {origin} → {destination} ({len(steps)} stops, {total_time:.0f} min, {total_distance:.1f} km)")
        
        return Route(
            origin=origin,
            destination=destination,
            steps=steps,
            total_distance=round(total_distance, 2),
            total_time=round(total_time, 1),
            metadata={
                "origin_uic": origin_uic,
                "destination_uic": destination_uic,
                "path_uic": chemin_uic,
                "num_stations": len(steps),
                "mode": "temps_reel" if self._use_enhanced else "distance",
                "segments": segment_details
            }
        )
