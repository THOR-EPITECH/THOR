"""
Modèle NLP utilisant spaCy pour l'extraction NER.
"""
import re
from pathlib import Path
from typing import Optional, List, Tuple

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    spacy = None

from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction
from src.common.logging import setup_logging
from src.common.text_norm import clean_station_name
from src.nlp.utils import ensure_origin_destination_distinct

logger = setup_logging(module="nlp.spacy")


class SpacyFRModel(NLPModel):
    """
    Modèle NLP basé sur spaCy pour extraire origine/destination.
    
    Utilise NER (Named Entity Recognition) et des patterns pour identifier
    les villes et déterminer origine/destination.
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.model_name = self.config.get("model_name", "fr_core_news_md")
        self.custom_model_path = self.config.get("custom_model_path")  # Chemin vers modèle fine-tuné
        self._nlp = None
    
    def _load_model(self):
        """Charge le modèle spaCy."""
        if not SPACY_AVAILABLE:
            raise ImportError("spacy is required. Install with: pip install spacy")
        
        if self.custom_model_path:
            model_path = Path(self.custom_model_path)
            if model_path.exists():
                logger.info(f"Loading custom fine-tuned model: {model_path}")
                self._nlp = spacy.load(model_path)
                logger.info("Custom model loaded successfully")
                return
            else:
                logger.warning(f"Custom model not found at {model_path}, using base model")
        
        logger.info(f"Loading spaCy model: {self.model_name}")
        try:
            self._nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.error(f"Model {self.model_name} not found. Install with: python -m spacy download {self.model_name}")
            raise
    
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination avec spaCy.
        
        Args:
            text: Texte à analyser
        
        Returns:
            NLPExtraction avec origine et destination
        """
        if not self._initialized:
            self.initialize()
        
        doc = self._nlp(text)
        
        locations = []
        origin_entities = []
        destination_entities = []
        
        for ent in doc.ents:
            if ent.label_ == "LOC":
                locations.append(ent.text)
            elif ent.label_ == "ORIGIN":
                origin_entities.append(ent.text)
            elif ent.label_ == "DESTINATION":
                destination_entities.append(ent.text)
        
        proper_nouns = []
        for token in doc:
            if (token.pos_ in ["PROPN", "NOUN", "ADJ"]) and len(token.text) > 2:
                context = doc[max(0, token.i-3):min(len(doc), token.i+4)]
                context_text = " ".join([t.text.lower() for t in context])
                travel_keywords = ["aller", "rendre", "depuis", "vers", "à", "de", "partir", "voyager"]
                if any(kw in context_text for kw in travel_keywords):
                    proper_nouns.append(token.text)
        
        if origin_entities or destination_entities:
            origin = clean_station_name(origin_entities[0]) if origin_entities else None
            destination = clean_station_name(destination_entities[0]) if destination_entities else None
            all_cities = list(set(locations + proper_nouns + origin_entities + destination_entities))
            all_cities = [clean_station_name(city) for city in all_cities]
        else:
            all_cities = list(set(locations + proper_nouns))
            all_cities = [clean_station_name(city) for city in all_cities]
            
            common_words = {"le", "la", "les", "de", "du", "des", "un", "une", "et", "ou"}
            all_cities = [city for city in all_cities if len(city) > 2 and city.lower() not in common_words]
            
            origin, destination = self._determine_origin_destination(text, all_cities, doc)
        
        is_valid = self._is_travel_request(text, origin, destination)
        confidence = self._calculate_confidence(
            origin, destination, origin_entities, destination_entities,
            all_cities, is_valid
        )

        origin, destination = ensure_origin_destination_distinct(origin, destination)

        return NLPExtraction(
            origin=origin,
            destination=destination,
            is_valid=is_valid,
            confidence=confidence,
            entities=[{"text": city, "label": "LOC"} for city in all_cities],
            metadata={
                "model": f"spacy-{self.model_name}",
                "locations_found": all_cities,
                "extraction_method": "ner_patterns" if not (origin_entities or destination_entities) else "fine_tuned_ner"
            }
        )

    def _calculate_confidence(
        self,
        origin: Optional[str],
        destination: Optional[str],
        origin_entities: List[str],
        destination_entities: List[str],
        all_cities: List[str],
        is_valid: bool
    ) -> float:
        """
        Calcule la confiance de l'extraction basée sur plusieurs facteurs.
        
        Args:
            origin: Origine extraite
            destination: Destination extraite
            origin_entities: Entités ORIGIN détectées par le modèle fine-tuné
            destination_entities: Entités DESTINATION détectées par le modèle fine-tuné
            all_cities: Toutes les villes trouvées
            is_valid: Si la demande est valide
        
        Returns:
            Score de confiance entre 0.0 et 1.0
        """
        confidence = 0.0
        
        if all_cities:
            confidence += 0.2
        
        if origin_entities or destination_entities:
            confidence += 0.4  # Modèle fine-tuné = plus confiant
            if origin_entities and destination_entities:
                confidence += 0.2  # Les deux détectées directement
        else:
            confidence += 0.2
        
        if origin and destination:
            confidence += 0.2
        elif origin or destination:
            confidence += 0.1
        
        if is_valid and (origin or destination):
            confidence += 0.1
        
        if all_cities and not origin and not destination:
            confidence *= 0.5
        
        confidence = min(1.0, max(0.0, confidence))
        
        return round(confidence, 2)
    
    def _determine_origin_destination(self, text: str, cities: List[str], doc) -> tuple[Optional[str], Optional[str]]:
        """Détermine quelle ville est l'origine et laquelle est la destination."""
        origin = None
        destination = None
        
        text_lower = text.lower()
        
        pattern_depuis = re.search(r'depuis\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
        if pattern_depuis:
            origin_candidate = clean_station_name(pattern_depuis.group(1))
            text_avant_depuis = text[:pattern_depuis.start()]
            pattern_dest = re.search(r'(?:aller|rendre|voyager|se\s+rendre)\s+(?:à|vers|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text_avant_depuis, re.IGNORECASE)
            if pattern_dest:
                dest_candidate = clean_station_name(pattern_dest.group(1))
                for city in cities:
                    if city.lower() == origin_candidate.lower():
                        origin = city
                    if city.lower() == dest_candidate.lower():
                        destination = city
        
        if not origin or not destination:
            pattern_de_a = re.search(r'\bde\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)\s+(?:à|vers|pour|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_de_a:
                origin_candidate = clean_station_name(pattern_de_a.group(1))
                dest_candidate = clean_station_name(pattern_de_a.group(2))
                for city in cities:
                    if city.lower() == origin_candidate.lower() and not origin:
                        origin = city
                    if city.lower() == dest_candidate.lower() and not destination:
                        destination = city
        
        if not destination:
            pattern_aller_a = re.search(r'(?:aller|rendre|voyager|se\s+rendre)\s+(?:à|vers|a)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_aller_a:
                dest_candidate = clean_station_name(pattern_aller_a.group(1))
                for city in cities:
                    if city.lower() == dest_candidate.lower():
                        destination = city
                        break
        
        if not origin:
            pattern_partir_de = re.search(r'(?:partir|quitter)\s+(?:de|depuis)\s+([a-zéèêàôùç-]+(?:\s+[a-zéèêàôùç-]+)?)', text, re.IGNORECASE)
            if pattern_partir_de:
                origin_candidate = clean_station_name(pattern_partir_de.group(1))
                for city in cities:
                    if city.lower() == origin_candidate.lower():
                        origin = city
                        break
        
        if not origin and not destination and len(cities) == 2:
            origin = cities[0]
            destination = cities[1]
        elif not destination and len(cities) >= 1:
            available_cities = [c for c in cities if c != origin]
            if available_cities:
                destination = available_cities[0]
        
        return origin, destination
    
    def _is_travel_request(self, text: str, origin: Optional[str], destination: Optional[str]) -> bool:
        """Détermine si le texte est une demande de trajet valide."""
        travel_keywords = [
            "aller", "rendre", "voyager", "trajet", "billet", "train",
            "partir", "quitter", "arriver", "destination", "origine"
        ]
        
        text_lower = text.lower()
        has_travel_keyword = any(keyword in text_lower for keyword in travel_keywords)
        
        return (origin is not None or destination is not None) and has_travel_keyword
    
    def train(self, train_dataset: str | Path, valid_dataset: str | Path = None, output_dir: str | Path = None):
        """
        Entraîne (fine-tune) le modèle spaCy sur un dataset.
        
        Args:
            train_dataset: Chemin vers le dataset d'entraînement (JSONL)
            valid_dataset: Chemin vers le dataset de validation (JSONL, optionnel)
            output_dir: Dossier où sauvegarder le modèle entraîné
        """
        from src.nlp.training.convert import convert_to_spacy_format
        from src.nlp.training.trainer import train_spacy_model
        
        if not SPACY_AVAILABLE:
            raise ImportError("spacy is required. Install with: pip install spacy")
        
        output_dir = Path(output_dir) if output_dir else Path("models/nlp/spacy_finetuned")
        
        logger.info(f"Starting fine-tuning with base model: {self.model_name}")
        logger.info(f"Training dataset: {train_dataset}")
        
        train_data = convert_to_spacy_format(train_dataset)
        
        valid_data = None
        if valid_dataset:
            valid_data = convert_to_spacy_format(valid_dataset)
            logger.info(f"Validation dataset: {valid_dataset} ({len(valid_data)} samples)")
        
        model_path = train_spacy_model(
            base_model_name=self.model_name,
            train_data=train_data,
            output_dir=output_dir,
            n_iter=self.config.get("n_iter", 20),
            dropout=self.config.get("dropout", 0.1),
            valid_data=valid_data,
            labels=["ORIGIN", "DESTINATION"]
        )
        
        logger.info(f"Fine-tuning complete! Model saved to {model_path}")
        logger.info(f"To use this model, set 'custom_model_path' in config to: {model_path}")
        
        return model_path
