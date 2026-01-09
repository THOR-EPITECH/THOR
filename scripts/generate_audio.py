"""
Script pour générer les fichiers audio à partir du dataset JSONL.
Utilise TTS (Text-to-Speech) pour créer les fichiers audio.
"""
import json
from pathlib import Path
from typing import Optional
import argparse
from src.common.io import read_jsonl
from src.common.logging import setup_logging

logger = setup_logging(module="scripts.generate_audio")

try:
    from gtts import gTTS
    import os
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


def generate_audio_gtts(text: str, output_path: str, language: str = "fr", slow: bool = False):
    """
    Génère un fichier audio avec gTTS (Google Text-to-Speech).
    
    Args:
        text: Texte à convertir
        output_path: Chemin de sortie
        language: Code langue (fr, en, es)
        slow: Parler plus lentement
    """
    if not GTTS_AVAILABLE:
        raise ImportError("gTTS is required. Install with: pip install gtts")
    
    tts = gTTS(text=text, lang=language, slow=slow)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tts.save(str(output_path))


def generate_audio_pyttsx3(text: str, output_path: str, language: str = "fr"):
    """
    Génère un fichier audio avec pyttsx3 (offline).
    
    Args:
        text: Texte à convertir
        output_path: Chemin de sortie
        language: Code langue (fr, en, es)
    """
    if not PYTTSX3_AVAILABLE:
        raise ImportError("pyttsx3 is required. Install with: pip install pyttsx3")
    
    import pyttsx3
    
    engine = pyttsx3.init()
    
    # Configure la voix selon la langue
    voices = engine.getProperty('voices')
    if language == "fr":
        # Cherche une voix française
        for voice in voices:
            if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
    elif language == "es":
        # Cherche une voix espagnole
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
    
    # Configure la vitesse et le volume
    engine.setProperty('rate', 150)  # Vitesse de parole
    engine.setProperty('volume', 0.9)  # Volume
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()


def detect_language(text: str) -> str:
    """
    Détecte la langue du texte (simple heuristique).
    
    Args:
        text: Texte à analyser
    
    Returns:
        Code langue (fr, en, es)
    """
    text_lower = text.lower()
    
    # Mots clés français
    french_words = ['je', 'veux', 'aller', 'depuis', 'comment', 'rendre', 'souhaite']
    # Mots clés anglais
    english_words = ['i', 'want', 'go', 'from', 'how', 'get', 'would']
    # Mots clés espagnol
    spanish_words = ['quiero', 'ir', 'desde', 'cómo', 'llegar', 'me']
    
    french_count = sum(1 for word in french_words if word in text_lower)
    english_count = sum(1 for word in english_words if word in text_lower)
    spanish_count = sum(1 for word in spanish_words if word in text_lower)
    
    if spanish_count > english_count and spanish_count > french_count:
        return "es"
    elif english_count > french_count:
        return "en"
    else:
        return "fr"


def generate_audio_from_dataset(
    dataset_path: str | Path,
    audio_dir: str | Path,
    tts_engine: str = "gtts",
    skip_existing: bool = True
):
    """
    Génère les fichiers audio à partir d'un dataset JSONL.
    
    Args:
        dataset_path: Chemin vers le fichier JSONL
        audio_dir: Dossier de sortie pour les audios
        tts_engine: Moteur TTS à utiliser ('gtts' ou 'pyttsx3')
        skip_existing: Passer les fichiers existants
    """
    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Generating audio from {dataset_path}")
    logger.info(f"Output directory: {audio_dir}")
    logger.info(f"TTS engine: {tts_engine}")
    
    samples = list(read_jsonl(dataset_path))
    total = len(samples)
    
    generated = 0
    skipped = 0
    errors = 0
    
    for i, sample in enumerate(samples, 1):
        transcript = sample.get("transcript", "")
        audio_path = Path(sample.get("audio_path", ""))
        
        if not transcript:
            logger.warning(f"Sample {sample.get('id')} has no transcript, skipping")
            continue
        
        # Construit le chemin de sortie
        output_path = audio_dir / audio_path.name if audio_path.name else f"{sample.get('id', i)}.wav"
        
        # Skip si existe déjà
        if skip_existing and output_path.exists():
            skipped += 1
            if i % 100 == 0:
                logger.info(f"Progress: {i}/{total} (generated: {generated}, skipped: {skipped}, errors: {errors})")
            continue
        
        # Détecte la langue
        language = detect_language(transcript)
        
        try:
            # Génère l'audio
            if tts_engine == "gtts":
                generate_audio_gtts(transcript, str(output_path), language=language)
            elif tts_engine == "pyttsx3":
                generate_audio_pyttsx3(transcript, str(output_path), language=language)
            else:
                raise ValueError(f"Unknown TTS engine: {tts_engine}")
            
            generated += 1
            
            if i % 50 == 0:
                logger.info(f"Progress: {i}/{total} (generated: {generated}, skipped: {skipped}, errors: {errors})")
        
        except Exception as e:
            logger.error(f"Failed to generate audio for {sample.get('id')}: {e}")
            errors += 1
    
    logger.info(f"\n=== Summary ===")
    logger.info(f"Total samples: {total}")
    logger.info(f"Generated: {generated}")
    logger.info(f"Skipped (existing): {skipped}")
    logger.info(f"Errors: {errors}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Generate audio files from STT dataset")
    parser.add_argument("--dataset", required=True, help="Path to JSONL dataset file")
    parser.add_argument("--audio-dir", default="data/raw/audio", help="Output audio directory")
    parser.add_argument("--tts-engine", choices=["gtts", "pyttsx3"], default="gtts", 
                       help="TTS engine to use")
    parser.add_argument("--no-skip-existing", action="store_true", 
                       help="Regenerate existing files")
    
    args = parser.parse_args()
    
    # Vérifie la disponibilité du moteur TTS
    if args.tts_engine == "gtts" and not GTTS_AVAILABLE:
        logger.error("gTTS is not available. Install with: pip install gtts")
        logger.info("Or use pyttsx3: pip install pyttsx3")
        return
    
    if args.tts_engine == "pyttsx3" and not PYTTSX3_AVAILABLE:
        logger.error("pyttsx3 is not available. Install with: pip install pyttsx3")
        logger.info("Or use gTTS: pip install gtts")
        return
    
    generate_audio_from_dataset(
        args.dataset,
        args.audio_dir,
        tts_engine=args.tts_engine,
        skip_existing=not args.no_skip_existing
    )


if __name__ == "__main__":
    main()

