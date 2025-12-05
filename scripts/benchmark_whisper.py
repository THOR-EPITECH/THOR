"""Script principal pour lancer les benchmarks Whisper."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.benchmark import (
    WhisperBenchmarkRunner,
    MarkdownReporter,
    JSONReporter
)
from src.speech_to_text.factory import SpeechToTextFactory


def main():
    """Fonction principale pour lancer les benchmarks."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Benchmark des modèles Whisper"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Chemin vers un fichier audio de test"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=5.0,
        help="Durée d'enregistrement si microphone (défaut: 5.0)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="fr",
        help="Langue pour la transcription (défaut: fr)"
    )
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        help="Modèles à tester (ex: whisper-tiny whisper-base)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Répertoire de sortie pour les rapports (défaut: tests/results/benchmarks)"
    )
    
    args = parser.parse_args()
    
    runner = WhisperBenchmarkRunner(test_audio_path=args.file)
    
    if args.models:
        model_types = args.models
    else:
        model_types = SpeechToTextFactory.list_available_models()
    
    results = runner.run_benchmarks(
        model_types=model_types,
        duration=args.duration,
        language=args.language
    )
    
    if args.output:
        output_path = Path(args.output)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        output_path = project_root / "tests" / "results" / "benchmarks"
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    
    md_reporter = MarkdownReporter(test_audio_path=args.file)
    json_reporter = JSONReporter(test_audio_path=args.file)
    
    md_path = md_reporter.save_report(
        results,
        str(output_path / f"benchmark_whisper_{timestamp}.md")
    )
    
    json_path = json_reporter.save_report(
        results,
        str(output_path / f"benchmark_whisper_{timestamp}.json")
    )
    
    print(f"\n{'='*60}")
    print("RAPPORT")
    print(f"{'='*60}")
    print(md_reporter.generate_report(results))
    print(f"{'='*60}")
    print(f"\n✓ Rapports sauvegardés:")
    print(f"  - Markdown: {md_path}")
    print(f"  - JSON: {json_path}")


if __name__ == "__main__":
    main()

