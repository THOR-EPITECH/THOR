"""
Modèle STT dummy pour tests et baseline.
"""
import time
from pathlib import Path
from src.stt.interfaces import STTModel
from src.common.types import STTResult
from src.common.audio import get_audio_info


class DummySTTModel(STTModel):
    """
    Modèle STT baseline qui retourne soit le texte vide,
    soit répète une partie du nom du fichier.
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.mode = self.config.get("mode", "empty")  # "empty" ou "repeat"
    
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """
        Transcrit (simule) un fichier audio.
        
        Args:
            audio_path: Chemin vers le fichier audio
        
        Returns:
            STTResult avec texte vide ou répété
        """
        audio_path = Path(audio_path)
        start_time = time.time()
        
        time.sleep(0.1)
        
        if self.mode == "empty":
            text = ""
        elif self.mode == "repeat":
            text = audio_path.stem
        else:
            text = ""
        
        processing_time = time.time() - start_time
        
        return STTResult(
            text=text,
            confidence=0.0,
            processing_time=processing_time,
            metadata={
                "model": "dummy",
                "mode": self.mode
            }
        )

