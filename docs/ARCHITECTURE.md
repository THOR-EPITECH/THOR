# Architecture du Projet THOR (Travel Order Resolver)

## Vue d'ensemble

Le projet se concentre actuellement sur le module **Speech-to-Text (STT)** : Conversion audio → texte.

Le module STT peut être testé avec différents modèles (Whisper, Vosk, etc.).

## Structure du projet

```
thor/
  README.md
  pyproject.toml
  .env.example
  .gitignore
  .pre-commit-config.yaml

  docs/
    index.md
    architecture.md              # Ce fichier (détaillé)
    datasets.md
    metrics.md
    experiments.md
    modules/
      stt/
        index.md
        models/
          whisper-small.md
          vosk-fr.md

  data/
    raw/
      audio/                     # .wav/.mp3 pour STT
    processed/
      audio_wav16k/              # Audio normalisé (mono, 16kHz)
    splits/
      train/                     # Données d'entraînement (JSONL avec audio_path + transcript)
      test/                      # Données de test (JSONL avec audio_path + transcript)
      valid/                     # Données de validation (JSONL avec audio_path + transcript)

  src/
    common/
      types.py                   # Dataclasses partagées
      io.py                      # Lecture/écriture fichiers
      audio.py                   # Utilitaires audio
      text_norm.py               # Normalisation texte
      registry.py                # Registre des modèles (plugin)
      config.py                  # Configuration YAML + CLI
      logging.py                 # Logging unifié

    stt/
      README.md
      interfaces.py              # STTModel: transcribe() -> STTResult
      models/
        __init__.py
        whisper.py
        vosk.py
        dummy.py                 # Baseline pour tests
      eval/
        metrics.py               # WER, CER, latency, RTF
        evaluate.py              # Évaluation sur split
        error_analysis.py         # Analyse d'erreurs

    cli/
      stt.py                     # CLI pour STT

  configs/
    base.yaml
    stt/
      whisper_small.yaml
      whisper_medium.yaml
      vosk_fr.yaml

  experiments/
    runner.py                    # Lance évaluation standardisée
    sweep.py                     # Compare modèles/configs
    reports/
      build_report.py            # Génère rapports markdown/PDF
      templates/
        report_template.md

  results/
    runs/
      <timestamp>_stt_<model>_<uuid>/
        config.yaml
        dataset_manifest.json
        metrics.json
        predictions.jsonl
        errors_top.csv
        report.md
        plots/
          metrics.png
          errors.png

  tests/
    test_text_norm.py
    test_metrics.py
    test_stt_contract.py

  scripts/
    prepare_data.py              # Préparation datasets
    download_models.py           # Téléchargement modèles
    prepare_splits.py            # Division en train/test/valid
```

## Principes de design

### 1. Interface commune
Le module STT expose une interface standard :
- `STTModel.transcribe(audio_path) -> STTResult`

### 2. Système de registre
Les modèles sont enregistrés via `registry.py` pour faciliter le chargement dynamique.

### 3. Configuration hiérarchique
- `configs/base.yaml` : Configuration de base
- `configs/stt/<model>.yaml` : Configurations spécifiques
- Override via variables d'environnement ou CLI

### 4. Métriques standardisées
Le module expose des métriques via `metrics.json` avec format standardisé (WER, CER, latency, RTF).

### 5. Documentation
Le dossier `src/stt/` contient un `README.md` expliquant :
- Architecture du module
- Modèles disponibles
- Comment ajouter un nouveau modèle
- Exemples d'utilisation

## Workflow de test

### Test du module STT
```bash
# Transcrire un fichier audio
python -m src.cli.stt transcribe --audio audio.wav --model whisper

# Évaluer un modèle
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --output-dir results/stt/whisper_test
```

## Améliorations par rapport à l'architecture initiale

1. **Structure simplifiée** : Focus sur STT uniquement
2. **Splits globaux** : train/test/valid au niveau racine de splits/
3. **Métriques standardisées** : Format JSON commun
4. **Documentation complète** : README par module + docs détaillées
5. **Tests de contrat** : Vérification que les modèles respectent les interfaces
6. **Scripts utilitaires** : Préparation données, téléchargement modèles
