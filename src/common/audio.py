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

def trim_silence(
    audio: np.ndarray,
    sr: int,
    top_db: int = 20
) -> np.ndarray:
    """
    Supprime le silence au début et à la fin.
    
    Args:
        audio: Signal audio
        sr: Fréquence d'échantillonnage
        top_db: Seuil en dB pour détecter le silence
    
    Returns:
        Audio sans silence
    """
    if not AUDIO_AVAILABLE:
        raise ImportError("librosa is required for audio processing")
    trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
    return trimmed


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

