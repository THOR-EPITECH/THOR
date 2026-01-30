#!/usr/bin/env python3
"""
Script pour extraire les tracés géométriques des voies ferrées.

Version 4: Utilise le nouveau fichier shapes.json complet avec lignes nommées.
"""

import json
import math
from pathlib import Path
from collections import defaultdict
from typing import Optional

# Chemins des fichiers
BASE_DIR = Path(__file__).parent.parent
INPUT_SHAPES = BASE_DIR / "data/raw/shapes.json"
INPUT_LIAISONS = BASE_DIR / "data/train_station/dataset_liaisons_enhanced.json"
INPUT_GARES = BASE_DIR / "data/train_station/dataset_gares.json"
OUTPUT_FILE = BASE_DIR / "data/train_station/dataset_liaisons_with_shapes.json"


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calcule la distance en km entre deux points GPS."""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_railway_lines(shapes_file: Path) -> dict:
    """
    Charge les lignes ferroviaires depuis shapes.json.
    
    Returns:
        Dict[code_ligne] -> {
            'nom': str,
            'troncons': [(pk_debut, pk_fin, coordinates), ...]
        }
    """
    print(f"  Chargement de {shapes_file}...")
    with open(shapes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lines = defaultdict(lambda: {'nom': '', 'troncons': []})
    
    for item in data:
        code = item.get('codeLigne')
        if not code:
            continue
        
        nom = item.get('nomLigne', '')
        geom = item.get('geometry')
        if not geom:
            continue
        
        coords = geom.get('coordinates', [])
        if not coords:
            continue
        
        pk_debut = item.get('pkDebut', 0)
        pk_fin = item.get('pkFin', 0)
        
        if not lines[code]['nom']:
            lines[code]['nom'] = nom
        
        lines[code]['troncons'].append({
            'pk_debut': pk_debut,
            'pk_fin': pk_fin,
            'coordinates': coords
        })
    
    # Trier les tronçons par PK pour chaque ligne
    for code in lines:
        lines[code]['troncons'].sort(key=lambda x: x['pk_debut'])
    
    print(f"    → {len(lines)} lignes chargées")
    return dict(lines)


def get_full_line_coordinates(line_data: dict) -> list:
    """Récupère toutes les coordonnées d'une ligne, ordonnées et aplaties."""
    all_coords = []
    for troncon in line_data['troncons']:
        coords = flatten_coordinates(troncon['coordinates'])
        all_coords.extend(coords)
    return all_coords


def flatten_coordinates(coords: list) -> list:
    """Aplatit les coordonnées si elles sont imbriquées."""
    if not coords:
        return []
    
    # Vérifier si c'est déjà [lon, lat] ou [[lon, lat], ...]
    first = coords[0]
    if isinstance(first, (int, float)):
        # C'est un seul point [lon, lat]
        return [coords]
    elif isinstance(first, list):
        if len(first) > 0 and isinstance(first[0], (int, float)):
            # C'est déjà [[lon, lat], ...]
            return coords
        else:
            # C'est imbriqué [[[lon, lat], ...], ...]
            flat = []
            for sublist in coords:
                if isinstance(sublist, list):
                    flat.extend(flatten_coordinates(sublist))
            return flat
    return coords


def find_closest_point_index(coords: list, lon: float, lat: float) -> tuple[int, float]:
    """Trouve l'index du point le plus proche et sa distance."""
    min_dist = float('inf')
    min_idx = 0
    
    for i, coord in enumerate(coords):
        # S'assurer que coord est [lon, lat]
        if not isinstance(coord, list) or len(coord) < 2:
            continue
        if isinstance(coord[0], list):
            continue  # Skip si encore imbriqué
        
        try:
            dist = haversine(lon, lat, float(coord[0]), float(coord[1]))
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        except (TypeError, ValueError):
            continue
    
    return min_idx, min_dist


def extract_segment_from_line(
    coords: list,
    start_lon: float, start_lat: float,
    end_lon: float, end_lat: float,
    max_dist: float = 5.0
) -> Optional[list]:
    """
    Extrait un segment entre deux points sur une ligne.
    
    Returns:
        Liste de coordonnées ou None si les points sont trop loin
    """
    start_idx, start_dist = find_closest_point_index(coords, start_lon, start_lat)
    end_idx, end_dist = find_closest_point_index(coords, end_lon, end_lat)
    
    if start_dist > max_dist or end_dist > max_dist:
        return None
    
    # S'assurer que start < end
    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx
    
    # Extraire le segment
    segment = coords[start_idx:end_idx + 1]
    
    return segment if len(segment) > 1 else None


def find_best_line_for_liaison(
    lines: dict,
    start_lon: float, start_lat: float,
    end_lon: float, end_lat: float,
    max_search_dist: float = 10.0
) -> Optional[tuple[str, list]]:
    """
    Trouve la meilleure ligne pour une liaison.
    
    Returns:
        (code_ligne, coordinates) ou None
    """
    best_line = None
    best_segment = None
    best_score = float('inf')
    
    for code, line_data in lines.items():
        coords = get_full_line_coordinates(line_data)
        if len(coords) < 2:
            continue
        
        # Trouver les points les plus proches
        start_idx, start_dist = find_closest_point_index(coords, start_lon, start_lat)
        end_idx, end_dist = find_closest_point_index(coords, end_lon, end_lat)
        
        # Vérifier si les deux points sont proches de la ligne
        if start_dist > max_search_dist or end_dist > max_search_dist:
            continue
        
        # Score = somme des distances + pénalité si segment court
        score = start_dist + end_dist
        
        # S'assurer que le segment couvre une distance significative
        if abs(start_idx - end_idx) < 2:
            continue
        
        if score < best_score:
            # Extraire le segment
            if start_idx > end_idx:
                start_idx, end_idx = end_idx, start_idx
            segment = coords[start_idx:end_idx + 1]
            
            if len(segment) > 5:
                best_score = score
                best_line = code
                best_segment = segment
    
    return (best_line, best_segment) if best_segment else None


