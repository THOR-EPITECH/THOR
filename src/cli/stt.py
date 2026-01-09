"""
CLI pour le module Speech-to-Text.
"""
import argparse
from pathlib import Path
from src.common.config import Config
from src.common.logging import setup_logging
from src.stt.models.dummy import DummySTTModel
from src.stt.models.whisper import WhisperModel
from src.stt.eval.evaluate import evaluate_model
from src.stt.eval.error_analysis import analyze_errors

logger = setup_logging(module="cli.stt")


def load_model(model_name: str, config: Config) -> "STTModel":
    """Charge un modèle STT."""
    if model_name == "dummy":
        return DummySTTModel(config.get("stt", {}))
    elif model_name == "whisper":
        stt_config = config.get("stt", {})
        return WhisperModel({
            "model_size": stt_config.get("model_size", "small"),
            "language": stt_config.get("language", "fr"),
            "device": stt_config.get("device", "cpu")
        })
    else:
        raise ValueError(f"Unknown model: {model_name}")


def transcribe_command(args):
    """Commande pour transcrire un fichier audio."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    logger.info(f"Transcribing {args.audio} with {args.model}")
    result = model.transcribe(args.audio)
    
    print(f"Text: {result.text}")
    if result.processing_time:
        print(f"Processing time: {result.processing_time:.2f}s")
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
    
    # Analyse des erreurs
    if args.analyze_errors:
        logger.info("Analyzing errors...")
        analyze_errors(
            output_dir / "predictions.jsonl",
            output_dir,
            top_n=args.top_errors
        )


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="THOR Speech-to-Text CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commande transcribe
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe an audio file")
    transcribe_parser.add_argument("--audio", required=True, help="Path to audio file")
    transcribe_parser.add_argument("--model", default="whisper", help="STT model to use")
    transcribe_parser.add_argument("--config", help="Path to config file")
    
    # Commande evaluate
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a model")
    eval_parser.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    eval_parser.add_argument("--model", default="whisper", help="STT model to use")
    eval_parser.add_argument("--config", help="Path to config file")
    eval_parser.add_argument("--output-dir", default="results/stt", help="Output directory")
    eval_parser.add_argument("--analyze-errors", action="store_true", help="Analyze errors")
    eval_parser.add_argument("--top-errors", type=int, default=20, help="Number of top errors to show")
    
    args = parser.parse_args()
    
    if args.command == "transcribe":
        transcribe_command(args)
    elif args.command == "evaluate":
        evaluate_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

