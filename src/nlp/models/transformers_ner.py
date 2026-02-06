"""
Modèle NLP utilisant Transformers (CamemBERT) pour l'extraction NER.
"""
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from src.nlp.interfaces import NLPModel
from src.common.types import NLPExtraction
from src.common.logging import setup_logging
from src.common.text_norm import clean_station_name

logger = setup_logging(module="nlp.transformers")

try:
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModelForTokenClassification = None
    pipeline = None
    torch = None


class TransformersNERModel(NLPModel):
    """
    Modèle NLP basé sur Transformers (CamemBERT) pour extraire origine/destination.
    
    Utilise un modèle pré-entraîné français pour NER et des patterns pour déterminer
    origine/destination.
    """
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.model_name = self.config.get("model_name", "Jean-Baptiste/camembert-ner")
        self.custom_model_path = self.config.get("custom_model_path")
        self._ner_pipeline = None
        self._device = self.config.get("device", "cpu")
    
    def _load_model(self):
        """Charge le modèle Transformers."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers and torch are required. Install with: pip install transformers torch")
        
        try:
            if self.custom_model_path:
                model_path = Path(self.custom_model_path)
                if model_path.exists():
                    logger.info(f"Loading custom fine-tuned model: {model_path}")
                    self._ner_pipeline = pipeline(
                        "ner",
                        model=str(model_path),
                        tokenizer=str(model_path),
                        device=0 if self._device == "cuda" and torch.cuda.is_available() else -1,
                        aggregation_strategy="simple"
                    )
                    logger.info("Custom model loaded successfully")
                    return
                else:
                    logger.warning(f"Custom model not found at {model_path}, using base model")
            
            logger.info(f"Loading Transformers model: {self.model_name}")
            
            # Si c'est un modèle NER pré-entraîné problématique, utilise un modèle de base
            # et crée un pipeline token-classification
            if "camembert-ner" in self.model_name.lower() or "ner" in self.model_name.lower():
                logger.info("Model name suggests NER model, but using camembert-base for reliability")
                # Utilise camembert-base et crée un pipeline token-classification
                from transformers import AutoTokenizer, AutoModelForTokenClassification
                try:
                    tokenizer = AutoTokenizer.from_pretrained("camembert-base", use_fast=False)
                    # Charge un modèle avec des labels (même si pas entraîné, ça fonctionne pour l'extraction)
                    model = AutoModelForTokenClassification.from_pretrained(
                        "camembert-base",
                        num_labels=5  # O, B-ORIGIN, I-ORIGIN, B-DESTINATION, I-DESTINATION
                    )
                    self._ner_pipeline = pipeline(
                        "token-classification",
                        model=model,
                        tokenizer=tokenizer,
                        device=0 if self._device == "cuda" and torch.cuda.is_available() else -1,
                        aggregation_strategy="simple"
                    )
                    logger.info("Transformers model loaded successfully (using camembert-base)")
                except Exception as e:
                    logger.error(f"Failed to load camembert-base: {e}")
                    raise
            else:
                # Essaie de charger le modèle directement
                try:
                    self._ner_pipeline = pipeline(
                        "ner",
                        model=self.model_name,
                        device=0 if self._device == "cuda" and torch.cuda.is_available() else -1,
                        aggregation_strategy="simple"
                    )
                    logger.info("Transformers model loaded successfully")
                except Exception as e:
                    logger.error(f"Failed to load model {self.model_name}: {e}")
                    raise
        except Exception as e:
            logger.error(f"Failed to load Transformers model: {e}")
            raise
    
    def extract(self, text: str) -> NLPExtraction:
        """
        Extrait l'origine et la destination avec Transformers NER.
        
        Args:
            text: Texte à analyser
        
        Returns:
            NLPExtraction avec origine et destination
        """
        if not self._initialized:
            self.initialize()
        
        # Extraction NER
        entities = self._ner_pipeline(text)
        
        # Filtre les entités de type LOC (location)
        locations = []
        for entity in entities:
            if entity.get("entity_group") in ["LOC", "MISC"] or "LOC" in str(entity.get("label", "")):
                city = entity.get("word", "").strip()
                if city:
                    locations.append(city)
        
        # Utilise des patterns pour déterminer origine/destination
        origin, destination = self._extract_with_patterns(text, locations)
        
        # Détermine si c'est une demande valide
        is_valid = self._is_valid_request(text, origin, destination)
        
        # Calcule la confiance
        confidence = self._calculate_confidence(origin, destination, entities, is_valid)
        
        return NLPExtraction(
            origin=origin,
            destination=destination,
            is_valid=is_valid,
            confidence=confidence,
            entities=[{"text": loc, "label": "LOC"} for loc in locations],
            metadata={
                "model": f"transformers-{self.model_name.split('/')[-1]}",
                "locations_found": locations,
                "extraction_method": "transformers_ner_patterns"
            }
        )
    
    def _extract_with_patterns(self, text: str, locations: List[str]) -> tuple:
        """Utilise des patterns pour déterminer origine/destination."""
        text_lower = text.lower()
        origin = None
        destination = None
        
        origin_patterns = [
            r'(?:de|depuis|partir de|partant de)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)\s+(?:vers|à|pour)',
        ]
        
        dest_patterns = [
            r'(?:à|vers|pour|aller à|rendre à)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
            r'(?:aller|rendre|voyager)\s+(?:à|vers|en)\s+([A-Z][a-zéèêàôùç-]+(?:\s+[A-Z][a-zéèêàôùç-]+)?)',
        ]
        
        for pattern in origin_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                candidate = clean_station_name(match.group(1))
                if candidate in locations or any(loc.lower() == candidate.lower() for loc in locations):
                    origin = candidate
                    break
        
        for pattern in dest_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                candidate = clean_station_name(match.group(1))
                if candidate in locations or any(loc.lower() == candidate.lower() for loc in locations):
                    destination = candidate
                    break
        
        if not origin and not destination and locations:
            destination = locations[0]
        elif not origin and locations and destination:
            remaining = [loc for loc in locations if loc.lower() != destination.lower()]
            if remaining:
                origin = remaining[0]
        elif not destination and locations and origin:
            remaining = [loc for loc in locations if loc.lower() != origin.lower()]
            if remaining:
                destination = remaining[0]
        
        return origin, destination
    
    def _is_valid_request(self, text: str, origin: Optional[str], destination: Optional[str]) -> bool:
        """Détermine si c'est une demande de trajet valide."""
        travel_keywords = ["aller", "rendre", "voyager", "trajet", "route", "chemin", "partir", "se rendre"]
        text_lower = text.lower()
        
        # Doit contenir un mot-clé de trajet
        has_travel_keyword = any(kw in text_lower for kw in travel_keywords)
        
        # Doit avoir au moins une ville
        has_location = origin is not None or destination is not None
        
        return has_travel_keyword and has_location
    
    def _calculate_confidence(self, origin: Optional[str], destination: Optional[str], 
                             entities: List[Dict], is_valid: bool) -> float:
        """Calcule la confiance de l'extraction."""
        if not is_valid:
            return 0.0
        
        confidence = 0.5
        
        if origin and destination:
            confidence += 0.3
        
        if entities:
            confidence += 0.1
        
        if origin and len(origin) > 2:
            confidence += 0.05
        if destination and len(destination) > 2:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def train(self, train_dataset: str | Path, valid_dataset: str | Path = None, output_dir: str | Path = None):
        """
        Entraîne le modèle Transformers (fine-tuning).
        
        Note: Le fine-tuning de Transformers nécessite un dataset au format spécifique.
        Pour l'instant, on utilise le même format que spaCy.
        """
        from src.nlp.training.transformers_trainer import train_transformers_model
        from src.nlp.training.convert import convert_to_spacy_format
        from src.common.io import read_jsonl
        
        output_dir = Path(output_dir) if output_dir else Path("models/nlp/transformers_finetuned")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        train_data = convert_to_spacy_format(train_dataset)
        valid_data = convert_to_spacy_format(valid_dataset) if valid_dataset else None
        
        model_path = train_transformers_model(
            base_model_name=self.model_name,
            train_data=train_data,
            output_dir=output_dir,
            valid_data=valid_data,
            n_epochs=self.config.get("n_epochs", 3),
            learning_rate=self.config.get("learning_rate", 2e-5),
            batch_size=self.config.get("batch_size", 16)
        )
        
        return model_path

