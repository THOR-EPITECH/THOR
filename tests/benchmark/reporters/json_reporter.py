"""Reporter JSON pour les benchmarks."""

import json
import time
from typing import List, Optional
from pathlib import Path
from dataclasses import asdict

from ..base.benchmark_interface import BenchmarkResult
from .reporter_interface import ReporterInterface


class JSONReporter(ReporterInterface):
    """Reporter qui génère des rapports au format JSON."""
    
    def __init__(self, test_audio_path: Optional[str] = None):
        """Initialise le reporter JSON.
        
        Args:
            test_audio_path (Optional[str]): Chemin vers le fichier audio de test.
        """
        self.test_audio_path = test_audio_path
    
    def generate_report(
        self,
        results: List[BenchmarkResult],
        **kwargs
    ) -> str:
        """Génère un rapport JSON.
        
        Args:
            results (List[BenchmarkResult]): Résultats des benchmarks.
            **kwargs: Arguments additionnels (ignorés pour JSON).
        
        Returns:
            str: Rapport formaté en JSON.
        """
        json_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "test_audio": self.test_audio_path,
            "results": [asdict(r) for r in results]
        }
        
        return json.dumps(json_data, indent=2, ensure_ascii=False)
    
    def save_report(
        self,
        results: List[BenchmarkResult],
        output_path: str,
        **kwargs
    ) -> str:
        """Sauvegarde le rapport JSON dans un fichier.
        
        Args:
            results (List[BenchmarkResult]): Résultats des benchmarks.
            output_path (str): Chemin du fichier de sortie.
            **kwargs: Arguments additionnels (ignorés).
        
        Returns:
            str: Chemin du fichier sauvegardé.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report(results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(output_file)

