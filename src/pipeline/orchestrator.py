"""
Orchestrateur du pipeline complet THOR : Audio → STT → NLP → Pathfinding.

Ce module coordonne l'exécution séquentielle des trois étapes principales du système :
1. Transcription audio (STT)
2. Extraction des entités (NLP)
3. Calcul d'itinéraire (Pathfinding)
"""
from pathlib import Path
from typing import Optional
from src.stt.interfaces import STTModel
from src.nlp.interfaces import NLPModel
from src.pathfinding.interfaces import PathfindingModel
from src.common.types import STTResult, NLPExtraction, Route
from src.common.logging import setup_logging
from src.common.validators import ExtractionValidator

logger = setup_logging(module="pipeline")


class Pipeline:
    """
    Orchestrateur du pipeline end-to-end THOR.
    
    Cette classe coordonne l'exécution séquentielle des modèles STT, NLP et Pathfinding
    pour transformer une requête vocale en itinéraire ferroviaire complet.
    
    Le flux d'exécution est le suivant:
        Audio fichier → Transcription (STT) → Extraction origine/destination (NLP) →
        Calcul itinéraire (Pathfinding) → Résultat complet
    
    Attributes:
        stt_model (STTModel): Modèle de transcription audio.
        nlp_model (NLPModel): Modèle d'extraction NLP.
        pathfinding_model (Optional[PathfindingModel]): Modèle de pathfinding (optionnel).
        _initialized (bool): Indique si tous les modèles sont initialisés.
        
    Example:
        >>> from src.stt.models.whisper import WhisperModel
        >>> from src.nlp.models.spacy_fr import SpacyFRModel
        >>> from src.pathfinding.models.dijkstra import DijkstraModel
        >>> 
        >>> pipeline = Pipeline(
        ...     stt_model=WhisperModel({"model_size": "small"}),
        ...     nlp_model=SpacyFRModel(),
        ...     pathfinding_model=DijkstraModel()
        ... )
        >>> result = pipeline.process("audio.wav")
        >>> print(result["origin"], "→", result["destination"])
    """
    
    def __init__(self, stt_model: STTModel, nlp_model: NLPModel, pathfinding_model: Optional[PathfindingModel] = None):
        """
        Initialise le pipeline avec les modèles spécifiés.
        
        Args:
            stt_model (STTModel): Instance du modèle STT à utiliser (Whisper, Vosk, etc).
            nlp_model (NLPModel): Instance du modèle NLP à utiliser (spaCy, Transformers, etc).
            pathfinding_model (Optional[PathfindingModel], optional): Instance du modèle
                de pathfinding (Dijkstra, A*, etc). Si None, seule l'extraction NLP est effectuée.
        """
        self.stt_model = stt_model
        self.nlp_model = nlp_model
        self.pathfinding_model = pathfinding_model
        self._initialized = False
        self.validator = ExtractionValidator()
    
    def initialize(self):
        """
        Initialise tous les modèles du pipeline.
        
        Cette méthode charge tous les modèles en mémoire. Elle est appelée automatiquement
        lors de la première utilisation du pipeline si elle n'a pas été appelée explicitement.
        
        Note:
            L'initialisation peut prendre du temps selon les modèles (téléchargement, chargement).
        """
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
        Traite un fichier audio de bout en bout et retourne l'itinéraire complet.
        
        Cette méthode orchestre les trois étapes du pipeline:
        1. Transcription de l'audio en texte (STT)
        2. Extraction de l'origine et destination (NLP)
        3. Calcul de l'itinéraire optimal (Pathfinding)
        
        Args:
            audio_path (str | Path): Chemin vers le fichier audio contenant la requête vocale.
                Formats supportés: WAV, MP3, FLAC, etc (selon le modèle STT).
        
        Returns:
            dict: Dictionnaire contenant:
                - audio_path (str): Chemin du fichier audio traité
                - transcript (str): Texte transcrit
                - origin (str|None): Ville de départ extraite
                - destination (str|None): Ville d'arrivée extraite
                - is_valid (bool): Validité de l'extraction NLP
                - confidence (float|None): Score de confiance NLP
                - error_message (str|None): Message d'erreur si applicable
                - route (dict|None): Détails de l'itinéraire si trouvé
                - stt_metadata (dict): Métadonnées du modèle STT
                - nlp_metadata (dict): Métadonnées du modèle NLP
                
        Raises:
            FileNotFoundError: Si le fichier audio n'existe pas.
            
        Example:
            >>> result = pipeline.process("requete.wav")
            >>> if result["route"]:
            ...     print(f"Itinéraire: {' → '.join(result['route']['steps'])}")
            ...     print(f"Distance: {result['route']['total_distance']} km")
        """
        if not self._initialized:
            self.initialize()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Processing audio: {audio_path}")
        
        logger.info("Step 1: Transcribing audio...")
        stt_result = self.stt_model.transcribe(audio_path)
        transcript = stt_result.text
        
        logger.info(f"Transcription: {transcript}")
        
        logger.info("Step 2: Extracting origin/destination...")
        nlp_result = self.nlp_model.extract(transcript)
        
        logger.info(f"Extraction: {nlp_result.origin} → {nlp_result.destination}")
        
        validation = self.validator.validate_extraction(
            transcript=transcript,
            origin=nlp_result.origin,
            destination=nlp_result.destination,
            nlp_confidence=nlp_result.confidence or 0.5
        )
        
        error_message = None
        error_type = None
        suggestions = []
        issues = []
        route = None
        
        corrected_origin = validation.get("corrected_origin") or nlp_result.origin
        corrected_destination = validation.get("corrected_destination") or nlp_result.destination
        
        if not validation["is_valid"]:
            error_type = validation.get("error_type")
            error_message = validation.get("error_message")
            suggestions = validation.get("suggestions", [])
            issues = validation.get("issues", [])
            
            logger.warning(f"Validation failed: {error_message}")
            logger.warning(f"Issues: {issues}")
            logger.info(f"Suggestions: {suggestions}")
        elif self.pathfinding_model and corrected_origin and corrected_destination:
            logger.info("Step 3: Finding route...")
            try:
                route = self.pathfinding_model.find_route(corrected_origin, corrected_destination)
                if route.steps:
                    logger.info(f"Route found: {len(route.steps)} stations, {route.total_distance:.2f} km")
                else:
                    logger.warning("No route found")
                    error_type = "no_route_found"
                    error_message = f"Aucun itinéraire trouvé entre {corrected_origin} et {corrected_destination}"
                    suggestions = [
                        "Vérifiez que ces villes sont bien desservies par le train",
                        "Essayez avec des villes plus importantes (gares principales)"
                    ]
            except Exception as e:
                logger.error(f"Pathfinding error: {e}")
                error_type = "pathfinding_error"
                error_message = "Erreur lors de la recherche d'itinéraire"
                suggestions = ["Réessayez avec d'autres villes"]
        
        return {
            "audio_path": str(audio_path),
            "transcript": transcript,
            "origin": corrected_origin,
            "destination": corrected_destination,
            "is_valid": validation["is_valid"],
            "confidence": validation.get("confidence", nlp_result.confidence),
            "error_message": error_message,
            "error_type": error_type,
            "suggestions": suggestions,
            "issues": issues,
            "validation_details": {
                "transcript_valid": validation.get("confidence", 0) > 0.4,
                "origin_validation": validation.get("origin_validation"),
                "destination_validation": validation.get("destination_validation")
            },
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

