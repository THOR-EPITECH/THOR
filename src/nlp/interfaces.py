"""
Interfaces abstraites pour les modèles de traitement du langage naturel (NLP).

Ce module définit le contrat que doivent respecter tous les modèles NLP
(spaCy, Transformers, Regex, etc.) pour être intégrés dans le pipeline THOR.
"""
from pathlib import Path
from abc import ABC, abstractmethod
from src.common.types import NLPExtraction


class NLPModel(ABC):
    """
    Interface abstraite pour tous les modèles NLP.
    
    Cette classe définit les méthodes que chaque modèle NLP doit implémenter
    pour extraire les villes d'origine et de destination depuis un texte.
    Les modèles peuvent optionnellement implémenter l'entraînement.
    
    Attributes:
        config (dict): Configuration spécifique au modèle.
        _initialized (bool): Indique si le modèle a été initialisé.
        
    Example:
        >>> class CustomNLP(NLPModel):
        ...     def extract(self, text):
        ...         return NLPExtraction(origin="Paris", destination="Lyon")
        ...     def _load_model(self):
        ...         pass
    """
    
    def __init__(self, config: dict = None):
        """
        Initialise l'instance du modèle NLP.
        
        Args:
            config (dict, optional): Dictionnaire de configuration contenant
                les paramètres spécifiques au modèle (ex: model_name, custom_model_path).
        """
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination depuis un texte en langage naturel.
        
        Cette méthode doit être implémentée par chaque modèle concret.
        Elle analyse le texte et identifie les villes de départ et d'arrivée.
        
        Args:
            text (str): Texte à analyser (ex: "Je veux aller de Paris à Lyon").
        
        Returns:
            NLPExtraction: Objet contenant l'origine, la destination, la validité
                de l'extraction, et les entités détectées avec leurs métadonnées.
                
        Example:
            >>> model = SpacyFRModel()
            >>> result = model.extract("Je veux aller de Paris à Bordeaux")
            >>> print(result.origin, result.destination)
            Paris Bordeaux
        """
        pass
    
    def initialize(self):
        """
        Initialise le modèle (chargement des poids, vocabulaire).
        
        Cette méthode est appelée automatiquement lors de la première utilisation
        si le modèle n'a pas encore été initialisé.
        """
        if not self._initialized:
            self._load_model()
            self._initialized = True
    
    def _load_model(self):
        """
        Charge le modèle en mémoire.
        
        Cette méthode doit être implémentée par les sous-classes pour charger
        les ressources nécessaires (modèle spaCy, transformers, patterns regex, etc).
        """
        pass
    
    def train(self, train_dataset: str | Path, valid_dataset: str | Path = None, output_dir: str | Path = None):
        """
        Entraîne ou fine-tune le modèle sur un dataset personnalisé.
        
        Cette méthode est optionnelle et peut être implémentée par les modèles
        qui supportent l'entraînement (ex: transformers, spaCy).
        
        Args:
            train_dataset (str | Path): Chemin vers le dataset d'entraînement au format JSONL.
                Chaque ligne doit contenir un objet avec 'text', 'origin', 'destination'.
            valid_dataset (str | Path, optional): Chemin vers le dataset de validation (JSONL).
            output_dir (str | Path, optional): Dossier où sauvegarder le modèle entraîné.
                
        Note:
            Par défaut, cette méthode ne fait rien pour les modèles basés sur des règles
            qui ne nécessitent pas d'entraînement (ex: Regex, Dummy).
        """
        pass
    
    @property
    def name(self) -> str:
        """
        Retourne le nom du modèle.
        
        Returns:
            str: Nom de la classe du modèle (ex: "SpacyFRModel", "TransformersNER").
        """
        return self.__class__.__name__

