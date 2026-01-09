"""
Entraînement (fine-tuning) de modèles NLP avec spaCy.
"""
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import random

try:
    import spacy
    from spacy.training import Example
    from spacy.util import minibatch, compounding
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

from src.nlp.training.convert import convert_to_spacy_format
from src.common.logging import setup_logging

logger = setup_logging(module="nlp.training")


def train_spacy_model(
    base_model_name: str,
    train_data: List[Tuple[str, Dict]],
    output_dir: str | Path,
    n_iter: int = 20,
    dropout: float = 0.1,
    valid_data: Optional[List[Tuple[str, Dict]]] = None,
    labels: List[str] = None
) -> Path:
    """
    Entraîne (fine-tune) un modèle spaCy pour l'extraction d'origine/destination.
    
    Args:
        base_model_name: Nom du modèle spaCy de base (ex: "fr_core_news_md")
        train_data: Données d'entraînement au format spaCy
        output_dir: Dossier où sauvegarder le modèle entraîné
        n_iter: Nombre d'itérations d'entraînement
        dropout: Taux de dropout
        valid_data: Données de validation (optionnel)
        labels: Labels d'entités à entraîner (défaut: ["ORIGIN", "DESTINATION"])
    
    Returns:
        Chemin vers le modèle entraîné
    """
    if not SPACY_AVAILABLE:
        raise ImportError("spacy is required. Install with: pip install spacy")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    labels = labels or ["ORIGIN", "DESTINATION"]
    
    logger.info(f"Loading base model: {base_model_name}")
    try:
        nlp = spacy.load(base_model_name)
    except OSError:
        logger.error(f"Model {base_model_name} not found. Install with: python -m spacy download {base_model_name}")
        raise
    
    # Ajoute les nouveaux labels au NER si nécessaire
    ner = nlp.get_pipe("ner")
    for label in labels:
        if label not in ner.labels:
            ner.add_label(label)
            logger.info(f"Added label: {label}")
    
    # Prépare les exemples d'entraînement
    examples = []
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)
    
    logger.info(f"Prepared {len(examples)} training examples")
    
    # Désactive les autres composants pendant l'entraînement
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        # Initialise les poids si nécessaire
        if "ner" not in nlp.pipe_names:
            nlp.add_pipe("ner")
        
        # Entraînement
        logger.info(f"Starting training for {n_iter} iterations...")
        nlp.begin_training()
        
        for itn in range(n_iter):
            random.shuffle(examples)
            losses = {}
            
            # Mini-batches
            batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=dropout, losses=losses)
            
            # Log des métriques
            if valid_data and (itn + 1) % 5 == 0:
                # Évaluation sur validation
                valid_examples = [
                    Example.from_dict(nlp.make_doc(text), ann)
                    for text, ann in valid_data
                ]
                scores = nlp.evaluate(valid_examples)
                logger.info(f"Iteration {itn + 1}/{n_iter} - Loss: {losses.get('ner', 0):.4f} - "
                          f"NER P: {scores.get('ents_p', 0):.4f} - "
                          f"NER R: {scores.get('ents_r', 0):.4f} - "
                          f"NER F: {scores.get('ents_f', 0):.4f}")
            else:
                logger.info(f"Iteration {itn + 1}/{n_iter} - Loss: {losses.get('ner', 0):.4f}")
    
    # Sauvegarde le modèle
    model_path = output_dir / "model"
    nlp.to_disk(model_path)
    logger.info(f"Model saved to {model_path}")
    
    return model_path

