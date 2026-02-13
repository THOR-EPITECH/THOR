"""
Génération de rapports markdown pour les évaluations Pathfinding.
"""
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from src.common.io import read_jsonl


def save_report(
    output_dir: str | Path,
    model_name: str,
    dataset_path: str | Path,
    metrics: Dict[str, float]
) -> Path:
    """
    Génère et sauvegarde un rapport markdown.
    
    Args:
        output_dir: Dossier contenant les résultats
        model_name: Nom du modèle évalué
        dataset_path: Chemin vers le dataset utilisé
        metrics: Dictionnaire des métriques
    
    Returns:
        Chemin du fichier de rapport créé
    """
    output_dir = Path(output_dir)
    report_path = output_dir / "report.md"
    
    predictions_path = output_dir / "predictions.jsonl"
    predictions = list(read_jsonl(predictions_path)) if predictions_path.exists() else []
    
    total_samples = len(predictions)
    route_found_count = sum(1 for p in predictions if p.get("route_found", False))
    
    report = f"""# Rapport d'évaluation Pathfinding - {model_name}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Modèle**: {model_name}  
**Dataset**: {dataset_path}  
**Nombre d'échantillons**: {total_samples}

---

## 📊 Métriques globales

### Précision Origine/Destination
- **Précision origine**: {metrics.get('origin_accuracy_mean', 0):.4f} ± {metrics.get('origin_accuracy_std', 0):.4f}
- **Précision destination**: {metrics.get('destination_accuracy_mean', 0):.4f} ± {metrics.get('destination_accuracy_std', 0):.4f}

### Taux de succès
- **Itinéraires trouvés**: {route_found_count} / {total_samples} ({route_found_count/total_samples*100:.1f}%)
- **Taux de succès moyen**: {metrics.get('route_found_rate', 0):.4f}

### Précision du chemin
- **Précision du chemin moyenne**: {metrics.get('path_accuracy_mean', 'N/A')}
- **Écart-type**: {metrics.get('path_accuracy_std', 'N/A')}

### Distance
- **Erreur de distance moyenne**: {metrics.get('distance_error_mean', 'N/A')} km
- **Erreur relative moyenne**: {metrics.get('distance_relative_error_mean', 'N/A')}

### Nombre d'étapes
- **Nombre d'étapes moyen**: {metrics.get('num_steps_mean', 0):.2f} ± {metrics.get('num_steps_std', 0):.2f}

---

## 📈 Statistiques

- **Total d'échantillons**: {total_samples}
- **Itinéraires trouvés**: {route_found_count} ({route_found_count/total_samples*100:.1f}%)
- **Itinéraires non trouvés**: {total_samples - route_found_count} ({(total_samples - route_found_count)/total_samples*100:.1f}%)

---

## ✅ Exemples d'itinéraires trouvés

"""
    
    successful = [p for p in predictions if p.get("route_found", False)][:5]
    for i, pred in enumerate(successful, 1):
        report += f"""### {i}. {pred.get('origin', 'N/A')} → {pred.get('destination', 'N/A')}

- **Étapes**: {len(pred.get('predicted_steps', []))}
- **Distance**: {pred.get('predicted_distance', 'N/A')} km
- **Précision du chemin**: {pred.get('path_accuracy', 'N/A')}

"""
    
    report += """---

## ❌ Exemples d'itinéraires non trouvés

"""
    
    failed = [p for p in predictions if not p.get("route_found", False)][:5]
    for i, pred in enumerate(failed, 1):
        error = pred.get('error', 'Raison inconnue')
        report += f"""### {i}. {pred.get('origin', 'N/A')} → {pred.get('destination', 'N/A')}

- **Erreur**: {error}

"""
    
    report += f"""
---

## 📁 Fichiers

- **Dataset**: `{dataset_path}`
- **Prédictions**: `predictions.jsonl`
- **Métriques**: `metrics.json`
- **Rapport**: `report.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le système d'évaluation THOR.
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path
