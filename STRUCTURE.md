# Structure du Projet THOR

## Organisation des fichiers

```
THOR/
├── src/                          # Code source principal
│   └── speech_to_text/          # Module speech-to-text
│       ├── base/                # Interfaces et classes de base
│       ├── models/               # Implémentations des modèles
│       ├── factory.py            # Factory pour créer les modèles
│       └── README.md             # Documentation complète du module
│
├── tests/                        # Tests organisés par module
│   ├── speech_to_text/          # Tests du module speech-to-text
│   │   └── test_speech_to_text.py # Fichier de test principal (TOUT-EN-UN)
│   ├── benchmark/               # Architecture de benchmark
│   │   ├── base/                # Interfaces communes
│   │   ├── metrics/              # Métriques de performance
│   │   ├── runners/             # Runners de benchmark
│   │   └── reporters/           # Générateurs de rapports
│   └── README.md                # Documentation des tests
│
├── scripts/                      # Scripts utilitaires
│   ├── download_whisper_model.py # Téléchargement des modèles
│   └── benchmark_whisper.py     # Script d'exécution des benchmarks
│
├── examples/                      # Exemples d'utilisation
│   └── whisper_example.py        # Exemple basique
│
├── docs/                         # Documentation
│   ├── DOCUMENTATION.md          # Documentation complète
│   └── project.pdf              # PDF du projet
│
├── requirements.txt              # Dépendances Python
└── README_SPEECH_TO_TEXT.md     # Lien vers la doc (voir src/speech_to_text/README.md)
```

## Tests

**Tests organisés par module** : `tests/speech_to_text/test_speech_to_text.py`

Tous les tests sont regroupés dans ce fichier unique avec des options en ligne de commande :

```bash
# Test basique
python tests/speech_to_text/test_speech_to_text.py --basic

# Test microphone
python tests/speech_to_text/test_speech_to_text.py --mic

# Test avec fichier audio
python tests/speech_to_text/test_speech_to_text.py --file audio.wav

# Voir toutes les options
python tests/speech_to_text/test_speech_to_text.py
```

## Benchmarks

**Script de benchmark** : `scripts/benchmark_whisper.py`

```bash
# Benchmark avec microphone
python scripts/benchmark_whisper.py --duration 5

# Benchmark avec fichier audio
python scripts/benchmark_whisper.py --file audio.wav

# Benchmark de modèles spécifiques
python scripts/benchmark_whisper.py --models whisper-tiny whisper-base
```

## Avantages de cette structure

✅ **Un seul fichier de test** : Plus simple à maintenir  
✅ **Options en ligne de commande** : Flexible et puissant  
✅ **Structure claire** : Séparation code/tests/scripts/docs  
✅ **Documentation** : README dans chaque dossier important  

## Scripts utilitaires

Les scripts utilitaires sont dans `scripts/` :
- `scripts/download_whisper_model.py` : Téléchargement des modèles
- `scripts/benchmark_whisper.py` : Exécution des benchmarks Whisper

