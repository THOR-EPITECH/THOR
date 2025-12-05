# Architecture des Benchmarks

## Structure

```
tests/benchmark/
├── __init__.py
├── base/
│   ├── __init__.py
│   └── benchmark_interface.py      # Interface commune
├── metrics/
│   ├── __init__.py
│   └── performance_metrics.py      # Mesure des performances
├── runners/
│   ├── __init__.py
│   └── whisper_runner.py           # Runner pour Whisper
└── reporters/
    ├── __init__.py
    ├── reporter_interface.py       # Interface pour reporters
    ├── markdown_reporter.py        # Reporter Markdown
    └── json_reporter.py            # Reporter JSON
```

## Principes d'architecture

### 1. Séparation des responsabilités

- **base/** : Interfaces communes pour tous les benchmarks
- **metrics/** : Mesure des performances système (mémoire, CPU, temps)
- **runners/** : Exécution des benchmarks pour différents types de modèles
- **reporters/** : Génération de rapports dans différents formats

### 2. Interface commune

Tous les runners implémentent `BenchmarkInterface` pour permettre :
- L'ajout facile de nouveaux types de benchmarks
- La comparaison équitable entre différents runners
- L'extensibilité sans modifier le code existant

### 3. Reporters extensibles

Tous les reporters implémentent `ReporterInterface` pour permettre :
- L'ajout de nouveaux formats de rapport (CSV, HTML, etc.)
- La génération de rapports personnalisés
- La réutilisation du code existant

## Utilisation

### Via le script principal

```bash
python scripts/benchmark_whisper.py --file audio.wav
python scripts/benchmark_whisper.py --duration 5
```

### Via l'API Python

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
md_path = md_reporter.save_report(results, "report.md")
```

## Extensibilité

### Ajouter un nouveau runner

1. Créer une classe qui hérite de `BenchmarkInterface`
2. Implémenter `run_benchmark()` et `run_benchmarks()`
3. Ajouter dans `runners/__init__.py`

### Ajouter un nouveau reporter

1. Créer une classe qui hérite de `ReporterInterface`
2. Implémenter `generate_report()` et `save_report()`
3. Ajouter dans `reporters/__init__.py`

## Avantages

✅ **Modularité** : Chaque composant a une responsabilité unique  
✅ **Extensibilité** : Facile d'ajouter de nouveaux runners/reporters  
✅ **Testabilité** : Chaque composant peut être testé indépendamment  
✅ **Réutilisabilité** : Les composants peuvent être réutilisés ailleurs  
✅ **Maintenabilité** : Code organisé et facile à maintenir

