"""
Orchestrateur du pipeline complet : Audio → STT → NLP → Extraction.
"""
from pathlib import Path
from typing import Optional
from src.stt.interfaces import STTModel
from src.nlp.interfaces import NLPModel
from src.common.types import STTResult, NLPExtraction
from src.common.logging import setup_logging

logger = setup_logging(module="pipeline")


class Pipeline:
    """
    Pipeline complet pour traiter une commande de voyage depuis un audio.
    
    Flux: Audio → STT → NLP → Origine/Destination
    """
    
    def __init__(self, stt_model: STTModel, nlp_model: NLPModel):
        """
        Initialise le pipeline.
        
        Args:
            stt_model: Modèle STT pour la transcription
            nlp_model: Modèle NLP pour l'extraction
        """
        self.stt_model = stt_model
        self.nlp_model = nlp_model
        self._initialized = False
    
    def initialize(self):
        """Initialise tous les modèles."""
        if not self._initialized:
            logger.info("Initializing pipeline models...")
            self.stt_model.initialize()
            self.nlp_model.initialize()
            self._initialized = True
            logger.info("Pipeline initialized")
    
    def process(self, audio_path: str | Path) -> dict:
        """
        Traite un fichier audio complet : transcription → extraction.
        
        Args:
            audio_path: Chemin vers le fichier audio
        
        Returns:
            Dictionnaire avec transcription, origine, destination, is_valid
        """
        if not self._initialized:
            self.initialize()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Processing audio: {audio_path}")
        
        # Étape 1: Transcription STT
        logger.info("Step 1: Transcribing audio...")
        stt_result = self.stt_model.transcribe(audio_path)
        transcript = stt_result.text
        
        logger.info(f"Transcription: {transcript}")
        
        # Étape 2: Extraction NLP
        logger.info("Step 2: Extracting origin/destination...")
        nlp_result = self.nlp_model.extract(transcript)
        
        logger.info(f"Extraction: {nlp_result.origin} → {nlp_result.destination}")
        
        return {
            "audio_path": str(audio_path),
            "transcript": transcript,
            "origin": nlp_result.origin,
            "destination": nlp_result.destination,
            "is_valid": nlp_result.is_valid,
            "confidence": nlp_result.confidence,
            "stt_metadata": stt_result.metadata,
            "nlp_metadata": {
                **nlp_result.metadata,
                "entities": nlp_result.entities,
            }
        }

