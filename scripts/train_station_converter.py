import pandas as pd
import json
import os

# 1. On localise le dossier où se trouve le script (scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. On définit les chemins en remontant d'un cran (..) pour trouver "data"
# Cela permet d'accéder à data/ depuis scripts/
input_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'dataset_gares.csv'))
output_folder = os.path.abspath(os.path.join(script_dir, '..', 'data', 'train_station'))
output_file = os.path.join(output_folder, 'dataset_gares.json')

def convert_csv_to_json():
    # Création du dossier de destination s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Dossier créé : {output_folder}")

    try:
        # Lecture du CSV
        df = pd.read_csv(input_path, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier est introuvable au chemin : {input_path}")
        return

    json_result = []

    for _, row in df.iterrows():
        # Traitement des UIC séparés par un point-virgule
        uic_raw = str(row['id_gare'])
        if uic_raw and uic_raw != 'nan':
            uic_list = [u.strip() for u in uic_raw.split(';')]
        else:
            uic_list = []

        station_data = {
            "uic": uic_list,
            "nom_gare": row['nom_gare'],
            "trigramme": row['trigramme'],
            "position_geographique": {
                "lat": float(str(row['lat']).replace(',', '.')),
                "lon": float(str(row['lon']).replace(',', '.'))
            },
            "ville": {
                "id_commune": str(row['id_commune']),
                "nom_commune": row['nom_commune']
            }
        }
        json_result.append(station_data)

    # Sauvegarde du JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Conversion réussie !")
    print(f"Fichier créé : {output_file}")

if __name__ == "__main__":
    convert_csv_to_json()