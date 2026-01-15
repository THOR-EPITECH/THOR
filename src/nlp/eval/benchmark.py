"""
Benchmark de plusieurs modèles NLP avec comparaison des métriques.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.nlp.interfaces import NLPModel
from src.nlp.eval.evaluate import evaluate_model
from src.common.logging import setup_logging

logger = setup_logging(module="nlp.benchmark")


def benchmark_models(
    models: List[tuple[str, NLPModel, Optional[Dict[str, Any]]]],
    dataset_path: str | Path,
    output_dir: str | Path,
    save_individual_results: bool = True
) -> Dict[str, Any]:
    """
    Compare plusieurs modèles NLP sur le même dataset.
    
    Args:
        models: Liste de tuples (nom_modèle, modèle, config_dict)
        dataset_path: Chemin vers le dataset JSONL
        output_dir: Dossier de sortie pour les résultats
        save_individual_results: Sauvegarder les résultats individuels de chaque modèle
    
    Returns:
        Dictionnaire avec les résultats comparatifs
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting benchmark of {len(models)} models on {dataset_path}")
    
    results = {}
    
    # Évalue chaque modèle
    for model_name, model, config in models:
        logger.info(f"Evaluating model: {model_name}")
        
        # Dossier de sortie pour ce modèle
        model_output_dir = output_dir / model_name if save_individual_results else output_dir / "temp"
        model_output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Évalue le modèle
            metrics = evaluate_model(
                model=model,
                dataset_path=dataset_path,
                output_dir=model_output_dir,
                save_predictions=save_individual_results
            )
            
            results[model_name] = {
                "metrics": metrics,
                "config": config,
                "status": "success"
            }
            
            logger.info(f"✅ {model_name} - F1: {metrics.get('f1_mean', 0):.4f}")
            
        except Exception as e:
            logger.error(f"❌ {model_name} failed: {e}")
            results[model_name] = {
                "metrics": {},
                "config": config,
                "status": "error",
                "error": str(e)
            }
    
    # Génère le rapport comparatif
    report_path = generate_comparative_report(
        results,
        dataset_path,
        output_dir
    )
    
    # Sauvegarde les résultats comparatifs en JSON
    comparison_path = output_dir / "comparison.json"
    with open(comparison_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Benchmark complete. Report: {report_path}")
    
    return {
        "results": results,
        "report_path": report_path,
        "comparison_path": comparison_path
    }


def generate_comparative_report(
    results: Dict[str, Dict[str, Any]],
    dataset_path: str | Path,
    output_dir: Path
) -> Path:
    """
    Génère un rapport markdown comparatif des modèles.
    
    Args:
        results: Dictionnaire des résultats par modèle
        dataset_path: Chemin du dataset utilisé
        output_dir: Dossier de sortie
    
    Returns:
        Chemin vers le rapport généré
    """
    report = f"""# Benchmark NLP - Comparaison de modèles

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dataset**: {dataset_path}  
**Nombre de modèles**: {len(results)}

---

## 📊 Résultats comparatifs

### Tableau récapitulatif

| Modèle | F1-Score | Precision | Recall | Origin Acc. | Dest. Acc. | Valid Acc. | Status |
|--------|----------|-----------|--------|-------------|------------|-------------|--------|
"""
    
    # Trie les modèles par F1 décroissant
    sorted_models = sorted(
        results.items(),
        key=lambda x: x[1].get("metrics", {}).get("f1_mean", 0.0),
        reverse=True
    )
    
    for model_name, result in sorted_models:
        if result.get("status") == "error":
            report += f"| {model_name} | ❌ Erreur | - | - | - | - | - | ❌ |\n"
            continue
        
        metrics = result.get("metrics", {})
        f1 = metrics.get("f1_mean", 0.0)
        precision = metrics.get("precision_mean", 0.0)
        recall = metrics.get("recall_mean", 0.0)
        origin_acc = metrics.get("origin_accuracy_mean", 0.0)
        dest_acc = metrics.get("destination_accuracy_mean", 0.0)
        valid_acc = metrics.get("validation_accuracy_mean", 0.0)
        
        # Emoji pour le meilleur score
        best_f1 = max(r.get("metrics", {}).get("f1_mean", 0.0) for r in results.values() if r.get("status") == "success")
        f1_emoji = "🏆" if f1 == best_f1 and best_f1 > 0 else ""
        
        report += f"| {model_name} {f1_emoji} | {f1:.4f} | {precision:.4f} | {recall:.4f} | {origin_acc:.4f} | {dest_acc:.4f} | {valid_acc:.4f} | ✅ |\n"
    
    report += "\n---\n\n## 📈 Détails par modèle\n\n"
    
    # Détails pour chaque modèle
    for model_name, result in sorted_models:
        if result.get("status") == "error":
            report += f"""### ❌ {model_name}

**Erreur**: {result.get('error', 'Unknown error')}

"""
            continue
        
        metrics = result.get("metrics", {})
        config = result.get("config", {})
        
        report += f"""### {model_name}

#### Métriques principales

- **F1-Score**: {metrics.get('f1_mean', 0):.4f} ± {metrics.get('f1_std', 0):.4f}
- **Precision**: {metrics.get('precision_mean', 0):.4f} ± {metrics.get('precision_std', 0):.4f}
- **Recall**: {metrics.get('recall_mean', 0):.4f} ± {metrics.get('recall_std', 0):.4f}

#### Précision par entité

- **Origine**: {metrics.get('origin_accuracy_mean', 0):.4f} ± {metrics.get('origin_accuracy_std', 0):.4f}
- **Destination**: {metrics.get('destination_accuracy_mean', 0):.4f} ± {metrics.get('destination_accuracy_std', 0):.4f}
- **Les deux correctes**: {metrics.get('both_correct_mean', 0):.4f} ± {metrics.get('both_correct_std', 0):.4f}

#### Validation

- **Précision de validation**: {metrics.get('validation_accuracy_mean', 0):.4f} ± {metrics.get('validation_accuracy_std', 0):.4f}

"""
        
        if config:
            report += f"""#### Configuration

```yaml
{json.dumps(config, indent=2, ensure_ascii=False)}
```

"""
        
        # Lien vers le rapport détaillé si disponible
        model_dir = output_dir / model_name
        if (model_dir / "report.md").exists():
            report += f"📄 [Rapport détaillé](./{model_name}/report.md)\n\n"
        
        report += "---\n\n"
    
    # Analyse comparative
    report += """## 🔍 Analyse comparative

"""
    
    successful_models = [r for r in results.values() if r.get("status") == "success"]
    if len(successful_models) > 1:
        best_model = max(
            results.items(),
            key=lambda x: x[1].get("metrics", {}).get("f1_mean", 0.0) if x[1].get("status") == "success" else 0.0
        )
        best_name = best_model[0]
        best_f1 = best_model[1].get("metrics", {}).get("f1_mean", 0.0)
        
        report += f"""### 🏆 Meilleur modèle: **{best_name}**

- **F1-Score**: {best_f1:.4f}

### Comparaison

"""
        
        # Compare avec le meilleur
        for model_name, result in sorted_models:
            if result.get("status") == "error" or model_name == best_name:
                continue
            
            metrics = result.get("metrics", {})
            f1 = metrics.get("f1_mean", 0.0)
            diff = f1 - best_f1
            diff_pct = (diff / best_f1 * 100) if best_f1 > 0 else 0
            
            report += f"- **{model_name}** vs **{best_name}**: {diff:+.4f} ({diff_pct:+.1f}%)\n"
    
    report += """
---

## 📁 Fichiers générés

- `comparison.json`: Résultats comparatifs au format JSON
- `benchmark_report.md`: Ce rapport
- `<model_name>/`: Dossiers individuels avec résultats détaillés (si `save_individual_results=True`)

---

## 📝 Notes

Ce benchmark compare les modèles NLP sur le même dataset pour une évaluation équitable.

Pour plus de détails sur un modèle spécifique, consultez son rapport individuel dans son dossier.
"""
    
    # Sauvegarde le rapport
    report_path = output_dir / "benchmark_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

