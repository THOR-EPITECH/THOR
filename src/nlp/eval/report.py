"""
Génération de rapports markdown pour les évaluations NLP.
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from src.common.io import read_jsonl


def generate_markdown_report(
    output_dir: str | Path,
    model_name: str,
    dataset_path: str | Path,
    metrics: Dict[str, float],
    config: Dict[str, Any] = None
) -> str:
    """Génère un rapport markdown complet des résultats d'évaluation NLP."""
    output_dir = Path(output_dir)
    
    # Charge les prédictions
    predictions_path = output_dir / "predictions.jsonl"
    predictions = list(read_jsonl(predictions_path)) if predictions_path.exists() else []
    
    # Charge les métriques détaillées
    metrics_path = output_dir / "metrics.json"
    if metrics_path.exists():
        with open(metrics_path, 'r', encoding='utf-8') as f:
            detailed_metrics = json.load(f)
    else:
        detailed_metrics = metrics
    
    # Analyse
    total_samples = len(predictions)
    perfect_extractions = sum(1 for p in predictions if p.get("both_correct", 0) == 1.0)
    origin_correct = sum(1 for p in predictions if p.get("origin_accuracy", 0) == 1.0)
    dest_correct = sum(1 for p in predictions if p.get("destination_accuracy", 0) == 1.0)
    
    # Meilleures et pires prédictions
    sorted_predictions = sorted(predictions, key=lambda x: x.get("f1", 0.0), reverse=True)
    best_predictions = sorted_predictions[:5]
    worst_predictions = sorted_predictions[-5:]
    
    # Génère le rapport
    report = f"""# Rapport d'évaluation NLP - {model_name}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Modèle**: {model_name}  
**Dataset**: {dataset_path}  
**Nombre d'échantillons**: {total_samples}

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: {detailed_metrics.get('precision_mean', 0):.4f} ± {detailed_metrics.get('precision_std', 0):.4f}
- **Recall**: {detailed_metrics.get('recall_mean', 0):.4f} ± {detailed_metrics.get('recall_std', 0):.4f}
- **F1-Score**: {detailed_metrics.get('f1_mean', 0):.4f} ± {detailed_metrics.get('f1_std', 0):.4f}

### Précision par entité
- **Origine correcte**: {origin_correct}/{total_samples} ({origin_correct/total_samples*100:.1f}%)
- **Destination correcte**: {dest_correct}/{total_samples} ({dest_correct/total_samples*100:.1f}%)
- **Les deux correctes**: {perfect_extractions}/{total_samples} ({perfect_extractions/total_samples*100:.1f}%)

### Validation
- **Précision de validation**: {detailed_metrics.get('validation_accuracy_mean', 0):.4f} ± {detailed_metrics.get('validation_accuracy_std', 0):.4f}

---

## 📈 Statistiques

- **Total d'échantillons**: {total_samples}
- **Extractions parfaites (origine + destination)**: {perfect_extractions} ({perfect_extractions/total_samples*100:.1f}%)
- **Origine correcte**: {origin_correct} ({origin_correct/total_samples*100:.1f}%)
- **Destination correcte**: {dest_correct} ({dest_correct/total_samples*100:.1f}%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

"""
    
    for i, pred in enumerate(best_predictions, 1):
        report += f"""### {i}. F1: {pred.get('f1', 0):.4f}

- **Texte**: {pred.get('text', 'N/A')}
- **Reference**: {pred.get('reference_origin', 'N/A')} → {pred.get('reference_destination', 'N/A')}
- **Prediction**: {pred.get('predicted_origin', 'N/A')} → {pred.get('predicted_destination', 'N/A')}
- **Precision**: {pred.get('precision', 0):.4f}, **Recall**: {pred.get('recall', 0):.4f}

"""
    
    report += """---

## ❌ Pires extractions (F1 le plus bas)

"""
    
    for i, pred in enumerate(reversed(worst_predictions), 1):
        report += f"""### {i}. F1: {pred.get('f1', 0):.4f}

- **Texte**: {pred.get('text', 'N/A')}
- **Reference**: {pred.get('reference_origin', 'N/A')} → {pred.get('reference_destination', 'N/A')}
- **Prediction**: {pred.get('predicted_origin', 'N/A')} → {pred.get('predicted_destination', 'N/A')}
- **Precision**: {pred.get('precision', 0):.4f}, **Recall**: {pred.get('recall', 0):.4f}

"""
    
    report += """---

## 📁 Fichiers générés

- `metrics.json`: Métriques agrégées au format JSON
- `predictions.jsonl`: Toutes les prédictions avec métriques détaillées
- `predictions.csv`: Même contenu en format CSV
- `report.md`: Ce rapport

---

## 📝 Notes

Ce rapport a été généré automatiquement par le système d'évaluation THOR.

Pour plus de détails, consultez les fichiers JSON/CSV dans le dossier de résultats.
"""
    
    return report


def save_report(
    output_dir: str | Path,
    model_name: str,
    dataset_path: str | Path,
    metrics: Dict[str, float],
    config: Dict[str, Any] = None
):
    """Génère et sauvegarde le rapport markdown."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report = generate_markdown_report(
        output_dir,
        model_name,
        dataset_path,
        metrics,
        config
    )
    
    report_path = output_dir / "report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

