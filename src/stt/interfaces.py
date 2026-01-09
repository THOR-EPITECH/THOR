"""
Interfaces pour les modèles STT.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from src.common.types import STTResult


class STTModel(ABC):
    """Interface pour tous les modèles STT."""
    
    def __init__(self, config: dict = None):
        """
        Initialise le modèle.
        
        Args:
            config: Configuration du modèle
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def transcribe(self, audio_path: str | Path) -> STTResult:
        """
        Transcrit un fichier audio en texte.
        
        Args:
            audio_path: Chemin vers le fichier audio
        
        Returns:
            STTResult avec le texte transcrit
        """
        pass
    
    def initialize(self):
        """Initialise le modèle (chargement, etc.)."""
        if not self._initialized:
            self._load_model()
            self._initialized = True
    
    def _load_model(self):
        """Charge le modèle (à implémenter par les sous-classes)."""
        pass
    
    @property
    def name(self) -> str:
        """Retourne le nom du modèle."""
        return self.__class__.__name__

