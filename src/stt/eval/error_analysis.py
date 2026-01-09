"""
Analyse des erreurs de transcription.
"""
from collections import Counter
from typing import List, Dict, Any
from src.common.io import read_jsonl, write_csv
from pathlib import Path


def analyze_errors(
    predictions_path: str | Path,
    output_dir: str | Path,
    top_n: int = 20
):
    """
    Analyse les erreurs les plus fréquentes.
    
    Args:
        predictions_path: Chemin vers predictions.jsonl
        output_dir: Dossier de sortie
        top_n: Nombre d'erreurs à afficher
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    errors = []
    high_wer_samples = []
    
    for item in read_jsonl(predictions_path):
        wer = item.get("wer", 0.0)
        cer = item.get("cer", 0.0)
        
        errors.append({
            "id": item.get("id", ""),
            "wer": wer,
            "cer": cer,
            "reference": item.get("reference", ""),
            "prediction": item.get("prediction", "")
        })
        
        if wer > 0.5:  # Erreurs importantes
            high_wer_samples.append(item)
    
    # Trie par WER décroissant
    errors.sort(key=lambda x: x["wer"], reverse=True)
    
    # Sauvegarde top erreurs
    write_csv(output_dir / "errors_top.csv", errors[:top_n])
    
    # Analyse des patterns d'erreur
    analysis = {
        "total_samples": len(errors),
        "high_error_samples": len(high_wer_samples),
        "avg_wer": sum(e["wer"] for e in errors) / len(errors) if errors else 0.0,
        "avg_cer": sum(e["cer"] for e in errors) / len(errors) if errors else 0.0,
    }
    
    return analysis

