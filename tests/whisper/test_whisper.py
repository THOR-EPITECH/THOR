"""Tests pour le module Whisper."""

import sys
import ssl
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from src.speech_to_text.factory import SpeechToTextFactory


def test_model_creation():
    """Test la création des différents modèles Whisper."""
    print("=" * 60)
    print("TEST: Création des modèles")
    print("=" * 60)
    
    models_to_test = ["whisper-tiny", "whisper-base", "whisper-small"]
    
    for model_type in models_to_test:
        try:
            print(f"\nCréation du modèle: {model_type}")
            model = SpeechToTextFactory.create(model_type)
            print(f"  ✓ Modèle créé: {model.model_name}")
            print(f"  ✓ Type: {model.model_type}")
            print(f"  ✓ Langues supportées: {len(model.supported_languages)} langues")
            print(f"  ✓ Formats supportés: {', '.join(model.supported_formats)}")
        except Exception as e:
            print(f"  ✗ Erreur: {e}")
    
    print("\n" + "=" * 60)


def test_list_models():
    """Test la liste des modèles disponibles."""
    print("=" * 60)
    print("TEST: Liste des modèles disponibles")
    print("=" * 60)
    
    available = SpeechToTextFactory.list_available_models()
    print(f"\nModèles disponibles: {len(available)}")
    for model_type in available:
        info = SpeechToTextFactory.get_model_info(model_type)
        print(f"  - {model_type}: {info.get('architecture', 'N/A')}")
    
    print("\n" + "=" * 60)


def test_transcribe_file(audio_path: str):
    """Test la transcription d'un fichier audio.
    
    Args:
        audio_path (str): Chemin vers le fichier audio.
    """
    print("=" * 60)
    print("TEST: Transcription d'un fichier audio")
    print("=" * 60)
    
    audio_file = Path(audio_path)
    
    if not audio_file.exists():
        print(f"\n✗ Fichier non trouvé: {audio_path}")
        print("\nPour tester avec un fichier audio:")
        print("  python tests/whisper/test_whisper.py --file <chemin_vers_audio>")
        return
    
    print(f"\nFichier audio: {audio_file}")
    print(f"Taille: {audio_file.stat().st_size / 1024:.2f} KB")
    
    try:
        print("\nChargement du modèle Whisper base...")
        model = SpeechToTextFactory.create("whisper-base")
        print("✓ Modèle chargé")
        
        print(f"\nTranscription en cours...")
        result = model.transcribe(audio_file, language="fr")
        
        if result.is_valid:
            print("\n✓ Transcription réussie!")
            print(f"\nTexte transcrit:")
            print(f"  {result.text}")
            print(f"\nDétails:")
            print(f"  - Langue détectée: {result.language}")
            print(f"  - Confiance: {result.confidence:.2%}")
            if result.segments:
                print(f"  - Nombre de segments: {len(result.segments)}")
        else:
            print(f"\n✗ Erreur de transcription:")
            print(f"  {result.error_message}")
    
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


def test_microphone(duration: float = 5.0, language: str = "fr", model_size: str = "base"):
    """Test la transcription depuis le microphone.
    
    Args:
        duration (float): Durée d'enregistrement en secondes.
        language (str): Langue (fr/en).
        model_size (str): Taille du modèle (tiny/base/small).
    """
    print("=" * 60)
    print("TEST: Transcription depuis le microphone")
    print("=" * 60)
    print()
    
    try:
        import sounddevice as sd
        print("✓ sounddevice est installé")
        print(f"✓ Périphériques audio disponibles: {len(sd.query_devices())}")
        print()
    except ImportError:
        print("✗ sounddevice n'est pas installé")
        print("\nInstallez-le avec:")
        print("  pip install sounddevice")
        return
    
    print(f"Chargement du modèle Whisper {model_size}...")
    print("(Premier chargement: téléchargement du modèle, peut prendre quelques minutes)")
    try:
        model = SpeechToTextFactory.create(f"whisper-{model_size}")
        print(f"✓ Modèle chargé: {model.model_name}")
        print()
    except Exception as e:
        error_msg = str(e)
        print(f"✗ Erreur lors du chargement: {error_msg}")
        return
    
    print(f"Durée d'enregistrement: {duration} secondes")
    print(f"Langue: {language}")
    print()
    print("=" * 60)
    print("PRÊT À ENREGISTRER")
    print("=" * 60)
    print()
    
    result = model.transcribe_from_microphone(
        duration=duration,
        language=language
    )
    
    print()
    print("=" * 60)
    print("RÉSULTAT")
    print("=" * 60)
    
    if result.is_valid:
        print(f"\n📝 Texte transcrit:")
        print(f"   {result.text}")
        print(f"\n📊 Détails:")
        print(f"   - Langue détectée: {result.language}")
        print(f"   - Confiance: {result.confidence:.2%}")
        if result.segments:
            print(f"   - Segments: {len(result.segments)}")
    else:
        print(f"\n✗ Erreur:")
        print(f"   {result.error_message}")
    
    print()
    print("=" * 60)


