"""
Normalisation de texte.
"""
import re
import unicodedata
from typing import Optional

def clean_station_name(name: str) -> str:
    """
    Nettoie un nom de gare/ville.
    
    Args:
        name: Nom de gare/ville
    
    Returns:
        Nom nettoyé
    """
    name = re.sub(r'^(gare de|gare d\'|gare du|gare des|gare)\s+', '', name, flags=re.IGNORECASE)
    name = name.strip()
    
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'\s*-\s*', '-', name)
    
    return name

