"""
CLI pour le module NLP.
"""
import argparse
from pathlib import Path
from src.common.config import Config
from src.common.logging import setup_logging
from src.nlp.models.dummy import DummyNLPModel
from src.nlp.eval.evaluate import evaluate_model

logger = setup_logging(module="cli.nlp")


def load_model(model_name: str, config: Config) -> "NLPModel":
    """Charge un modèle NLP."""
    if model_name == "dummy":
        return DummyNLPModel(config.get("nlp", {}))
    elif model_name == "spacy":
        from src.nlp.models.spacy_fr import SpacyFRModel
        nlp_config = config.get("nlp", {})
        return SpacyFRModel({
            "model_name": nlp_config.get("model_name", "fr_core_news_md")
        })
    else:
        raise ValueError(f"Unknown model: {model_name}")


def extract_command(args):
    """Commande pour extraire origine/destination d'un texte."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    logger.info(f"Extracting from text with {args.model}")
    result = model.extract(args.text)
    
    print(f"Origine: {result.origin}")
    print(f"Destination: {result.destination}")
    print(f"Valide: {result.is_valid}")
    if result.confidence is not None:
        print(f"Confidence: {result.confidence:.2f}")


def evaluate_command(args):
    """Commande pour évaluer un modèle."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Evaluating {args.model} on {args.dataset}")
    metrics = evaluate_model(model, args.dataset, output_dir)
    
    print("\n=== Metrics ===")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")


def train_command(args):
    """Commande pour entraîner un modèle."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    output_dir = Path(args.output_dir) if args.output_dir else Path("models/nlp")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Training {args.model} on {args.train_dataset}")
    if args.valid_dataset:
        logger.info(f"Using validation dataset: {args.valid_dataset}")
    
    # Passe les paramètres d'entraînement dans la config
    if args.n_iter:
        model.config["n_iter"] = args.n_iter
    if args.dropout:
        model.config["dropout"] = args.dropout
    
    model_path = model.train(
        train_dataset=args.train_dataset,
        valid_dataset=args.valid_dataset,
        output_dir=output_dir
    )
    
    print(f"\n✅ Training complete!")
    print(f"Model saved to: {model_path}")
    print(f"\nTo use this fine-tuned model, update your config:")
    print(f"  custom_model_path: {model_path}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="THOR NLP CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commande extract
    extract_parser = subparsers.add_parser("extract", help="Extract origin/destination from text")
    extract_parser.add_argument("--text", required=True, help="Text to analyze")
    extract_parser.add_argument("--model", default="dummy", help="NLP model to use")
    extract_parser.add_argument("--config", help="Path to config file")
    
    # Commande evaluate
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a model")
    eval_parser.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    eval_parser.add_argument("--model", default="dummy", help="NLP model to use")
    eval_parser.add_argument("--config", help="Path to config file")
    eval_parser.add_argument("--output-dir", default="results/nlp", help="Output directory")
    
    # Commande train
    train_parser = subparsers.add_parser("train", help="Train (fine-tune) a model")
    train_parser.add_argument("--train-dataset", required=True, help="Path to training dataset JSONL")
    train_parser.add_argument("--valid-dataset", help="Path to validation dataset JSONL")
    train_parser.add_argument("--model", default="spacy", help="NLP model to train (spacy)")
    train_parser.add_argument("--config", help="Path to config file")
    train_parser.add_argument("--output-dir", help="Output directory for trained model")
    train_parser.add_argument("--n-iter", type=int, default=20, help="Number of training iterations")
    train_parser.add_argument("--dropout", type=float, default=0.1, help="Dropout rate")
    
    args = parser.parse_args()
    
    if args.command == "extract":
        extract_command(args)
    elif args.command == "evaluate":
        evaluate_command(args)
    elif args.command == "train":
        train_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

