"""
Types de données communs pour tous les modules.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ModuleType(str, Enum):
    """Type de module."""
    STT = "stt"
    NLP = "nlp"
    PATHFINDING = "pathfinding"


@dataclass
class AudioSample:
    """Représente un échantillon audio."""
    path: str
    duration: float  # en secondes
    sample_rate: int
    channels: int
    transcript: Optional[str] = None  # Ground truth


@dataclass
class STTResult:
    """Résultat de la transcription speech-to-text."""
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None
    processing_time: Optional[float] = None  # en secondes
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NLPExtraction:
    """Résultat de l'extraction NLP."""
    origin: Optional[str] = None
    destination: Optional[str] = None
    is_valid: bool = True
    confidence: Optional[float] = None
    entities: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Route:
    """Résultat du pathfinding."""
    origin: str
    destination: str
    steps: List[str]  # Liste des villes/gares
    total_distance: Optional[float] = None  # en km
    total_time: Optional[float] = None  # en minutes
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Metrics:
    """Métriques génériques."""
    module: ModuleType
    model_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    metrics: Dict[str, float] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)

