"""
Modèle NLP utilisant des patterns regex avancés pour l'extraction.
"""
import re
from pathlib import Path
from typing import Optional, List, Dict
from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction
from src.common.logging import setup_logging
from src.common.text_norm import clean_station_name

logger = setup_logging(module="nlp.regex")


class RegexAdvancedModel(NLPModel):
    """
    Modèle NLP basé sur des patterns regex avancés pour extraire origine/destination.
    
    Utilise des patterns sophistiqués et une liste de villes connues pour améliorer
    la précision par rapport au modèle dummy.
    """
    
    # Liste de villes françaises communes
    FRENCH_CITIES = {
        "paris", "lyon", "marseille", "toulouse", "nice", "nantes", "strasbourg",
        "montpellier", "bordeaux", "lille", "rennes", "reims", "saint-étienne",
        "toulon", "le havre", "grenoble", "dijon", "angers", "villeurbanne",
        "saint-denis", "nîmes", "aix-en-provence", "clermont-ferrand", "brest",
        "limoges", "tours", "amiens", "perpignan", "metz", "besançon", "boulogne-billancourt",
        "orléans", "mulhouse", "caen", "rouen", "nancy", "argenteuil", "saint-denis",
        "roubaix", "tourcoing", "nanterre", "avignon", "créteil", "dunkirk", "poitiers",
        "asnières-sur-seine", "courbevoie", "versailles", "vitry-sur-seine", "aulnay-sous-bois",
        "colombes", "la rochelle", "champigny-sur-marne", "aubervilliers", "cannes", "antony",
        "bourges", "calais", "beziers", "merignac", "saint-herblain", "drancy", "colmar",
        "issy-les-moulineaux", "noisy-le-grand", "evry", "cergy", "pessac", "valence",
        "venissieux", "clichy", "troyes", "antibes", "la seyne-sur-mer", "montauban",
        "neuilly-sur-seine", "niort", "haguenau", "pantin", "sarcelles", "lorient",
        "laval", "bayonne", "meaux", "epinal", "brive-la-gaillarde", "cholet", "tarbes",
        "charleville-mezieres", "arcueil", "saint-ouen", "corbeil-essonnes", "massy",
        "belfort", "albi", "salon-de-provence", "agen", "hyeres", "mantes-la-jolie",
        "sète", "blois", "châteauroux", "saint-brieuc", "beauvais", "annecy", "boulogne-sur-mer",
        "frejus", "arles", "montlucon", "saint-quentin", "cherbourg", "caluire-et-cuire",
        "béziers", "vaulx-en-velin", "saint-priest", "rosny-sous-bois", "saint-chamond",
        "gennevilliers", "saint-laurent-du-var", "issy-les-moulineaux", "noisy-le-sec",
        "puteaux", "saint-malo", "mérignac", "saint-nazaire", "cagnes-sur-mer", "livry-gargan",
        "châlons-en-champagne", "saint-germain-en-laye", "issy-les-moulineaux", "puteaux"
    }
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self._initialized = True  # Pas besoin de charger un modèle
    
    def _load_model(self):
        """Pas de modèle à charger pour regex."""
        pass
    
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination avec des patterns regex avancés.
        
        Args:
            text: Texte à analyser
        
        Returns:
            NLPExtraction avec origine et destination
        """
        # Normalise le texte
        text_normalized = text.lower()
        
        # Patterns pour origine
        origin_patterns = [
            r'(?:de|depuis|partir de|partant de|venant de)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)\s+(?:vers|à|pour|jusqu\'?à)',
            r'(?:je suis|nous sommes|on est)\s+(?:à|en|dans)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
        ]
        
        # Patterns pour destination
        dest_patterns = [
            r'(?:à|vers|pour|aller à|rendre à|se rendre à|aller en|aller dans)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'(?:aller|rendre|voyager|me rendre|se rendre)\s+(?:à|vers|en|dans)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'(?:destination|arrivée|arriver)\s+(?:à|en|dans)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)\s+(?:est|sera)\s+(?:ma|mon|notre)\s+(?:destination|arrivée)',
        ]
        
        origin = None
        destination = None
        
        # Cherche origine
        for pattern in origin_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                candidate = clean_station_name(match.group(1))
                # Vérifie si c'est une ville connue ou ressemble à une ville
                if self._is_likely_city(candidate):
                    origin = candidate
                    break
        
        # Cherche destination
        for pattern in dest_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                candidate = clean_station_name(match.group(1))
                if self._is_likely_city(candidate):
                    destination = candidate
                    break
        
        # Si pas trouvé par patterns, cherche des villes dans le texte
        if not origin and not destination:
            cities_found = self._extract_cities_from_text(text)
            if len(cities_found) >= 2:
                origin = cities_found[0]
                destination = cities_found[1]
            elif len(cities_found) == 1:
                destination = cities_found[0]
        
        # Détermine si c'est une demande valide
        is_valid = self._is_valid_request(text, origin, destination)
        
        # Calcule la confiance
        confidence = self._calculate_confidence(origin, destination, is_valid)
        
        return NLPExtraction(
            origin=origin,
            destination=destination,
            is_valid=is_valid,
            confidence=confidence,
            metadata={
                "model": "regex_advanced",
                "extraction_method": "advanced_patterns"
            }
        )
    
    def _is_likely_city(self, text: str) -> bool:
        """Vérifie si le texte ressemble à une ville."""
        if not text or len(text) < 2:
            return False
        
        text_lower = text.lower().strip()
        
        # Vérifie dans la liste de villes connues
        if text_lower in self.FRENCH_CITIES:
            return True
        
        # Vérifie si ça ressemble à un nom de ville (commence par majuscule, pas de chiffres)
        if re.match(r'^[A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?$', text):
            return True
        
        return False
    
    def _extract_cities_from_text(self, text: str) -> List[str]:
        """Extrait les villes potentielles du texte."""
        cities = []
        
        # Cherche des mots qui commencent par majuscule et ressemblent à des villes
        words = re.findall(r'\b([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)\b', text)
        
        for word in words:
            cleaned = clean_station_name(word)
            if self._is_likely_city(cleaned) and cleaned not in cities:
                cities.append(cleaned)
        
        return cities
    
    def _is_valid_request(self, text: str, origin: Optional[str], destination: Optional[str]) -> bool:
        """Détermine si c'est une demande de trajet valide."""
        travel_keywords = [
            "aller", "rendre", "voyager", "trajet", "route", "chemin", "partir",
            "se rendre", "me rendre", "déplacement", "voyage", "itinéraire"
        ]
        text_lower = text.lower()
        
        # Doit contenir un mot-clé de trajet
        has_travel_keyword = any(kw in text_lower for kw in travel_keywords)
        
        # Doit avoir au moins une ville
        has_location = origin is not None or destination is not None
        
        return has_travel_keyword and has_location
    
    def _calculate_confidence(self, origin: Optional[str], destination: Optional[str], is_valid: bool) -> float:
        """Calcule la confiance de l'extraction."""
        if not is_valid:
            return 0.0
        
        confidence = 0.4  # Base pour regex
        
        # Bonus si on a les deux
        if origin and destination:
            confidence += 0.3
        
        # Bonus si les villes sont dans la liste connue
        if origin and origin.lower() in self.FRENCH_CITIES:
            confidence += 0.1
        if destination and destination.lower() in self.FRENCH_CITIES:
            confidence += 0.1
        
        # Bonus si les noms sont bien formés
        if origin and len(origin) > 2:
            confidence += 0.05
        if destination and len(destination) > 2:
            confidence += 0.05
        
        return min(confidence, 1.0)

