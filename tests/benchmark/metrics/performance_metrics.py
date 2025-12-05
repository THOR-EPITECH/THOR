"""Métriques de performance pour mesurer les benchmarks."""

import time
import psutil
import os
from typing import Optional
from contextlib import contextmanager


class PerformanceMetrics:
    """Classe pour mesurer les performances système."""
    
    def __init__(self):
        """Initialise les métriques de performance."""
        self.process = psutil.Process(os.getpid())
    
    @contextmanager
    def measure(self):
        """Context manager pour mesurer les performances.
        
        Yields:
            dict: Dictionnaire avec les métriques mesurées.
        
        Example:
            >>> metrics = PerformanceMetrics()
            >>> with metrics.measure() as m:
            ...     # Code à mesurer
            ...     pass
            >>> print(f"Temps: {m['time']}s, Mémoire: {m['memory']}MB")
        """
        start_time = time.time()
        start_memory = self.process.memory_info().rss / 1024 / 1024
        start_cpu = self.process.cpu_percent()
        
        metrics = {}
        
        try:
            yield metrics
        finally:
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024
            end_cpu = self.process.cpu_percent()
            
            metrics['time'] = end_time - start_time
            metrics['memory'] = end_memory - start_memory
            metrics['cpu'] = (start_cpu + end_cpu) / 2 if start_cpu > 0 else end_cpu
    
    def get_current_memory(self) -> float:
        """Retourne l'utilisation mémoire actuelle en MB.
        
        Returns:
            float: Mémoire utilisée en MB.
        """
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_current_cpu(self) -> float:
        """Retourne l'utilisation CPU actuelle en pourcentage.
        
        Returns:
            float: Utilisation CPU en pourcentage.
        """
        return self.process.cpu_percent()

