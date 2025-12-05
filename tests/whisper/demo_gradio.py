"""Interface Gradio pour tester Whisper."""

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

import gradio as gr
from src.speech_to_text.factory import SpeechToTextFactory

_model_cache = {}


def get_model(model_type: str):
    """Récupère ou crée un modèle avec cache.
    
    Args:
        model_type (str): Type de modèle à charger.
    
    Returns:
        Modèle speech-to-text.
    """
    if model_type not in _model_cache:
        print(f"Chargement du modèle {model_type}...")
        _model_cache[model_type] = SpeechToTextFactory.create(model_type)
        print(f"✓ Modèle {model_type} chargé")
    return _model_cache[model_type]


def transcribe_file(audio_file, model_type: str, language: str):
    """Transcrit un fichier audio uploadé.
    
    Args:
        audio_file: Fichier audio uploadé.
        model_type (str): Type de modèle à utiliser.
        language (str): Langue pour la transcription.
    
    Returns:
        str: Texte transcrit.
    """
    if audio_file is None:
        return ""
    
    try:
        model = get_model(model_type)
        
        if isinstance(audio_file, str):
            audio_path = audio_file
        elif hasattr(audio_file, 'name'):
            audio_path = audio_file.name
        else:
            return ""
        
        lang = language if language != "auto" else None
        result = model.transcribe(audio_path, language=lang)
        
        if result.is_valid:
            return result.text
        else:
            return f"Erreur: {result.error_message}"
    
    except Exception as e:
        return f"Erreur: {str(e)}"


def transcribe_microphone(audio_data, model_type: str, language: str):
    """Transcrit l'audio depuis le microphone.
    
    Utilise la même logique que transcribe_from_microphone dans WhisperModel.
    
    Args:
        audio_data: Données audio depuis Gradio (tuple: (sample_rate, audio_array)).
        model_type (str): Type de modèle à utiliser.
        language (str): Langue pour la transcription.
    
    Returns:
        str: Texte transcrit.
    """
    if audio_data is None:
        return ""
    
    try:
        model = get_model(model_type)
        sample_rate, audio_array = audio_data
        
        import numpy as np
        import warnings
        
        if audio_array.ndim > 1:
            audio_array = audio_array.flatten()
        
        if len(audio_array) == 0:
            return ""
        
        audio_array = audio_array.astype(np.float32, copy=False)
        
        audio_array = model._preprocess_audio(audio_array, sample_rate)
        
        audio_array = audio_array.astype(np.float32, copy=False)
        
        lang = language if language != "auto" else None
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*FP16.*")
            result_dict = model.model.transcribe(
                audio_array,
                language=lang,
                verbose=False,
                temperature=0.0,
                beam_size=5,
                best_of=5,
                patience=1.0,
                condition_on_previous_text=True,
                word_timestamps=False,
            )
        
        text = result_dict["text"].strip()
        return text
    
    except Exception as e:
        return f"Erreur: {str(e)}"


def create_interface():
    """Crée l'interface Gradio."""
    
    available_models = SpeechToTextFactory.list_available_models()
    
    with gr.Blocks(title="THOR - Whisper") as demo:
        gr.Markdown("# THOR Speech-to-Text (Whisper)")
        
        with gr.Row():
            model_choice = gr.Dropdown(
                choices=available_models,
                value="whisper-base",
                label="Modèle"
            )
            
            language_choice = gr.Dropdown(
                choices=[
                    ("Auto-détection", "auto"),
                    ("Français", "fr"),
                    ("Anglais", "en"),
                    ("Espagnol", "es"),
                    ("Allemand", "de"),
                    ("Italien", "it"),
                    ("Portugais", "pt"),
                    ("Russe", "ru"),
                    ("Japonais", "ja"),
                    ("Chinois", "zh"),
                    ("Arabe", "ar")
                ],
                value="fr",
                label="Langue"
            )
        
        with gr.Tabs():
            with gr.Tab("Fichier audio"):
                file_input = gr.Audio(
                    type="filepath",
                    label="Fichier audio",
                    sources=["upload"]
                )
                file_output = gr.Textbox(
                    label="Transcription",
                    lines=10
                )
                file_input.change(
                    fn=transcribe_file,
                    inputs=[file_input, model_choice, language_choice],
                    outputs=file_output
                )
            
            with gr.Tab("Microphone"):
                mic_input = gr.Audio(
                    type="numpy",
                    label="Enregistrement",
                    sources=["microphone"]
                )
                mic_output = gr.Textbox(
                    label="Transcription",
                    lines=10
                )
                mic_input.change(
                    fn=transcribe_microphone,
                    inputs=[mic_input, model_choice, language_choice],
                    outputs=mic_output
                )
    
    return demo


def main():
    """Fonction principale."""
    import argparse
    import socket
    
    parser = argparse.ArgumentParser(description="Interface Gradio pour Whisper")
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port pour l'interface Gradio (défaut: 7860)"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Créer un lien public partagé"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Interface Gradio - Whisper THOR")
    print("=" * 60)
    print()
    print("Lancement de l'interface...")
    print(f"L'interface sera accessible à: http://localhost:{args.port}")
    print()
    print("Appuyez sur Ctrl+C pour arrêter")
    print("=" * 60)
    
    demo = create_interface()
    
    def find_free_port(start_port: int) -> int:
        """Trouve un port libre à partir d'un port de départ.
        
        Args:
            start_port (int): Port de départ.
        
        Returns:
            int: Port libre.
        """
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        raise OSError("Aucun port libre trouvé")
    
    try:
        demo.launch(
            server_name="127.0.0.1",
            server_port=args.port,
            share=args.share,
            show_error=True
        )
    except OSError as e:
        if "address already in use" in str(e) or "Cannot find empty port" in str(e):
            print(f"\n⚠️  Le port {args.port} est déjà utilisé.")
            print(f"🔍 Recherche d'un port libre...")
            
            try:
                free_port = find_free_port(args.port + 1)
                print(f"✓ Port libre trouvé: {free_port}")
                print(f"🚀 Relancement sur le port {free_port}...\n")
                
                demo.launch(
                    server_name="127.0.0.1",
                    server_port=free_port,
                    share=args.share,
                    show_error=True
                )
            except OSError:
                print(f"\n❌ Impossible de trouver un port libre.")
                print(f"\n💡 Solutions:")
                print(f"   1. Arrêter l'autre processus utilisant le port {args.port}")
                print(f"   2. Spécifier un port manuellement: python tests/whisper/demo_gradio.py --port 8000")
        else:
            raise


if __name__ == "__main__":
    main()