def test_microphone_loop(duration: float = 5.0, language: str = "fr", model_size: str = "base"):
    """Test en boucle - continue d'enregistrer jusqu'à interruption.
    
    Args:
        duration (float): Durée d'enregistrement en secondes.
        language (str): Langue (fr/en).
        model_size (str): Taille du modèle (tiny/base/small).
    """
    print("=" * 60)
    print("MODE BOUCLE - Appuyez sur Ctrl+C pour arrêter")
    print("=" * 60)
    print()
    
    try:
        import sounddevice as sd
    except ImportError:
        print("✗ sounddevice n'est pas installé")
        print("  pip install sounddevice")
        return
    
    print("Chargement du modèle...")
    model = SpeechToTextFactory.create(f"whisper-{model_size}")
    print(f"✓ Modèle chargé: {model.model_name}\n")
    
    try:
        while True:
            print("-" * 60)
            print(f"Enregistrement de {duration} secondes...")
            print("Parlez maintenant (Ctrl+C pour arrêter)")
            
            result = model.transcribe_from_microphone(
                duration=duration,
                language=language
            )
            
            if result.is_valid and result.text.strip():
                print(f"\n✓ Transcription: {result.text}")
            else:
                print(f"\n✗ Aucune transcription (ou erreur)")
            
            print()
    
    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur")
        print("=" * 60)


def test_basic():
    """Test basique sans fichier audio - vérifie juste que le module fonctionne."""
    print("=" * 60)
    print("TEST: Vérification du module (sans fichier audio)")
    print("=" * 60)
    
    try:
        print("\n1. Test de création du modèle...")
        model = SpeechToTextFactory.create("whisper-tiny")
        print("   ✓ Modèle créé avec succès")
        
        print("\n2. Test des propriétés...")
        print(f"   ✓ Nom: {model.model_name}")
        print(f"   ✓ Type: {model.model_type}")
        print(f"   ✓ Langues: {len(model.supported_languages)} langues")
        print(f"   ✓ Formats: {', '.join(model.supported_formats)}")
        
        print("\n3. Test de la factory...")
        available = SpeechToTextFactory.list_available_models()
        print(f"   ✓ {len(available)} modèles disponibles")
        
        print("\n" + "=" * 60)
        print("✓ Tous les tests de base ont réussi!")
        print("\nPour tester avec un vrai fichier audio:")
        print("  python tests/whisper/test_whisper.py --file <chemin_vers_audio>")
        print("\nPour tester avec le microphone:")
        print("  python tests/whisper/test_whisper.py --mic")
        print("\n" + "=" * 60)
    
    except ImportError as e:
        print(f"\n✗ Erreur d'import: {e}")
        print("\nAssurez-vous d'avoir installé les dépendances:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        import traceback
        traceback.print_exc()


def print_usage():
    """Affiche l'aide d'utilisation."""
    print("=" * 60)
    print("TESTS DU MODULE WHISPER")
    print("=" * 60)
    print()
    print("Usage:")
    print("  python tests/whisper/test_whisper.py [options]")
    print()
    print("Options:")
    print("  --basic              Test basique (vérification du module)")
    print("  --models             Test de création des modèles")
    print("  --list               Liste les modèles disponibles")
    print("  --mic                Test avec le microphone")
    print("  --mic-loop           Test microphone en boucle")
    print("  --file <chemin>      Test avec un fichier audio")
    print("  --duration <sec>     Durée d'enregistrement (défaut: 5.0)")
    print("  --language <lang>    Langue (fr/en, défaut: fr)")
    print("  --model <size>       Taille du modèle (tiny/base/small, défaut: base)")
    print()
    print("Exemples:")
    print("  python tests/whisper/test_whisper.py --basic")
    print("  python tests/whisper/test_whisper.py --mic")
    print("  python tests/whisper/test_whisper.py --mic --duration 10 --language fr")
    print("  python tests/whisper/test_whisper.py --file data/audio/test.wav")
    print("  python tests/whisper/test_whisper.py --mic-loop")
    print()


def main():
    """Fonction principale."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Tests pour le module Whisper"
    )
    parser.add_argument("--basic", action="store_true", help="Test basique")
    parser.add_argument("--models", action="store_true", help="Test de création des modèles")
    parser.add_argument("--list", action="store_true", help="Liste les modèles disponibles")
    parser.add_argument("--mic", action="store_true", help="Test avec le microphone")
    parser.add_argument("--mic-loop", action="store_true", help="Test microphone en boucle")
    parser.add_argument("--file", type=str, help="Chemin vers un fichier audio")
    parser.add_argument("--duration", type=float, default=5.0, help="Durée d'enregistrement")
    parser.add_argument("--language", type=str, default="fr", help="Langue (fr/en)")
    parser.add_argument("--model", type=str, default="base", help="Taille du modèle (tiny/base/small)")
    
    args = parser.parse_args()
    
    if not any([args.basic, args.models, args.list, args.mic, args.mic_loop, args.file]):
        print_usage()
        test_basic()
        return
    
    if args.basic:
        test_basic()
    
    if args.models:
        test_model_creation()
    
    if args.list:
        test_list_models()
    
    if args.file:
        test_transcribe_file(args.file)
    
    if args.mic:
        test_microphone(
            duration=args.duration,
            language=args.language,
            model_size=args.model
        )
    
    if args.mic_loop:
        test_microphone_loop(
            duration=args.duration,
            language=args.language,
            model_size=args.model
        )


if __name__ == "__main__":
    main()

