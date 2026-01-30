"""
Évaluation d'un modèle Pathfinding sur un dataset.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

from src.pathfinding.interfaces import PathfindingModel
from src.pathfinding.eval.metrics import calculate_pathfinding_result, aggregate_metrics
from src.common.io import read_jsonl, write_jsonl, write_csv
from src.common.logging import setup_logging

logger = setup_logging(module="pathfinding.eval")


def evaluate_model(
    model: PathfindingModel,
    dataset_path: str | Path,
    output_dir: str | Path,
    save_predictions: bool = True
) -> Dict[str, Any]:
    """
    Évalue un modèle Pathfinding sur un dataset.
    
    Le dataset doit être un fichier JSONL avec les champs :
    - origin: Ville de départ
    - destination: Ville d'arrivée
    - reference_steps: Liste des étapes de référence (optionnel)
    - reference_distance: Distance de référence en km (optionnel)
    
    Args:
        model: Modèle Pathfinding à évaluer
        dataset_path: Chemin vers le fichier JSONL du dataset
        output_dir: Dossier de sortie pour les résultats
        save_predictions: Sauvegarder les prédictions
    
    Returns:
        Dictionnaire avec les métriques agrégées
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Evaluating model {model.name} on {dataset_path}")
    
    # Initialise le modèle
    model.initialize()
    
    # Charge le dataset
    metrics_list = []
    predictions = []
    
    for item in tqdm(read_jsonl(dataset_path), desc="Evaluating"):
        origin = item.get("origin", "")
        destination = item.get("destination", "")
        reference_steps = item.get("reference_steps")
        reference_distance = item.get("reference_distance")
        sample_id = item.get("id", "")
        
        if not origin or not destination:
            logger.warning(f"Skipping sample {sample_id}: missing origin or destination")
            continue
        
        # Recherche d'itinéraire
        try:
            result = model.find_route(origin, destination)
            
            # Évaluation
            metrics = calculate_pathfinding_result(
                result,
                origin,
                destination,
                reference_steps,
                reference_distance
            )
            metrics_list.append(metrics)
            
            # Sauvegarde prédiction
            predictions.append({
                "id": sample_id,
                "origin": origin,
                "destination": destination,
                "predicted_steps": result.steps,
                "predicted_distance": result.total_distance,
                "reference_steps": reference_steps,
                "reference_distance": reference_distance,
                "route_found": len(result.steps) > 0,
                **metrics
            })
            
        except Exception as e:
            logger.error(f"Failed to find route for {origin} → {destination}: {e}")
            metrics_list.append({
                "origin_accuracy": 0.0,
                "destination_accuracy": 0.0,
                "route_found": 0.0,
                "path_accuracy": 0.0,
                "num_steps": 0
            })
            predictions.append({
                "id": sample_id,
                "origin": origin,
                "destination": destination,
                "predicted_steps": [],
                "predicted_distance": None,
                "reference_steps": reference_steps,
                "reference_distance": reference_distance,
                "route_found": False,
                "error": str(e)
            })
    
    # Agrège les métriques
    aggregated = aggregate_metrics(metrics_list)
    
    # Sauvegarde
    if save_predictions:
        write_jsonl(output_dir / "predictions.jsonl", predictions)
        write_csv(output_dir / "predictions.csv", predictions)
    
    # Sauvegarde métriques
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Evaluation complete. Route found rate: {aggregated.get('route_found_rate', 0):.4f}")
    
    # Génère le rapport markdown
    try:
        from src.pathfinding.eval.report import save_report
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
