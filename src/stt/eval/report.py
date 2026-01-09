"""
Génération de rapports markdown pour les évaluations STT.
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
    """
    Génère un rapport markdown complet des résultats d'évaluation.
    
    Args:
        output_dir: Dossier contenant les résultats
        model_name: Nom du modèle évalué
        dataset_path: Chemin vers le dataset utilisé
        metrics: Dictionnaire des métriques
        config: Configuration utilisée (optionnel)
    
    Returns:
        Contenu du rapport markdown
    """
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
    
    # Analyse des prédictions
    total_samples = len(predictions)
    perfect_predictions = sum(1 for p in predictions if p.get("wer", 1.0) == 0.0)
    high_error = sum(1 for p in predictions if p.get("wer", 1.0) > 0.5)
    
    # Trouve les meilleures et pires prédictions
    sorted_predictions = sorted(predictions, key=lambda x: x.get("wer", 1.0))
    best_predictions = sorted_predictions[:5]
    worst_predictions = sorted_predictions[-5:]
    
    # Génère le rapport
    report = f"""# Rapport d'évaluation STT - {model_name}

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Modèle**: {model_name}  
**Dataset**: {dataset_path}  
**Nombre d'échantillons**: {total_samples}

---

## 📊 Métriques globales

### Word Error Rate (WER)
- **Moyenne**: {detailed_metrics.get('wer_mean', 0):.4f}
- **Écart-type**: {detailed_metrics.get('wer_std', 0):.4f}

### Character Error Rate (CER)
- **Moyenne**: {detailed_metrics.get('cer_mean', 0):.4f}
- **Écart-type**: {detailed_metrics.get('cer_std', 0):.4f}

### Performance
- **Latency moyenne**: {detailed_metrics.get('latency_mean', 0):.4f} secondes
- **Écart-type**: {detailed_metrics.get('latency_std', 0):.4f} secondes
- **Real-Time Factor (RTF) moyen**: {detailed_metrics.get('rtf_mean', 0):.4f}
- **Écart-type RTF**: {detailed_metrics.get('rtf_std', 0):.4f}

### Confiance (si disponible)
- **Moyenne**: {detailed_metrics.get('confidence_mean', 'N/A')}
- **Écart-type**: {detailed_metrics.get('confidence_std', 'N/A')}

---

## 📈 Statistiques

- **Total d'échantillons**: {total_samples}
- **Transcriptions parfaites (WER = 0.0)**: {perfect_predictions} ({perfect_predictions/total_samples*100:.1f}%)
- **Erreurs importantes (WER > 0.5)**: {high_error} ({high_error/total_samples*100:.1f}%)

---

## ✅ Meilleures transcriptions (WER le plus bas)

"""
    
    for i, pred in enumerate(best_predictions, 1):
        report += f"""### {i}. WER: {pred.get('wer', 0):.4f}

- **Reference**: {pred.get('reference', 'N/A')}
- **Prediction**: {pred.get('prediction', 'N/A')}
- **CER**: {pred.get('cer', 0):.4f}
- **Latency**: {pred.get('latency', 0):.4f}s
- **ID**: {pred.get('id', 'N/A')}

"""
    
    report += """---

## ❌ Pires transcriptions (WER le plus élevé)

"""
    
    for i, pred in enumerate(reversed(worst_predictions), 1):
        report += f"""### {i}. WER: {pred.get('wer', 0):.4f}

- **Reference**: {pred.get('reference', 'N/A')}
- **Prediction**: {pred.get('prediction', 'N/A')}
- **CER**: {pred.get('cer', 0):.4f}
- **Latency**: {pred.get('latency', 0):.4f}s
- **ID**: {pred.get('id', 'N/A')}

"""
    
    # Analyse par catégorie si possible
    report += """---

## 🔍 Analyse détaillée

### Distribution des erreurs

"""
    
    # Calcule la distribution des WER
    wer_ranges = {
        "Parfait (0.0)": sum(1 for p in predictions if p.get("wer", 1.0) == 0.0),
        "Excellent (0.0-0.1)": sum(1 for p in predictions if 0.0 < p.get("wer", 1.0) <= 0.1),
        "Bon (0.1-0.3)": sum(1 for p in predictions if 0.1 < p.get("wer", 1.0) <= 0.3),
        "Moyen (0.3-0.5)": sum(1 for p in predictions if 0.3 < p.get("wer", 1.0) <= 0.5),
        "Mauvais (>0.5)": sum(1 for p in predictions if p.get("wer", 1.0) > 0.5),
    }
    
    for range_name, count in wer_ranges.items():
        percentage = (count / total_samples * 100) if total_samples > 0 else 0
        report += f"- **{range_name}**: {count} échantillons ({percentage:.1f}%)\n"
    
    # Configuration si disponible
    if config:
        report += """\n---

## ⚙️ Configuration

```yaml
"""
        report += json.dumps(config, indent=2, ensure_ascii=False)
        report += "\n```\n"
    
    # Fichiers générés
    report += """---

## 📁 Fichiers générés

- `metrics.json`: Métriques agrégées au format JSON
- `predictions.jsonl`: Toutes les prédictions avec métriques détaillées
- `predictions.csv`: Même contenu en format CSV
- `errors_top.csv`: Top erreurs triées par WER
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
    """
    Génère et sauvegarde le rapport markdown.
    
    Args:
        output_dir: Dossier de sortie
        model_name: Nom du modèle
        dataset_path: Chemin du dataset
        metrics: Métriques
        config: Configuration (optionnel)
    """
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

