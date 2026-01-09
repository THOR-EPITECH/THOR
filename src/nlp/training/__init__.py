"""
Module d'entraînement pour les modèles NLP.
"""
from src.nlp.training.convert import convert_to_spacy_format
from src.nlp.training.trainer import train_spacy_model

__all__ = ["convert_to_spacy_format", "train_spacy_model"]

