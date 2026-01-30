"""
Interfaces pour les modèles Pathfinding.
"""
from abc import ABC, abstractmethod
from src.common.types import Route


class PathfindingModel(ABC):
    """Interface pour tous les modèles Pathfinding."""
    
    def __init__(self, config: dict = None):
        """
        Initialise le modèle.
        
        Args:
            config: Configuration du modèle
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def find_route(self, origin: str, destination: str) -> Route:
        """
        Trouve un itinéraire entre deux villes.
        
        Args:
            origin: Ville de départ
            destination: Ville d'arrivée
        
        Returns:
            Route avec les étapes, distance, temps, etc.
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
