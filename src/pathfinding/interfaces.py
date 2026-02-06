"""
Interfaces abstraites pour les modèles de recherche d'itinéraire (Pathfinding).

Ce module définit le contrat que doivent respecter tous les algorithmes de pathfinding
(Dijkstra, A*, etc.) pour être intégrés dans le pipeline THOR.
"""
from abc import ABC, abstractmethod
from src.common.types import Route


class PathfindingModel(ABC):
    """
    Interface abstraite pour tous les modèles de pathfinding.
    
    Cette classe définit les méthodes que chaque algorithme de recherche d'itinéraire
    doit implémenter pour calculer le meilleur chemin entre deux villes.
    
    Attributes:
        config (dict): Configuration spécifique au modèle.
        _initialized (bool): Indique si le modèle a été initialisé.
        
    Example:
        >>> class CustomPathfinding(PathfindingModel):
        ...     def find_route(self, origin, destination):
        ...         return Route(origin=origin, destination=destination, steps=[origin, destination])
        ...     def _load_model(self):
        ...         pass
    """
    
    def __init__(self, config: dict = None):
        """
        Initialise l'instance du modèle de pathfinding.
        
        Args:
            config (dict, optional): Dictionnaire de configuration contenant
                les paramètres spécifiques (ex: data_path, use_time_weights).
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def find_route(self, origin: str, destination: str) -> Route:
        """
        Calcule l'itinéraire optimal entre deux villes.
        
        Cette méthode doit être implémentée par chaque modèle concret.
        Elle utilise le graphe ferroviaire pour trouver le meilleur chemin.
        
        Args:
            origin (str): Ville ou gare de départ (ex: "Paris", "Lyon").
            destination (str): Ville ou gare d'arrivée (ex: "Marseille").
        
        Returns:
            Route: Objet contenant les étapes de l'itinéraire, la distance totale,
                le temps de trajet estimé, et les métadonnées (segments, coordonnées).
                
        Example:
            >>> model = DijkstraModel()
            >>> route = model.find_route("Paris", "Lyon")
            >>> print(route.steps)
            ['Paris', 'Dijon', 'Lyon']
            >>> print(route.total_distance)
            462.5
        """
        pass
    
    def initialize(self):
        """
        Initialise le modèle (chargement du graphe, données GTFS).
        
        Cette méthode est appelée automatiquement lors de la première utilisation
        si le modèle n'a pas encore été initialisé. Elle charge les données nécessaires
        pour le calcul d'itinéraire.
        """
        if not self._initialized:
            self._load_model()
            self._initialized = True
    
    def _load_model(self):
        """
        Charge les données nécessaires au pathfinding.
        
        Cette méthode doit être implémentée par les sous-classes pour charger
        le graphe ferroviaire, les gares, et les liaisons depuis les fichiers de données.
        """
        pass
    
    @property
    def name(self) -> str:
        """
        Retourne le nom du modèle.
        
        Returns:
            str: Nom de la classe du modèle (ex: "DijkstraModel", "AStarModel").
        """
        return self.__class__.__name__
