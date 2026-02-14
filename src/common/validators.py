"""
Module de validation pour le pipeline THOR.

Fournit des fonctions de validation pour STT, NLP et Pathfinding.
"""
import re
from typing import Optional, List, Tuple, Dict
from pathlib import Path
import json


class TranscriptValidator:
    """
    Validateur pour les transcriptions STT.
    
    Détecte les transcriptions de mauvaise qualité ou incohérentes.
    """
    
    FRENCH_COMMON_WORDS = {
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
        "le", "la", "les", "un", "une", "des", "de", "du",
        "à", "au", "aux", "de", "du", "des",
        "et", "ou", "mais", "donc", "car",
        "aller", "veux", "vouloir", "partir", "voyager", "rendre",
        "train", "gare", "trajet", "itinéraire"
    }
    
    TRAVEL_KEYWORDS = [
        "aller", "veux aller", "je veux", "partir", "voyager",
        "train", "gare", "trajet", "itinéraire",
        "comment", "de", "à", "vers", "depuis",
        "rendre", "me rendre", "rejoindre"
    ]
    
    @staticmethod
    def validate(text: str) -> Dict[str, any]:
        """
        Valide une transcription.
        
        Args:
            text: Texte transcrit
            
        Returns:
            Dict avec is_valid, confidence, issues, suggestions
        """
        issues = []
        confidence = 1.0
        suggestions = []
        
        text_lower = text.lower().strip()
        
        if len(text) < 5:
            issues.append("Transcription trop courte")
            confidence = 0.0
            suggestions.append("Essayez de parler plus clairement et plus longtemps")
            return {
                "is_valid": False,
                "confidence": confidence,
                "issues": issues,
                "suggestions": suggestions
            }
        
        words = text_lower.split()
        
        french_word_count = sum(1 for w in words if w in TranscriptValidator.FRENCH_COMMON_WORDS)
        french_ratio = french_word_count / len(words) if words else 0
        
        if french_ratio < 0.15:
            issues.append("La transcription ne semble pas être en français")
            confidence *= 0.3
            suggestions.append("Assurez-vous de parler en français")
        
        has_travel_keyword = any(kw in text_lower for kw in TranscriptValidator.TRAVEL_KEYWORDS)
        if not has_travel_keyword:
            issues.append("Aucun mot-clé de voyage détecté dans la transcription")
            confidence *= 0.5
            suggestions.append("Utilisez des mots comme 'aller', 'train', 'gare', 'de X à Y'")
        
        if text.count('?') > 3 or text.count('!') > 3:
            issues.append("Transcription inhabituelle (ponctuation excessive)")
            confidence *= 0.6
        
        repeated_pattern = re.search(r'(\b\w+\b)(\s+\1){2,}', text_lower)
        if repeated_pattern:
            issues.append(f"Répétitions détectées: '{repeated_pattern.group(1)}'")
            confidence *= 0.7
            suggestions.append("La transcription contient des répétitions, essayez de reparler")
        
        is_valid = confidence >= 0.4
        
        return {
            "is_valid": is_valid,
            "confidence": confidence,
            "issues": issues,
            "suggestions": suggestions
        }


