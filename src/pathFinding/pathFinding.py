import math
import json
from heapq import heappop, heappush

# 1. Calcul de distance (Haversine)
def haversine(pos1, pos2):
    R = 6371  # Rayon de la Terre en km
    lat1, lon1 = pos1['lat'], pos1['lon']
    lat2, lon2 = pos2['lat'], pos2['lon']
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# 2. Chargement et préparation des données
def load_data(path_gares, path_liaisons):
    with open(path_gares, 'r', encoding='utf-8') as f:
        data_gares = json.load(f)
    with open(path_liaisons, 'r', encoding='utf-8') as f:
        data_liaisons = json.load(f)

    # Indexation des gares par UIC (on prend le 1er de la liste)
    # Format : { "87313759": {nom: "Abancourt", pos: {...}}, ... }
    stations = {g['uic'][0]: g for g in data_gares}
    
    # Construction du graphe (Liste d'adjacence)
    graph = {}
    for l in data_liaisons:
        uic_dep = str(l['depart'])
        uic_arr = str(l['arrivee'])
        
        if uic_dep in stations and uic_arr in stations:
            dist = haversine(stations[uic_dep]['position_geographique'], 
                             stations[uic_arr]['position_geographique'])
            
            # On ajoute la liaison dans les deux sens (graphe non-orienté)
            graph.setdefault(uic_dep, []).append((uic_arr, dist))
            graph.setdefault(uic_arr, []).append((uic_dep, dist))
            
    return stations, graph

# 3. Algorithme de Dijkstra
def find_shortest_path(graph, stations, start_uic, end_uic):
    queue = [(0, start_uic, [])]
    visited = set()
    min_dist = {start_uic: 0}

    while queue:
        (cost, current, path) = heappop(queue)

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

def load_data(path_gares, path_liaisons):
    with open(path_gares, 'r', encoding='utf-8') as f:
        data_gares = json.load(f)
    with open(path_liaisons, 'r', encoding='utf-8') as f:
        data_liaisons = json.load(f)

    stations_by_uic = {}
    commune_to_uic = {}

    for g in data_gares:
        uic = str(g['uic'][0])
        code_insee = str(g['ville']['id_commune'])
        
        # On stocke la gare par son UIC
        stations_by_uic[uic] = g
        
        # On crée le lien Code Commune -> UIC
        # Note : Si une commune a plusieurs gares, ceci prendra la dernière lue.
        commune_to_uic[code_insee] = uic
    
    # Construction du graphe (comme précédemment)
    graph = {}
    for l in data_liaisons:
        uic_dep, uic_arr = str(l['depart']), str(l['arrivee'])
        if uic_dep in stations_by_uic and uic_arr in stations_by_uic:
            dist = haversine(stations_by_uic[uic_dep]['position_geographique'], 
                             stations_by_uic[uic_arr]['position_geographique'])
            graph.setdefault(uic_dep, []).append((uic_arr, dist))
            graph.setdefault(uic_arr, []).append((uic_dep, dist))
            
    return stations_by_uic, commune_to_uic, graph






stations, city_map, graphe = load_data('/home/louisetienne/Documents/THOR/data/train_station/dataset_gares.json', '/home/louisetienne/Documents/THOR/data/train_station/dataset_liaisons.json')

code_dep = "60001"  # Abancourt
code_arr = "35238"  # Exemple pour Paris

uic_depart = city_map.get(code_dep)
uic_arrivee = city_map.get(code_arr)

distance, chemin = find_shortest_path(graphe, stations, uic_depart, uic_arrivee)

if uic_depart and uic_arrivee:
    distance, chemin = find_shortest_path(graphe, stations, uic_depart, uic_arrivee)
    
    if chemin:
        print(f"Trajet trouvé ({round(distance, 2)} km) :")
        for uic in chemin:
            print(f" -> {stations[uic]['nom_gare']} ({uic})")
    else:
        print("Désolé, aucun chemin de fer ne relie ces deux communes.")
else:
    print("Un des codes commune n'a pas été trouvé dans la base de données des gares.")