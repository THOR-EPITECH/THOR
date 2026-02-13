"""
Évaluation d'un modèle NLP sur un dataset.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from src.nlp.interfaces import NLPModel
from src.nlp.eval.metrics import evaluate_nlp_result, aggregate_metrics
from src.nlp.eval.report import save_report
from src.common.io import read_jsonl, write_jsonl, write_csv
from src.common.logging import setup_logging

logger = setup_logging(module="nlp.eval")


def evaluate_model(
    model: NLPModel,
    dataset_path: str | Path,
    output_dir: str | Path,
    save_predictions: bool = True
) -> Dict[str, Any]:
    """
    Évalue un modèle NLP sur un dataset.
    
    Args:
        model: Modèle NLP à évaluer
        dataset_path: Chemin vers le fichier JSONL du dataset
        output_dir: Dossier de sortie pour les résultats
        save_predictions: Sauvegarder les prédictions
    
    Returns:
        Dictionnaire avec les métriques agrégées
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Evaluating model {model.name} on {dataset_path}")
    
    model.initialize()
    
    metrics_list = []
    predictions = []
    
    for item in tqdm(read_jsonl(dataset_path), desc="Evaluating"):
        text = item.get("sentence", item.get("transcript", ""))
        reference_origin = item.get("origin")
        reference_destination = item.get("destination")
        reference_is_valid = item.get("is_valid", True)
        sample_id = item.get("id", "")
        
        if not text:
            continue
        
        try:
            result = model.extract(text)
            
            metrics = evaluate_nlp_result(
                result,
                reference_origin,
                reference_destination,
                reference_is_valid
            )
            metrics_list.append(metrics)
            
            predictions.append({
                "id": sample_id,
                "text": text,
                "reference_origin": reference_origin,
                "reference_destination": reference_destination,
                "reference_is_valid": reference_is_valid,
                "predicted_origin": result.origin,
                "predicted_destination": result.destination,
                "predicted_is_valid": result.is_valid,
                **metrics
            })
            
        except Exception as e:
            logger.error(f"Failed to extract from text {sample_id}: {e}")
            metrics_list.append({
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "origin_accuracy": 0.0,
                "destination_accuracy": 0.0,
                "validation_accuracy": 0.0
            })
            predictions.append({
                "id": sample_id,
                "text": text,
                "reference_origin": reference_origin,
                "reference_destination": reference_destination,
                "error": str(e)
            })
    
    aggregated = aggregate_metrics(metrics_list)
    
    if save_predictions:
        write_jsonl(output_dir / "predictions.jsonl", predictions)
        write_csv(output_dir / "predictions.csv", predictions)
    
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Evaluation complete. F1: {aggregated.get('f1_mean', 'N/A'):.4f}")
    
    try:
        from src.nlp.eval.report import save_report
        report_path = save_report(
            output_dir,
            model.name,
            dataset_path,
            aggregated
        )
        logger.info(f"Report generated: {report_path}")
    except Exception as e:
        logger.warning(f"Failed to generate report: {e}")
    
    return aggregated

