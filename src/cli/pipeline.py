"""
CLI pour le pipeline complet Audio → STT → NLP.
"""
import argparse
import json
from pathlib import Path
from src.common.config import Config
from src.common.logging import setup_logging
from src.pipeline.orchestrator import Pipeline
from src.stt.models.whisper import WhisperModel
from src.stt.models.vosk import VoskModel
from src.nlp.models.spacy_fr import SpacyFRModel

logger = setup_logging(module="cli.pipeline")


def load_stt_model(model_name: str, config: Config) -> "STTModel":
    """Charge un modèle STT."""
    if model_name == "whisper":
        stt_config = config.get("stt", {})
        return WhisperModel({
            "model_size": stt_config.get("model_size", "small"),
            "language": stt_config.get("language", "fr"),
            "device": stt_config.get("device", "cpu")
        })
    elif model_name == "vosk":
        from src.stt.models.vosk import VoskModel
        stt_config = config.get("stt", {})
        return VoskModel({
            "model_path": stt_config.get("model_path", "models/vosk-fr"),
            "sample_rate": stt_config.get("sample_rate", 16000)
        })
    else:
        raise ValueError(f"Unknown STT model: {model_name}")


def load_nlp_model(model_name: str, config: Config) -> "NLPModel":
    """Charge un modèle NLP."""
    if model_name == "spacy":
        nlp_config = config.get("nlp", {})
        return SpacyFRModel({
            "model_name": nlp_config.get("model_name", "fr_core_news_md")
        })
    else:
        raise ValueError(f"Unknown NLP model: {model_name}")


def process_command(args):
    """Commande pour traiter un fichier audio."""
    config = Config(args.config) if args.config else Config()
    
    # Charge les modèles
    stt_model = load_stt_model(args.stt_model, config)
    nlp_model = load_nlp_model(args.nlp_model, config)
    
    # Crée le pipeline
    pipeline = Pipeline(stt_model, nlp_model)
    
    # Traite l'audio
    result = pipeline.process(args.audio)
    
    # Affiche les résultats
    print("\n=== Résultats ===")
    print(f"Transcription: {result['transcript']}")
    print(f"Origine: {result['origin'] if result['origin'] else 'Non détectée'}")
    print(f"Destination: {result['destination'] if result['destination'] else 'Non détectée'}")
    print(f"Valide: {result['is_valid']}")
    if result.get('confidence'):
        print(f"Confidence: {result['confidence']:.2f}")
    
    # Affiche le message d'erreur si présent
    if result.get('error_message'):
        print(f"\n{result['error_message']}")
    
    # Détermine le chemin de sortie
    if args.output:
        output_path = Path(args.output)
    else:
        # Génère un nom automatique basé sur l'audio
        audio_name = Path(args.audio).stem
        output_dir = Path("results/pipeline")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{audio_name}_result.json"
    
    # Sauvegarde JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nRésultats JSON sauvegardés dans: {output_path}")
    
    # Génère le rapport markdown
    from src.pipeline.report import generate_pipeline_report
    report_path = output_path.with_suffix('.md')
    generate_pipeline_report(result, report_path)
    print(f"Rapport markdown généré: {report_path}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="THOR Pipeline CLI")
    
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--stt-model", default="whisper", help="STT model to use (whisper, vosk)")
    parser.add_argument("--nlp-model", default="spacy", help="NLP model to use (spacy)")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--output", help="Path to save results JSON")
    
    args = parser.parse_args()
    
    process_command(args)


if __name__ == "__main__":
    main()

