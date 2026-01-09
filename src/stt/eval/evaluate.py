"""
Évaluation d'un modèle STT sur un dataset.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from src.stt.interfaces import STTModel
from src.stt.eval.metrics import evaluate_stt_result, aggregate_metrics
from src.stt.eval.report import save_report
from src.common.io import read_jsonl, write_jsonl, write_csv
from src.common.types import AudioSample, STTResult
from src.common.logging import setup_logging
from src.common.audio import get_audio_info

logger = setup_logging(module="stt.eval")


def evaluate_model(
    model: STTModel,
    dataset_path: str | Path,
    output_dir: str | Path,
    save_predictions: bool = True
) -> Dict[str, Any]:
    """
    Évalue un modèle STT sur un dataset.
    
    Le dataset peut être un fichier JSONL ou un dossier contenant des fichiers JSONL.
    Si c'est un dossier, tous les fichiers JSONL seront traités.
    
    Args:
        model: Modèle STT à évaluer
        dataset_path: Chemin vers le fichier JSONL ou dossier du dataset
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
    samples = []
    metrics_list = []
    predictions = []
    
    for item in tqdm(read_jsonl(dataset_path), desc="Evaluating"):
        audio_path = item["audio_path"]
        reference = item.get("transcript", "")
        sample_id = item.get("id", "")
        
        # Récupère les infos audio
        try:
            audio_info = get_audio_info(audio_path)
            audio_duration = audio_info["duration"]
        except Exception as e:
            logger.warning(f"Failed to get audio info for {audio_path}: {e}")
            audio_duration = 0.0
        
        # Transcription
        try:
            result = model.transcribe(audio_path)
            
            # Évaluation
            metrics = evaluate_stt_result(result, reference, audio_duration)
            metrics_list.append(metrics)
            
            # Sauvegarde prédiction
            predictions.append({
                "id": sample_id,
                "audio_path": str(audio_path),
                "reference": reference,
                "prediction": result.text,
                **metrics
            })
            
        except Exception as e:
            logger.error(f"Failed to transcribe {audio_path}: {e}")
            metrics_list.append({
                "wer": 1.0,
                "cer": 1.0,
                "latency": 0.0,
                "rtf": 0.0
            })
            predictions.append({
                "id": sample_id,
                "audio_path": str(audio_path),
                "reference": reference,
                "prediction": "",
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
    
    logger.info(f"Evaluation complete. WER: {aggregated.get('wer_mean', 'N/A'):.4f}")
    
    # Génère le rapport markdown
    try:
        report_path = save_report(
            output_dir,
            model.name,
            dataset_path,
            aggregated,
            config=None  # TODO: passer la config si disponible
        )
        logger.info(f"Report generated: {report_path}")
    except Exception as e:
        logger.warning(f"Failed to generate report: {e}")
    
    return aggregated

