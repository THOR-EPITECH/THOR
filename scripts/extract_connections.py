import pandas as pd
import json
import os
import re

# Chemins selon ton arborescence
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'stop_times.txt'))
output_folder = os.path.abspath(os.path.join(script_dir, '..', 'data', 'train_station'))
output_file = os.path.join(output_folder, 'dataset_liaisons.json')

def clean_uic(stop_id):
    """Extrait le code UIC (8 chiffres) du stop_id."""
    match = re.search(r'(\d{8})', str(stop_id))
    return match.group(1) if match else None

def generate_liaisons():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Analyse du fichier stop_times.txt... (cela peut prendre 1 à 2 minutes)")
    
    # Lecture optimisée (par morceaux)
    reader = pd.read_csv(input_file, usecols=['trip_id', 'stop_id', 'stop_sequence'], chunksize=500000)
    
    liaisons_set = set()
    last_trip_id = None
    last_uic = None

    for chunk in reader:
        for _, row in chunk.iterrows():
            current_trip_id = row['trip_id']
            current_uic = clean_uic(row['stop_id'])
            
            if not current_uic:
                continue

            # Si on est dans le même train que la ligne précédente
            if current_trip_id == last_trip_id and last_uic is not None:
                if last_uic != current_uic:
                    # On ajoute les deux sens pour le pathfinding
                    liaisons_set.add((last_uic, current_uic))
                    liaisons_set.add((current_uic, last_uic))
            
            last_trip_id = current_trip_id
            last_uic = current_uic

    # Transformation en format JSON propre
    # On utilise "source" et "target" (noms standards en théorie des graphes)
    result = []
    for uic_a, uic_b in liaisons_set:
        result.append({
            "depart": uic_a,
            "arrivee": uic_b
        })

    print(f"Sauvegarde de {len(result)} arcs (liaisons orientées)...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"Terminé ! Fichier : {output_file}")

if __name__ == "__main__":
    generate_liaisons()