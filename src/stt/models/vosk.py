"""
Modèle STT utilisant Vosk (offline, français).
"""
import time
import json
from pathlib import Path
from typing import Optional

try:
    from vosk import Model, KaldiRecognizer
    import wave
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    Model = None
    KaldiRecognizer = None
    wave = None

try:
    import soundfile as sf
    import librosa
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    sf = None
    librosa = None
    np = None

from src.stt.interfaces import STTModel
from src.common.types import STTResult
from src.common.logging import setup_logging

logger = setup_logging(module="stt.vosk")


class VoskModel(STTModel):
    """
    Modèle STT basé sur Vosk (offline, français).
    
    Nécessite un modèle Vosk téléchargé (voir https://alphacephei.com/vosk/models)
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.model_path = self.config.get("model_path", "models/vosk-fr")
        self.sample_rate = self.config.get("sample_rate", 16000)
        self._model = None
        self._recognizer = None
    
    def _load_model(self):
        """Charge le modèle Vosk."""
        if not VOSK_AVAILABLE:
            raise ImportError("vosk is required. Install with: pip install vosk")
        
        model_path = Path(self.model_path)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}. "
                f"Download from https://alphacephei.com/vosk/models"
            )
        
        logger.info(f"Loading Vosk model from {model_path}")
        try:
            self._model = Model(str(model_path))
            self._recognizer = KaldiRecognizer(self._model, self.sample_rate)
            logger.info("Vosk model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Vosk model: {e}")
            raise
    
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """
        Transcrit un fichier audio avec Vosk.
        
        Args:
            audio_path: Chemin vers le fichier audio (WAV, 16kHz, mono)
        
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
                audio_data, sr = librosa.load(str(audio_path), sr=self.sample_rate, mono=True)
                
                audio_int16 = (audio_data * 32767).astype(np.int16)
                
                text_parts = []
                chunk_size = 4000
                for i in range(0, len(audio_int16), chunk_size):
                    chunk = audio_int16[i:i+chunk_size]
                    chunk_bytes = chunk.tobytes()
                    
                    if self._recognizer.AcceptWaveform(chunk_bytes):
                        result = json.loads(self._recognizer.Result())
                        if "text" in result:
                            text_parts.append(result["text"])
                
                final_result = json.loads(self._recognizer.FinalResult())
                if "text" in final_result:
                    text_parts.append(final_result["text"])
            else:
                wf = wave.open(str(audio_path), "rb")
                
                if wf.getnchannels() != 1:
                    logger.warning("Audio is not mono, conversion may be needed")
                if wf.getsampwidth() != 2:
                    logger.warning("Audio sample width is not 16-bit")
                if wf.getcomptype() != "NONE":
                    logger.warning("Audio is compressed")
                
                text_parts = []
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    
                    if self._recognizer.AcceptWaveform(data):
                        result = json.loads(self._recognizer.Result())
                        if "text" in result:
                            text_parts.append(result["text"])
                
                final_result = json.loads(self._recognizer.FinalResult())
                if "text" in final_result:
                    text_parts.append(final_result["text"])
                
                wf.close()
            
            text = " ".join(text_parts).strip()
            processing_time = time.time() - start_time
            
            return STTResult(
                text=text,
                confidence=None,  # Vosk ne retourne pas de confidence globale
                language="fr",
                processing_time=processing_time,
                metadata={
                    "model": "vosk",
                    "model_path": str(self.model_path)
                }
            )
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

