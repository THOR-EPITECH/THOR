# Benchmark des Modèles Whisper

## Architecture

Le système de benchmark suit une architecture modulaire :

- **base/** : Interfaces communes pour tous les benchmarks
- **metrics/** : Mesure des performances système
- **runners/** : Exécution des benchmarks pour différents modèles
- **reporters/** : Génération de rapports (Markdown, JSON)

Voir `tests/benchmark/README.md` pour plus de détails sur l'architecture.

## Utilisation

### Benchmark avec microphone

```bash
python tests/benchmark_whisper.py --duration 5
```

### Benchmark avec fichier audio

```bash
python tests/benchmark_whisper.py --file data/audio/test.wav
```

### Benchmark de modèles spécifiques

```bash
python tests/benchmark_whisper.py --models whisper-tiny whisper-base whisper-small
```

### Options complètes

```bash
python tests/benchmark_whisper.py \
    --file audio.wav \
    --language fr \
    --models whisper-base whisper-small \
    --output results/my_benchmark
```

## Options disponibles

- `--file <chemin>` : Chemin vers un fichier audio de test
- `--duration <sec>` : Durée d'enregistrement si microphone (défaut: 5.0)
- `--language <lang>` : Langue pour la transcription (défaut: fr)
- `--models <liste>` : Modèles à tester (ex: whisper-tiny whisper-base)
- `--output <dir>` : Répertoire de sortie pour les rapports (défaut: results/benchmarks)

## Métriques mesurées

Le benchmark mesure :

- **Temps de transcription** : Temps nécessaire pour transcrire l'audio
- **Utilisation mémoire** : Mémoire RAM utilisée (en MB)
- **Utilisation CPU** : Pourcentage d'utilisation du CPU
- **Confiance** : Score de confiance de la transcription (0.0 à 1.0)
- **Longueur du texte** : Nombre de caractères transcrits

## Rapports générés

Le benchmark génère deux fichiers :

1. **Rapport Markdown** (`benchmark_whisper_YYYYMMDD_HHMMSS.md`) :
   - Tableau comparatif des résultats
   - Comparaison des performances
   - Détails pour chaque modèle

2. **Rapport JSON** (`benchmark_whisper_YYYYMMDD_HHMMSS.json`) :
   - Données structurées pour analyse
   - Peut être utilisé pour générer des graphiques

## Exemples de résultats

Le rapport inclut :

- Tableau comparatif de tous les modèles
- Identification du modèle le plus rapide
- Identification du modèle le plus efficace en mémoire
- Identification du modèle avec la meilleure confiance
- Détails complets pour chaque modèle

## Structure des résultats

Les résultats sont sauvegardés dans `results/benchmarks/` :

```
results/
└── benchmarks/
    ├── benchmark_whisper_20250101_120000.md
    └── benchmark_whisper_20250101_120000.json
```

