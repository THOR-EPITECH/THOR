"""
Métriques pour l'évaluation du pathfinding.
"""
from typing import Dict, List, Optional
from src.common.types import Route
import statistics


def calculate_path_accuracy(
    reference_steps: List[str],
    predicted_steps: List[str]
) -> float:
    """
    Calcule la précision du chemin (proportion d'étapes correctes).
    
    Args:
        reference_steps: Étapes de référence
        predicted_steps: Étapes prédites
    
    Returns:
        Précision entre 0 et 1
    """
    if not reference_steps or not predicted_steps:
        return 0.0
    
    # Compare les étapes dans l'ordre
    correct = 0
    min_len = min(len(reference_steps), len(predicted_steps))
    
    for i in range(min_len):
        if reference_steps[i].lower() == predicted_steps[i].lower():
            correct += 1
    
    return correct / len(reference_steps) if reference_steps else 0.0


def calculate_distance_error(
    reference_distance: Optional[float],
    predicted_distance: Optional[float]
) -> Optional[float]:
    """
    Calcule l'erreur de distance.
    
    Args:
        reference_distance: Distance de référence (km)
        predicted_distance: Distance prédite (km)
    
    Returns:
        Erreur absolue en km, ou None si une des distances est manquante
    """
    if reference_distance is None or predicted_distance is None:
        return None
    
    return abs(reference_distance - predicted_distance)


def calculate_pathfinding_result(
    result: Route,
    reference_origin: str,
    reference_destination: str,
    reference_steps: Optional[List[str]] = None,
    reference_distance: Optional[float] = None
) -> Dict[str, float]:
    """
    Évalue un résultat de pathfinding.
    
    Args:
        result: Résultat du pathfinding
        reference_origin: Origine de référence
        reference_destination: Destination de référence
        reference_steps: Étapes de référence (optionnel)
        reference_distance: Distance de référence (optionnel)
    
    Returns:
        Dictionnaire avec toutes les métriques
    """
    metrics = {}
    
    # Vérification origine/destination
    origin_correct = (result.origin.lower() == reference_origin.lower()) if result.origin else False
    destination_correct = (result.destination.lower() == reference_destination.lower()) if result.destination else False
    
    metrics["origin_accuracy"] = 1.0 if origin_correct else 0.0
    metrics["destination_accuracy"] = 1.0 if destination_correct else 0.0
    metrics["route_found"] = 1.0 if result.steps else 0.0
    
    # Précision du chemin si les étapes de référence sont fournies
    if reference_steps:
        metrics["path_accuracy"] = calculate_path_accuracy(reference_steps, result.steps)
    else:
        metrics["path_accuracy"] = None
    
    # Erreur de distance si la distance de référence est fournie
    if reference_distance is not None and result.total_distance is not None:
        metrics["distance_error"] = calculate_distance_error(reference_distance, result.total_distance)
        metrics["distance_relative_error"] = metrics["distance_error"] / reference_distance if reference_distance > 0 else None
    else:
        metrics["distance_error"] = None
        metrics["distance_relative_error"] = None
    
    # Nombre d'étapes
    metrics["num_steps"] = len(result.steps) if result.steps else 0
    
    return metrics


def aggregate_metrics(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Agrège les métriques d'une liste de résultats.
    
    Args:
        metrics_list: Liste de dictionnaires de métriques
    
    Returns:
        Dictionnaire avec les métriques agrégées (moyennes, etc.)
    """
    if not metrics_list:
        return {}
    
    aggregated = {}
    
    # Liste des clés numériques
    numeric_keys = [
        "origin_accuracy", "destination_accuracy", "route_found",
        "path_accuracy", "distance_error", "distance_relative_error", "num_steps"
    ]
    
    for key in numeric_keys:
        values = [m.get(key) for m in metrics_list if m.get(key) is not None]
        if values:
            aggregated[f"{key}_mean"] = statistics.mean(values)
            if len(values) > 1:
                aggregated[f"{key}_std"] = statistics.stdev(values)
            else:
                aggregated[f"{key}_std"] = 0.0
    
    # Statistiques supplémentaires
    route_found_count = sum(1 for m in metrics_list if m.get("route_found", 0) == 1.0)
    aggregated["route_found_count"] = route_found_count
    aggregated["route_found_rate"] = route_found_count / len(metrics_list) if metrics_list else 0.0
    
    return aggregated
