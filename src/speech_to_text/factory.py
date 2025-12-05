"""Factory pour créer des instances de modèles speech-to-text."""

from typing import Dict, Type
from .base.model_interface import SpeechToTextInterface
from .models.whisper_model import WhisperModel


class SpeechToTextFactory:
    """Factory pour créer des instances de modèles de reconnaissance vocale.
    
    Permet de créer facilement différents modèles de speech-to-text
    sans avoir à connaître les détails d'implémentation de chacun.
    """
    
    _models: Dict[str, Type[SpeechToTextInterface]] = {
        "whisper-tiny": WhisperModel,
        "whisper-base": WhisperModel,
        "whisper-small": WhisperModel,
        "whisper-medium": WhisperModel,
        "whisper-large": WhisperModel,
    }
    
    @classmethod
    def create(
        cls,
        model_type: str,
        **kwargs
    ) -> SpeechToTextInterface:
        """Crée une instance d'un modèle speech-to-text.
        
        Args:
            model_type (str): Type de modèle à créer.
                Options disponibles:
                - 'whisper-tiny': Whisper tiny (le plus rapide, moins précis)
                - 'whisper-base': Whisper base (bon compromis)
                - 'whisper-small': Whisper small (meilleure précision)
                - 'whisper-medium': Whisper medium (très bonne précision)
                - 'whisper-large': Whisper large (meilleure précision, plus lent)
            **kwargs: Arguments additionnels pour l'initialisation du modèle.
                Pour Whisper: model_size, device, model_path.
        
        Returns:
            SpeechToTextInterface: Instance du modèle.
        
        Raises:
            ValueError: Si le type de modèle est inconnu.
        
        Example:
            >>> # Créer un modèle Whisper base
            >>> model = SpeechToTextFactory.create("whisper-base")
            >>> result = model.transcribe("audio.wav")
            >>> print(result.text)
            
            >>> # Créer un modèle Whisper small avec device spécifique
            >>> model = SpeechToTextFactory.create(
            ...     "whisper-small",
            ...     device="cuda"
            ... )
        """
        if model_type not in cls._models:
            available = ", ".join(cls._models.keys())
            raise ValueError(
                f"Unknown model type: {model_type}. "
                f"Available models: {available}"
            )
        
        model_class = cls._models[model_type]
        
        if model_type.startswith("whisper-"):
            model_size = model_type.replace("whisper-", "")
            if "model_size" not in kwargs:
                kwargs["model_size"] = model_size
        
        return model_class(**kwargs)
    
    @classmethod
    def list_available_models(cls) -> list[str]:
        """Liste tous les modèles disponibles.
        
        Returns:
            list[str]: Liste des noms de modèles disponibles.
        
        Example:
            >>> models = SpeechToTextFactory.list_available_models()
            >>> print(models)
            ['whisper-tiny', 'whisper-base', 'whisper-small', ...]
        """
        return list(cls._models.keys())
    
    @classmethod
    def get_model_info(cls, model_type: str) -> dict:
        """Retourne des informations sur un modèle.
        
        Args:
            model_type (str): Type de modèle.
        
        Returns:
            dict: Informations sur le modèle (taille, type, etc.).
        
        Raises:
            ValueError: Si le type de modèle est inconnu.
        """
        if model_type not in cls._models:
            available = ", ".join(cls._models.keys())
            raise ValueError(
                f"Unknown model type: {model_type}. "
                f"Available: {available}"
            )
        
        info = {
            "model_type": model_type,
            "class": cls._models[model_type].__name__
        }
        
        if model_type.startswith("whisper-"):
            size = model_type.replace("whisper-", "")
            info.update({
                "model_family": "whisper",
                "model_size": size,
                "architecture": "transformer"
            })
        
        return info

