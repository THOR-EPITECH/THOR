"""
CLI pour le module NLP.
"""
import argparse
from pathlib import Path
from src.common.config import Config
from src.common.logging import setup_logging
from src.nlp.models.dummy import DummyNLPModel
from src.nlp.eval.evaluate import evaluate_model
from src.nlp.eval.benchmark import benchmark_models

logger = setup_logging(module="cli.nlp")


def load_model(model_name: str, config: Config) -> "NLPModel":
    """Charge un modèle NLP."""
    nlp_config = config.get("nlp", {})
    
    if model_name == "dummy":
        return DummyNLPModel(nlp_config)
    elif model_name == "spacy":
        from src.nlp.models.spacy_fr import SpacyFRModel
        return SpacyFRModel({
            "model_name": nlp_config.get("model_name", "fr_core_news_md"),
            "custom_model_path": nlp_config.get("custom_model_path")
        })
    elif model_name == "transformers":
        from src.nlp.models.transformers_ner import TransformersNERModel
        return TransformersNERModel({
            "model_name": nlp_config.get("model_name", "Jean-Baptiste/camembert-ner"),
            "custom_model_path": nlp_config.get("custom_model_path"),
            "device": nlp_config.get("device", "cpu")
        })
    elif model_name == "regex_advanced" or model_name == "regex":
        from src.nlp.models.regex_advanced import RegexAdvancedModel
        return RegexAdvancedModel(nlp_config)
    else:
        raise ValueError(f"Unknown model: {model_name}. Available: dummy, spacy, transformers, regex_advanced")


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


def benchmark_command(args):
    """Commande pour benchmarker plusieurs modèles."""
    from src.nlp.models.spacy_fr import SpacyFRModel
    
    # Parse les modèles à comparer
    models_to_benchmark = []
    
    # Modèles par défaut si aucun spécifié
    if not args.models:
        args.models = ["dummy", "regex_advanced", "spacy"]
    
    # Charge chaque modèle avec sa config
    for model_spec in args.models:
        parts = model_spec.split(":")
        model_name = parts[0]
        config_path = parts[1] if len(parts) > 1 else None
        
        config = Config(config_path) if config_path else Config()
        nlp_config = config.get("nlp", {})
        
        try:
            if model_name == "dummy":
                from src.nlp.models.dummy import DummyNLPModel
                model = DummyNLPModel(nlp_config)
                model_config = nlp_config
            elif model_name == "spacy":
                from src.nlp.models.spacy_fr import SpacyFRModel
                model = SpacyFRModel({
                    "model_name": nlp_config.get("model_name", "fr_core_news_md"),
                    "custom_model_path": nlp_config.get("custom_model_path")
                })
                model_config = nlp_config
            elif model_name == "transformers":
                from src.nlp.models.transformers_ner import TransformersNERModel
                model = TransformersNERModel({
                    "model_name": nlp_config.get("model_name", "Jean-Baptiste/camembert-ner"),
                    "custom_model_path": nlp_config.get("custom_model_path"),
                    "device": nlp_config.get("device", "cpu")
                })
                model_config = nlp_config
            elif model_name in ["regex_advanced", "regex"]:
                from src.nlp.models.regex_advanced import RegexAdvancedModel
                model = RegexAdvancedModel(nlp_config)
                model_config = nlp_config
            else:
                logger.warning(f"Unknown model: {model_name}, skipping")
                continue
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            continue
        
        # Nom complet pour le benchmark
        display_name = f"{model_name}"
        if config_path:
            display_name += f" ({Path(config_path).stem})"
        elif model_name == "spacy" and nlp_config.get("custom_model_path"):
            display_name += " (finetuned)"
        
        models_to_benchmark.append((display_name, model, model_config))
    
    if not models_to_benchmark:
        logger.error("No valid models to benchmark")
        return
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Benchmarking {len(models_to_benchmark)} models on {args.dataset}")
    
    # Lance le benchmark
    results = benchmark_models(
        models=models_to_benchmark,
        dataset_path=args.dataset,
        output_dir=output_dir,
        save_individual_results=args.save_individual
    )
    
    print(f"\n✅ Benchmark complete!")
    print(f"Report: {results['report_path']}")
    print(f"Comparison: {results['comparison_path']}")
    
    # Affiche un résumé
    print("\n=== Résumé ===")
    for model_name, result in results["results"].items():
        if result.get("status") == "success":
            metrics = result.get("metrics", {})
            f1 = metrics.get("f1_mean", 0.0)
            print(f"{model_name}: F1={f1:.4f}")
        else:
            print(f"{model_name}: ❌ Erreur")


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
    train_parser.add_argument("--model", default="spacy", help="NLP model to train (spacy, transformers)")
    train_parser.add_argument("--config", help="Path to config file")
    train_parser.add_argument("--output-dir", help="Output directory for trained model")
    train_parser.add_argument("--n-iter", type=int, default=20, help="Number of training iterations")
    train_parser.add_argument("--dropout", type=float, default=0.1, help="Dropout rate")
    
    # Commande benchmark
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark multiple NLP models")
    benchmark_parser.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    benchmark_parser.add_argument("--models", nargs="+", help="Models to benchmark (format: model_name[:config_path]). Default: dummy spacy")
    benchmark_parser.add_argument("--output-dir", default="results/nlp/benchmark", help="Output directory")
    benchmark_parser.add_argument("--save-individual", action="store_true", default=True, help="Save individual model results (default: True)")
    benchmark_parser.add_argument("--no-save-individual", dest="save_individual", action="store_false", help="Don't save individual model results")
    
    args = parser.parse_args()
    
    if args.command == "extract":
        extract_command(args)
    elif args.command == "evaluate":
        evaluate_command(args)
    elif args.command == "train":
        train_command(args)
    elif args.command == "benchmark":
        benchmark_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

