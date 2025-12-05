"""Script pour télécharger manuellement le modèle Whisper."""

import whisper
import ssl
import urllib.request

def download_whisper_model(model_size="tiny"):
    """Télécharge le modèle Whisper avec gestion des erreurs SSL.
    
    Args:
        model_size (str): Taille du modèle (tiny, base, small, etc.)
    """
    print(f"Téléchargement du modèle Whisper {model_size}...")
    print("(Cela peut prendre quelques minutes)")
    
    try:
        model = whisper.load_model(model_size)
        print(f"✓ Modèle {model_size} téléchargé avec succès!")
        return model
    except ssl.SSLError as e:
        print(f"✗ Erreur SSL: {e}")
        print("\n💡 Solutions possibles:")
        print("1. Vérifiez votre connexion internet")
        print("2. Si vous êtes derrière un proxy:")
        print("   export https_proxy=http://votre-proxy:port")
        print("3. Téléchargez manuellement depuis:")
        print("   https://github.com/openai/whisper")
        print("\n4. Ou désactivez temporairement la vérification SSL (non recommandé):")
        print("   ssl._create_default_https_context = ssl._create_unverified_context")
        return None
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return None


if __name__ == "__main__":
    import sys
    
    model_size = sys.argv[1] if len(sys.argv) > 1 else "tiny"
    download_whisper_model(model_size)

