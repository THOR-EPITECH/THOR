"""
Orchestrateur du pipeline complet : Audio → STT → NLP → Pathfinding.
"""
from pathlib import Path
from typing import Optional
from src.stt.interfaces import STTModel
from src.nlp.interfaces import NLPModel
from src.pathfinding.interfaces import PathfindingModel
from src.common.types import STTResult, NLPExtraction, Route
from src.common.logging import setup_logging

logger = setup_logging(module="pipeline")


class Pipeline:
    """
    Pipeline complet pour traiter une commande de voyage depuis un audio.
    
    Flux: Audio → STT → NLP → Pathfinding → Itinéraire
    """
    
    def __init__(self, stt_model: STTModel, nlp_model: NLPModel, pathfinding_model: Optional[PathfindingModel] = None):
        """
        Initialise le pipeline.
        
        Args:
            stt_model: Modèle STT pour la transcription
            nlp_model: Modèle NLP pour l'extraction
            pathfinding_model: Modèle Pathfinding pour trouver l'itinéraire (optionnel)
        """
        self.stt_model = stt_model
        self.nlp_model = nlp_model
        self.pathfinding_model = pathfinding_model
        self._initialized = False
    
    def initialize(self):
        """Initialise tous les modèles."""
        if not self._initialized:
            logger.info("Initializing pipeline models...")
            self.stt_model.initialize()
            self.nlp_model.initialize()
            if self.pathfinding_model:
                self.pathfinding_model.initialize()
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
        
        # Génère un message d'erreur si une ville manque
        error_message = None
        route = None
        
        if nlp_result.is_valid:
            if not nlp_result.origin and not nlp_result.destination:
                error_message = "❌ Erreur : Aucune ville détectée. Veuillez préciser une ville de départ et/ou d'arrivée."
            elif not nlp_result.origin:
                error_message = "⚠️ Attention : La ville de départ est manquante. Veuillez préciser d'où vous partez."
            elif not nlp_result.destination:
                error_message = "⚠️ Attention : La ville d'arrivée est manquante. Veuillez préciser votre destination."
            elif self.pathfinding_model and nlp_result.origin and nlp_result.destination:
                # Étape 3: Pathfinding
                logger.info("Step 3: Finding route...")
                route = self.pathfinding_model.find_route(nlp_result.origin, nlp_result.destination)
                if route.steps:
                    logger.info(f"Route found: {len(route.steps)} stations, {route.total_distance:.2f} km")
                else:
                    logger.warning("No route found")
        
        return {
            "audio_path": str(audio_path),
            "transcript": transcript,
            "origin": nlp_result.origin,
            "destination": nlp_result.destination,
            "is_valid": nlp_result.is_valid,
            "confidence": nlp_result.confidence,
            "error_message": error_message,
            "route": {
                "steps": route.steps if route else [],
                "total_distance": route.total_distance if route else None,
                "total_time": route.total_time if route else None,
                "metadata": route.metadata if route else {}
            } if route else None,
            "stt_metadata": stt_result.metadata,
            "nlp_metadata": {
                **nlp_result.metadata,
                "entities": nlp_result.entities,
            }
        }