def simplify_path(points: list, max_points: int = 300) -> list:
    """Simplifie un chemin en gardant max_points points."""
    if len(points) <= max_points:
        return points
    
    step = len(points) / (max_points - 1)
    indices = [int(i * step) for i in range(max_points - 1)] + [len(points) - 1]
    return [points[i] for i in indices]


def main():
    print("=" * 70)
    print("GÉNÉRATION DES TRACÉS GÉOMÉTRIQUES V4")
    print("Utilisation du fichier shapes.json complet")
    print("=" * 70)
    
    # Charger les lignes ferroviaires
    print(f"\n1. Chargement des lignes ferroviaires...")
    lines = load_railway_lines(INPUT_SHAPES)
    
    total_points = sum(
        sum(len(t['coordinates']) for t in l['troncons'])
        for l in lines.values()
    )
    print(f"    → {total_points:,} points géométriques")
    
    # Charger les liaisons
    print(f"\n2. Chargement des liaisons...")
    with open(INPUT_LIAISONS, 'r', encoding='utf-8') as f:
        liaisons_data = json.load(f)
    liaisons = liaisons_data.get('liaisons', liaisons_data)
    print(f"    → {len(liaisons)} liaisons")
    
    # Charger les gares
    print(f"\n3. Chargement des gares...")
    with open(INPUT_GARES, 'r', encoding='utf-8') as f:
        gares = json.load(f)
    
    gares_by_uic = {}
    for g in gares:
        for uic in g['uic']:
            gares_by_uic[str(uic)] = {
                'nom': g['nom_gare'],
                'lat': g['position_geographique']['lat'],
                'lon': g['position_geographique']['lon']
            }
    print(f"    → {len(gares_by_uic)} codes UIC")
    
    # Traiter les liaisons
    print(f"\n4. Recherche des tracés pour chaque liaison...")
    
    enriched_liaisons = []
    stats = {'with_path': 0, 'direct_line': 0, 'no_gare': 0}
    
    total = len(liaisons)
    for i, liaison in enumerate(liaisons):
        if i % 100 == 0 or i == total - 1:
            pct = (i + 1) / total * 100
            print(f"\r    [{pct:5.1f}%] {i+1}/{total} - {stats['with_path']} tracés trouvés", end="", flush=True)
        
        uic_dep = str(liaison['depart'])
        uic_arr = str(liaison['arrivee'])
        
        gare_dep = gares_by_uic.get(uic_dep)
        gare_arr = gares_by_uic.get(uic_arr)
        
        if not gare_dep or not gare_arr:
            stats['no_gare'] += 1
            enriched_liaisons.append(liaison)
            continue
        
        # Chercher la meilleure ligne
        result = find_best_line_for_liaison(
            lines,
            gare_dep['lon'], gare_dep['lat'],
            gare_arr['lon'], gare_arr['lat'],
            max_search_dist=8.0
        )
        
        if result:
            code_ligne, segment = result
            
            # Ajouter les points de départ et d'arrivée
            segment = [[gare_dep['lon'], gare_dep['lat']]] + segment + [[gare_arr['lon'], gare_arr['lat']]]
            
            # Simplifier si nécessaire
            segment = simplify_path(segment, max_points=300)
            
            liaison_copy = liaison.copy()
            liaison_copy['geometry'] = {
                'type': 'LineString',
                'coordinates': segment
            }
            liaison_copy['ligne_code'] = code_ligne
            liaison_copy['ligne_nom'] = lines[code_ligne]['nom']
            enriched_liaisons.append(liaison_copy)
            stats['with_path'] += 1
        else:
            # Fallback: ligne droite
            liaison_copy = liaison.copy()
            liaison_copy['geometry'] = {
                'type': 'LineString',
                'coordinates': [
                    [gare_dep['lon'], gare_dep['lat']],
                    [gare_arr['lon'], gare_arr['lat']]
                ]
            }
            enriched_liaisons.append(liaison_copy)
            stats['direct_line'] += 1
    
    print()  # Nouvelle ligne après la barre de progression
    
    print(f"\n    Résultats:")
    print(f"    ✓ {stats['with_path']} liaisons avec tracé détaillé")
    print(f"    → {stats['direct_line']} liaisons avec ligne droite")
    print(f"    ✗ {stats['no_gare']} liaisons sans gare trouvée")
    
    # Sauvegarder
    print(f"\n5. Sauvegarde...")
    output_data = {
        'metadata': {
            'source': 'SNCF Open Data - shapes.json',
            'liaisons_count': len(enriched_liaisons),
            'liaisons_with_shapes': stats['with_path']
        },
        'liaisons': enriched_liaisons
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False)
    
    print(f"\n✅ Terminé ! Fichier: {OUTPUT_FILE}")
    
    # Afficher quelques exemples
    print(f"\n📊 Exemples de tracés détaillés:")
    examples = sorted(
        [l for l in enriched_liaisons if l.get('geometry', {}).get('coordinates', []) and len(l['geometry']['coordinates']) > 20],
        key=lambda x: -len(x['geometry']['coordinates'])
    )[:15]
    
    for l in examples:
        coords = l['geometry']['coordinates']
        ligne = l.get('ligne_nom', '')[:40]
        print(f"    {l.get('depart_nom', '?')[:25]:25} → {l.get('arrivee_nom', '?')[:25]:25}: {len(coords):4} pts | {ligne}")


if __name__ == '__main__':
    main()
