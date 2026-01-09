"""
Script pour générer un dataset NLP avec annotations origine/destination.
"""
import json
from pathlib import Path
from typing import List, Dict
import random
from src.common.io import write_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.generate_nlp_dataset")

# Phrases avec origine et destination
COMPLETE_REQUESTS = [
    ("Je veux aller à Paris depuis Lyon", "Lyon", "Paris", True),
    ("Je souhaite voyager de Bordeaux à Toulouse", "Bordeaux", "Toulouse", True),
    ("Comment me rendre à Marseille depuis Lyon ?", "Lyon", "Marseille", True),
    ("Je voudrais un billet pour aller de Nice à Cannes", "Nice", "Cannes", True),
    ("Pouvez-vous me dire comment aller de Strasbourg à Nancy ?", "Strasbourg", "Nancy", True),
    ("Je dois me rendre à Lille en partant de Reims", "Reims", "Lille", True),
    ("Je cherche un trajet entre Nantes et Rennes", "Nantes", "Rennes", True),
    ("Comment faire pour aller de Montpellier à Perpignan ?", "Montpellier", "Perpignan", True),
    ("Je veux aller à Paris depuis Toulouse", "Toulouse", "Paris", True),
    ("Je souhaite me rendre à Marseille depuis Lyon", "Lyon", "Marseille", True),
    ("A quelle heure y a-t-il des trains vers Paris en partance de Toulouse ?", "Toulouse", "Paris", True),
    ("Je voudrais réserver un billet de train de Lyon à Paris", "Lyon", "Paris", True),
    ("Comment puis-je me rendre de Bordeaux à Marseille ?", "Bordeaux", "Marseille", True),
    ("Je dois aller à Nice, je pars de Marseille", "Marseille", "Nice", True),
    ("Je cherche un itinéraire entre Lyon et Paris", "Lyon", "Paris", True),
    ("Pouvez-vous m'indiquer comment aller de Paris à Lyon ?", "Paris", "Lyon", True),
    ("Je veux voyager de Toulouse à Bordeaux", "Toulouse", "Bordeaux", True),
    ("Je souhaite un trajet de Nantes à Rennes", "Nantes", "Rennes", True),
    ("Comment me rendre à Strasbourg depuis Nancy ?", "Nancy", "Strasbourg", True),
    ("Je voudrais aller de Lille à Paris", "Lille", "Paris", True),
]

# Demandes sans destination
NO_DEST_REQUESTS = [
    ("Je veux partir de Lyon", "Lyon", None, True),
    ("Comment partir de Paris ?", "Paris", None, True),
    ("Je dois quitter Marseille", "Marseille", None, True),
    ("Je souhaite partir de Bordeaux", "Bordeaux", None, True),
    ("Comment faire pour quitter Toulouse ?", "Toulouse", None, True),
]

# Demandes sans origine
NO_ORIGIN_REQUESTS = [
    ("Je veux aller à Paris", None, "Paris", True),
    ("Comment me rendre à Marseille ?", None, "Marseille", True),
    ("Je souhaite aller à Lyon", None, "Lyon", True),
    ("Je voudrais me rendre à Bordeaux", None, "Bordeaux", True),
    ("Comment aller à Toulouse ?", None, "Toulouse", True),
    ("Je dois aller à Nice", None, "Nice", True),
    ("Je cherche à aller à Strasbourg", None, "Strasbourg", True),
    ("Je veux me rendre à Lille", None, "Lille", True),
    ("Comment faire pour aller à Rennes ?", None, "Rennes", True),
    ("Je souhaite aller à Nancy", None, "Nancy", True),
]

# Phrases avec villes mais PAS des demandes de trajet
CITIES_NOT_TRAVEL = [
    ("Paris est la capitale de la France", None, None, False),
    ("J'ai visité Lyon l'année dernière", None, None, False),
    ("Marseille est une belle ville", None, None, False),
    ("Mon ami habite à Bordeaux", None, None, False),
    ("Toulouse est connue pour sa culture", None, None, False),
    ("J'adore Nice en été", None, None, False),
    ("Lyon est célèbre pour sa gastronomie", None, None, False),
    ("Paris est très touristique", None, None, False),
    ("Marseille a un beau port", None, None, False),
    ("Bordeaux produit du vin", None, None, False),
    ("Je connais quelqu'un qui habite à Toulouse", None, None, False),
    ("Paris est ma ville préférée", None, None, False),
    ("J'ai un rendez-vous à Paris demain", None, None, False),
    ("Mon cousin travaille à Lyon", None, None, False),
    ("J'ai passé mes vacances à Marseille", None, None, False),
]

