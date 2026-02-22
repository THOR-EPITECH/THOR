"""
Utilitaires pour le traitement audio.
"""
try:
    import soundfile as sf
    import librosa
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    sf = None
    librosa = None

import numpy as np
from pathlib import Path
from typing import Optional

def get_audio_info(file_path: str | Path) -> dict:
    """
    Récupère les informations d'un fichier audio.
    
    Args:
        file_path: Chemin vers le fichier audio
    
    Returns:
        Dictionnaire avec les métadonnées
    """
    if not AUDIO_AVAILABLE:
        raise ImportError("soundfile is required for audio processing")
    info = sf.info(str(file_path))
    duration = info.frames / info.samplerate
    
    return {
        "sample_rate": info.samplerate,
        "channels": info.channels,
        "duration": duration,
        "frames": info.frames,
        "format": info.format,
        "subtype": info.subtype
    }

