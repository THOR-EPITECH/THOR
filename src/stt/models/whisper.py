"""
Modèle STT utilisant OpenAI Whisper.
"""
import time
from pathlib import Path
from typing import Optional
import numpy as np

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

try:
    import soundfile as sf
    import librosa
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    sf = None
    librosa = None

from src.stt.interfaces import STTModel
from src.common.types import STTResult
from src.common.logging import setup_logging

logger = setup_logging(module="stt.whisper")


class WhisperModel(STTModel):
    """
    Modèle STT basé sur Whisper d'OpenAI.
    
    Supporte les modèles: tiny, base, small, medium, large
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.model_size = self.config.get("model_size", "small")
        self.language = self.config.get("language", "fr")
        self.device = self.config.get("device", "cpu")
        self._model = None
    
    def _load_model(self):
        """Charge le modèle Whisper."""
        if not WHISPER_AVAILABLE:
            raise ImportError("openai-whisper is required. Install with: pip install openai-whisper")
        
        logger.info(f"Loading Whisper model: {self.model_size}")
        try:
            self._model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """
        Transcrit un fichier audio avec Whisper.
        
        Args:
            audio_path: Chemin vers le fichier audio
        
        Returns:
            STTResult avec le texte transcrit
        """
        if not self._initialized:
            self.initialize()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        start_time = time.time()
        
        try:
            if AUDIO_AVAILABLE:
                audio, sr = librosa.load(str(audio_path), sr=16000, mono=True)
                audio = audio.astype(np.float32)
                
                result = self._model.transcribe(
                    audio,
                    language=self.language,
                    task="transcribe"
                )
            else:
                logger.warning("soundfile/librosa not available, Whisper will try to load file directly (requires ffmpeg)")
                result = self._model.transcribe(
                    str(audio_path),
                    language=self.language,
                    task="transcribe"
                )
            
            processing_time = time.time() - start_time
            
            return STTResult(
                text=result["text"].strip(),
                confidence=None,  # Whisper ne retourne pas de confidence globale
                language=result.get("language", self.language),
                processing_time=processing_time,
                metadata={
                    "model": f"whisper-{self.model_size}",
                    "segments": len(result.get("segments", [])),
                    "detected_language": result.get("language")
                }
            )
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

