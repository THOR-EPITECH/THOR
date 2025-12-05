"""Modèle de reconnaissance vocale basé sur Whisper (OpenAI)."""

import whisper
import torch
from pathlib import Path
from typing import Optional
import numpy as np
import io
import warnings

from ..base.model_interface import SpeechToTextInterface, TranscriptionResult

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False


class WhisperModel(SpeechToTextInterface):
    """Modèle de reconnaissance vocale utilisant Whisper.
    
    Whisper est un modèle transformer open-source développé par OpenAI,
    spécialisé dans la transcription multilingue avec une excellente
    précision pour le français.
    
    Attributes:
        model: Modèle Whisper chargé.
        device (str): Device utilisé pour l'inférence (cpu/cuda).
        model_size (str): Taille du modèle (tiny, base, small, medium, large).
    """
    
    AVAILABLE_SIZES = ["tiny", "base", "small", "medium", "large"]
    
    SUPPORTED_LANGUAGES = [
        "fr", "en", "es", "de", "it", "pt", "ru", "ja", "zh", "ar"
    ]
    
    SUPPORTED_FORMATS = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
    
    def __init__(
        self,
        model_size: str = "base",
        device: Optional[str] = None,
        model_path: Optional[str] = None
    ):
        """Initialise le modèle Whisper.
        
        Args:
            model_size (str): Taille du modèle Whisper.
                Options: 'tiny', 'base', 'small', 'medium', 'large'.
                Plus le modèle est grand, meilleure est la précision
                mais plus il est lent. Defaults to "base".
            device (Optional[str]): Device pour l'inférence.
                Si None, détecte automatiquement (cuda si disponible, sinon cpu).
                Defaults to None.
            model_path (Optional[str]): Chemin vers un modèle personnalisé.
                Si None, télécharge le modèle depuis Hugging Face.
                Defaults to None.
        
        Raises:
            ValueError: Si la taille du modèle n'est pas valide.
        
        Example:
            >>> model = WhisperModel(model_size="base")
            >>> result = model.transcribe("audio.wav")
            >>> print(result.text)
        """
        if model_size not in self.AVAILABLE_SIZES:
            available = ", ".join(self.AVAILABLE_SIZES)
            raise ValueError(
                f"Invalid model size: {model_size}. "
                f"Available sizes: {available}"
            )
        
        self.model_size = model_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*FP16.*")
            if model_path:
                self.model = whisper.load_model(model_path, device=self.device)
            else:
                self.model = whisper.load_model(model_size, device=self.device)
        
        self._model_name = f"whisper-{model_size}"
        self._model_type = "transformer"
    
    def transcribe(
        self,
        audio_path: str | Path,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit un fichier audio en texte avec Whisper.
        
        Args:
            audio_path (str | Path): Chemin vers le fichier audio.
            language (Optional[str], optional): Code langue ISO (ex: 'fr').
                Si None, Whisper détecte automatiquement la langue.
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        
        Raises:
            FileNotFoundError: Si le fichier audio n'existe pas.
            ValueError: Si le format audio n'est pas supporté.
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=f"Fichier audio non trouvé: {audio_path}"
            )
        
        if audio_path.suffix.lower() not in self.supported_formats:
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=(
                    f"Format non supporté: {audio_path.suffix}. "
                    f"Formats supportés: {', '.join(self.supported_formats)}"
                )
            )
        
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message=".*FP16.*")
                result = self.model.transcribe(
                    str(audio_path),
                    language=language,
                    verbose=False,
                    temperature=0.0,
                    beam_size=5,
                    best_of=5,
                    patience=1.0,
                    condition_on_previous_text=True,
                    initial_prompt=None,
                    word_timestamps=False,
                )
            
            text = result["text"].strip()
            detected_language = result.get("language", language)
            
            segments = result.get("segments", [])
            if segments:
                confidences = [
                    seg.get("no_speech_prob", 0.0) 
                    for seg in segments 
                    if "no_speech_prob" in seg
                ]
                confidence = 1.0 - np.mean(confidences) if confidences else 0.8
            else:
                confidence = 0.8
            
            return TranscriptionResult(
                text=text,
                language=detected_language,
                confidence=float(confidence),
                segments=segments,
                is_valid=True
            )
        
        except Exception as e:
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=f"Erreur lors de la transcription: {str(e)}"
            )
    
    def transcribe_from_bytes(
        self,
        audio_bytes: bytes,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit des données audio brutes en texte.
        
        Args:
            audio_bytes (bytes): Données audio brutes (format PCM 16-bit).
            sample_rate (int): Taux d'échantillonnage en Hz. Defaults to 16000.
            language (Optional[str], optional): Code langue ISO.
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        
        Note:
            Les bytes doivent être au format PCM 16-bit (int16).
            Whisper attend un array numpy de type float32 normalisé entre -1 et 1.
        """
        try:
            audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
            audio_array = (audio_int16.astype(np.float32) / 32768.0).astype(np.float32)
            
            audio_array = self._preprocess_audio(audio_array, sample_rate)
            
            audio_array = audio_array.astype(np.float32, copy=False)
            
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message=".*FP16.*")
                result = self.model.transcribe(
                    audio_array,
                    language=language,
                    verbose=False,
                    temperature=0.0,
                    beam_size=5,
                    best_of=5,
                    patience=1.0,
                    condition_on_previous_text=True,
                    word_timestamps=False,
                )
            
            text = result["text"].strip()
            detected_language = result.get("language", language)
            
            segments = result.get("segments", [])
            if segments:
                confidences = [
                    seg.get("no_speech_prob", 0.0)
                    for seg in segments
                    if "no_speech_prob" in seg
                ]
                confidence = 1.0 - np.mean(confidences) if confidences else 0.8
            else:
                confidence = 0.8
            
            return TranscriptionResult(
                text=text,
                language=detected_language,
                confidence=float(confidence),
                segments=segments,
                is_valid=True
            )
        
        except Exception as e:
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=f"Erreur lors de la transcription: {str(e)}"
            )
    
    def transcribe_from_microphone(
        self,
        duration: float = 5.0,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit l'audio capturé depuis le microphone en temps réel.
        
        Args:
            duration (float): Durée d'enregistrement en secondes. Defaults to 5.0.
            sample_rate (int): Taux d'échantillonnage en Hz. Defaults to 16000.
            language (Optional[str], optional): Code langue ISO (ex: 'fr').
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        
        Raises:
            ImportError: Si sounddevice n'est pas installé.
            RuntimeError: Si aucun microphone n'est disponible.
        
        Example:
            >>> model = WhisperModel("base")
            >>> result = model.transcribe_from_microphone(duration=5.0, language="fr")
            >>> print(result.text)
        """
        if not HAS_SOUNDDEVICE:
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=(
                    "sounddevice n'est pas installé. "
                    "Installez-le avec: pip install sounddevice"
                )
            )
        
        try:
            print(f"🎤 Enregistrement en cours ({duration} secondes)...")
            print("   Parlez maintenant...")
            
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype=np.float32
            )
            sd.wait()
            
            print("✓ Enregistrement terminé, transcription en cours...")
            
            audio_data = audio_data.flatten()
            
            audio_data = audio_data.astype(np.float32, copy=False)
            
            audio_data = self._preprocess_audio(audio_data, sample_rate)
            
            audio_data = audio_data.astype(np.float32, copy=False)
            
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message=".*FP16.*")
                result = self.model.transcribe(
                    audio_data,
                    language=language,
                    verbose=False,
                    temperature=0.0,
                    beam_size=5,
                    best_of=5,
                    patience=1.0,
                    condition_on_previous_text=True,
                    word_timestamps=False,
                )
            
            text = result["text"].strip()
            detected_language = result.get("language", language)
            
            segments = result.get("segments", [])
            if segments:
                confidences = [
                    seg.get("no_speech_prob", 0.0)
                    for seg in segments
                    if "no_speech_prob" in seg
                ]
                confidence = 1.0 - np.mean(confidences) if confidences else 0.8
            else:
                confidence = 0.8
            
            return TranscriptionResult(
                text=text,
                language=detected_language,
                confidence=float(confidence),
                segments=segments,
                is_valid=True
            )
        
        except Exception as e:
            return TranscriptionResult(
                text="",
                language=None,
                confidence=0.0,
                is_valid=False,
                error_message=f"Erreur lors de la capture microphone: {str(e)}"
            )
    
    @property
    def model_name(self) -> str:
        """Retourne le nom du modèle.
        
        Returns:
            str: Nom du modèle (ex: 'whisper-base').
        """
        return self._model_name
    
    @property
    def model_type(self) -> str:
        """Retourne le type du modèle.
        
        Returns:
            str: Type du modèle ('transformer').
        """
        return self._model_type
    
    @property
    def supported_languages(self) -> list[str]:
        """Retourne la liste des langues supportées.
        
        Returns:
            list[str]: Liste des codes langue ISO supportés.
        """
        return self.SUPPORTED_LANGUAGES.copy()
    
    @property
    def supported_formats(self) -> list[str]:
        """Retourne la liste des formats audio supportés.
        
        Returns:
            list[str]: Liste des extensions supportées.
        """
        return self.SUPPORTED_FORMATS.copy()
    
    def _preprocess_audio(
        self, 
        audio: np.ndarray, 
        sample_rate: int = 16000
    ) -> np.ndarray:
        """Prétraite l'audio pour améliorer la qualité de transcription.
        
        Args:
            audio (np.ndarray): Signal audio en float32.
            sample_rate (int): Taux d'échantillonnage. Defaults to 16000.
        
        Returns:
            np.ndarray: Audio prétraité en float32.
        """
        audio = audio.astype(np.float32, copy=False)
        
        max_val = np.abs(audio).max()
        if max_val > 0:
            audio = (audio / max_val * 0.95).astype(np.float32)
        
        if len(audio) > 1:
            kernel_size = min(5, len(audio) // 100)
            if kernel_size > 1 and kernel_size % 2 == 1:
                kernel = np.ones(kernel_size, dtype=np.float32) / float(kernel_size)
                audio = np.convolve(audio, kernel, mode='same').astype(np.float32)
        
        threshold = np.float32(0.01)
        non_silent = np.where(np.abs(audio) > threshold)[0]
        if len(non_silent) > 0:
            audio = audio[non_silent[0]:non_silent[-1] + 1].astype(np.float32)
        
        if len(audio) == 0:
            audio = np.zeros(int(sample_rate * 0.1), dtype=np.float32)
        
        return audio.astype(np.float32, copy=False)

