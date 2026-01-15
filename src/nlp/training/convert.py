"""
Conversion de datasets JSONL vers format spaCy pour l'entraînement.
"""
from pathlib import Path
from typing import List, Dict, Tuple
from src.common.io import read_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="nlp.training")


def find_city_in_text(text: str, city: str) -> List[Tuple[int, int]]:
    """
    Trouve toutes les occurrences d'une ville dans le texte.
    
    Args:
        text: Texte à analyser
        city: Nom de la ville à chercher
    
    Returns:
        Liste de tuples (start, end) pour chaque occurrence
    """
    if not city:
        return []
    
    positions = []
    text_lower = text.lower()
    city_lower = city.lower()
    
    start = 0
    while True:
        pos = text_lower.find(city_lower, start)
        if pos == -1:
            break
        positions.append((pos, pos + len(city)))
        start = pos + 1
    
    return positions


def convert_to_spacy_format(
    dataset_path: str | Path,
    output_path: str | Path = None
) -> List[Tuple[str, Dict]]:
    """
    Convertit un dataset JSONL en format spaCy pour l'entraînement.
    
    Format spaCy attendu:
    [
        ("Je veux aller à Paris depuis Lyon", {
            "entities": [(start, end, "LABEL"), ...]
        }),
        ...
    ]
    
    Args:
        dataset_path: Chemin vers le fichier JSONL
        output_path: Chemin de sortie (optionnel, pour sauvegarder)
    
    Returns:
        Liste de tuples (text, annotations) au format spaCy
    """
    dataset_path = Path(dataset_path)
    training_data = []
    
    logger.info(f"Converting {dataset_path} to spaCy format...")
    
    for item in read_jsonl(dataset_path):
        text = item.get("sentence", item.get("transcript", ""))
        origin = item.get("origin")
        destination = item.get("destination")
        
        if not text:
            continue
        
        entities = []
        
        # Trouve les positions de l'origine
        if origin:
            origin_positions = find_city_in_text(text, origin)
            for start, end in origin_positions:
                entities.append((start, end, "ORIGIN"))
        
        # Trouve les positions de la destination
        if destination:
            dest_positions = find_city_in_text(text, destination)
            for start, end in dest_positions:
                # Évite les doublons si origine et destination sont la même ville
                if not any(start == orig_start and end == orig_end 
                          for orig_start, orig_end, _ in entities):
                    entities.append((start, end, "DESTINATION"))
        
        # Trie les entités par position (spaCy le requiert)
        entities.sort(key=lambda x: x[0])
        
        # Vérifie qu'il n'y a pas de chevauchement
        valid_entities = []
        for i, (start, end, label) in enumerate(entities):
            # Vérifie les chevauchements avec les entités précédentes
            overlaps = False
            for prev_start, prev_end, _ in valid_entities:
                if not (end <= prev_start or start >= prev_end):
                    overlaps = True
                    break
            
            if not overlaps:
                valid_entities.append((start, end, label))
        
        if valid_entities:
            training_data.append((text, {"entities": valid_entities}))
        else:
            # Si pas d'entités, on ajoute quand même pour l'entraînement négatif
            training_data.append((text, {"entities": []}))
    
    logger.info(f"Converted {len(training_data)} samples")
    
    # Sauvegarde si demandé
    if output_path:
        import json
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved to {output_path}")
    
    return training_data


