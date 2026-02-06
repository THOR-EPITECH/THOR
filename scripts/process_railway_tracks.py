"""
Script pour traiter les données des voies ferroviaires et créer un mapping
utilisable pour afficher les tracés précis sur la carte.

Utilise le fichier : fichier-de-formes-des-voies-du-reseau-ferre-national.json
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


def load_railway_tracks(input_file: Path) -> List[Dict]:
    """Charge les données des voies ferroviaires."""
    print(f"📂 Chargement de {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        tracks = json.load(f)
    print(f"✅ {len(tracks)} voies chargées")
    return tracks


def group_tracks_by_line(tracks: List[Dict]) -> Dict[str, List[Dict]]:
    """Groupe les voies par code de ligne."""
    print("\n📊 Groupement par ligne...")
    by_line = defaultdict(list)
    
    for track in tracks:
        code_ligne = track.get('code_ligne')
        if code_ligne and track.get('geo_shape'):
            by_line[code_ligne].append(track)
    
    print(f"✅ {len(by_line)} lignes identifiées")
    return dict(by_line)


def extract_main_tracks(tracks_by_line: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """Extrait les voies principales (VPA) pour chaque ligne."""
    print("\n🚄 Extraction des voies principales...")
    
    main_tracks = {}
    
    for code_ligne, tracks in tracks_by_line.items():
        vpa_tracks = [t for t in tracks if t.get('type_voie') == 'VPA']
        
        if not vpa_tracks:
            vpa_tracks = tracks
        
        def parse_pk(pk_str: str) -> float:
            """Parse PK format: 000+047 ou 000-047 -> 0.047"""
            try:
                pk_str = pk_str.replace('+', '.').replace('-', '.')
                return float(pk_str)
            except:
                return 0.0
        
        vpa_tracks.sort(key=lambda t: parse_pk(t.get('pk_debut_r', '0+0')))
        
        all_coords = []
        for track in vpa_tracks:
            geo = track.get('geo_shape', {}).get('geometry', {})
            coords = geo.get('coordinates', [])
            if coords:
                all_coords.extend(coords)
        
        if all_coords:
            main_tracks[code_ligne] = {
                'code_ligne': code_ligne,
                'num_segments': len(vpa_tracks),
                'geometry': {
                    'type': 'LineString',
                    'coordinates': all_coords
                },
                'metadata': {
                    'ligne': tracks[0].get('ligne', ''),
                    'pk_debut': vpa_tracks[0].get('pk_debut_r', ''),
                    'pk_fin': vpa_tracks[-1].get('pk_fin_r', ''),
                    'num_tracks': len(tracks),
                    'num_vpa': len(vpa_tracks)
                }
            }
    
    print(f"✅ {len(main_tracks)} lignes principales extraites")
    return main_tracks


def create_station_to_lines_mapping(gares_file: Path) -> Dict[str, List[str]]:
    """Crée un mapping UIC gare -> codes ligne."""
    print("\n🚉 Création du mapping gares -> lignes...")
    
    if not gares_file.exists():
        print("⚠️  Fichier gares non trouvé, skip mapping")
        return {}
    
    gares = json.load(open(gares_file, 'r', encoding='utf-8'))
    
    mapping = defaultdict(list)
    
    print(f"✅ Mapping créé pour {len(gares)} gares")
    return dict(mapping)


def save_processed_data(
    main_tracks: Dict[str, Dict],
    output_file: Path
):
    """Sauvegarde les données traitées."""
    print(f"\n💾 Sauvegarde dans {output_file}...")
    
    output_data = {
        'metadata': {
            'source': 'SNCF Open Data - Formes des voies du RFN',
            'num_lines': len(main_tracks),
            'total_coordinates': sum(
                len(t['geometry']['coordinates']) 
                for t in main_tracks.values()
            )
        },
        'lines': main_tracks
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"✅ Fichier créé : {size_mb:.2f} MB")


def create_simplified_version(
    main_tracks: Dict[str, Dict],
    output_file: Path,
    simplification_factor: int = 5
):
    """Crée une version simplifiée pour le web (moins de points)."""
    print(f"\n🔧 Création version simplifiée (facteur {simplification_factor})...")
    
    simplified = {}
    
    for code, track in main_tracks.items():
        coords = track['geometry']['coordinates']
        simplified_coords = coords[::simplification_factor]
        
        if coords[-1] not in simplified_coords:
            simplified_coords.append(coords[-1])
        
        simplified[code] = {
            **track,
            'geometry': {
                'type': 'LineString',
                'coordinates': simplified_coords
            }
        }
    
    output_data = {
        'metadata': {
            'source': 'SNCF Open Data - Formes des voies du RFN (simplifié)',
            'num_lines': len(simplified),
            'simplification_factor': simplification_factor
        },
        'lines': simplified
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False)
    
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"✅ Version simplifiée créée : {size_mb:.2f} MB")


def main():
    """Traite les données des voies ferroviaires."""
    print("=" * 70)
    print("🚄 TRAITEMENT DES VOIES FERROVIAIRES")
    print("=" * 70)
    
    input_file = Path('data/raw/fichier-de-formes-des-voies-du-reseau-ferre-national(1).json')
    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    
    output_full = output_dir / 'railway_tracks_full.json'
    output_simplified = output_dir / 'railway_tracks_simplified.json'
    gares_file = Path('data/train_station/dataset_gares.json')
    
    tracks = load_railway_tracks(input_file)
    
    tracks_by_line = group_tracks_by_line(tracks)
    
    main_tracks = extract_main_tracks(tracks_by_line)
    
    save_processed_data(main_tracks, output_full)
    
    create_simplified_version(main_tracks, output_simplified, simplification_factor=3)
    
    print("\n" + "=" * 70)
    print("✅ TRAITEMENT TERMINÉ")
    print("=" * 70)
    print(f"\n📁 Fichiers créés:")
    print(f"  - {output_full}")
    print(f"  - {output_simplified}")
    print(f"\n💡 Utilise le fichier simplifié pour le web (plus léger)")


if __name__ == "__main__":
    main()
