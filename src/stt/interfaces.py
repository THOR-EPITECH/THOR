"""
Interfaces abstraites pour les modèles Speech-to-Text (STT).

Ce module définit le contrat que doivent respecter tous les modèles STT
(Whisper, Vosk, etc.) pour être intégrés dans le pipeline THOR.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from src.common.types import STTResult


class STTModel(ABC):
    """
    Interface abstraite pour tous les modèles de Speech-to-Text.
    
    Cette classe définit les méthodes que chaque modèle STT doit implémenter
    pour être compatible avec le pipeline. Les modèles concrets héritent de
    cette classe et implémentent la méthode transcribe() et _load_model().
    
    Attributes:
        config (dict): Configuration spécifique au modèle.
        _initialized (bool): Indique si le modèle a été initialisé.
        
    Example:
        >>> class CustomSTT(STTModel):
        ...     def transcribe(self, audio_path):
        ...         return STTResult(text="transcription")
        ...     def _load_model(self):
        ...         pass
    """
    
    def __init__(self, config: dict = None):
        """
        Initialise l'instance du modèle STT.
        
        Args:
            config (dict, optional): Dictionnaire de configuration contenant
                les paramètres spécifiques au modèle (ex: model_size, device).
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """
        Transcrit un fichier audio en texte.
        
        Cette méthode doit être implémentée par chaque modèle concret.
        
        Args:
            audio_path (str | Path): Chemin vers le fichier audio à transcrire.
                Formats supportés dépendent du modèle (généralement wav, mp3, flac).
        
        Returns:
            STTResult: Objet contenant le texte transcrit et les métadonnées
                (confiance, langue détectée, temps de traitement).
                
        Raises:
            FileNotFoundError: Si le fichier audio n'existe pas.
            Exception: Si la transcription échoue.
        """
        pass
    
    def initialize(self):
        """
        Initialise le modèle (chargement des poids, préparation).
        
        Cette méthode est appelée automatiquement lors de la première utilisation
        si le modèle n'a pas encore été initialisé. Elle évite les chargements multiples.
        """
        if not self._initialized:
            self._load_model()
            self._initialized = True
    
    def _load_model(self):
        """
        Charge le modèle en mémoire.
        
        Cette méthode doit être implémentée par les sous-classes pour charger
        les ressources nécessaires (poids du modèle, vocabulaire, etc).
        """
        pass
    
    @property
    def name(self) -> str:
        """
        Retourne le nom du modèle.
        
        Returns:
            str: Nom de la classe du modèle (ex: "WhisperModel", "VoskModel").
        """
        return self.__class__.__name__

