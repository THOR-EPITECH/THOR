"""Runner de benchmark pour les modèles Whisper."""

import sys
import ssl
import numpy as np
import tempfile
from pathlib import Path
from typing import Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from src.speech_to_text.factory import SpeechToTextFactory
from ..base.benchmark_interface import BenchmarkInterface, BenchmarkResult
from ..metrics.performance_metrics import PerformanceMetrics


class WhisperBenchmarkRunner(BenchmarkInterface):
    """Runner de benchmark pour les modèles Whisper."""
    
    def __init__(self, test_audio_path: Optional[str] = None):
        """Initialise le runner de benchmark.
        
        Args:
            test_audio_path (Optional[str]): Chemin vers un fichier audio de test.
                Si None, utilise l'enregistrement microphone.
        """
        self.test_audio_path = test_audio_path
        self.metrics = PerformanceMetrics()
        self.cached_audio = None
        self.cached_audio_path = None
    
    def run_benchmark(
        self,
        model_type: str,
        duration: float = 5.0,
        language: str = "fr"
    ) -> BenchmarkResult:
        """Exécute un benchmark pour un modèle Whisper.
        
        Args:
            model_type (str): Type de modèle (whisper-tiny, whisper-base, etc.).
            duration (float): Durée d'enregistrement si utilisation microphone.
            language (str): Langue pour la transcription.
        
        Returns:
            BenchmarkResult: Résultat du benchmark.
        """
        print(f"\n{'='*60}")
        print(f"Benchmark: {model_type}")
        print(f"{'='*60}")
        
        try:
            with self.metrics.measure() as m:
                model = SpeechToTextFactory.create(model_type)
                
                if self.test_audio_path and Path(self.test_audio_path).exists():
                    audio_to_use = self.test_audio_path
                elif self.cached_audio_path and Path(self.cached_audio_path).exists():
                    audio_to_use = self.cached_audio_path
                else:
                    audio_to_use = None
                
                if audio_to_use:
                    result = model.transcribe(audio_to_use, language=language)
                else:
                    print(f"Enregistrement de {duration} secondes...")
                    result = model.transcribe_from_microphone(
                        duration=duration,
                        language=language
                    )
            
            transcribed_text = result.text if result.is_valid else ""
            text_length = len(transcribed_text)
            
            return BenchmarkResult(
                model_name=model.model_name,
                model_size=model_type.replace("whisper-", ""),
                transcription_time=m['time'],
                memory_usage_mb=m['memory'],
                cpu_percent=m['cpu'],
                text_length=text_length,
                confidence=result.confidence if result.is_valid else 0.0,
                transcribed_text=transcribed_text,
                is_valid=result.is_valid,
                error_message=result.error_message if not result.is_valid else None
            )
        
        except Exception as e:
            return BenchmarkResult(
                model_name=model_type,
                model_size=model_type.replace("whisper-", ""),
                transcription_time=0.0,
                memory_usage_mb=0.0,
                cpu_percent=0.0,
                text_length=0,
                confidence=0.0,
                transcribed_text="",
                is_valid=False,
                error_message=str(e)
            )
    
    def _record_audio_once(self, duration: float, sample_rate: int = 16000) -> str:
        """Enregistre l'audio une seule fois et le sauvegarde temporairement.
        
        Args:
            duration (float): Durée d'enregistrement en secondes.
            sample_rate (int): Taux d'échantillonnage.
        
        Returns:
            str: Chemin vers le fichier audio temporaire.
        """
        try:
            import sounddevice as sd
        except ImportError:
            raise ImportError("sounddevice n'est pas installé")
        
        print(f"\n🎤 Enregistrement unique de {duration} secondes...")
        print("   Parlez maintenant (cet enregistrement sera utilisé pour tous les modèles)...")
        
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        
        print("✓ Enregistrement terminé\n")
        
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.wav',
            delete=False
        )
        temp_path = temp_file.name
        temp_file.close()
        
        import soundfile as sf
        sf.write(temp_path, audio_data, sample_rate)
        
        return temp_path
    
    def run_benchmarks(
        self,
        model_types: List[str],
        duration: float = 5.0,
        language: str = "fr"
    ) -> List[BenchmarkResult]:
        """Exécute des benchmarks pour plusieurs modèles Whisper.
        
        Args:
            model_types (List[str]): Liste des types de modèles à benchmarker.
            duration (float): Durée d'enregistrement si utilisation microphone.
            language (str): Langue pour la transcription.
        
        Returns:
            List[BenchmarkResult]: Liste des résultats de benchmark.
        """
        print(f"\n{'='*60}")
        print("BENCHMARK DES MODÈLES WHISPER")
        print(f"{'='*60}")
        print(f"Modèles à tester: {len(model_types)}")
        
        if self.test_audio_path:
            print(f"Fichier audio: {self.test_audio_path}")
            audio_path = self.test_audio_path
        else:
            print(f"Mode microphone: {duration} secondes")
            print("(Un seul enregistrement sera utilisé pour tous les modèles)")
            audio_path = self._record_audio_once(duration)
            self.cached_audio_path = audio_path
        
        print(f"Langue: {language}")
        print(f"{'='*60}")
        
        results = []
        for model_type in model_types:
            result = self.run_benchmark(model_type, duration, language)
            results.append(result)
            
            if result.is_valid:
                print(f"\n✓ {model_type}")
                print(f"  Temps: {result.transcription_time:.2f}s")
                print(f"  Mémoire: {result.memory_usage_mb:.2f} MB")
                print(f"  CPU: {result.cpu_percent:.1f}%")
                print(f"  Confiance: {result.confidence:.2%}")
                if result.transcribed_text:
                    print(f"  Texte: \"{result.transcribed_text}\"")
            else:
                print(f"\n✗ {model_type}: {result.error_message}")
        
        if self.cached_audio_path and Path(self.cached_audio_path).exists():
            try:
                Path(self.cached_audio_path).unlink()
            except Exception:
                pass
        
        return results

