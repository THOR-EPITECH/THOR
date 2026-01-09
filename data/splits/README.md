# Datasets splits

Ce dossier contient les datasets divisés en train/test/valid pour le module STT.

## Structure

```
splits/
  train/          # Données d'entraînement
  test/           # Données de test
  valid/          # Données de validation
```

## Format

Chaque dossier peut contenir un ou plusieurs fichiers JSONL.

Format d'une ligne pour STT :
```json
{
  "id": "sample_001",
  "audio_path": "data/raw/audio/sample_001.wav",
  "transcript": "Je veux aller à Paris depuis Lyon"
}
```

Champs :
- `id` : Identifiant unique de l'échantillon
- `audio_path` : Chemin relatif vers le fichier audio
- `transcript` : Transcription de référence (ground truth)

## Utilisation

Les splits sont utilisés pour :
- **train/** : Entraînement des modèles
- **valid/** : Validation pendant l'entraînement (hyperparamètres, early stopping)
- **test/** : Évaluation finale (métriques de performance)

## Exemple d'utilisation

```bash
# Évaluer sur le split de test
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --output-dir results/stt/whisper_test
```

## Préparer des splits

Utilisez le script `scripts/prepare_splits.py` pour diviser un dataset complet :

```bash
python scripts/prepare_splits.py \
    --input data/raw/sentences/all.jsonl \
    --output data/splits \
    --train-ratio 0.7 \
    --valid-ratio 0.15 \
    --test-ratio 0.15
```
