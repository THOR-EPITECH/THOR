# Documentation THOR - Normes et Bonnes Pratiques

## Table des matières
1. [Normes de Commit](#normes-de-commit)
2. [Documentation Python (Docstrings)](#documentation-python-docstrings)
3. [Architecture de Code Python](#architecture-de-code-python)
4. [Architecture Multi-Modèles NLP](#architecture-multi-modèles-nlp)
5. [Benchmarking et Comparaison de Modèles](#benchmarking-et-comparaison-de-modèles)
6. [Découpage et Organisation du Code](#découpage-et-organisation-du-code)

---

## Normes de Commit

### Format des messages de commit

Les messages de commit doivent suivre le format **Conventional Commits** :

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types de commits

- **feat**: Nouvelle fonctionnalité
- **fix**: Correction de bug
- **docs**: Documentation uniquement
- **style**: Changements de formatage (pas de changement de code)
- **refactor**: Refactorisation du code
- **perf**: Amélioration de performance
- **test**: Ajout ou modification de tests
- **chore**: Tâches de maintenance (dépendances, build, etc.)
- **ci**: Changements de configuration CI/CD

### Exemples

```bash
feat(nlp): ajout de la reconnaissance des villes avec accents
fix(pathfinder): correction du calcul de distance dans le graphe
docs(readme): mise à jour de la documentation d'installation
refactor(parser): simplification de la fonction extract_cities
test(nlp): ajout de tests unitaires pour le tokenizer
```

### Règles importantes

- **Description courte** : Maximum 50 caractères pour la première ligne
- **Corps optionnel** : Détails supplémentaires après une ligne vide
- **Imperatif** : Utiliser l'impératif ("ajouter" pas "ajouté" ou "ajoute")
- **Pas de point final** : La première ligne ne doit pas se terminer par un point
- **Scope optionnel** : Indiquer le module/package concerné entre parenthèses

### Exemple complet

```bash
feat(nlp): extraction des villes avec gestion des fautes d'orthographe

- Ajout de la fonction fuzzy_matching pour les noms de villes
- Support des accents et caractères spéciaux
- Gestion des noms composés (ex: Port-Boulet)

Closes #42
```

---

## Documentation Python (Docstrings)

### Style de documentation

Nous utilisons le format **Google Style** pour les docstrings Python.

### Format de base

```python
def fonction(param1: type, param2: type) -> type_retour:
    """Description courte en une ligne.
    
    Description détaillée si nécessaire. Peut s'étendre sur
    plusieurs lignes pour expliquer le comportement de la fonction,
    ses cas d'usage, ou des détails d'implémentation importants.
    
    Args:
        param1 (type): Description du premier paramètre.
        param2 (type): Description du second paramètre.
            Peut être sur plusieurs lignes si nécessaire.
    
    Returns:
        type_retour: Description de la valeur retournée.
    
    Raises:
        TypeError: Description de quand cette exception est levée.
        ValueError: Description de quand cette exception est levée.
    
    Example:
        >>> fonction("exemple", 42)
        "résultat attendu"
        
        >>> fonction("autre", 10)
        "autre résultat"
    
    Note:
        Notes importantes sur l'utilisation ou les limitations.
    """
    pass
```

### Classes

```python
class MaClasse:
    """Description courte de la classe.
    
    Description détaillée de la classe, son rôle dans l'application,
    et comment elle s'intègre avec les autres composants.
    
    Attributes:
        attribut1 (type): Description de l'attribut.
        attribut2 (type): Description de l'attribut.
    
    Example:
        >>> obj = MaClasse("valeur1", "valeur2")
        >>> obj.methode()
        "résultat"
    """
    
    def __init__(self, param1: str, param2: int):
        """Initialise une instance de MaClasse.
        
        Args:
            param1 (str): Description du paramètre.
            param2 (int): Description du paramètre.
        """
        self.attribut1 = param1
        self.attribut2 = param2
```

### Modules

```python
"""Description courte du module.

Description détaillée du module, son objectif principal,
et les fonctionnalités qu'il fournit.

Example:
    Utilisation basique du module:
    
    >>> from mon_module import fonction_principale
    >>> resultat = fonction_principale()
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"
```

### Types complexes

```python
from typing import List, Dict, Optional, Tuple

def traiter_donnees(
    villes: List[str],
    config: Optional[Dict[str, int]] = None
) -> Tuple[List[str], int]:
    """Traite une liste de villes selon une configuration.
    
    Args:
        villes (List[str]): Liste des noms de villes à traiter.
        config (Optional[Dict[str, int]], optional): Configuration
            de traitement. Si None, utilise la configuration par défaut.
            Defaults to None.
    
    Returns:
        Tuple[List[str], int]: Tuple contenant:
            - Liste des villes traitées
            - Nombre de villes valides
    
    Raises:
        ValueError: Si la liste de villes est vide.
    """
    pass
```

### Bonnes pratiques

1. **Toujours documenter** : Chaque fonction publique doit avoir une docstring
2. **Type hints** : Utiliser les annotations de type Python 3.5+
3. **Exemples** : Inclure des exemples d'utilisation quand c'est pertinent
4. **Exceptions** : Documenter toutes les exceptions possibles
5. **Cohérence** : Maintenir le même style dans tout le projet

---

## Architecture de Code Python

### Structure de projet recommandée

```
thor/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── benchmarks.md
├── src/
│   ├── __init__.py
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── model_interface.py    # Interface commune
│   │   │   └── base_model.py         # Classe de base abstraite
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── simple_model.py       # Modèle simple (baseline)
│   │   │   ├── camembert_model.py    # CamemBERT
│   │   │   ├── transformer_model.py  # Autres transformers
│   │   │   └── bert_model.py         # BERT français
│   │   ├── parser.py                 # Parser générique
│   │   ├── tokenizer.py              # Tokenizers communs
│   │   ├── extractor.py              # Extraction de villes
│   │   └── factory.py                # Factory pour créer modèles
│   ├── pathfinder/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   └── algorithms.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py                # Métriques d'évaluation
│   │   ├── benchmark.py              # Benchmarking
│   │   └── comparator.py             # Comparaison de modèles
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_nlp/
│   │   ├── test_parser.py
│   │   ├── test_extractor.py
│   │   └── test_models/
│   │       ├── test_simple_model.py
│   │       ├── test_camembert_model.py
│   │       └── test_transformer_model.py
│   ├── test_pathfinder/
│   │   └── test_graph.py
│   └── test_evaluation/
│       └── test_benchmark.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── datasets/
│       ├── train.csv
│       ├── test.csv
│       └── validation.csv
├── models/
│   ├── camembert/
│   ├── bert/
│   └── checkpoints/
├── results/
│   ├── benchmarks/
│   └── comparisons/
└── scripts/
    ├── train.py
    ├── evaluate.py
    ├── benchmark.py
    └── compare_models.py
```

### Principes d'architecture

#### 1. Séparation des responsabilités (SoC)

Chaque module doit avoir une responsabilité unique et bien définie :

- **nlp/** : Traitement du langage naturel uniquement
- **pathfinder/** : Recherche de chemin dans le graphe uniquement
- **utils/** : Fonctions utilitaires réutilisables
- **main.py** : Point d'entrée et orchestration

#### 2. Couches d'abstraction

```
┌─────────────────────────────────┐
│      Interface Utilisateur      │
│         (CLI / API)             │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      Orchestration              │
│        (main.py)                │
└──────────────┬──────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐          ┌─────▼─────┐
│  NLP   │          │ Pathfinder│
│ Module │          │  Module   │
└───┬────┘          └─────┬─────┘
    │                     │
┌───▼─────────────────────▼─────┐
│      Utilitaires / Helpers     │
└────────────────────────────────┘
```

#### 3. Dépendances

- **Dépendances vers le bas** : Les modules de haut niveau dépendent des modules de bas niveau
- **Pas de dépendances circulaires** : Utiliser des interfaces ou des callbacks si nécessaire
- **Injection de dépendances** : Passer les dépendances en paramètres plutôt que de les importer directement

#### 4. Configuration

```python
# config.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration de l'application."""
    model_path: str = "models/camembert"
    max_sequence_length: int = 512
    batch_size: int = 32
    learning_rate: float = 2e-5
    database_url: Optional[str] = None
```

### Patterns recommandés

#### Strategy Pattern (pour les modèles NLP)

```python
# nlp/base/model_interface.py
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class ExtractionResult:
    """Résultat d'extraction d'une commande."""
    departure: Optional[str]
    destination: Optional[str]
    intermediate_stops: list[str]
    is_valid: bool
    confidence: float
    error_message: Optional[str] = None


class NLPModelInterface(ABC):
    """Interface commune pour tous les modèles NLP."""
    
    @abstractmethod
    def extract(self, text: str) -> ExtractionResult:
        """Extrait les informations d'une commande.
        
        Args:
            text (str): Texte de la commande à analyser.
        
        Returns:
            ExtractionResult: Résultat de l'extraction.
        """
        pass
    
    @abstractmethod
    def validate_order(self, text: str) -> bool:
        """Valide si le texte est une commande valide.
        
        Args:
            text (str): Texte à valider.
        
        Returns:
            bool: True si c'est une commande valide.
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Retourne le nom du modèle."""
        pass
    
    @property
    @abstractmethod
    def model_type(self) -> str:
        """Retourne le type du modèle (simple, transformer, etc.)."""
        pass
```

#### Factory Pattern amélioré

```python
# nlp/factory.py
from typing import Dict, Type
from nlp.base.model_interface import NLPModelInterface
from nlp.models.simple_model import SimpleNLPModel
from nlp.models.camembert_model import CamemBERTModel
from nlp.models.transformer_model import TransformerModel

class NLPModelFactory:
    """Factory pour créer des instances de modèles NLP."""
    
    _models: Dict[str, Type[NLPModelInterface]] = {
        "simple": SimpleNLPModel,
        "camembert": CamemBERTModel,
        "transformer": TransformerModel,
    }
    
    @classmethod
    def create(
        self, 
        model_type: str, 
        **kwargs
    ) -> NLPModelInterface:
        """Crée une instance d'un modèle NLP.
        
        Args:
            model_type (str): Type de modèle à créer.
            **kwargs: Arguments additionnels pour l'initialisation.
        
        Returns:
            NLPModelInterface: Instance du modèle.
        
        Raises:
            ValueError: Si le type de modèle est inconnu.
        
        Example:
            >>> model = NLPModelFactory.create("camembert", model_path="models/camembert")
            >>> result = model.extract("Je veux aller de Paris à Lyon")
        """
        if model_type not in self._models:
            available = ", ".join(self._models.keys())
            raise ValueError(
                f"Unknown model type: {model_type}. "
                f"Available: {available}"
            )
        
        model_class = self._models[model_type]
        return model_class(**kwargs)
    
    @classmethod
    def list_available_models(cls) -> list[str]:
        """Liste tous les modèles disponibles.
        
        Returns:
            list[str]: Liste des noms de modèles disponibles.
        """
        return list(cls._models.keys())
```

#### Repository Pattern

```python
# pathfinder/repository.py
from abc import ABC, abstractmethod

class StationRepository(ABC):
    @abstractmethod
    def find_station(self, name: str) -> Optional[Station]:
        pass
    
    @abstractmethod
    def get_all_stations(self) -> List[Station]:
        pass

class SNCFStationRepository(StationRepository):
    def __init__(self, database_url: str):
        self.db = connect(database_url)
    
    def find_station(self, name: str) -> Optional[Station]:
        # Implémentation spécifique
        pass
```

---

## Architecture Multi-Modèles NLP

### Principe : Interface commune pour tous les modèles

Tous les modèles NLP doivent implémenter la même interface (`NLPModelInterface`) pour permettre :
- Le remplacement facile d'un modèle par un autre
- La comparaison équitable entre modèles
- Le benchmarking automatisé
- L'ajout de nouveaux modèles sans modifier le code existant

### Structure d'un modèle NLP

#### Exemple : Modèle simple (baseline)

```python
# nlp/models/simple_model.py
from typing import List, Optional
from nlp.base.model_interface import NLPModelInterface, ExtractionResult
from nlp.extractor import CityExtractor
from nlp.tokenizer import SimpleTokenizer

class SimpleNLPModel(NLPModelInterface):
    """Modèle NLP simple utilisant des règles et dictionnaires.
    
    Ce modèle sert de baseline pour comparer avec les modèles
    plus complexes comme les transformers.
    """
    
    def __init__(self, city_list: List[str]):
        """Initialise le modèle simple.
        
        Args:
            city_list (List[str]): Liste des villes connues.
        """
        self.city_extractor = CityExtractor(city_list)
        self.tokenizer = SimpleTokenizer()
        self._model_name = "simple"
        self._model_type = "rule-based"
    
    def extract(self, text: str) -> ExtractionResult:
        """Extrait les informations avec un modèle simple.
        
        Args:
            text (str): Texte de la commande.
        
        Returns:
            ExtractionResult: Résultat de l'extraction.
        """
        tokens = self.tokenizer.tokenize(text)
        cities = self.city_extractor.extract(tokens)
        
        if len(cities) < 2:
            return ExtractionResult(
                departure=None,
                destination=None,
                intermediate_stops=[],
                is_valid=False,
                confidence=0.0,
                error_message="Pas assez de villes trouvées"
            )
        
        # Logique simple pour déterminer départ/destination
        departure, destination = self._identify_departure_destination(
            text, cities
        )
        
        return ExtractionResult(
            departure=departure,
            destination=destination,
            intermediate_stops=[],
            is_valid=True,
            confidence=0.7  # Confiance moyenne pour baseline
        )
    
    def validate_order(self, text: str) -> bool:
        """Valide si c'est une commande valide."""
        result = self.extract(text)
        return result.is_valid
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    @property
    def model_type(self) -> str:
        return self._model_type
    
    def _identify_departure_destination(
        self, 
        text: str, 
        cities: List[str]
    ) -> tuple[Optional[str], Optional[str]]:
        """Identifie départ et destination."""
        # Logique basée sur mots-clés (de, depuis, à, vers)
        # ...
        pass
```

#### Exemple : Modèle CamemBERT

```python
# nlp/models/camembert_model.py
from transformers import CamembertTokenizer, CamembertForSequenceClassification
from nlp.base.model_interface import NLPModelInterface, ExtractionResult
import torch

class CamemBERTModel(NLPModelInterface):
    """Modèle NLP basé sur CamemBERT pour le français."""
    
    def __init__(
        self, 
        model_path: str = "camembert-base",
        device: str = "cpu"
    ):
        """Initialise le modèle CamemBERT.
        
        Args:
            model_path (str): Chemin vers le modèle pré-entraîné.
            device (str): Device pour l'inférence (cpu/cuda).
        """
        self.tokenizer = CamembertTokenizer.from_pretrained(model_path)
        self.model = CamembertForSequenceClassification.from_pretrained(
            model_path
        )
        self.model.eval()
        self.device = device
        self.model.to(device)
        self._model_name = "camembert"
        self._model_type = "transformer"
    
    def extract(self, text: str) -> ExtractionResult:
        """Extrait les informations avec CamemBERT.
        
        Args:
            text (str): Texte de la commande.
        
        Returns:
            ExtractionResult: Résultat de l'extraction.
        """
        # Tokenisation
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        # Inférence
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(
                outputs.logits, 
                dim=-1
            )
        
        # Extraction des villes et classification
        departure, destination = self._extract_cities_from_output(
            text, predictions
        )
        confidence = float(predictions.max())
        
        return ExtractionResult(
            departure=departure,
            destination=destination,
            intermediate_stops=[],
            is_valid=departure is not None and destination is not None,
            confidence=confidence
        )
    
    def validate_order(self, text: str) -> bool:
        """Valide si c'est une commande valide."""
        result = self.extract(text)
        return result.is_valid
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    @property
    def model_type(self) -> str:
        return self._model_type
    
    def _extract_cities_from_output(
        self, 
        text: str, 
        predictions: torch.Tensor
    ) -> tuple[Optional[str], Optional[str]]:
        """Extrait les villes depuis les prédictions du modèle."""
        # Logique d'extraction spécifique à CamemBERT
        # ...
        pass
```

### Utilisation des modèles

```python
# Exemple d'utilisation avec différents modèles
from nlp.factory import NLPModelFactory

# Créer différents modèles
simple_model = NLPModelFactory.create("simple", city_list=VILLES_FRANCE)
camembert_model = NLPModelFactory.create(
    "camembert", 
    model_path="models/camembert-finetuned"
)

# Utiliser de la même manière grâce à l'interface commune
text = "Je veux aller de Paris à Lyon"

result_simple = simple_model.extract(text)
result_camembert = camembert_model.extract(text)

# Comparer les résultats
print(f"Simple: {result_simple.departure} -> {result_simple.destination}")
print(f"CamemBERT: {result_camembert.departure} -> {result_camembert.destination}")
```

---

## Benchmarking et Comparaison de Modèles

### Architecture de benchmarking

```python
# evaluation/benchmark.py
from typing import List, Dict
from nlp.base.model_interface import NLPModelInterface
from evaluation.metrics import Metrics
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    """Résultat d'un benchmark pour un modèle."""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    inference_time: float  # en secondes
    memory_usage: float    # en MB
    total_samples: int
    correct_predictions: int


class ModelBenchmark:
    """Classe pour benchmarker plusieurs modèles NLP."""
    
    def __init__(self, test_dataset: List[Dict]):
        """Initialise le benchmark.
        
        Args:
            test_dataset (List[Dict]): Dataset de test avec format:
                [{"id": "1", "text": "...", "departure": "...", "destination": "..."}]
        """
        self.test_dataset = test_dataset
        self.metrics = Metrics()
    
    def benchmark_model(
        self, 
        model: NLPModelInterface
    ) -> BenchmarkResult:
        """Benchmarke un modèle unique.
        
        Args:
            model (NLPModelInterface): Modèle à évaluer.
        
        Returns:
            BenchmarkResult: Résultats du benchmark.
        """
        import time
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        correct = 0
        total = len(self.test_dataset)
        predictions = []
        ground_truth = []
        
        start_time = time.time()
        
        for sample in self.test_dataset:
            result = model.extract(sample["text"])
            predictions.append({
                "departure": result.departure,
                "destination": result.destination
            })
            ground_truth.append({
                "departure": sample["departure"],
                "destination": sample["destination"]
            })
            
            if (result.departure == sample["departure"] and 
                result.destination == sample["destination"]):
                correct += 1
        
        inference_time = time.time() - start_time
        end_memory = process.memory_info().rss / 1024 / 1024
        memory_usage = end_memory - start_memory
        
        # Calcul des métriques
        accuracy = correct / total
        precision, recall, f1 = self.metrics.calculate(
            predictions, 
            ground_truth
        )
        
        return BenchmarkResult(
            model_name=model.model_name,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            inference_time=inference_time,
            memory_usage=memory_usage,
            total_samples=total,
            correct_predictions=correct
        )
    
    def compare_models(
        self, 
        models: List[NLPModelInterface]
    ) -> Dict[str, BenchmarkResult]:
        """Compare plusieurs modèles.
        
        Args:
            models (List[NLPModelInterface]): Liste des modèles à comparer.
        
        Returns:
            Dict[str, BenchmarkResult]: Résultats par modèle.
        """
        results = {}
        for model in models:
            print(f"Benchmarking {model.model_name}...")
            results[model.model_name] = self.benchmark_model(model)
        return results
    
    def generate_report(
        self, 
        results: Dict[str, BenchmarkResult]
    ) -> str:
        """Génère un rapport de comparaison.
        
        Args:
            results (Dict[str, BenchmarkResult]): Résultats des benchmarks.
        
        Returns:
            str: Rapport formaté en markdown.
        """
        report = "# Rapport de Comparaison des Modèles NLP\n\n"
        report += "| Modèle | Accuracy | Precision | Recall | F1 | Temps (s) | Mémoire (MB) |\n"
        report += "|--------|----------|-----------|--------|----|-----------|--------------|\n"
        
        for model_name, result in results.items():
            report += (
                f"| {model_name} | "
                f"{result.accuracy:.3f} | "
                f"{result.precision:.3f} | "
                f"{result.recall:.3f} | "
                f"{result.f1_score:.3f} | "
                f"{result.inference_time:.2f} | "
                f"{result.memory_usage:.2f} |\n"
            )
        
        return report
```

### Métriques d'évaluation

```python
# evaluation/metrics.py
from typing import List, Dict
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

class Metrics:
    """Classe pour calculer les métriques d'évaluation."""
    
    def calculate(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> tuple[float, float, float]:
        """Calcule precision, recall et F1-score.
        
        Args:
            predictions (List[Dict]): Prédictions du modèle.
            ground_truth (List[Dict]): Vérité terrain.
        
        Returns:
            tuple[float, float, float]: (precision, recall, f1_score)
        """
        # Convertir en format binaire pour sklearn
        y_true = self._to_binary(ground_truth)
        y_pred = self._to_binary(predictions)
        
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')
        
        return precision, recall, f1
    
    def _to_binary(
        self, 
        data: List[Dict]
    ) -> np.ndarray:
        """Convertit les données en format binaire."""
        # Implémentation selon votre format de données
        pass
    
    def calculate_city_extraction_accuracy(
        self,
        predictions: List[Dict],
        ground_truth: List[Dict]
    ) -> Dict[str, float]:
        """Calcule l'accuracy pour l'extraction de villes.
        
        Returns:
            Dict avec 'departure_accuracy' et 'destination_accuracy'
        """
        departure_correct = sum(
            1 for p, gt in zip(predictions, ground_truth)
            if p["departure"] == gt["departure"]
        )
        destination_correct = sum(
            1 for p, gt in zip(predictions, ground_truth)
            if p["destination"] == gt["destination"]
        )
        
        total = len(predictions)
        
        return {
            "departure_accuracy": departure_correct / total,
            "destination_accuracy": destination_correct / total,
            "both_correct": sum(
                1 for p, gt in zip(predictions, ground_truth)
                if p["departure"] == gt["departure"] and 
                   p["destination"] == gt["destination"]
            ) / total
        }
```

### Script de comparaison

```python
# scripts/compare_models.py
"""Script pour comparer tous les modèles NLP."""

from nlp.factory import NLPModelFactory
from evaluation.benchmark import ModelBenchmark
import json

def load_test_dataset(path: str) -> List[Dict]:
    """Charge le dataset de test."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Charger le dataset de test
    test_data = load_test_dataset("data/datasets/test.json")
    
    # Créer tous les modèles à comparer
    models = [
        NLPModelFactory.create("simple", city_list=load_cities()),
        NLPModelFactory.create("camembert", model_path="models/camembert"),
        NLPModelFactory.create("transformer", model_path="models/transformer"),
    ]
    
    # Créer le benchmark
    benchmark = ModelBenchmark(test_data)
    
    # Comparer tous les modèles
    results = benchmark.compare_models(models)
    
    # Générer le rapport
    report = benchmark.generate_report(results)
    
    # Sauvegarder
    with open("results/comparisons/comparison_report.md", "w") as f:
        f.write(report)
    
    print("Rapport généré dans results/comparisons/comparison_report.md")

if __name__ == "__main__":
    main()
```

### Bonnes pratiques pour le benchmarking

1. **Dataset de test fixe** : Utiliser le même dataset pour tous les modèles
2. **Environnement reproductible** : Fixer les seeds aléatoires
3. **Métriques multiples** : Accuracy, F1, temps d'inférence, mémoire
4. **Tests statistiques** : Utiliser des tests de significativité si nécessaire
5. **Documentation** : Documenter les hyperparamètres de chaque modèle
6. **Versioning** : Versionner les modèles et leurs résultats

### Structure des résultats

```
results/
├── benchmarks/
│   ├── simple_model_20250101.json
│   ├── camembert_model_20250101.json
│   └── transformer_model_20250101.json
└── comparisons/
    ├── comparison_20250101.md
    └── comparison_20250101.json
```

---

## Découpage et Organisation du Code

### Règle d'or : Une fonction = Une responsabilité

#### ❌ Mauvais exemple

```python
def traiter_commande(texte: str) -> dict:
    """Fait tout en une seule fonction."""
    # Tokenisation
    tokens = texte.split()
    
    # Extraction des villes
    villes = []
    for token in tokens:
        if token.capitalize() in LISTE_VILLES:
            villes.append(token)
    
    # Validation
    if len(villes) < 2:
        return {"error": "Pas assez de villes"}
    
    # Recherche de chemin
    graphe = charger_graphe()
    chemin = dijkstra(graphe, villes[0], villes[1])
    
    # Formatage
    resultat = ",".join(chemin)
    
    return {"chemin": resultat}
```

#### ✅ Bon exemple

```python
def traiter_commande(texte: str) -> dict:
    """Orchestre le traitement d'une commande."""
    try:
        # Extraction
        extraction = extraire_villes(texte)
        if not extraction.is_valid():
            return {"error": extraction.error_message}
        
        # Recherche de chemin
        chemin = trouver_itineraire(
            extraction.departure,
            extraction.destination
        )
        
        # Formatage
        return formater_resultat(chemin)
    except Exception as e:
        return {"error": str(e)}


def extraire_villes(texte: str) -> ExtractionResult:
    """Extrait les villes de départ et d'arrivée."""
    tokens = tokeniser(texte)
    villes = identifier_villes(tokens)
    return valider_extraction(villes)


def tokeniser(texte: str) -> List[str]:
    """Tokenise le texte en mots."""
    return texte.lower().split()


def identifier_villes(tokens: List[str]) -> List[str]:
    """Identifie les villes dans une liste de tokens."""
    villes = []
    for token in tokens:
        ville = chercher_ville(token)
        if ville:
            villes.append(ville)
    return villes


def trouver_itineraire(depart: str, arrivee: str) -> List[str]:
    """Trouve l'itinéraire optimal entre deux villes."""
    graphe = charger_graphe()
    return dijkstra(graphe, depart, arrivee)
```

### Principes de découpage

#### 1. Fonctions courtes (max 20-30 lignes)

```python
# ❌ Trop long
def process_all(data):
    # 100 lignes de code...
    pass

# ✅ Découpé
def process_all(data):
    """Traite toutes les données."""
    validated = validate_data(data)
    processed = [process_item(item) for item in validated]
    return format_results(processed)

def validate_data(data):
    """Valide les données d'entrée."""
    # 10-15 lignes max
    pass

def process_item(item):
    """Traite un élément individuel."""
    # 10-15 lignes max
    pass
```

#### 2. Éviter les niveaux d'imbrication profonds

```python
# ❌ Trop d'imbrication
def process(data):
    if data:
        for item in data:
            if item.is_valid():
                for subitem in item.subitems:
                    if subitem.value > 0:
                        result.append(subitem.value)

# ✅ Découpé avec early returns
def process(data):
    """Traite les données."""
    if not data:
        return []
    
    results = []
    for item in data:
        if item.is_valid():
            results.extend(process_valid_item(item))
    return results

def process_valid_item(item):
    """Traite un élément valide."""
    return [subitem.value 
            for subitem in item.subitems 
            if subitem.value > 0]
```

#### 3. Extraire les constantes et configurations

```python
# ❌ Magic numbers et strings
def calculate_price(quantity):
    return quantity * 9.99 * 1.20

# ✅ Constantes explicites
TAXE_TVA = 1.20
PRIX_UNITAIRE = 9.99

def calculate_price(quantity: int) -> float:
    """Calcule le prix total avec TVA."""
    return quantity * PRIX_UNITAIRE * TAXE_TVA
```

#### 4. Séparer la logique métier de l'I/O

```python
# ❌ Mélange I/O et logique
def process_file(filename):
    with open(filename) as f:
        data = f.read()
        # 50 lignes de traitement...
        with open("output.txt", "w") as out:
            out.write(result)

# ✅ Séparation
def process_file(filename: str) -> None:
    """Traite un fichier."""
    data = lire_fichier(filename)
    resultat = traiter_donnees(data)
    ecrire_resultat(resultat, "output.txt")

def lire_fichier(filename: str) -> str:
    """Lit le contenu d'un fichier."""
    with open(filename, encoding="utf-8") as f:
        return f.read()

def traiter_donnees(data: str) -> str:
    """Traite les données (logique métier pure)."""
    # Logique métier sans I/O
    pass

def ecrire_resultat(resultat: str, filename: str) -> None:
    """Écrit le résultat dans un fichier."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resultat)
```

#### 5. Utiliser des classes pour regrouper des fonctionnalités liées

```python
# ❌ Fonctions dispersées
def parse_sentence(text):
    pass

def extract_cities(text):
    pass

def validate_order(text):
    pass

# ✅ Classe cohérente
class OrderParser:
    """Parse et valide les commandes de voyage."""
    
    def __init__(self, nlp_model):
        self.nlp_model = nlp_model
    
    def parse(self, text: str) -> ParsedOrder:
        """Parse une commande."""
        tokens = self._tokenize(text)
        cities = self._extract_cities(tokens)
        return ParsedOrder(cities)
    
    def validate(self, order: ParsedOrder) -> bool:
        """Valide une commande parsée."""
        return order.has_departure() and order.has_destination()
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenise le texte."""
        pass
    
    def _extract_cities(self, tokens: List[str]) -> List[str]:
        """Extrait les villes."""
        pass
```

### Checklist de découpage

Avant de commiter, vérifiez :

- [ ] Chaque fonction fait une seule chose
- [ ] Les fonctions font moins de 30 lignes
- [ ] Pas plus de 3 niveaux d'imbrication
- [ ] Les noms de fonctions sont explicites
- [ ] La logique métier est séparée de l'I/O
- [ ] Les constantes sont extraites
- [ ] Les fonctions réutilisables sont dans `utils/`
- [ ] Les fonctions liées sont regroupées en classes ou modules

### Exemple complet : Module NLP

```python
# nlp/parser.py
"""Module de parsing des commandes de voyage."""

from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ParsedOrder:
    """Représente une commande parsée."""
    departure: Optional[str]
    destination: Optional[str]
    is_valid: bool
    error_message: Optional[str] = None


class OrderParser:
    """Parse les commandes de voyage en français."""
    
    def __init__(self, city_extractor, validator):
        """Initialise le parser.
        
        Args:
            city_extractor: Extractor de villes.
            validator: Validateur de commandes.
        """
        self.city_extractor = city_extractor
        self.validator = validator
    
    def parse(self, text: str) -> ParsedOrder:
        """Parse une commande de voyage.
        
        Args:
            text (str): Texte de la commande.
        
        Returns:
            ParsedOrder: Commande parsée avec départ et destination.
        """
        normalized = self._normalize_text(text)
        cities = self.city_extractor.extract(normalized)
        
        validation = self.validator.validate(cities)
        if not validation.is_valid:
            return ParsedOrder(
                departure=None,
                destination=None,
                is_valid=False,
                error_message=validation.error
            )
        
        return ParsedOrder(
            departure=validation.departure,
            destination=validation.destination,
            is_valid=True
        )
    
    def _normalize_text(self, text: str) -> str:
        """Normalise le texte d'entrée.
        
        Args:
            text (str): Texte brut.
        
        Returns:
            str: Texte normalisé.
        """
        return text.lower().strip()
```

---

## Résumé des bonnes pratiques

### Commits
- Format Conventional Commits
- Messages clairs et descriptifs
- Un commit = une modification logique

### Documentation
- Docstrings Google Style pour toutes les fonctions publiques
- Type hints obligatoires
- Exemples d'utilisation quand pertinent

### Architecture
- Séparation des responsabilités
- Modules indépendants et testables
- Configuration centralisée
- Interface commune pour tous les modèles NLP
- Architecture extensible pour ajouter de nouveaux modèles

### Découpage
- Fonctions courtes et focalisées
- Une fonction = une responsabilité
- Logique métier séparée de l'I/O
- Réutilisabilité maximale

### Multi-Modèles NLP
- Interface commune (`NLPModelInterface`) pour tous les modèles
- Factory Pattern pour créer des modèles facilement
- Benchmarking automatisé pour comparer les performances
- Architecture extensible pour ajouter de nouveaux modèles

---

*Documentation générée pour le projet THOR - Travel Order Resolver*

