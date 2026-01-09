"""
Script pour générer un dataset STT avec une grande variété de phrases.
"""
import json
import random
from pathlib import Path
from typing import List, Dict
from src.common.io import write_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.generate_stt_dataset")

# Phrases de demande de trajet (complètes)
TRAVEL_REQUESTS_COMPLETE = [
    "Je veux aller à Paris depuis Lyon",
    "Comment me rendre à Marseille ?",
    "Je souhaite voyager de Bordeaux à Toulouse",
    "Je voudrais un billet pour aller de Nice à Cannes",
    "Pouvez-vous me dire comment aller de Strasbourg à Nancy ?",
    "Je dois me rendre à Lille en partant de Reims",
    "Je cherche un trajet entre Nantes et Rennes",
    "Comment faire pour aller de Montpellier à Perpignan ?",
    "Je veux aller à Paris depuis Toulouse",
    "Je souhaite me rendre à Marseille depuis Lyon",
    "A quelle heure y a-t-il des trains vers Paris en partance de Toulouse ?",
    "Je voudrais réserver un billet de train de Lyon à Paris",
    "Comment puis-je me rendre de Bordeaux à Marseille ?",
    "Je dois aller à Nice, je pars de Marseille",
    "Je cherche un itinéraire entre Lyon et Paris",
    "Pouvez-vous m'indiquer comment aller de Paris à Lyon ?",
    "Je veux voyager de Toulouse à Bordeaux",
    "Je souhaite un trajet de Nantes à Rennes",
    "Comment me rendre à Strasbourg depuis Nancy ?",
    "Je voudrais aller de Lille à Paris",
]

# Demandes de trajet sans destination
TRAVEL_REQUESTS_NO_DEST = [
    "Je veux partir de Lyon",
    "Comment partir de Paris ?",
    "Je dois quitter Marseille",
    "Je souhaite partir de Bordeaux",
    "Comment faire pour quitter Toulouse ?",
    "Je veux partir de Nice",
    "Je dois quitter Nantes",
]

# Demandes de trajet sans origine
TRAVEL_REQUESTS_NO_ORIGIN = [
    "Je veux aller à Paris",
    "Comment me rendre à Marseille ?",
    "Je souhaite aller à Lyon",
    "Je voudrais me rendre à Bordeaux",
    "Comment aller à Toulouse ?",
    "Je dois aller à Nice",
    "Je cherche à aller à Strasbourg",
    "Je veux me rendre à Lille",
    "Comment faire pour aller à Rennes ?",
    "Je souhaite aller à Nancy",
]

# Phrases avec noms de villes mais PAS des demandes de trajet
CITIES_NOT_TRAVEL = [
    "Paris est la capitale de la France",
    "J'ai visité Lyon l'année dernière",
    "Marseille est une belle ville",
    "Mon ami habite à Bordeaux",
    "Toulouse est connue pour sa culture",
    "J'adore Nice en été",
    "Lyon est célèbre pour sa gastronomie",
    "Paris est très touristique",
    "Marseille a un beau port",
    "Bordeaux produit du vin",
    "Je connais quelqu'un qui habite à Toulouse",
    "Paris est ma ville préférée",
    "Lyon est située dans le sud-est",
    "Marseille est la deuxième ville de France",
    "Bordeaux est dans le sud-ouest",
    "Toulouse est la ville rose",
    "Nice est sur la Côte d'Azur",
    "J'ai un rendez-vous à Paris demain",
    "Mon cousin travaille à Lyon",
    "J'ai passé mes vacances à Marseille",
]

# Phrases de la vie de tous les jours
DAILY_LIFE = [
    "Quel temps fait-il aujourd'hui ?",
    "J'ai faim, on va manger ?",
    "Quelle heure est-il ?",
    "Comment allez-vous ?",
    "Je suis fatigué",
    "Il fait beau aujourd'hui",
    "J'ai oublié mon parapluie",
    "Où est la gare la plus proche ?",
    "Combien ça coûte ?",
    "Je ne comprends pas",
    "Pouvez-vous répéter s'il vous plaît ?",
    "Merci beaucoup",
    "De rien",
    "Excusez-moi",
    "Bonjour, comment ça va ?",
    "Je vais bien merci",
    "À bientôt",
    "Au revoir",
    "Bonne journée",
    "Bonne soirée",
    "Qu'est-ce que vous faites ce weekend ?",
    "J'ai un rendez-vous demain",
    "Je dois faire les courses",
    "Il pleut dehors",
    "J'ai perdu mes clés",
]

