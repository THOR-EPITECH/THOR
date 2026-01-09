"""
Normalisation de texte.
"""
import re
import unicodedata
from typing import Optional


def normalize_text(
    text: str,
    lowercase: bool = True,
    remove_accents: bool = False,
    remove_punctuation: bool = False,
    normalize_whitespace: bool = True
) -> str:
    """
    Normalise un texte.
    
    Args:
        text: Texte à normaliser
        lowercase: Convertir en minuscules
        remove_accents: Supprimer les accents
        remove_punctuation: Supprimer la ponctuation
        normalize_whitespace: Normaliser les espaces
    
    Returns:
        Texte normalisé
    """
    if not text:
        return ""
    
    # Minuscules
    if lowercase:
        text = text.lower()
    
    # Accents
    if remove_accents:
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    # Ponctuation
    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)
    
    # Espaces
    if normalize_whitespace:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
    
    return text


def clean_station_name(name: str) -> str:
    """
    Nettoie un nom de gare/ville.
    
    Args:
        name: Nom de gare/ville
    
    Returns:
        Nom nettoyé
    """
    # Supprime les préfixes/suffixes communs
    name = re.sub(r'^(gare de|gare d\'|gare du|gare des|gare)\s+', '', name, flags=re.IGNORECASE)
    name = name.strip()
    
    # Normalise les espaces et tirets
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'\s*-\s*', '-', name)
    
    return name

