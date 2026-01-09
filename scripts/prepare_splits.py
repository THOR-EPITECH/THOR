"""
Script pour préparer les splits train/test/valid depuis les données brutes.
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Any
import argparse
from src.common.io import read_jsonl, write_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.prepare_splits")


def split_dataset(
    input_file: str | Path,
    output_dir: str | Path,
    train_ratio: float = 0.7,
    valid_ratio: float = 0.15,
    test_ratio: float = 0.15,
    shuffle: bool = True,
    seed: int = 42
):
    """
    Divise un dataset en train/valid/test.
    
    Args:
        input_file: Fichier JSONL d'entrée
        output_dir: Dossier de sortie
        train_ratio: Proportion pour train (0.0-1.0)
        valid_ratio: Proportion pour valid (0.0-1.0)
        test_ratio: Proportion pour test (0.0-1.0)
        shuffle: Mélanger les données avant de diviser
        seed: Seed pour la reproductibilité
    """
    # Vérifie que les ratios somment à 1.0
    total_ratio = train_ratio + valid_ratio + test_ratio
    if abs(total_ratio - 1.0) > 0.01:
        raise ValueError(f"Ratios must sum to 1.0, got {total_ratio}")
    
    # Charge les données
    logger.info(f"Loading dataset from {input_file}")
    data = list(read_jsonl(input_file))
    logger.info(f"Loaded {len(data)} samples")
    
    # Mélange si demandé
    if shuffle:
        random.seed(seed)
        random.shuffle(data)
    
    # Calcule les indices de division
    n_total = len(data)
    n_train = int(n_total * train_ratio)
    n_valid = int(n_total * valid_ratio)
    # n_test = n_total - n_train - n_valid (reste)
    
    # Divise
    train_data = data[:n_train]
    valid_data = data[n_train:n_train + n_valid]
    test_data = data[n_train + n_valid:]
    
    logger.info(f"Split: train={len(train_data)}, valid={len(valid_data)}, test={len(test_data)}")
    
    # Crée les dossiers
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "train").mkdir(exist_ok=True)
    (output_dir / "valid").mkdir(exist_ok=True)
    (output_dir / "test").mkdir(exist_ok=True)
    
    # Sauvegarde (fichiers nommés selon le split)
    write_jsonl(output_dir / "train" / "train.jsonl", train_data)
    write_jsonl(output_dir / "valid" / "valid.jsonl", valid_data)
    write_jsonl(output_dir / "test" / "test.jsonl", test_data)
    
    logger.info(f"Splits saved to {output_dir}")
    
    # Sauvegarde un manifest
    manifest = {
        "source": str(input_file),
        "total_samples": n_total,
        "train_samples": len(train_data),
        "valid_samples": len(valid_data),
        "test_samples": len(test_data),
        "ratios": {
            "train": train_ratio,
            "valid": valid_ratio,
            "test": test_ratio
        },
        "seed": seed,
        "shuffled": shuffle
    }
    
    with open(output_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    logger.info("Manifest saved")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Prepare train/test/valid splits")
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Train ratio (default: 0.7)")
    parser.add_argument("--valid-ratio", type=float, default=0.15, help="Valid ratio (default: 0.15)")
    parser.add_argument("--test-ratio", type=float, default=0.15, help="Test ratio (default: 0.15)")
    parser.add_argument("--no-shuffle", action="store_true", help="Don't shuffle data")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    
    args = parser.parse_args()
    
    split_dataset(
        args.input,
        args.output,
        train_ratio=args.train_ratio,
        valid_ratio=args.valid_ratio,
        test_ratio=args.test_ratio,
        shuffle=not args.no_shuffle,
        seed=args.seed
    )


if __name__ == "__main__":
    main()

