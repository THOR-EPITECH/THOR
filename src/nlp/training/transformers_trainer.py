"""
Entraînement (fine-tuning) de modèles Transformers pour NER.
"""
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import json

try:
    from transformers import (
        AutoTokenizer, AutoModelForTokenClassification,
        TrainingArguments, Trainer, DataCollatorForTokenClassification
    )
    from datasets import Dataset
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForTokenClassification = None
    TrainingArguments = None
    Trainer = None
    DataCollatorForTokenClassification = None
    Dataset = None
    torch = None

from src.common.logging import setup_logging

logger = setup_logging(module="nlp.training.transformers")


def convert_to_ner_format(spacy_data: List[Tuple[str, Dict]]) -> List[Dict]:
    """
    Convertit les données spaCy au format NER pour Transformers.
    
    Args:
        spacy_data: Liste de tuples (text, annotations) au format spaCy
    
    Returns:
        Liste de dictionnaires au format Transformers NER
    """
    ner_data = []
    
    for text, annotations in spacy_data:
        entities = annotations.get("entities", [])
        
        # Crée les labels BIO
        tokens = text.split()
        labels = ["O"] * len(tokens)
        
        for start, end, label in entities:
            # Trouve les tokens correspondants
            char_to_token = {}
            char_pos = 0
            for i, token in enumerate(tokens):
                for j in range(len(token)):
                    char_to_token[char_pos + j] = i
                char_pos += len(token) + 1  # +1 pour l'espace
            
            # Marque les tokens
            start_token = char_to_token.get(start, 0)
            end_token = char_to_token.get(end, len(tokens) - 1)
            
            if start_token < len(labels):
                labels[start_token] = f"B-{label}"
                for i in range(start_token + 1, min(end_token + 1, len(labels))):
                    labels[i] = f"I-{label}"
        
        ner_data.append({
            "tokens": tokens,
            "ner_tags": labels,
            "text": text
        })
    
    return ner_data


def train_transformers_model(
    base_model_name: str,
    train_data: List[Tuple[str, Dict]],
    output_dir: str | Path,
    valid_data: Optional[List[Tuple[str, Dict]]] = None,
    n_epochs: int = 3,
    learning_rate: float = 2e-5,
    batch_size: int = 16
) -> Path:
    """
    Entraîne (fine-tune) un modèle Transformers pour l'extraction NER.
    
    Args:
        base_model_name: Nom du modèle Transformers de base
        train_data: Données d'entraînement au format spaCy
        output_dir: Dossier où sauvegarder le modèle entraîné
        valid_data: Données de validation (optionnel)
        n_epochs: Nombre d'époques d'entraînement
        learning_rate: Taux d'apprentissage
        batch_size: Taille des batches
    
    Returns:
        Chemin vers le modèle entraîné
    """
    if not TRANSFORMERS_AVAILABLE:
        raise ImportError("transformers, torch, and datasets are required. Install with: pip install transformers torch datasets")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Loading base model: {base_model_name}")
    
    # Utilise camembert-base comme modèle de base (plus fiable que les modèles NER pré-entraînés)
    # Si le modèle demandé contient "ner", on utilise camembert-base à la place
    if "ner" in base_model_name.lower() or "camembert-ner" in base_model_name.lower():
        logger.info("Using camembert-base as base model (more reliable for fine-tuning)")
        base_model = "camembert-base"
    else:
        base_model = base_model_name
    
    try:
        from transformers import CamembertConfig
        
        # Charge le tokenizer
        tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=False)  # use_fast=False pour éviter les problèmes
        
        # Crée la configuration avec 5 labels
        config = CamembertConfig.from_pretrained(base_model)
        config.num_labels = 5
        
        # Charge le modèle avec la nouvelle configuration
        model = AutoModelForTokenClassification.from_pretrained(base_model, config=config)
        
        logger.info(f"Successfully loaded {base_model} with 5 labels (O, B-ORIGIN, I-ORIGIN, B-DESTINATION, I-DESTINATION)")
    except Exception as e:
        logger.error(f"Failed to load model {base_model}: {e}")
        raise
    
    # Convertit les données
    train_ner = convert_to_ner_format(train_data)
    valid_ner = convert_to_ner_format(valid_data) if valid_data else None
    
    # Crée les datasets
    train_dataset = Dataset.from_list(train_ner)
    valid_dataset = Dataset.from_list(valid_ner) if valid_ner else None
    
    # Tokenize
    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(
            examples["tokens"],
            truncation=True,
            padding=True,
            is_split_into_words=True
        )
        
        labels = []
        for i, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:
                    label_ids.append(label_to_id.get(label[word_idx], 0))
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)
        
        tokenized_inputs["labels"] = labels
        return tokenized_inputs
    
    # Label mapping
    label_to_id = {"O": 0, "B-ORIGIN": 1, "I-ORIGIN": 2, "B-DESTINATION": 3, "I-DESTINATION": 4}
    
    train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
    if valid_dataset:
        valid_dataset = valid_dataset.map(tokenize_and_align_labels, batched=True)
    
    # Arguments d'entraînement
    training_args = TrainingArguments(
        output_dir=str(output_dir / "checkpoints"),
        num_train_epochs=n_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=0.01,
        logging_dir=str(output_dir / "logs"),
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch" if valid_dataset else "no",  # eval_strategy au lieu de evaluation_strategy
        eval_steps=100 if valid_dataset else None,  # Évalue tous les 100 steps
    )
    
    # Data collator
    data_collator = DataCollatorForTokenClassification(tokenizer)
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    # Entraînement
    logger.info(f"Starting training for {n_epochs} epochs...")
    trainer.train()
    
    # Sauvegarde
    model_path = output_dir / "model"
    model.save_pretrained(str(model_path))
    tokenizer.save_pretrained(str(model_path))
    
    logger.info(f"Model saved to {model_path}")
    
    return model_path

