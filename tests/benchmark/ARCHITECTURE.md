# Architecture du Système de Benchmark

## Vue d'ensemble

Le système de benchmark suit une architecture modulaire et extensible, conforme aux principes définis dans la documentation du projet.

## Structure

```
tests/benchmark/
├── __init__.py                    # Exports principaux
├── base/
│   ├── __init__.py
│   └── benchmark_interface.py    # Interface commune (BenchmarkInterface)
├── metrics/
│   ├── __init__.py
│   └── performance_metrics.py    # Mesure des performances (PerformanceMetrics)
├── runners/
│   ├── __init__.py
│   └── whisper_runner.py         # Runner pour Whisper (WhisperBenchmarkRunner)
└── reporters/
    ├── __init__.py
    ├── reporter_interface.py      # Interface pour reporters (ReporterInterface)
    ├── markdown_reporter.py      # Reporter Markdown (MarkdownReporter)
    └── json_reporter.py          # Reporter JSON (JSONReporter)
```

## Composants

### 1. Base (Interfaces)

**`BenchmarkInterface`** : Interface commune pour tous les runners de benchmark.

- `run_benchmark(model_type, **kwargs)` : Exécute un benchmark pour un modèle
- `run_benchmarks(model_types, **kwargs)` : Exécute des benchmarks pour plusieurs modèles

**`BenchmarkResult`** : Dataclass représentant le résultat d'un benchmark.

### 2. Metrics (Métriques)

**`PerformanceMetrics`** : Classe pour mesurer les performances système.

- `measure()` : Context manager pour mesurer temps, mémoire, CPU
- `get_current_memory()` : Mémoire actuelle en MB
- `get_current_cpu()` : CPU actuel en pourcentage

### 3. Runners (Exécuteurs)

**`WhisperBenchmarkRunner`** : Runner spécifique pour les modèles Whisper.

- Implémente `BenchmarkInterface`
- Gère l'exécution des benchmarks Whisper
- Utilise `PerformanceMetrics` pour mesurer les performances

### 4. Reporters (Générateurs de rapports)

**`ReporterInterface`** : Interface commune pour tous les reporters.

- `generate_report(results, **kwargs)` : Génère un rapport
- `save_report(results, output_path, **kwargs)` : Sauvegarde un rapport

**`MarkdownReporter`** : Génère des rapports au format Markdown.

**`JSONReporter`** : Génère des rapports au format JSON.

## Flux d'exécution

```
1. Création du Runner
   ↓
2. Exécution des benchmarks (via Runner)
   ↓
3. Mesure des performances (via PerformanceMetrics)
   ↓
4. Collecte des résultats (BenchmarkResult)
   ↓
5. Génération des rapports (via Reporters)
   ↓
6. Sauvegarde des rapports (Markdown + JSON)
```

## Avantages de cette architecture

✅ **Séparation des responsabilités** : Chaque composant a un rôle unique  
✅ **Extensibilité** : Facile d'ajouter de nouveaux runners/reporters  
✅ **Testabilité** : Chaque composant peut être testé indépendamment  
✅ **Réutilisabilité** : Les composants peuvent être réutilisés ailleurs  
✅ **Maintenabilité** : Code organisé et facile à maintenir  
✅ **Interface commune** : Permet la comparaison équitable entre différents types de benchmarks

## Exemple d'utilisation

```python
from tests.benchmark import (
    WhisperBenchmarkRunner,
    MarkdownReporter,
    JSONReporter
)

runner = WhisperBenchmarkRunner(test_audio_path="audio.wav")
results = runner.run_benchmarks(
    model_types=["whisper-tiny", "whisper-base"],
    language="fr"
)

md_reporter = MarkdownReporter()
json_reporter = JSONReporter()

md_path = md_reporter.save_report(results, "report.md")
json_path = json_reporter.save_report(results, "report.json")
```

## Extension future

Pour ajouter un nouveau type de benchmark (ex: Wav2Vec2) :

1. Créer `runners/wav2vec2_runner.py`
2. Implémenter `BenchmarkInterface`
3. Ajouter dans `runners/__init__.py`

Pour ajouter un nouveau format de rapport (ex: CSV) :

1. Créer `reporters/csv_reporter.py`
2. Implémenter `ReporterInterface`
3. Ajouter dans `reporters/__init__.py`

