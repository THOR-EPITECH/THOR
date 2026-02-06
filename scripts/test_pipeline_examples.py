"""
Script pour tester le pipeline sur plusieurs exemples.
"""
import json
from pathlib import Path
from src.pipeline.orchestrator import Pipeline
from src.stt.models.whisper import WhisperModel
from src.nlp.models.spacy_fr import SpacyFRModel
from src.common.config import Config
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.test_pipeline")

def test_audio_files(audio_files: list, config_path: str = None):
    """Teste le pipeline sur plusieurs fichiers audio."""
    if config_path:
        config = Config(config_path)
        nlp_config = config.get("nlp", {})
    else:
        nlp_config = {"custom_model_path": "models/nlp/spacy_finetuned/model"}
    
    stt_model = WhisperModel({"model_size": "small", "language": "fr"})
    nlp_model = SpacyFRModel(nlp_config)
    
    pipeline = Pipeline(stt_model, nlp_model)
    
    results = []
    
    for audio_path in audio_files:
        audio_path = Path(audio_path)
        if not audio_path.exists():
            logger.warning(f"Audio file not found: {audio_path}")
            continue
        
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Testing: {audio_path.name}")
            logger.info(f"{'='*60}")
            
            result = pipeline.process(audio_path)
            
            print(f"\n📝 Transcription: {result['transcript']}")
            print(f"📍 Origine: {result['origin'] if result['origin'] else 'Non détectée'}")
            print(f"🎯 Destination: {result['destination'] if result['destination'] else 'Non détectée'}")
            print(f"✅ Valide: {result['is_valid']}")
            print(f"📊 Confiance: {result.get('confidence', 'N/A')}")
            
            if result.get('error_message'):
                print(f"{result['error_message']}")
            
            results.append({
                "audio": str(audio_path),
                "transcript": result['transcript'],
                "origin": result['origin'],
                "destination": result['destination'],
                "is_valid": result['is_valid'],
                "confidence": result.get('confidence')
            })
            
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {e}")
            results.append({
                "audio": str(audio_path),
                "error": str(e)
            })
    
    return results


def test_text_examples(texts: list, config_path: str = None):
    """Teste le modèle NLP directement sur des textes."""
    if config_path:
        config = Config(config_path)
        nlp_config = config.get("nlp", {})
    else:
        nlp_config = {"custom_model_path": "models/nlp/spacy_finetuned/model"}
    
    nlp_model = SpacyFRModel(nlp_config)
    nlp_model.initialize()
    
    results = []
    
    for text in texts:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Testing text: {text[:50]}...")
            logger.info(f"{'='*60}")
            
            result = nlp_model.extract(text)
            
            print(f"\n📝 Texte: {text}")
            print(f"📍 Origine: {result.origin if result.origin else 'Non détectée'}")
            print(f"🎯 Destination: {result.destination if result.destination else 'Non détectée'}")
            print(f"✅ Valide: {result.is_valid}")
            print(f"📊 Confiance: {result.confidence}")
            print(f"🏷️  Entités: {result.metadata.get('locations_found', [])}")
            
            if result.is_valid:
                if not result.origin and not result.destination:
                    print("❌ Erreur : Aucune ville détectée. Veuillez préciser une ville de départ et/ou d'arrivée.")
                elif not result.origin:
                    print("⚠️ Attention : La ville de départ est manquante. Veuillez préciser d'où vous partez.")
                elif not result.destination:
                    print("⚠️ Attention : La ville d'arrivée est manquante. Veuillez préciser votre destination.")
            
            results.append({
                "text": text,
                "origin": result.origin,
                "destination": result.destination,
                "is_valid": result.is_valid,
                "confidence": result.confidence,
                "entities": result.metadata.get('locations_found', [])
            })
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            results.append({
                "text": text,
                "error": str(e)
            })
    
    return results


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test pipeline on multiple examples")
    parser.add_argument("--audio-dir", help="Directory with audio files to test")
    parser.add_argument("--audio-files", nargs="+", help="List of audio files to test")
    parser.add_argument("--texts", nargs="+", help="List of texts to test")
    parser.add_argument("--dataset", help="JSONL dataset file with sentences to test")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--num-samples", type=int, default=10, help="Number of samples from dataset")
    
    args = parser.parse_args()
    
    results = []
    
    if args.audio_dir:
        audio_dir = Path(args.audio_dir)
        audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))
        if audio_files:
            logger.info(f"Found {len(audio_files)} audio files")
            audio_results = test_audio_files(audio_files[:args.num_samples], args.config)
            results.extend(audio_results)
    
    if args.audio_files:
        audio_results = test_audio_files(args.audio_files, args.config)
        results.extend(audio_results)
    
    if args.texts:
        text_results = test_text_examples(args.texts, args.config)
        results.extend(text_results)
    
    if args.dataset:
        from src.common.io import read_jsonl
        import random
        
        dataset = list(read_jsonl(args.dataset))
        random.shuffle(dataset)
        sample_texts = [item.get("sentence", item.get("transcript", "")) 
                        for item in dataset[:args.num_samples] if item.get("sentence")]
        
        logger.info(f"Testing {len(sample_texts)} samples from dataset")
        text_results = test_text_examples(sample_texts, args.config)
        results.extend(text_results)
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"\n✅ Results saved to {output_path}")
    
    print(f"\n{'='*60}")
    print(f"📊 Résumé: {len(results)} exemples testés")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

