"""
Script pour entraîner tous les modèles NLP disponibles.
"""
import sys
from pathlib import Path

# Ajoute le répertoire parent au PYTHONPATH pour trouver les modules src
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

import argparse
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.train_all_nlp")


def train_all_models(
    train_dataset: str,
    valid_dataset: str = None,
    output_base_dir: str = "models/nlp"
):
    """
    Entraîne tous les modèles NLP disponibles.
    
    Args:
        train_dataset: Chemin vers le dataset d'entraînement
        valid_dataset: Chemin vers le dataset de validation (optionnel)
        output_base_dir: Dossier de base pour sauvegarder les modèles
    """
    from src.common.config import Config
    from src.cli.nlp import load_model
    
    output_base = Path(output_base_dir)
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Liste des modèles à entraîner
    models_to_train = [
        ("spacy", None, "spacy_finetuned"),
        ("transformers", None, "transformers_finetuned"),
    ]
    
    results = []
    
    for model_name, config_path, output_name in models_to_train:
        logger.info(f"\n{'='*60}")
        logger.info(f"Training {model_name}...")
        logger.info(f"{'='*60}")
        
        try:
            config = Config(config_path) if config_path else Config()
            model = load_model(model_name, config)
            
            output_dir = output_base / output_name
            
            model_path = model.train(
                train_dataset=train_dataset,
                valid_dataset=valid_dataset,
                output_dir=output_dir
            )
            
            results.append({
                "model": model_name,
                "status": "success",
                "path": str(model_path)
            })
            
            logger.info(f"✅ {model_name} trained successfully: {model_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to train {model_name}: {e}")
            results.append({
                "model": model_name,
                "status": "error",
                "error": str(e)
            })
    
    # Résumé
    logger.info(f"\n{'='*60}")
    logger.info("Training Summary")
    logger.info(f"{'='*60}")
    
    for result in results:
        if result["status"] == "success":
            logger.info(f"✅ {result['model']}: {result['path']}")
        else:
            logger.info(f"❌ {result['model']}: {result.get('error', 'Unknown error')}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Train all NLP models")
    parser.add_argument("--train-dataset", required=True, help="Path to training dataset JSONL")
    parser.add_argument("--valid-dataset", help="Path to validation dataset JSONL")
    parser.add_argument("--output-dir", default="models/nlp", help="Base output directory")
    
    args = parser.parse_args()
    
    train_all_models(
        train_dataset=args.train_dataset,
        valid_dataset=args.valid_dataset,
        output_base_dir=args.output_dir
    )


if __name__ == "__main__":
    main()

