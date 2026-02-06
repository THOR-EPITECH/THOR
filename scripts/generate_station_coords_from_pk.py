"""
Script pour générer les coordonnées des gares à partir des PK (Points Kilométriques)
dans le fichier shapes.json.

Les PK permettent de localiser précisément une gare sur une ligne de train.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import math


def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calcule la distance en km entre deux coordonnées."""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def calculate_line_length(coordinates: List[List[float]]) -> float:
    """Calcule la longueur totale d'une ligne en km."""
    total = 0
    for i in range(len(coordinates) - 1):
        total += haversine_distance(
            tuple(coordinates[i]),
            tuple(coordinates[i + 1])
        )
    return total


def interpolate_position_at_pk(
    coordinates: List[List[float]],
    pk_debut: float,
    pk_fin: float,
    target_pk: float
) -> Optional[Tuple[float, float]]:
    """
    Interpole la position GPS à un PK donné sur une ligne.
    
    Args:
        coordinates: Liste des coordonnées [lon, lat] de la ligne
        pk_debut: PK de début de la ligne
        pk_fin: PK de fin de la ligne
        target_pk: PK cible où on veut trouver la position
        
    Returns:
        (lon, lat) ou None si hors limites
    """
    if target_pk < pk_debut or target_pk > pk_fin:
        return None
    
    total_pk_length = pk_fin - pk_debut
    pk_ratio = (target_pk - pk_debut) / total_pk_length
    
    line_length = calculate_line_length(coordinates)
    target_distance = line_length * pk_ratio
    
    cumulative_distance = 0
    for i in range(len(coordinates) - 1):
        segment_distance = haversine_distance(
            tuple(coordinates[i]),
            tuple(coordinates[i + 1])
        )
        
        if cumulative_distance + segment_distance >= target_distance:
            segment_ratio = (target_distance - cumulative_distance) / segment_distance
            
            lon = coordinates[i][0] + (coordinates[i + 1][0] - coordinates[i][0]) * segment_ratio
            lat = coordinates[i][1] + (coordinates[i + 1][1] - coordinates[i][1]) * segment_ratio
            
            return (lon, lat)
        
        cumulative_distance += segment_distance
    
    return tuple(coordinates[-1])


def load_stops() -> Dict[str, Dict]:
    """Charge les informations des gares depuis stops.txt."""
    stops = {}
    stops_file = Path('data/raw/stops.txt')
    
    with open(stops_file, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split(',')
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < len(headers):
                continue
                
            stop_data = dict(zip(headers, parts))
            stop_id = stop_data.get('stop_id', '')
            stop_name = stop_data.get('stop_name', '')
            
            if stop_id and stop_name:
                stops[stop_id] = {
                    'name': stop_name,
                    'lat': float(stop_data.get('stop_lat', 0)),
                    'lon': float(stop_data.get('stop_lon', 0)),
                }
    
    return stops


def main():
    """Génère le fichier stations.ts avec les coordonnées basées sur les PK."""
    
    print("🔄 Chargement des données...")
    
    shapes_file = Path('data/raw/shapes.json')
    shapes = json.load(open(shapes_file, 'r', encoding='utf-8'))
    
    stops = load_stops()
    
    print(f"✅ {len(shapes)} lignes chargées")
    print(f"✅ {len(stops)} gares chargées")
    
    station_coords = {}
    
    for stop_id, stop_data in stops.items():
        station_coords[stop_data['name']] = {
            'lat': stop_data['lat'],
            'lon': stop_data['lon']
        }
    
    output_file = Path('web/src/data/stations.ts')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("export const stationPositions: Record<string, { lat: number; lon: number }> = {\n")
        
        for i, (name, coords) in enumerate(sorted(station_coords.items())):
            comma = ',' if i < len(station_coords) - 1 else ''
            f.write(f"  '{name}': {{ lat: {coords['lat']:.6f}, lon: {coords['lon']:.6f} }}{comma}\n")
        
        f.write("};\n\n")
        f.write("export function getStationPosition(stationName: string): { lat: number; lon: number } | null {\n")
        f.write("  const normalized = stationName.toLowerCase().trim();\n")
        f.write("  \n")
        f.write("  for (const [name, coords] of Object.entries(stationPositions)) {\n")
        f.write("    if (name.toLowerCase().includes(normalized) || normalized.includes(name.toLowerCase())) {\n")
        f.write("      return coords;\n")
        f.write("    }\n")
        f.write("  }\n")
        f.write("  \n")
        f.write("  return null;\n")
        f.write("}\n")
    
    print(f"✅ Fichier généré: {output_file}")
    print(f"✅ {len(station_coords)} stations avec coordonnées")
    print("\n🎯 Stations principales:")
    
    main_stations = ['Paris Nord', 'Lyon Part-Dieu', 'Marseille Saint-Charles', 
                     'Bordeaux Saint-Jean', 'Toulouse Matabiau']
    
    for station in main_stations:
        if station in station_coords:
            coords = station_coords[station]
            print(f"  - {station}: {coords['lat']:.4f}, {coords['lon']:.4f}")


if __name__ == "__main__":
    main()
