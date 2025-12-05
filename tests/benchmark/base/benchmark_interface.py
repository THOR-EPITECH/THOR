"""Interface commune pour les benchmarks."""

from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Résultat d'un benchmark pour un modèle.
    
    Attributes:
        model_name (str): Nom du modèle testé.
        model_size (str): Taille du modèle.
        transcription_time (float): Temps de transcription en secondes.
        memory_usage_mb (float): Utilisation mémoire en MB.
        cpu_percent (float): Utilisation CPU en pourcentage.
        text_length (int): Longueur du texte transcrit.
        confidence (float): Score de confiance (0.0 à 1.0).
        transcribed_text (str): Texte transcrit par le modèle.
        is_valid (bool): True si le benchmark a réussi.
        error_message (Optional[str]): Message d'erreur si échec.
    """
    model_name: str
    model_size: str
    transcription_time: float
    memory_usage_mb: float
    cpu_percent: float
    text_length: int
    confidence: float
    transcribed_text: str
    is_valid: bool
    error_message: Optional[str] = None


class BenchmarkInterface(ABC):
    """Interface commune pour tous les runners de benchmark."""
    
    @abstractmethod
    def run_benchmark(
        self,
        model_type: str,
        **kwargs
    ) -> BenchmarkResult:
        """Exécute un benchmark pour un modèle.
        
        Args:
            model_type (str): Type de modèle à benchmarker.
            **kwargs: Arguments additionnels spécifiques au benchmark.
        
        Returns:
            BenchmarkResult: Résultat du benchmark.
        """
        pass
    
    @abstractmethod
    def run_benchmarks(
        self,
        model_types: List[str],
        **kwargs
    ) -> List[BenchmarkResult]:
        """Exécute des benchmarks pour plusieurs modèles.
        
        Args:
            model_types (List[str]): Liste des types de modèles à benchmarker.
            **kwargs: Arguments additionnels spécifiques au benchmark.
        
        Returns:
            List[BenchmarkResult]: Liste des résultats de benchmark.
        """
        pass

