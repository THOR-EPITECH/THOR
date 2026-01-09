"""
Métriques pour l'évaluation STT.
"""
import time
from typing import List, Dict, Any
from src.common.types import STTResult, AudioSample
try:
    import jiwer  # Word Error Rate
except ImportError:
    jiwer = None


def calculate_wer(reference: str, hypothesis: str) -> float:
    """
    Calcule le Word Error Rate (WER).
    
    Args:
        reference: Texte de référence
        hypothesis: Texte transcrit
    
    Returns:
        WER (0.0 = parfait, 1.0+ = erreurs)
    """
    if not reference.strip():
        return 1.0 if hypothesis.strip() else 0.0
    
    if jiwer is None:
        # Implémentation simple si jiwer n'est pas disponible
        ref_words = reference.split()
        hyp_words = hypothesis.split()
        # Distance de Levenshtein simplifiée au niveau des mots
        if len(ref_words) == 0:
            return 1.0 if hyp_words else 0.0
        # Approximation simple
        matches = sum(1 for w in hyp_words if w in ref_words)
        return 1.0 - (matches / max(len(ref_words), len(hyp_words)))
    
    return jiwer.wer(reference, hypothesis)


def calculate_cer(reference: str, hypothesis: str) -> float:
    """
    Calcule le Character Error Rate (CER).
    
    Args:
        reference: Texte de référence
        hypothesis: Texte transcrit
    
    Returns:
        CER (0.0 = parfait, 1.0+ = erreurs)
    """
    if not reference:
        return 1.0 if hypothesis else 0.0
    
    if jiwer is None:
        # Implémentation simple si jiwer n'est pas disponible
        # Distance de Levenshtein au niveau des caractères
        def levenshtein(s1, s2):
            if len(s1) < len(s2):
                return levenshtein(s2, s1)
            if len(s2) == 0:
                return len(s1)
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]
        
        distance = levenshtein(reference, hypothesis)
        return distance / max(len(reference), len(hypothesis), 1)
    
    return jiwer.cer(reference, hypothesis)


def calculate_realtime_factor(audio_duration: float, processing_time: float) -> float:
    """
    Calcule le Real-Time Factor (RTF).
    
    RTF < 1.0 signifie traitement plus rapide que la durée audio.
    
    Args:
        audio_duration: Durée de l'audio en secondes
        processing_time: Temps de traitement en secondes
    
    Returns:
        RTF
    """
    if audio_duration == 0:
        return 0.0
    return processing_time / audio_duration


def evaluate_stt_result(
    result: STTResult,
    reference: str,
    audio_duration: float
) -> Dict[str, float]:
    """
    Évalue un résultat STT complet.
    
    Args:
        result: Résultat de la transcription
        reference: Texte de référence (ground truth)
        audio_duration: Durée de l'audio en secondes
    
    Returns:
        Dictionnaire avec toutes les métriques
    """
    metrics = {
        "wer": calculate_wer(reference, result.text),
        "cer": calculate_cer(reference, result.text),
    }
    
    if result.processing_time is not None:
        metrics["latency"] = result.processing_time
        metrics["rtf"] = calculate_realtime_factor(audio_duration, result.processing_time)
    
    if result.confidence is not None:
        metrics["confidence"] = result.confidence
    
    return metrics


def aggregate_metrics(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Agrège les métriques sur plusieurs échantillons.
    
    Args:
        metrics_list: Liste de dictionnaires de métriques
    
    Returns:
        Métriques agrégées (moyennes)
    """
    if not metrics_list:
        return {}
    
    aggregated = {}
    for key in metrics_list[0].keys():
        values = [m[key] for m in metrics_list if key in m]
        if values:
            aggregated[f"{key}_mean"] = sum(values) / len(values)
            aggregated[f"{key}_std"] = (
                sum((x - aggregated[f"{key}_mean"]) ** 2 for x in values) / len(values)
            ) ** 0.5
    
    return aggregated

