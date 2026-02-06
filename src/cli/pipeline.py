"""
CLI pour le pipeline complet Audio → STT → NLP → Pathfinding.
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
            "model_path": stt_config.get("model_path", "models/stt/vosk-fr/vosk-model-fr-0.22"),
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


def load_pathfinding_model(model_name: str, config: Config) -> "PathfindingModel":
    """Charge un modèle Pathfinding."""
    if model_name == "dijkstra":
        from src.pathfinding.models.dijkstra import DijkstraPathfindingModel
        pathfinding_config = config.get("pathfinding", {})
        return DijkstraPathfindingModel({
            "path_gares": pathfinding_config.get("path_gares", "data/train_station/dataset_gares.json"),
            "path_liaisons_enhanced": pathfinding_config.get("path_liaisons_enhanced", "data/train_station/dataset_liaisons_enhanced.json"),
            "path_liaisons": pathfinding_config.get("path_liaisons", "data/train_station/dataset_liaisons.json"),
            "mode": pathfinding_config.get("mode", "time")  # Utilise les temps de trajet réels par défaut
        })
    else:
        raise ValueError(f"Unknown Pathfinding model: {model_name}")


def process_command(args):
    """Commande pour traiter un fichier audio."""
    config = Config(args.config) if args.config else Config()
    
    stt_model = load_stt_model(args.stt_model, config)
    nlp_model = load_nlp_model(args.nlp_model, config)
    pathfinding_model = None
    
    if args.pathfinding_model:
        pathfinding_model = load_pathfinding_model(args.pathfinding_model, config)
    
    pipeline = Pipeline(stt_model, nlp_model, pathfinding_model)
    
    result = pipeline.process(args.audio)
    
    print("\n=== Configuration ===")
    print(f"Modèle STT: {args.stt_model}")
    print(f"Modèle NLP: {args.nlp_model}")
    if args.pathfinding_model:
        print(f"Modèle Pathfinding: {args.pathfinding_model}")
    
    print("\n=== Résultats ===")
    print(f"Transcription: {result['transcript']}")
    print(f"Origine: {result['origin'] if result['origin'] else 'Non détectée'}")
    print(f"Destination: {result['destination'] if result['destination'] else 'Non détectée'}")
    print(f"Valide: {result['is_valid']}")
    if result.get('confidence'):
        print(f"Confidence: {result['confidence']:.2f}")
    
    if result.get('route') and result['route'].get('steps'):
        route = result['route']
        print(f"\n=== Itinéraire ===")
        if route.get('total_time'):
            hours = int(route['total_time'] // 60)
            minutes = int(route['total_time'] % 60)
            print(f"⏱️  Temps de trajet: {hours}h{minutes:02d} ({route['total_time']:.0f} min)")
        if route.get('total_distance'):
            print(f"📏 Distance totale: {route['total_distance']:.1f} km")
        print(f"🛤️  Nombre d'étapes: {len(route['steps'])}")
        
        segments = route.get('metadata', {}).get('segments', [])
        if segments:
            print("\n📊 Détails du trajet:")
            for seg in segments:
                train_type = seg.get('type_train', 'Autre')
                if train_type == 'TGV':
                    emoji = '🚄'
                elif train_type == 'OUIGO':
                    emoji = '🟢'
                elif train_type == 'Intercités':
                    emoji = '🚃'
                elif train_type == 'TER':
                    emoji = '🚈'
                else:
                    emoji = '🚂'
                
                temps = seg.get('temps_min', 0)
                distance = seg.get('distance_km', 0)
                nb_trains = seg.get('nb_trains_jour', 0)
                
                print(f"   {emoji} [{train_type:12}] {seg['from']} → {seg['to']}")
                print(f"      ⏱️ {temps:.0f} min | 📏 {distance:.1f} km | 🚂 {nb_trains} trains/jour")
        else:
            print("\nÉtapes:")
            for i, step in enumerate(route['steps'], 1):
                print(f"  {i}. {step}")
    elif result.get('route') and result['route'].get('metadata', {}).get('error'):
        print(f"\n⚠️ Pathfinding: {result['route']['metadata']['error']}")
    
    if result.get('error_message'):
        print(f"\n{result['error_message']}")
    
    if args.output:
        output_path = Path(args.output)
    else:
        audio_name = Path(args.audio).stem
        output_dir = Path("results/pipeline")
        output_dir.mkdir(parents=True, exist_ok=True)
        if args.pathfinding_model:
            output_path = output_dir / f"{audio_name}_{args.stt_model}_{args.nlp_model}_{args.pathfinding_model}_result.json"
        else:
            output_path = output_dir / f"{audio_name}_{args.stt_model}_{args.nlp_model}_result.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nRésultats JSON sauvegardés dans: {output_path}")
    
    from src.pipeline.report import generate_pipeline_report
    report_path = output_path.with_suffix('.md')
    generate_pipeline_report(
        result, 
        report_path, 
        stt_model_name=args.stt_model, 
        nlp_model_name=args.nlp_model,
        pathfinding_model_name=args.pathfinding_model
    )
    print(f"Rapport markdown généré: {report_path}")
    
    print(f"\n=== Commande pour refaire le test ===")
    cmd = f"python3 -m src.cli.pipeline --audio {args.audio} --stt-model {args.stt_model} --nlp-model {args.nlp_model}"
    if args.pathfinding_model:
        cmd += f" --pathfinding-model {args.pathfinding_model}"
    print(cmd)


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="THOR Pipeline CLI")
    
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--stt-model", default="whisper", help="STT model to use (whisper, vosk)")
    parser.add_argument("--nlp-model", default="spacy", help="NLP model to use (spacy)")
    parser.add_argument("--pathfinding-model", help="Pathfinding model to use (dijkstra, optional)")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--output", help="Path to save results JSON")
    
    args = parser.parse_args()
    
    process_command(args)


if __name__ == "__main__":
    main()