# Phrases avec différentes tournures
DIFFERENT_PHRASINGS = [
    "Serait-il possible d'aller à Paris depuis Lyon ?",
    "Auriez-vous l'amabilité de me dire comment me rendre à Marseille ?",
    "Je me demande comment aller de Bordeaux à Toulouse",
    "Est-ce que je peux aller à Nice depuis Cannes ?",
    "Je cherche un moyen de transport pour aller de Lyon à Paris",
    "Pourriez-vous m'aider à trouver un trajet vers Paris ?",
    "J'aimerais savoir comment me rendre à Marseille",
    "Y a-t-il un train pour aller de Toulouse à Bordeaux ?",
    "Je me demande s'il y a un moyen d'aller à Nice",
    "Auriez-vous des informations sur un trajet vers Paris ?",
    "Je souhaiterais me rendre à Lyon",
    "Est-il possible d'aller à Marseille ?",
    "Je voudrais bien aller à Paris",
    "Comment pourrais-je me rendre à Toulouse ?",
    "Serait-ce possible d'aller à Nice ?",
]

# Phrases avec différentes ponctuations et intonations (à noter dans le transcript)
PUNCTUATION_VARIATIONS = [
    "Je veux aller à Paris depuis Lyon.",
    "Je veux aller à Paris depuis Lyon !",
    "Je veux aller à Paris depuis Lyon ?",
    "Je veux aller à Paris... depuis Lyon",
    "Je veux aller à Paris, depuis Lyon",
    "Je veux aller à Paris - depuis Lyon",
    "Je veux aller à Paris (depuis Lyon)",
    "Je veux aller à Paris : depuis Lyon",
    "Je veux aller à Paris ; depuis Lyon",
    "Je veux aller à Paris... depuis Lyon...",
]

# Phrases en anglais (pas en français)
ENGLISH_PHRASES = [
    "I want to go to Paris from Lyon",
    "How can I get to Marseille?",
    "I would like to travel from Bordeaux to Toulouse",
    "Can you tell me how to go to Nice?",
    "I need to go to Paris",
    "What time is the train to Marseille?",
    "I want to book a ticket from Lyon to Paris",
    "How do I get to Bordeaux?",
    "I need to go to Toulouse",
    "Can you help me find a route to Paris?",
]

# Phrases en espagnol
SPANISH_PHRASES = [
    "Quiero ir a París desde Lyon",
    "¿Cómo puedo llegar a Marsella?",
    "Me gustaría viajar de Burdeos a Toulouse",
    "¿Puedes decirme cómo ir a Niza?",
    "Necesito ir a París",
]

# Phrases avec erreurs de prononciation/orthographe (simulées)
PRONUNCIATION_VARIATIONS = [
    "Je veux aller à Paris depuis Lyon",  # Normal
    "Je veux aller à Paris depuis Lyon",  # Répété pour variété
    "Je veux aller à Paris depuis Lyon",  # Répété
]

# Phrases avec hésitations
HESITATIONS = [
    "Euh... je veux aller à Paris... depuis Lyon",
    "Je veux... aller à Paris... depuis Lyon",
    "Je veux aller à... Paris... depuis Lyon",
    "Je veux aller à Paris... euh... depuis Lyon",
    "Je... veux aller à Paris depuis Lyon",
]

# Phrases avec différents niveaux de formalité
FORMALITY_LEVELS = [
    "Je souhaiterais me rendre à Paris en partant de Lyon",  # Très formel
    "Je voudrais aller à Paris depuis Lyon",  # Formel
    "Je veux aller à Paris depuis Lyon",  # Neutre
    "J'veux aller à Paris depuis Lyon",  # Familier
    "J'aimerais bien aller à Paris depuis Lyon",  # Familier
]


