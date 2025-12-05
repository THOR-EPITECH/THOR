"""Reporter Markdown pour les benchmarks."""

import time
from typing import List, Optional
from pathlib import Path

from ..base.benchmark_interface import BenchmarkResult
from .reporter_interface import ReporterInterface


class MarkdownReporter(ReporterInterface):
    """Reporter qui génère des rapports au format Markdown."""
    
    def __init__(self, test_audio_path: Optional[str] = None):
        """Initialise le reporter Markdown.
        
        Args:
            test_audio_path (Optional[str]): Chemin vers le fichier audio de test.
        """
        self.test_audio_path = test_audio_path
    
    def generate_report(
        self,
        results: List[BenchmarkResult],
        **kwargs
    ) -> str:
        """Génère un rapport Markdown.
        
        Args:
            results (List[BenchmarkResult]): Résultats des benchmarks.
            **kwargs: Arguments additionnels (ignorés pour Markdown).
        
        Returns:
            str: Rapport formaté en Markdown.
        """
        valid_results = [r for r in results if r.is_valid]
        
        if not valid_results:
            return "# Rapport de Benchmark Whisper\n\nAucun résultat valide.\n"
        
        report = "# Rapport de Benchmark Whisper\n\n"
        report += f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if self.test_audio_path:
            report += f"**Source**: Fichier audio (`{self.test_audio_path}`)\n\n"
        else:
            report += "**Source**: Microphone\n\n"
        
        report += f"**Modèles testés**: {len(results)} | **Réussis**: {len(valid_results)} | **Échoués**: {len(results) - len(valid_results)}\n\n"
        
        report += "## Résultats\n\n"
        report += "| Modèle | Taille | Temps (s) | Mémoire (MB) | CPU (%) | Confiance | Texte |\n"
        report += "|--------|--------|-----------|--------------|---------|-----------|-------|\n"
        
        for result in valid_results:
            text_preview = result.transcribed_text[:30] + "..." if len(result.transcribed_text) > 30 else result.transcribed_text
            report += (
                f"| {result.model_name} | {result.model_size} | "
                f"{result.transcription_time:.2f} | "
                f"{result.memory_usage_mb:.2f} | "
                f"{result.cpu_percent:.1f} | "
                f"{result.confidence:.2%} | "
                f"`{text_preview}` |\n"
            )
        
        failed_results = [r for r in results if not r.is_valid]
        if failed_results:
            report += "\n### Modèles ayant échoué\n\n"
            for result in failed_results:
                report += f"- **{result.model_name}**: {result.error_message}\n"
            report += "\n"
        
        if len(valid_results) > 1:
            report += self._generate_comparison(valid_results)
        
        if len(valid_results) > 0:
            report += "\n## Transcriptions\n\n"
            for result in valid_results:
                if result.transcribed_text:
                    report += f"### {result.model_name}\n\n"
                    report += f"> {result.transcribed_text}\n\n"
            
            report += "\n## Statistiques détaillées\n\n"
            for result in valid_results:
                report += self._generate_details(result)
        
        if len(failed_results) > 0:
            report += "\n## Erreurs\n\n"
            for result in failed_results:
                report += self._generate_error_details(result)
        
        return report
    
    def _generate_comparison(self, results: List[BenchmarkResult]) -> str:
        """Génère la section de comparaison.
        
        Args:
            results (List[BenchmarkResult]): Résultats valides.
        
        Returns:
            str: Section de comparaison en Markdown.
        """
        if len(results) < 2:
            return ""
        
        comparison = "\n## Comparaison\n\n"
        
        fastest = min(results, key=lambda x: x.transcription_time)
        slowest = max(results, key=lambda x: x.transcription_time)
        most_efficient = min(results, key=lambda x: x.memory_usage_mb)
        least_efficient = max(results, key=lambda x: x.memory_usage_mb)
        most_confident = max(results, key=lambda x: x.confidence)
        least_confident = min(results, key=lambda x: x.confidence)
        
        comparison += "### Performance\n\n"
        comparison += f"- **Plus rapide**: `{fastest.model_name}` ({fastest.transcription_time:.2f}s)\n"
        comparison += f"- **Plus lent**: `{slowest.model_name}` ({slowest.transcription_time:.2f}s)\n"
        comparison += f"- **Différence**: {slowest.transcription_time - fastest.transcription_time:.2f}s ({((slowest.transcription_time / fastest.transcription_time - 1) * 100):.1f}% plus lent)\n\n"
        
        comparison += "### Mémoire\n\n"
        comparison += f"- **Moins de mémoire**: `{most_efficient.model_name}` ({most_efficient.memory_usage_mb:.2f} MB)\n"
        comparison += f"- **Plus de mémoire**: `{least_efficient.model_name}` ({least_efficient.memory_usage_mb:.2f} MB)\n"
        comparison += f"- **Différence**: {least_efficient.memory_usage_mb - most_efficient.memory_usage_mb:.2f} MB\n\n"
        
        comparison += "### Précision\n\n"
        comparison += f"- **Meilleure confiance**: `{most_confident.model_name}` ({most_confident.confidence:.2%})\n"
        comparison += f"- **Moins bonne confiance**: `{least_confident.model_name}` ({least_confident.confidence:.2%})\n"
        comparison += f"- **Différence**: {(most_confident.confidence - least_confident.confidence) * 100:.1f} points de pourcentage\n\n"
        
        comparison += "### Recommandation\n\n"
        if fastest == most_efficient and fastest == most_confident:
            comparison += f"**Modèle optimal**: `{fastest.model_name}` (meilleur sur tous les critères)\n"
        else:
            comparison += "- Pour la **vitesse**: `" + fastest.model_name + "`\n"
            comparison += "- Pour la **mémoire**: `" + most_efficient.model_name + "`\n"
            comparison += "- Pour la **précision**: `" + most_confident.model_name + "`\n"
        
        return comparison
    
    def _generate_details(self, result: BenchmarkResult) -> str:
        """Génère les détails pour un résultat valide.
        
        Args:
            result (BenchmarkResult): Résultat du benchmark.
        
        Returns:
            str: Détails formatés en Markdown.
        """
        details = f"### {result.model_name} ({result.model_size})\n\n"
        
        details += "**Performance**\n"
        details += f"- ⏱️ Temps de transcription: `{result.transcription_time:.2f}s`\n"
        details += f"- 💾 Utilisation mémoire: `{result.memory_usage_mb:.2f} MB`\n"
        details += f"- 🔄 Utilisation CPU: `{result.cpu_percent:.1f}%`\n\n"
        
        details += "**Qualité**\n"
        details += f"- ✅ Confiance: `{result.confidence:.2%}`\n"
        details += f"- 📝 Longueur texte: `{result.text_length} caractères`\n\n"
        
        if result.transcribed_text:
            details += "**Texte transcrit**\n"
            details += f"> {result.transcribed_text}\n\n"
        
        return details
    
    def _generate_error_details(self, result: BenchmarkResult) -> str:
        """Génère les détails pour un résultat en erreur.
        
        Args:
            result (BenchmarkResult): Résultat du benchmark en erreur.
        
        Returns:
            str: Détails d'erreur formatés en Markdown.
        """
        details = f"### ❌ {result.model_name}\n\n"
        details += f"**Erreur**: `{result.error_message}`\n\n"
        
        if "SSL" in result.error_message or "certificate" in result.error_message.lower():
            details += "**Solution**: Le problème SSL a été corrigé dans le runner.\n"
            details += "Relancez le benchmark pour tester ce modèle.\n\n"
        
        return details
    
    def save_report(
        self,
        results: List[BenchmarkResult],
        output_path: str,
        **kwargs
    ) -> str:
        """Sauvegarde le rapport Markdown dans un fichier.
        
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

