"""
Types de données communs pour tous les modules du pipeline THOR.

Ce module définit les dataclasses et enums utilisés pour la communication
entre les différents composants du système (STT, NLP, Pathfinding).
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ModuleType(str, Enum):
    """
    Énumération des types de modules du pipeline.
    
    Attributes:
        STT: Module de Speech-to-Text (transcription audio).
        NLP: Module de traitement du langage naturel (extraction d'entités).
        PATHFINDING: Module de recherche d'itinéraire.
    """
    STT = "stt"
    NLP = "nlp"
    PATHFINDING = "pathfinding"


@dataclass
class AudioSample:
    """
    Représente un échantillon audio pour le traitement STT.
    
    Attributes:
        path (str): Chemin vers le fichier audio.
        duration (float): Durée de l'audio en secondes.
        sample_rate (int): Fréquence d'échantillonnage en Hz (ex: 16000, 44100).
        channels (int): Nombre de canaux audio (1=mono, 2=stéréo).
        transcript (Optional[str]): Transcription de référence (ground truth) pour l'évaluation.
    """
    path: str
    duration: float
    sample_rate: int
    channels: int
    transcript: Optional[str] = None


@dataclass
class STTResult:
    """
    Résultat de la transcription speech-to-text.
    
    Attributes:
        text (str): Texte transcrit de l'audio.
        confidence (Optional[float]): Score de confiance de la transcription (0.0 à 1.0).
        language (Optional[str]): Langue détectée ou utilisée (ex: "fr", "en").
        processing_time (Optional[float]): Temps de traitement en secondes.
        metadata (Dict[str, Any]): Métadonnées additionnelles (modèle utilisé, segments, etc).
    """
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None
    processing_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NLPExtraction:
    """
    Résultat de l'extraction NLP (origine et destination).
    
    Attributes:
        origin (Optional[str]): Ville ou gare d'origine extraite.
        destination (Optional[str]): Ville ou gare de destination extraite.
        is_valid (bool): Indique si l'extraction est valide (au moins une ville trouvée).
        confidence (Optional[float]): Score de confiance de l'extraction (0.0 à 1.0).
        entities (List[Dict[str, Any]]): Liste des entités détectées avec leurs métadonnées.
        metadata (Dict[str, Any]): Métadonnées additionnelles du modèle NLP.
    """
    origin: Optional[str] = None
    destination: Optional[str] = None
    is_valid: bool = True
    confidence: Optional[float] = None
    entities: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Route:
    """
    Résultat du calcul d'itinéraire (pathfinding).
    
    Attributes:
        origin (str): Ville ou gare de départ.
        destination (str): Ville ou gare d'arrivée.
        steps (List[str]): Liste ordonnée des villes/gares de l'itinéraire.
        total_distance (Optional[float]): Distance totale en kilomètres.
        total_time (Optional[float]): Temps de trajet total en minutes.
        metadata (Dict[str, Any]): Métadonnées additionnelles (segments, coordonnées, etc).
    """
    origin: str
    destination: str
    steps: List[str]
    total_distance: Optional[float] = None
    total_time: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)