def generate_dataset(
    output_dir: str | Path,
    num_samples: int = 1000,
    audio_dir: str = "data/raw/audio"
) -> List[Dict]:
    """
    Génère un dataset STT avec une grande variété de phrases.
    
    Args:
        output_dir: Dossier de sortie pour le dataset
        num_samples: Nombre total d'échantillons à générer
        audio_dir: Dossier où seront stockés les fichiers audio
    
    Returns:
        Liste de dictionnaires représentant le dataset
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Combine toutes les catégories avec leurs poids
    all_phrases = []
    
    # Catégories avec leurs poids (pour diversité)
    categories = [
        (TRAVEL_REQUESTS_COMPLETE, 0.30),  # 30% - demandes complètes
        (TRAVEL_REQUESTS_NO_DEST, 0.05),   # 5% - sans destination
        (TRAVEL_REQUESTS_NO_ORIGIN, 0.10), # 10% - sans origine
        (CITIES_NOT_TRAVEL, 0.15),         # 15% - villes mais pas trajet
        (DAILY_LIFE, 0.15),                # 15% - vie quotidienne
        (DIFFERENT_PHRASINGS, 0.10),       # 10% - tournures différentes
        (PUNCTUATION_VARIATIONS, 0.05),   # 5% - ponctuation
        (ENGLISH_PHRASES, 0.05),           # 5% - anglais
        (SPANISH_PHRASES, 0.02),           # 2% - espagnol
        (HESITATIONS, 0.02),               # 2% - hésitations
        (FORMALITY_LEVELS, 0.01),          # 1% - niveaux de formalité
    ]
    
    # Construit la liste pondérée
    for phrases, weight in categories:
        count = int(num_samples * weight)
        all_phrases.extend(random.choices(phrases, k=count))
    
    # Complète jusqu'à num_samples si nécessaire
    while len(all_phrases) < num_samples:
        category = random.choice(categories)
        all_phrases.append(random.choice(category[0]))
    
    # Mélange
    random.shuffle(all_phrases)
    
    # Génère le dataset
    dataset = []
    for i, phrase in enumerate(all_phrases[:num_samples], 1):
        sample_id = f"sample_{i:06d}"
        audio_filename = f"{sample_id}.wav"
        audio_path = f"{audio_dir}/{audio_filename}"
        
        dataset.append({
            "id": sample_id,
            "audio_path": audio_path,
            "transcript": phrase.strip()
        })
    
    return dataset


def split_dataset(dataset: List[Dict], train_ratio=0.7, valid_ratio=0.15, test_ratio=0.15):
    """
    Divise le dataset en train/valid/test.
    
    Args:
        dataset: Dataset complet
        train_ratio: Proportion pour train
        valid_ratio: Proportion pour valid
        test_ratio: Proportion pour test
    
    Returns:
        Tuple (train, valid, test)
    """
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
    
    parser = argparse.ArgumentParser(description="Generate STT dataset")
    parser.add_argument("--output-dir", default="data/splits", help="Output directory")
    parser.add_argument("--num-samples", type=int, default=1000, help="Number of samples")
    parser.add_argument("--audio-dir", default="data/raw/audio", help="Audio directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    
    # Fixe la seed pour reproductibilité
    random.seed(args.seed)
    
    logger.info(f"Generating {args.num_samples} samples...")
    
    # Génère le dataset
    dataset = generate_dataset(
        args.output_dir,
        num_samples=args.num_samples,
        audio_dir=args.audio_dir
    )
    
    # Divise en train/valid/test
    train, valid, test = split_dataset(dataset)
    
    logger.info(f"Split: train={len(train)}, valid={len(valid)}, test={len(test)}")
    
    # Sauvegarde
    output_dir = Path(args.output_dir)
    write_jsonl(output_dir / "train" / "train.jsonl", train)
    write_jsonl(output_dir / "valid" / "valid.jsonl", valid)
    write_jsonl(output_dir / "test" / "test.jsonl", test)
    
    # Sauvegarde aussi un fichier complet pour référence
    write_jsonl(output_dir / "full_dataset.jsonl", dataset)
    
    logger.info(f"Dataset saved to {output_dir}")
    logger.info(f"Train: {len(train)} samples")
    logger.info(f"Valid: {len(valid)} samples")
    logger.info(f"Test: {len(test)} samples")
    
    # Affiche quelques statistiques
    logger.info("\n=== Statistics ===")
    logger.info(f"Total samples: {len(dataset)}")
    logger.info(f"Unique transcripts: {len(set(d['transcript'] for d in dataset))}")
    
    # Compte par catégorie (approximatif)
    travel_complete = sum(1 for d in dataset if any(city in d['transcript'] for city in ['Paris', 'Lyon', 'Marseille']) and 'aller' in d['transcript'].lower())
    logger.info(f"Travel requests (approx): {travel_complete}")


if __name__ == "__main__":
    main()

