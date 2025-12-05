"""Exemple d'utilisation du modèle Whisper pour la reconnaissance vocale."""

from pathlib import Path
from src.speech_to_text.factory import SpeechToTextFactory


def main():
    """Exemple d'utilisation de Whisper pour transcrire un fichier audio."""
    
    print("Chargement du modèle Whisper base...")
    model = SpeechToTextFactory.create("whisper-base")
    
    print(f"Modèle chargé: {model.model_name}")
    print(f"Type: {model.model_type}")
    print(f"Langues supportées: {model.supported_languages}")
    print(f"Formats supportés: {model.supported_formats}")
    print()
    
    audio_path = Path("data/audio/sample.wav")
    
    if audio_path.exists():
        print(f"Transcription de {audio_path}...")
        result = model.transcribe(audio_path, language="fr")
        
        if result.is_valid:
            print(f"Texte transcrit: {result.text}")
            print(f"Langue détectée: {result.language}")
            print(f"Confiance: {result.confidence:.2%}")
        else:
            print(f"Erreur: {result.error_message}")
    else:
        print(f"Fichier audio non trouvé: {audio_path}")
        print("Placez un fichier audio dans data/audio/sample.wav pour tester")
    
    print("\n" + "="*50)
    print("Comparaison de différentes tailles de Whisper:")
    print("="*50)
    
    for model_type in ["whisper-tiny", "whisper-base", "whisper-small"]:
        print(f"\nModèle: {model_type}")
        model = SpeechToTextFactory.create(model_type)
        print(f"  - Nom: {model.model_name}")
        print(f"  - Type: {model.model_type}")


if __name__ == "__main__":
    main()

