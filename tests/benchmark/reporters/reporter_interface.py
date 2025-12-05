"""Interface commune pour les reporters de benchmark."""

from abc import ABC, abstractmethod
from typing import List
from ..base.benchmark_interface import BenchmarkResult


class ReporterInterface(ABC):
    """Interface commune pour tous les reporters de benchmark."""
    
    @abstractmethod
    def generate_report(
        self,
        results: List[BenchmarkResult],
        **kwargs
    ) -> str:
        """Génère un rapport à partir des résultats de benchmark.
        
        Args:
            results (List[BenchmarkResult]): Résultats des benchmarks.
            **kwargs: Arguments additionnels pour la génération.
        
        Returns:
            str: Rapport généré.
        """
        pass
    
    @abstractmethod
    def save_report(
        self,
        results: List[BenchmarkResult],
        output_path: str,
        **kwargs
    ) -> str:
        """Sauvegarde un rapport dans un fichier.
        
        Args:
            results (List[BenchmarkResult]): Résultats des benchmarks.
            output_path (str): Chemin du fichier de sortie.
            **kwargs: Arguments additionnels pour la sauvegarde.
        
        Returns:
            str: Chemin du fichier sauvegardé.
        """
        pass