class CityValidator:
    """
    Validateur pour les noms de villes.
    
    Vérifie si les villes extraites sont valides et suggère des corrections.
    """
    
    def __init__(self, cities_file: Optional[str] = None):
        """
        Initialise le validateur.
        
        Args:
            cities_file: Chemin vers le fichier de villes valides (optionnel, charge depuis les datasets par défaut)
        """
        self.valid_cities = self._load_valid_cities(cities_file)
        self.normalized_to_original = self._build_normalized_mapping()
        self.city_aliases = self._build_aliases()
    
    @staticmethod
    def normalize_city_name(name: str) -> str:
        """
        Normalise un nom de ville pour la comparaison.
        Enlève les tirets, espaces multiples, apostrophes et met en minuscules.
        
        Args:
            name: Nom de ville à normaliser
            
        Returns:
            Nom normalisé
        """
        if not name:
            return ""
        
        normalized = name.lower().strip()
        normalized = normalized.replace('-', ' ').replace("'", ' ')
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = normalized.strip()
        
        return normalized
    
    def _build_normalized_mapping(self) -> Dict[str, str]:
        """
        Construit un mapping des noms normalisés vers les noms originaux.
        
        Returns:
            Dict[nom_normalisé] -> nom_original
        """
        mapping = {}
        for city in self.valid_cities:
            normalized = self.normalize_city_name(city)
            if normalized and normalized not in mapping:
                mapping[normalized] = city
        return mapping
    
    def _load_valid_cities(self, cities_file: Optional[str]) -> set:
        """Charge la liste des villes valides depuis les datasets."""
        valid_cities = set()
        
        if cities_file and Path(cities_file).exists():
            try:
                with open(cities_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        valid_cities = {city.lower() for city in data}
                        return valid_cities
            except Exception as e:
                print(f"Erreur lors du chargement de {cities_file}: {e}")
        
        base_path = Path(__file__).parent.parent.parent / "data" / "train_station"
        
        gares_file = base_path / "dataset_gares.json"
        if gares_file.exists():
            try:
                with open(gares_file, 'r', encoding='utf-8') as f:
                    gares = json.load(f)
                    for gare in gares:
                        nom_gare = gare.get('nom_gare', '').strip()
                        if nom_gare:
                            valid_cities.add(nom_gare.lower())
                            valid_cities.add(nom_gare.lower().replace('-', ' '))
                            
                            ville_principale = nom_gare.split()[0].lower()
                            if len(ville_principale) >= 3:
                                valid_cities.add(ville_principale)
                        
                        ville = gare.get('ville', {})
                        if isinstance(ville, dict):
                            nom_commune = ville.get('nom_commune', '').strip()
                            if nom_commune:
                                valid_cities.add(nom_commune.lower())
                                valid_cities.add(nom_commune.lower().replace('-', ' '))
                                
                                nom_base = nom_commune.lower().split('-')[0]
                                if len(nom_base) >= 3:
                                    valid_cities.add(nom_base)
            except Exception as e:
                print(f"Avertissement: Impossible de charger {gares_file}: {e}")
        
        villes_file = base_path / "dataset_villes.json"
        if villes_file.exists():
            try:
                with open(villes_file, 'r', encoding='utf-8') as f:
                    villes = json.load(f)
                    for ville in villes:
                        nom_commune = ville.get('nom_commune', '').strip()
                        if nom_commune:
                            valid_cities.add(nom_commune.lower())
                            valid_cities.add(nom_commune.lower().replace('-', ' '))
                            valid_cities.add(nom_commune.lower().replace("'", ' '))
                            
                            nom_base = nom_commune.lower().split('-')[0]
                            if len(nom_base) >= 3 and not nom_base.endswith('e'):
                                valid_cities.add(nom_base)
            except Exception as e:
                print(f"Avertissement: Impossible de charger {villes_file}: {e}")
        
        if not valid_cities:
            print("Avertissement: Aucun dataset chargé, utilisation de la liste par défaut")
            valid_cities = {
                "paris", "lyon", "marseille", "toulouse", "nice", "nantes",
                "montpellier", "strasbourg", "bordeaux", "lille", "rennes",
                "reims", "saint-étienne", "saint etienne", "toulon", "grenoble", 
                "dijon", "angers", "nîmes", "nimes", "villeurbanne", "le mans",
                "aix-en-provence", "aix en provence", "clermont-ferrand", 
                "clermont ferrand", "brest", "tours", "amiens", "limoges",
                "annecy", "perpignan", "boulogne-billancourt", "metz", "besançon",
                "orléans", "orleans", "rouen", "argenteuil", "mulhouse", "caen",
                "biarritz", "bayonne", "pau", "lourdes", "tarbes"
            }
        else:
            print(f"✓ {len(valid_cities)} villes/gares chargées dans le validateur")
        
        return valid_cities
    
    def _build_aliases(self) -> Dict[str, str]:
        """Construit un dictionnaire d'alias de villes."""
        aliases = {
            "st etienne": "saint-étienne",
            "saint etienne": "saint-étienne",
            "st étienne": "saint-étienne",
            "aix": "aix-en-provence",
            "clermont": "clermont-ferrand",
            "boulogne": "boulogne-billancourt",
        }
        
        additional_aliases = {}
        for city in self.valid_cities:
            city_no_accent = city.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
            city_no_accent = city_no_accent.replace('à', 'a').replace('â', 'a')
            city_no_accent = city_no_accent.replace('ô', 'o').replace('ù', 'u')
            city_no_accent = city_no_accent.replace('î', 'i').replace('ï', 'i')
            city_no_accent = city_no_accent.replace('û', 'u').replace('ü', 'u')
            
            if city_no_accent != city and city_no_accent not in self.valid_cities:
                additional_aliases[city_no_accent] = city
        
        aliases.update(additional_aliases)
        return aliases
    
    def validate_city(self, city: Optional[str]) -> Dict[str, any]:
        """
        Valide une ville et suggère des corrections.
        
        Args:
            city: Nom de la ville
            
        Returns:
            Dict avec is_valid, corrected_city, suggestions, confidence
        """
        if not city:
            return {
                "is_valid": False,
                "corrected_city": None,
                "suggestions": [],
                "confidence": 0.0,
                "issue": "Ville manquante"
            }
        
        city_lower = city.lower().strip()
        
        if city_lower in self.valid_cities:
            return {
                "is_valid": True,
                "corrected_city": city,
                "suggestions": [],
                "confidence": 1.0,
                "issue": None
            }
        
        city_normalized = self.normalize_city_name(city)
        
        if city_normalized in self.normalized_to_original:
            original_name = self.normalized_to_original[city_normalized]
            return {
                "is_valid": True,
                "corrected_city": original_name.title(),
                "suggestions": [] if city_lower == original_name else [f"Reconnu comme: {original_name.title()}"],
                "confidence": 1.0,
                "issue": None
            }
        
        if city_normalized in self.city_aliases:
            corrected = self.city_aliases[city_normalized]
            return {
                "is_valid": True,
                "corrected_city": corrected.title(),
                "suggestions": [f"Ville corrigée: {corrected.title()}"],
                "confidence": 0.95,
                "issue": None
            }
        
        best_match = None
        best_match_score = 0
        best_match_original = None
        
        for normalized_name, original_name in self.normalized_to_original.items():
            if len(city_normalized) >= 4:
                if city_normalized in normalized_name:
                    score = len(city_normalized) / len(normalized_name)
                    if score > best_match_score and score >= 0.5:
                        best_match_score = score
                        best_match = normalized_name
                        best_match_original = original_name
                
                elif normalized_name in city_normalized and len(normalized_name) >= 4:
                    score = len(normalized_name) / len(city_normalized)
                    if score > best_match_score and score >= 0.5:
                        best_match_score = score
                        best_match = normalized_name
                        best_match_original = original_name
        
        if best_match and best_match_original and best_match_score >= 0.7:
            return {
                "is_valid": True,
                "corrected_city": best_match_original.title(),
                "suggestions": [f"Correspondance trouvée: {best_match_original.title()}"],
                "confidence": 0.85 if best_match_score >= 0.9 else 0.75,
                "issue": None
            }
        
        suggestions = self._find_similar_cities(city_normalized)
        
        return {
            "is_valid": False,
            "corrected_city": None,
            "suggestions": suggestions,
            "confidence": 0.3 if suggestions else 0.1,
            "issue": f"Ville inconnue: '{city}'"
        }
    
    def _find_similar_cities(self, city: str, max_suggestions: int = 3) -> List[str]:
        """
        Trouve des villes similaires en utilisant la normalisation.
        
        Args:
            city: Nom de la ville normalisé
            max_suggestions: Nombre max de suggestions
            
        Returns:
            Liste de suggestions
        """
        suggestions = []
        city_normalized = self.normalize_city_name(city)
        
        for normalized_name, original_name in self.normalized_to_original.items():
            if city_normalized in normalized_name or normalized_name in city_normalized:
                if len(suggestions) < max_suggestions:
                    suggestions.append(original_name.title())
            elif self._simple_similarity(city_normalized, normalized_name) > 0.6:
                if len(suggestions) < max_suggestions:
                    suggestions.append(original_name.title())
        
        return suggestions[:max_suggestions]
    
    @staticmethod
    def _simple_similarity(s1: str, s2: str) -> float:
        """Calcule une similarité simple entre deux chaînes."""
        if not s1 or not s2:
            return 0.0
        
        longer = max(len(s1), len(s2))
        common = sum(1 for a, b in zip(s1, s2) if a == b)
        
        return common / longer


class ExtractionValidator:
    """
    Validateur complet pour l'extraction NLP.
    
    Combine validation de transcription et de villes.
    """
    
    def __init__(self, cities_file: Optional[str] = None):
        """
        Initialise le validateur.
        
        Args:
            cities_file: Chemin vers le fichier de villes valides
        """
        self.transcript_validator = TranscriptValidator()
        self.city_validator = CityValidator(cities_file)
    
    def validate_extraction(
        self,
        transcript: str,
        origin: Optional[str],
        destination: Optional[str],
        nlp_confidence: float
    ) -> Dict[str, any]:
        """
        Valide une extraction complète.
        
        Args:
            transcript: Texte transcrit
            origin: Origine extraite
            destination: Destination extraite
            nlp_confidence: Confiance du modèle NLP
            
        Returns:
            Dict complet avec validation, erreurs, suggestions
        """
        transcript_validation = self.transcript_validator.validate(transcript)
        
        if not transcript_validation["is_valid"]:
            return {
                "is_valid": False,
                "error_type": "transcript_invalid",
                "error_message": "La transcription audio est de mauvaise qualité",
                "issues": transcript_validation["issues"],
                "suggestions": transcript_validation["suggestions"],
                "confidence": transcript_validation["confidence"]
            }
        
        origin_validation = self.city_validator.validate_city(origin)
        dest_validation = self.city_validator.validate_city(destination)
        
        corrected_origin = origin_validation["corrected_city"] or origin
        corrected_destination = dest_validation["corrected_city"] or destination
        
        issues = []
        suggestions = []
        overall_confidence = nlp_confidence * transcript_validation["confidence"]
        
        if not origin and not destination:
            return {
                "is_valid": False,
                "error_type": "no_cities_detected",
                "error_message": "Aucune ville détectée dans votre demande",
                "issues": ["Aucune ville n'a pu être identifiée"],
                "suggestions": [
                    "Essayez de reformuler: 'Je veux aller de [VILLE] à [VILLE]'",
                    "Exemple: 'Je veux aller de Paris à Lyon'",
                    "Prononcez clairement les noms de villes"
                ],
                "confidence": 0.0
            }
        
        if not origin_validation["is_valid"]:
            issues.append(origin_validation["issue"])
            suggestions.extend(origin_validation["suggestions"])
            if origin_validation["suggestions"]:
                suggestions.insert(0, f"Vouliez-vous dire: {', '.join(origin_validation['suggestions'][:2])} ?")
            overall_confidence *= 0.5
        
        if not dest_validation["is_valid"]:
            issues.append(dest_validation["issue"])
            suggestions.extend(dest_validation["suggestions"])
            if dest_validation["suggestions"]:
                suggestions.insert(0, f"Vouliez-vous dire: {', '.join(dest_validation['suggestions'][:2])} ?")
            overall_confidence *= 0.5
        
        if not origin:
            issues.append("Ville de départ manquante")
            suggestions.append("Précisez la ville de départ: 'de [VILLE]' ou 'depuis [VILLE]'")
        
        if not destination:
            issues.append("Ville d'arrivée manquante")
            suggestions.append("Précisez la ville d'arrivée: 'à [VILLE]' ou 'vers [VILLE]'")
        
        if origin and destination and origin.lower() == destination.lower():
            return {
                "is_valid": False,
                "error_type": "same_origin_destination",
                "error_message": "La ville de départ et d'arrivée sont identiques",
                "issues": ["Origine et destination identiques"],
                "suggestions": [
                    "Veuillez choisir deux villes différentes",
                    "Exemple: 'Je veux aller de Paris à Lyon'"
                ],
                "confidence": 0.0
            }
        
        is_valid = (
            (origin_validation["is_valid"] or origin_validation["corrected_city"]) and
            (dest_validation["is_valid"] or dest_validation["corrected_city"]) and
            overall_confidence >= 0.3
        )
        
        error_type = None
        error_message = None
        
        if not is_valid:
            if issues:
                error_type = "extraction_errors"
                error_message = "Des erreurs ont été détectées dans l'extraction des villes"
        
        return {
            "is_valid": is_valid,
            "error_type": error_type,
            "error_message": error_message,
            "corrected_origin": corrected_origin,
            "corrected_destination": corrected_destination,
            "issues": issues,
            "suggestions": suggestions,
            "confidence": overall_confidence,
            "origin_validation": origin_validation,
            "destination_validation": dest_validation
        }
