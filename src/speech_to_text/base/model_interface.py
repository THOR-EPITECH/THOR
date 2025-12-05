"""Interface commune pour tous les modèles de speech-to-text."""

from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TranscriptionResult:
    """Résultat de transcription audio en texte.
    
    Attributes:
        text (str): Texte transcrit depuis l'audio.
        language (Optional[str]): Langue détectée (code ISO, ex: 'fr').
        confidence (float): Score de confiance de la transcription (0.0 à 1.0).
        segments (Optional[list[dict]]): Segments temporels si disponibles.
        is_valid (bool): True si la transcription est valide.
        error_message (Optional[str]): Message d'erreur si la transcription a échoué.
    """
    text: str
    language: Optional[str]
    confidence: float
    segments: Optional[list[dict]] = None
    is_valid: bool = True
    error_message: Optional[str] = None


class SpeechToTextInterface(ABC):
    """Interface commune pour tous les modèles de speech-to-text.
    
    Tous les modèles de reconnaissance vocale doivent implémenter
    cette interface pour permettre la comparaison et le benchmarking.
    """
    
    @abstractmethod
    def transcribe(
        self, 
        audio_path: str | Path,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit un fichier audio en texte.
        
        Args:
            audio_path (str | Path): Chemin vers le fichier audio.
            language (Optional[str], optional): Code langue ISO (ex: 'fr', 'en').
                Si None, le modèle détecte automatiquement la langue.
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        
        Raises:
            FileNotFoundError: Si le fichier audio n'existe pas.
            ValueError: Si le format audio n'est pas supporté.
        """
        pass
    
    @abstractmethod
    def transcribe_from_bytes(
        self,
        audio_bytes: bytes,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit des données audio brutes en texte.
        
        Args:
            audio_bytes (bytes): Données audio brutes.
            sample_rate (int): Taux d'échantillonnage en Hz. Defaults to 16000.
            language (Optional[str], optional): Code langue ISO.
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Retourne le nom du modèle.
        
        Returns:
            str: Nom du modèle (ex: 'whisper-base', 'whisper-small').
        """
        pass
    
    @property
    @abstractmethod
    def model_type(self) -> str:
        """Retourne le type du modèle.
        
        Returns:
            str: Type du modèle (ex: 'transformer', 'hmm', 'cloud').
        """
        pass
    
    @property
    @abstractmethod
    def supported_languages(self) -> list[str]:
        """Retourne la liste des langues supportées.
        
        Returns:
            list[str]: Liste des codes langue ISO supportés.
        """
        pass
    
    @property
    @abstractmethod
    def supported_formats(self) -> list[str]:
        """Retourne la liste des formats audio supportés.
        
        Returns:
            list[str]: Liste des extensions supportées (ex: ['.wav', '.mp3']).
        """
        pass
    
    def transcribe_from_microphone(
        self,
        duration: float = 5.0,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit l'audio capturé depuis le microphone en temps réel.
        
        Args:
            duration (float): Durée d'enregistrement en secondes. Defaults to 5.0.
            sample_rate (int): Taux d'échantillonnage en Hz. Defaults to 16000.
            language (Optional[str], optional): Code langue ISO.
                Defaults to None.
        
        Returns:
            TranscriptionResult: Résultat de la transcription.
        
        Note:
            Cette méthode est optionnelle. Si un modèle ne la supporte pas,
            il peut lever NotImplementedError.
        """
        raise NotImplementedError(
            f"Le modèle {self.model_name} ne supporte pas encore "
            "la transcription depuis le microphone"
        )

