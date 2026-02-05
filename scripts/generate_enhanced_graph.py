#!/usr/bin/env python3
"""
Génère un graphe enrichi pour le pathfinding avec les temps de trajet réels
extraits du fichier GTFS stop_times.txt.

Ce script crée dataset_liaisons_enhanced.json avec:
- Temps de trajet moyen, min, max (en minutes)
- Nombre de trains quotidiens par liaison
- Distance géographique (calculée via Haversine)

Usage:
    python scripts/generate_enhanced_graph.py
"""

import csv
import json
import math
import os
import re
from collections import defaultdict
from datetime import datetime

# Chemins
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

INPUT_STOP_TIMES = os.path.join(PROJECT_ROOT, 'data', 'raw', 'stop_times.txt')
INPUT_GARES = os.path.join(PROJECT_ROOT, 'data', 'train_station', 'dataset_gares.json')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'train_station', 'dataset_liaisons_enhanced.json')


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcule la distance en km entre deux points GPS."""
    R = 6371  # Rayon de la Terre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def extract_uic(stop_id: str) -> str | None:
    """Extrait le code UIC (8 chiffres) du stop_id GTFS."""
    match = re.search(r'(\d{8})', str(stop_id))
    return match.group(1) if match else None


# Mapping des codes GTFS vers les types de trains
TRAIN_TYPE_MAPPING = {
    'OCETGV INOUI': 'TGV',
    'OCETGV': 'TGV',
    'OCEOUIGO': 'OUIGO',
    'OCEINTERCITES': 'Intercités',
    'OCENavette': 'Navette',
    'OCETER': 'TER',
    'OCESN': 'TER',
    'OCET': 'TER',
    'OCEC': 'Car',
    'OCESA': 'Auto-train',
    'OCEEA': 'Eurostar',
    'OCELO': 'Train de nuit',
    'OCEL': 'Lyria',
}


def extract_train_type_from_stop(stop_id: str) -> str:
    """Extrait le type de train depuis le stop_id GTFS."""
    # Le stop_id contient le type de train: StopPoint:OCETGV INOUI-87212027
    stop_upper = stop_id.upper()
    
    # Vérifier les types de trains dans l'ordre de priorité
    if 'OCETGV' in stop_upper or 'TGV INOUI' in stop_upper:
        return 'TGV'
    elif 'OCEOUIGO' in stop_upper or 'OUIGO' in stop_upper:
        return 'OUIGO'
    elif 'OCEINTERCITES' in stop_upper or 'INTERCITES' in stop_upper:
        return 'Intercités'
    elif 'OCETER' in stop_upper:
        return 'TER'
    elif 'OCELO' in stop_upper:
        return 'Train de nuit'
    elif 'OCEEA' in stop_upper or 'EUROSTAR' in stop_upper or 'THALYS' in stop_upper:
        return 'Eurostar'
    elif 'OCEL' in stop_upper and 'LYRIA' in stop_upper:
        return 'Lyria'
    elif 'OCESA' in stop_upper:
        return 'Auto-train'
    elif 'OCENAVETTE' in stop_upper or 'NAVETTE' in stop_upper:
        return 'Navette'
    elif 'OCESN' in stop_upper:
        return 'TER'
    
    return 'Autre'


def extract_train_type(trip_id: str) -> str:
    """Extrait le type de train depuis le trip_id GTFS (fallback)."""
    trip_upper = trip_id.upper()
    
    if ':OUI:' in trip_upper:  # TGV InOui
        return 'TGV'
    elif 'OUIGO' in trip_upper:
        return 'OUIGO'
    elif 'INTERCITES' in trip_upper:
        return 'Intercités'
    
    for code, train_type in TRAIN_TYPE_MAPPING.items():
        if code.upper() in trip_upper:
            return train_type
    return 'Autre'


def parse_time_to_minutes(time_str: str) -> int:
    """Convertit HH:MM:SS en minutes depuis minuit."""
    parts = time_str.split(':')
    if len(parts) != 3:
        return 0
    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    return hours * 60 + minutes


def load_stations() -> dict:
    """Charge les données des gares avec leurs positions GPS.
    
    Indexe par TOUS les codes UIC pour capturer toutes les variantes
    (ex: Paris Montparnasse a 3 codes UIC différents).
    """
    print(f"Chargement des gares depuis {INPUT_GARES}...")
    with open(INPUT_GARES, 'r', encoding='utf-8') as f:
        gares = json.load(f)
    
    stations = {}
    for g in gares:
        station_info = {
            'nom': g['nom_gare'],
            'lat': g['position_geographique']['lat'],
            'lon': g['position_geographique']['lon'],
            'commune': g.get('ville', {}).get('nom_commune', ''),
            'id_commune': g.get('ville', {}).get('id_commune', ''),
            'primary_uic': str(g['uic'][0])  # Premier UIC comme référence
        }
        
        # Indexer par TOUS les codes UIC de la gare
        for uic in g['uic']:
            stations[str(uic)] = station_info
    
    print(f"  → {len(stations)} gares chargées")
    return stations


def process_stop_times(stations: dict) -> tuple[dict, dict]:
    """
    Parse le fichier stop_times.txt et extrait les connexions avec temps de trajet.
    
    Returns:
        Tuple (connections, train_types) où:
        - connections: {(uic_from, uic_to): [temps_trajet_1, temps_trajet_2, ...]}
        - train_types: {(uic_from, uic_to): {type: count, ...}}
    """
    print(f"\nAnalyse de {INPUT_STOP_TIMES}...")
    print("  (cela peut prendre 1-2 minutes pour 367k+ lignes)")
    
    # Structure: {(uic_from, uic_to): [temps_trajet_1, temps_trajet_2, ...]}
    connections = defaultdict(list)
    # Structure: {(uic_from, uic_to): {train_type: count, ...}}
    train_types = defaultdict(lambda: defaultdict(int))
    
    # Variables pour suivre le voyage en cours
    current_trip_id = None
    current_train_type = None
    current_trip_stops = []  # [(uic, departure_time_minutes, arrival_time_minutes, stop_sequence, train_type), ...]
    
    total_lines = 0
    valid_connections = 0
    
    with open(INPUT_STOP_TIMES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            total_lines += 1
            if total_lines % 100000 == 0:
                print(f"  ... {total_lines:,} lignes traitées")
            
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            arrival_time = row['arrival_time']
            departure_time = row['departure_time']
            stop_sequence = int(row['stop_sequence'])
            
            uic = extract_uic(stop_id)
            if not uic or uic not in stations:
                continue
            
            # Extraire le type de train depuis le stop_id
            train_type = extract_train_type_from_stop(stop_id)
            
            arrival_minutes = parse_time_to_minutes(arrival_time)
            departure_minutes = parse_time_to_minutes(departure_time)
            
            # Nouveau voyage ?
            if trip_id != current_trip_id:
                # Traiter le voyage précédent
                if current_trip_stops:
                    # Trier par stop_sequence (normalement déjà trié)
                    current_trip_stops.sort(key=lambda x: x[3])
                    
                    # Créer les connexions consécutives
                    for i in range(len(current_trip_stops) - 1):
                        uic_from = current_trip_stops[i][0]
                        departure_from = current_trip_stops[i][2]  # departure_time
                        segment_train_type = current_trip_stops[i][4]  # type de train
                        
                        uic_to = current_trip_stops[i + 1][0]
                        arrival_to = current_trip_stops[i + 1][1]  # arrival_time
                        
                        # Temps de trajet = arrivée à la prochaine gare - départ de la gare actuelle
                        travel_time = arrival_to - departure_from
                        
                        # Filtrer les valeurs aberrantes (négatif ou > 12h)
                        if 0 < travel_time <= 720:
                            connections[(uic_from, uic_to)].append(travel_time)
                            train_types[(uic_from, uic_to)][segment_train_type] += 1
                            valid_connections += 1
                
                # Réinitialiser pour le nouveau voyage
                current_trip_id = trip_id
                current_train_type = extract_train_type(trip_id)
                current_trip_stops = []
            
            # Ajouter l'arrêt au voyage courant (avec le type de train)
            current_trip_stops.append((uic, arrival_minutes, departure_minutes, stop_sequence, train_type))
    
    # Traiter le dernier voyage
    if current_trip_stops:
        current_trip_stops.sort(key=lambda x: x[3])
        for i in range(len(current_trip_stops) - 1):
            uic_from = current_trip_stops[i][0]
            departure_from = current_trip_stops[i][2]
            segment_train_type = current_trip_stops[i][4]
            uic_to = current_trip_stops[i + 1][0]
            arrival_to = current_trip_stops[i + 1][1]
            travel_time = arrival_to - departure_from
            if 0 < travel_time <= 720:
                connections[(uic_from, uic_to)].append(travel_time)
                train_types[(uic_from, uic_to)][segment_train_type] += 1
                valid_connections += 1
    
    print(f"\n  → {total_lines:,} lignes lues")
    print(f"  → {len(connections):,} connexions uniques trouvées")
    print(f"  → {valid_connections:,} observations de temps de trajet")
    
    return connections, train_types


def build_enhanced_graph(connections: dict, train_types: dict, stations: dict) -> dict:
    """
    Construit le graphe enrichi avec statistiques de temps de trajet et types de trains.
    """
    print("\nConstruction du graphe enrichi...")
    
    liaisons = []
    
    for (uic_from, uic_to), times in connections.items():
        if uic_from not in stations or uic_to not in stations:
            continue
        
        # Calculer les statistiques
        temps_moyen = round(sum(times) / len(times), 1)
        temps_min = min(times)
        temps_max = max(times)
        nb_trains = len(times)
        
        # Calculer la distance géographique
        station_from = stations[uic_from]
        station_to = stations[uic_to]
        distance = round(haversine(
            station_from['lat'], station_from['lon'],
            station_to['lat'], station_to['lon']
        ), 2)
        
        # Récupérer les types de trains pour cette liaison
        types_dict = train_types.get((uic_from, uic_to), {})
        # Trier par fréquence et trouver le type principal
        sorted_types = sorted(types_dict.items(), key=lambda x: -x[1])
        type_principal = sorted_types[0][0] if sorted_types else 'Autre'
        
        liaisons.append({
            "depart": uic_from,
            "arrivee": uic_to,
            "depart_nom": station_from['nom'],
            "arrivee_nom": station_to['nom'],
            "temps_moyen_min": temps_moyen,
            "temps_min_min": temps_min,
            "temps_max_min": temps_max,
            "nb_trains": nb_trains,
            "distance_km": distance,
            "type_train": type_principal,
            "types_details": dict(types_dict)
        })
    
    # Trier par nombre de trains (liaisons les plus fréquentes en premier)
    liaisons.sort(key=lambda x: -x['nb_trains'])
    
    # Collecter les gares uniques
    gares_uniques = set()
    for l in liaisons:
        gares_uniques.add(l['depart'])
        gares_uniques.add(l['arrivee'])
    
    # Statistiques globales
    temps_moyens = [l['temps_moyen_min'] for l in liaisons]
    
    result = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source_file": "stop_times.txt",
            "total_liaisons": len(liaisons),
            "unique_gares": len(gares_uniques),
            "stats": {
                "temps_trajet_moyen_global_min": round(sum(temps_moyens) / len(temps_moyens), 1) if temps_moyens else 0,
                "liaison_la_plus_frequente": liaisons[0] if liaisons else None,
                "total_trains_observes": sum(l['nb_trains'] for l in liaisons)
            }
        },
        "liaisons": liaisons
    }
    
    print(f"  → {len(liaisons)} liaisons avec temps de trajet")
    print(f"  → {len(gares_uniques)} gares uniques dans le graphe")
    
    return result


def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("GÉNÉRATION DU GRAPHE ENRICHI POUR PATHFINDING")
    print("=" * 60)
    
    # Vérifier les fichiers d'entrée
    if not os.path.exists(INPUT_STOP_TIMES):
        print(f"ERREUR: Fichier stop_times.txt non trouvé: {INPUT_STOP_TIMES}")
        return
    
    if not os.path.exists(INPUT_GARES):
        print(f"ERREUR: Fichier dataset_gares.json non trouvé: {INPUT_GARES}")
        return
    
    # Charger les gares
    stations = load_stations()
    
    # Traiter les horaires
    connections, train_types = process_stop_times(stations)
    
    # Construire le graphe enrichi
    graph = build_enhanced_graph(connections, train_types, stations)
    
    # Sauvegarder
    print(f"\nSauvegarde vers {OUTPUT_FILE}...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Terminé ! Fichier généré: {OUTPUT_FILE}")
    print("\n--- RÉSUMÉ ---")
    print(f"Liaisons totales: {graph['metadata']['total_liaisons']}")
    print(f"Gares uniques: {graph['metadata']['unique_gares']}")
    print(f"Temps de trajet moyen global: {graph['metadata']['stats']['temps_trajet_moyen_global_min']} min")
    
    if graph['metadata']['stats']['liaison_la_plus_frequente']:
        top = graph['metadata']['stats']['liaison_la_plus_frequente']
        print(f"Liaison la plus fréquente: {top['depart_nom']} → {top['arrivee_nom']} ({top['nb_trains']} trains)")


if __name__ == "__main__":
    main()
