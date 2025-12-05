# Tests du Module Speech-to-Text

## Utilisation

### Test basique (vérification du module)

```bash
python tests/speech_to_text/test_speech_to_text.py --basic
```

### Test avec le microphone

```bash
# Test simple (5 secondes, français, modèle base)
python tests/speech_to_text/test_speech_to_text.py --mic

# Test avec options personnalisées
python tests/speech_to_text/test_speech_to_text.py --mic --duration 10 --language fr --model small

# Test en boucle (continue jusqu'à Ctrl+C)
python tests/speech_to_text/test_speech_to_text.py --mic-loop
```

### Test avec un fichier audio

```bash
python tests/speech_to_text/test_speech_to_text.py --file chemin/vers/audio.wav
```

### Liste des modèles disponibles

```bash
python tests/speech_to_text/test_speech_to_text.py --list
```

### Test de création des modèles

```bash
python tests/speech_to_text/test_speech_to_text.py --models
```

## Options disponibles

- `--basic` : Test basique (vérification du module)
- `--models` : Test de création des modèles
- `--list` : Liste les modèles disponibles
- `--mic` : Test avec le microphone
- `--mic-loop` : Test microphone en boucle
- `--file <chemin>` : Test avec un fichier audio
- `--duration <sec>` : Durée d'enregistrement (défaut: 5.0)
- `--language <lang>` : Langue (fr/en, défaut: fr)
- `--model <size>` : Taille du modèle (tiny/base/small, défaut: base)

## Exemples complets

```bash
# Test rapide
python tests/speech_to_text/test_speech_to_text.py --basic

# Test microphone avec modèle small et durée de 10 secondes
python tests/speech_to_text/test_speech_to_text.py --mic --model small --duration 10

# Test avec fichier audio
python tests/speech_to_text/test_speech_to_text.py --file data/audio/commande.wav

# Test en boucle avec modèle tiny (rapide)
python tests/speech_to_text/test_speech_to_text.py --mic-loop --model tiny --duration 3
```

## Structure

```
tests/
├── speech_to_text/
│   └── test_speech_to_text.py    # Tests du module speech-to-text
├── benchmark/                     # Architecture de benchmark
│   ├── base/                      # Interfaces communes
│   ├── metrics/                   # Métriques de performance
│   ├── runners/                   # Runners de benchmark
│   └── reporters/                 # Générateurs de rapports
└── results/                       # Résultats des tests et benchmarks
```

- `tests/speech_to_text/test_speech_to_text.py` : Fichier de test principal unifié
- Tous les tests sont regroupés dans un seul fichier pour faciliter la maintenance
- Les tests sont organisés par module pour suivre la structure du code source

