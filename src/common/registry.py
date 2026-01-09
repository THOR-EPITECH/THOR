"""
Système de registre pour les modèles (pattern plugin).
"""
from typing import Dict, Type, Any, Optional
import importlib


class ModelRegistry:
    """Registre centralisé des modèles."""
    
    _registry: Dict[str, Dict[str, Type]] = {
        "stt": {},
        "nlp": {},
        "pathfinding": {}
    }
    
    @classmethod
    def register(cls, module_type: str, model_name: str, model_class: Type):
        """
        Enregistre un modèle.
        
        Args:
            module_type: Type de module ('stt', 'nlp', 'pathfinding')
            model_name: Nom du modèle
            model_class: Classe du modèle
        """
        if module_type not in cls._registry:
            raise ValueError(f"Module type '{module_type}' not supported")
        
        cls._registry[module_type][model_name] = model_class
    
    @classmethod
    def get(cls, module_type: str, model_name: str) -> Optional[Type]:
        """
        Récupère une classe de modèle.
        
        Args:
            module_type: Type de module
            model_name: Nom du modèle
        
        Returns:
            Classe du modèle ou None
        """
        return cls._registry.get(module_type, {}).get(model_name)
    
    @classmethod
    def list_models(cls, module_type: str) -> list[str]:
        """
        Liste les modèles disponibles pour un module.
        
        Args:
            module_type: Type de module
        
        Returns:
            Liste des noms de modèles
        """
        return list(cls._registry.get(module_type, {}).keys())
    
    @classmethod
    def load_from_module(cls, module_path: str, module_type: str, model_name: str):
        """
        Charge un modèle depuis un module Python.
        
        Args:
            module_path: Chemin du module (ex: 'src.stt.models.whisper')
            module_type: Type de module
            model_name: Nom du modèle
        """
        try:
            module = importlib.import_module(module_path)
            model_class = getattr(module, model_name)
            cls.register(module_type, model_name.lower(), model_class)
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load model {model_name} from {module_path}: {e}")

