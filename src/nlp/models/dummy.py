"""
Modèle NLP dummy pour tests et baseline.
"""
import re
from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction


class DummyNLPModel(NLPModel):
    """
    Modèle NLP baseline qui extrait les villes avec des patterns simples.
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.cities = [
            "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes",
            "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Rennes",
            "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble",
            "Dijon", "Angers", "Nîmes", "Villeurbanne", "Cannes", "Nancy"
        ]
    
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination avec des patterns simples.
        
        Args:
            text: Texte à analyser
        
        Returns:
            NLPExtraction avec origine et destination
        """
        origin = None
        destination = None
        is_valid = False
        
        pattern_depuis = re.search(r'depuis\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
        if pattern_depuis:
            origin = pattern_depuis.group(1).strip()
            text_avant_depuis = text[:pattern_depuis.start()]
            pattern_dest = re.search(r'(?:aller|rendre|voyager|se\s+rendre)\s+(?:à|vers|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text_avant_depuis, re.IGNORECASE)
            if pattern_dest:
                destination = pattern_dest.group(1).strip()
                is_valid = True
        
        if not origin or not destination:
            pattern_de_a = re.search(r'\bde\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)\s+(?:à|vers|pour|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_de_a:
                if not origin:
                    origin = pattern_de_a.group(1).strip()
                if not destination:
                    destination = pattern_de_a.group(2).strip()
                is_valid = True
        
        if not destination:
            pattern_aller_a = re.search(r'(?:aller|rendre|voyager|se\s+rendre)\s+(?:à|vers|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_aller_a:
                destination = pattern_aller_a.group(1).strip()
                is_valid = True
        
        if not origin:
            pattern_partir_de = re.search(r'(?:partir|quitter)\s+(?:de|depuis)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_partir_de:
                origin = pattern_partir_de.group(1).strip()
                is_valid = True
        
        if origin:
            origin = self._normalize_city(origin)
        if destination:
            destination = self._normalize_city(destination)
        
        return NLPExtraction(
            origin=origin,
            destination=destination,
            is_valid=is_valid,
            confidence=0.5 if (origin or destination) else 0.0,
            metadata={
                "model": "dummy",
                "extraction_method": "regex_patterns"
            }
        )
    
    def _normalize_city(self, city: str) -> str:
        """Normalise le nom de ville."""
        city = city.strip()
        words = city.split()
        normalized = ' '.join(word.capitalize() for word in words)
        return normalized