# Phrases de la vie quotidienne (pas de trajet)
DAILY_LIFE = [
    ("Quel temps fait-il aujourd'hui ?", None, None, False),
    ("J'ai faim, on va manger ?", None, None, False),
    ("Quelle heure est-il ?", None, None, False),
    ("Comment allez-vous ?", None, None, False),
    ("Je suis fatigué", None, None, False),
    ("Il fait beau aujourd'hui", None, None, False),
    ("J'ai oublié mon parapluie", None, None, False),
    ("Combien ça coûte ?", None, None, False),
    ("Je ne comprends pas", None, None, False),
    ("Pouvez-vous répéter s'il vous plaît ?", None, None, False),
]

# Phrases avec variations (minuscules, accents, etc.)
VARIATIONS = [
    ("je veux aller à paris depuis lyon", "Lyon", "Paris", True),
    ("JE VEUX ALLER À PARIS DEPUIS LYON", "Lyon", "Paris", True),
    ("je veux aller a paris depuis lyon", "Lyon", "Paris", True),  # sans accents
    ("Avec mes amis florence et paris, je voudrais aller de paris a florence", "Paris", "Florence", True),
    ("je souhaite voyager de bordeaux à toulouse", "Bordeaux", "Toulouse", True),
]


def generate_dataset(
    output_dir: str | Path,
    num_samples: int = 500
) -> List[Dict]:
    """
    Génère un dataset NLP avec annotations.
    
    Args:
        output_dir: Dossier de sortie
        num_samples: Nombre d'échantillons
    
    Returns:
        Liste de dictionnaires représentant le dataset
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Combine toutes les catégories
    all_samples = []
    
    categories = [
        (COMPLETE_REQUESTS, 0.40),  # 40%
        (NO_DEST_REQUESTS, 0.10),   # 10%
        (NO_ORIGIN_REQUESTS, 0.20),  # 20%
        (CITIES_NOT_TRAVEL, 0.20),  # 20%
        (DAILY_LIFE, 0.05),          # 5%
        (VARIATIONS, 0.05),          # 5%
    ]
    
    # Construit la liste pondérée
    for samples, weight in categories:
        count = int(num_samples * weight)
        all_samples.extend(random.choices(samples, k=count))
    
    # Complète jusqu'à num_samples
    while len(all_samples) < num_samples:
        category = random.choice(categories)
        all_samples.append(random.choice(category[0]))
    
    # Mélange
    random.shuffle(all_samples)
    
    # Génère le dataset
    dataset = []
    for i, (sentence, origin, destination, is_valid) in enumerate(all_samples[:num_samples], 1):
        sample_id = f"nlp_{i:06d}"
        
        dataset.append({
            "id": sample_id,
            "sentence": sentence,
            "origin": origin,
            "destination": destination,
            "is_valid": is_valid
        })
    
    return dataset


def split_dataset(dataset: List[Dict], train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    """Divise le dataset en train/valid/test."""
    random.shuffle(dataset)
    
    n_total = len(dataset)
    n_train = int(n_total * train_ratio)
    n_valid = int(n_total * valid_ratio)
    
    train = dataset[:n_train]
    valid = dataset[n_train:n_train + n_valid]
    test = dataset[n_train + n_valid:]
    
    return train, valid, test


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate NLP dataset")
    parser.add_argument("--output-dir", default="data/splits", help="Output directory")
    parser.add_argument("--num-samples", type=int, default=500, help="Number of samples")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    logger.info(f"Generating {args.num_samples} NLP samples...")
    
    # Génère le dataset
    dataset = generate_dataset(args.output_dir, num_samples=args.num_samples)
    
    # Divise en train/valid/test
    train, valid, test = split_dataset(dataset)
    
    logger.info(f"Split: train={len(train)}, valid={len(valid)}, test={len(test)}")
    
    # Sauvegarde
    output_dir = Path(args.output_dir)
    write_jsonl(output_dir / "train" / "train_nlp.jsonl", train)
    write_jsonl(output_dir / "valid" / "valid_nlp.jsonl", valid)
    write_jsonl(output_dir / "test" / "test_nlp.jsonl", test)
    
    # Sauvegarde aussi un fichier complet
    write_jsonl(output_dir / "full_nlp_dataset.jsonl", dataset)
    
    logger.info(f"Dataset saved to {output_dir}")


if __name__ == "__main__":
    main()

