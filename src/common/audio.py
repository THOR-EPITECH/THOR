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


def resample_audio(
    input_path: str | Path,
    output_path: str | Path,
    target_sr: int = 16000,
    mono: bool = True
) -> dict:
    """
    Rééchantillonne un fichier audio.
    
    Args:
        input_path: Chemin vers le fichier audio d'entrée
        output_path: Chemin vers le fichier de sortie
        target_sr: Fréquence d'échantillonnage cible (Hz)
        mono: Convertir en mono si True
    
    Returns:
        Dictionnaire avec les métadonnées audio
    """
    if not AUDIO_AVAILABLE:
        raise ImportError("soundfile and librosa are required for audio processing")
    
    # Charge l'audio
    audio, sr = librosa.load(str(input_path), sr=None, mono=mono)
    
    # Rééchantillonne si nécessaire
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    
    # Assure que c'est mono
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=0)
    
    # Sauvegarde
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), audio, target_sr)
    
    return {
        "sample_rate": target_sr,
        "channels": 1 if mono else audio.shape[0],
        "duration": len(audio) / target_sr,
        "dtype": audio.dtype
    }


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """
    Normalise l'audio (amplitude entre -1 et 1).
    
    Args:
        audio: Signal audio
    
    Returns:
        Audio normalisé
    """
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        return audio / max_val
    return audio


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

