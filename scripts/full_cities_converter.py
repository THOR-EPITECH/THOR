import pandas as pd
import json
import os

# Chemins selon ton arborescence
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'full_cities.csv'))
output_folder = os.path.abspath(os.path.join(script_dir, '..', 'data', 'train_station'))
output_file = os.path.join(output_folder, 'dataset_villes.json')

def convert_cities():
    # Création du dossier de destination s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Reading {input_file}...")

    # Lecture du CSV
    try:
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    except Exception:
        # Test de secours avec la virgule si le point-virgule échoue
        df = pd.read_csv(input_file, sep=',', encoding='utf-8')

    json_result = []

    for _, row in df.iterrows():
        # Construction de l'objet ville
        ville_data = {
            "id_commune": str(row['id_commune']),
            "nom_commune": row['nom_commune'],
            "position_geographique": {
                # Gestion des virgules éventuelles pour les nombres décimaux
                "lat": float(str(row['lat']).replace(',', '.')),
                "lon": float(str(row['lon']).replace(',', '.'))
            }
        }
        json_result.append(ville_data)

    # Sauvegarde en JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)
    
    print(f"Conversion terminée !")
    print(f"Fichier créé : {output_file} ({len(json_result)} villes)")

if __name__ == "__main__":
    convert_cities()