"""
Interfaces pour les modèles NLP.
"""
from pathlib import Path
from abc import ABC, abstractmethod
from src.common.types import NLPExtraction


class NLPModel(ABC):
    """Interface pour tous les modèles NLP."""
    
    def __init__(self, config: dict = None):
        """
        Initialise le modèle.
        
        Args:
            config: Configuration du modèle
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination depuis un texte.
        
        Args:
            text: Texte à analyser
        
        Returns:
            NLPExtraction avec origine, destination, is_valid
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
    
    def train(self, train_dataset: str | Path, valid_dataset: str | Path = None, output_dir: str | Path = None):
        """
        Entraîne le modèle sur un dataset.
        
        Args:
            train_dataset: Chemin vers le dataset d'entraînement (JSONL)
            valid_dataset: Chemin vers le dataset de validation (JSONL, optionnel)
            output_dir: Dossier où sauvegarder le modèle entraîné
        """
        # Par défaut, ne fait rien (pour les modèles qui ne nécessitent pas d'entraînement)
        pass
    
    @property
    def name(self) -> str:
        """Retourne le nom du modèle."""
        return self.__class__.__name__

