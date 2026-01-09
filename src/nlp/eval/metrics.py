"""
Métriques pour l'évaluation NLP.
"""
from typing import Dict, List
from src.common.types import NLPExtraction


def calculate_precision_recall_f1(
    true_origin: str | None,
    pred_origin: str | None,
    true_destination: str | None,
    pred_destination: str | None
) -> Dict[str, float]:
    """
    Calcule Precision, Recall et F1 pour l'extraction d'origine/destination.
    
    Args:
        true_origin: Origine de référence
        pred_origin: Origine prédite
        true_destination: Destination de référence
        pred_destination: Destination prédite
    
    Returns:
        Dictionnaire avec precision, recall, f1
    """
    # Normalise (case-insensitive)
    def normalize(s):
        return s.lower().strip() if s else None
    
    true_origin = normalize(true_origin)
    pred_origin = normalize(pred_origin)
    true_destination = normalize(true_destination)
    pred_destination = normalize(pred_destination)
    
    # Compte les vrais positifs, faux positifs, faux négatifs
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives
    
    # Origine
    if true_origin and pred_origin:
        if true_origin == pred_origin:
            tp += 1
        else:
            fp += 1
            fn += 1
    elif true_origin and not pred_origin:
        fn += 1
    elif not true_origin and pred_origin:
        fp += 1
    
    # Destination
    if true_destination and pred_destination:
        if true_destination == pred_destination:
            tp += 1
        else:
            fp += 1
            fn += 1
    elif true_destination and not pred_destination:
        fn += 1
    elif not true_destination and pred_destination:
        fp += 1
    
    # Calcule métriques
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn
    }


def calculate_entity_accuracy(
    true_origin: str | None,
    pred_origin: str | None,
    true_destination: str | None,
    pred_destination: str | None
) -> Dict[str, float]:
    """
    Calcule la précision par entité (origine et destination séparément).
    
    Args:
        true_origin: Origine de référence
        pred_origin: Origine prédite
        true_destination: Destination de référence
        pred_destination: Destination prédite
    
    Returns:
        Dictionnaire avec origin_accuracy, destination_accuracy
    """
    def normalize(s):
        return s.lower().strip() if s else None
    
    true_origin = normalize(true_origin)
    pred_origin = normalize(pred_origin)
    true_destination = normalize(true_destination)
    pred_destination = normalize(pred_destination)
    
    origin_correct = (true_origin == pred_origin) if (true_origin or pred_origin) else True
    destination_correct = (true_destination == pred_destination) if (true_destination or pred_destination) else True
    
    return {
        "origin_accuracy": 1.0 if origin_correct else 0.0,
        "destination_accuracy": 1.0 if destination_correct else 0.0,
        "both_correct": 1.0 if (origin_correct and destination_correct) else 0.0
    }


def evaluate_nlp_result(
    result: NLPExtraction,
    reference_origin: str | None,
    reference_destination: str | None,
    reference_is_valid: bool = True
) -> Dict[str, float]:
    """
    Évalue un résultat NLP complet.
    
    Args:
        result: Résultat de l'extraction NLP
        reference_origin: Origine de référence
        reference_destination: Destination de référence
        reference_is_valid: Si la référence est une demande valide
    
    Returns:
        Dictionnaire avec toutes les métriques
    """
    metrics = {}
    
    # Métriques d'extraction
    prf = calculate_precision_recall_f1(
        reference_origin,
        result.origin,
        reference_destination,
        result.destination
    )
    metrics.update(prf)
    
    # Précision par entité
    entity_acc = calculate_entity_accuracy(
        reference_origin,
        result.origin,
        reference_destination,
        result.destination
    )
    metrics.update(entity_acc)
    
    # Validation (is_valid)
    metrics["validation_accuracy"] = 1.0 if (result.is_valid == reference_is_valid) else 0.0
    
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

