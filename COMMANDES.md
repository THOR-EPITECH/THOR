# 📚 Documentation des Commandes THOR

Guide complet de toutes les commandes disponibles dans le projet THOR.

---

## 📋 Table des matières

1. [Commandes STT (Speech-to-Text)](#commandes-stt)
2. [Commandes NLP (Natural Language Processing)](#commandes-nlp)
3. [Commandes Pipeline](#commandes-pipeline)
4. [Scripts utilitaires](#scripts-utilitaires)
5. [Configuration](#configuration)

---

## 🎤 Commandes STT

### Transcrire un fichier audio

Transcrit un fichier audio en texte.

```bash
python -m src.cli.stt transcribe \
    --audio <chemin_vers_audio> \
    [--model <modèle>] \
    [--config <fichier_config>]
```

**Paramètres :**
- `--audio` (requis) : Chemin vers le fichier audio (.wav, .mp3)
- `--model` (optionnel) : Modèle STT à utiliser (`whisper`, `dummy`) - défaut: `whisper`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML

**Exemples :**
```bash
# Transcription simple avec Whisper
python -m src.cli.stt transcribe --audio data/raw/audio/sample_000001.wav

# Avec configuration personnalisée
python -m src.cli.stt transcribe \
    --audio data/raw/audio/sample_000001.wav \
    --model whisper \
    --config configs/stt/whisper_small.yaml
```

**Sortie :**
```
Text: Je voudrais bien aller à Paris.
Processing time: 2.34s
Confidence: 0.95
```

---

### Évaluer un modèle STT

Évalue un modèle STT sur un dataset de test.

```bash
python -m src.cli.stt evaluate \
    --dataset <chemin_dataset> \
    [--model <modèle>] \
    [--config <fichier_config>] \
    [--output-dir <dossier_sortie>] \
    [--analyze-errors] \
    [--top-errors <nombre>]
```

**Paramètres :**
- `--dataset` (requis) : Chemin vers le fichier JSONL du dataset de test
- `--model` (optionnel) : Modèle STT à évaluer (`whisper`, `dummy`) - défaut: `whisper`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML
- `--output-dir` (optionnel) : Dossier de sortie pour les résultats - défaut: `results/stt`
- `--analyze-errors` (optionnel) : Active l'analyse détaillée des erreurs
- `--top-errors` (optionnel) : Nombre d'erreurs principales à afficher - défaut: `20`

**Exemples :**
```bash
# Évaluation basique
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper

# Évaluation avec analyse d'erreurs
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --output-dir results/stt/whisper_test \
    --analyze-errors \
    --top-errors 30
```

**Fichiers générés :**
- `metrics.json` : Métriques agrégées (WER, CER, Latency, RTF)
- `predictions.jsonl` : Toutes les prédictions détaillées
- `predictions.csv` : Même chose en format CSV
- `report.md` : Rapport markdown complet
- `errors_top.csv` : Top erreurs (si `--analyze-errors` activé)

---

## 🧠 Commandes NLP

### Extraire origine/destination depuis un texte

Extrait la ville de départ et d'arrivée depuis un texte.

```bash
python -m src.cli.nlp extract \
    --text "<texte>" \
    [--model <modèle>] \
    [--config <fichier_config>]
```

**Paramètres :**
- `--text` (requis) : Texte à analyser
- `--model` (optionnel) : Modèle NLP à utiliser (`spacy`, `dummy`) - défaut: `dummy`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML

**Exemples :**
```bash
# Extraction simple
python -m src.cli.nlp extract \
    --text "Je veux aller à Paris depuis Lyon"

# Avec modèle fine-tuné
python -m src.cli.nlp extract \
    --text "Je souhaite voyager de Bordeaux à Toulouse" \
    --model spacy \
    --config configs/nlp/spacy_finetuned.yaml
```

**Sortie :**
```
Origine: Lyon
Destination: Paris
Valide: True
Confidence: 1.00
```

---

### Évaluer un modèle NLP

Évalue un modèle NLP sur un dataset de test.

```bash
python -m src.cli.nlp evaluate \
    --dataset <chemin_dataset> \
    [--model <modèle>] \
    [--config <fichier_config>] \
    [--output-dir <dossier_sortie>]
```

**Paramètres :**
- `--dataset` (requis) : Chemin vers le fichier JSONL du dataset de test
- `--model` (optionnel) : Modèle NLP à évaluer (`spacy`, `dummy`) - défaut: `dummy`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML
- `--output-dir` (optionnel) : Dossier de sortie pour les résultats - défaut: `results/nlp`

**Exemples :**
```bash
# Évaluation basique
python -m src.cli.nlp evaluate \
    --dataset data/splits/test/test_nlp.jsonl \
    --model spacy

# Évaluation avec modèle fine-tuné
python -m src.cli.nlp evaluate \
    --dataset data/splits/test/test_nlp.jsonl \
    --model spacy \
    --config configs/nlp/spacy_finetuned.yaml \
    --output-dir results/nlp/spacy_finetuned_test
```

**Fichiers générés :**
- `metrics.json` : Métriques agrégées (Precision, Recall, F1, Accuracy)
- `predictions.jsonl` : Toutes les prédictions détaillées
- `predictions.csv` : Même chose en format CSV
- `report.md` : Rapport markdown complet

**Métriques calculées :**
- **Precision, Recall, F1** : Pour l'extraction d'entités
- **Origin Accuracy** : Précision sur l'origine
- **Destination Accuracy** : Précision sur la destination
- **Validation Accuracy** : Précision sur la détection de demandes valides

---

### Entraîner (fine-tuner) un modèle NLP

Entraîne un modèle NLP sur un dataset d'entraînement.

```bash
python -m src.cli.nlp train \
    --train-dataset <chemin_train> \
    [--valid-dataset <chemin_valid>] \
    [--model <modèle>] \
    [--config <fichier_config>] \
    [--output-dir <dossier_sortie>] \
    [--n-iter <nombre_iterations>] \
    [--dropout <taux_dropout>]
```

**Paramètres :**
- `--train-dataset` (requis) : Chemin vers le dataset d'entraînement (JSONL)
- `--valid-dataset` (optionnel) : Chemin vers le dataset de validation (JSONL)
- `--model` (optionnel) : Modèle NLP à entraîner (`spacy`) - défaut: `spacy`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML
- `--output-dir` (optionnel) : Dossier où sauvegarder le modèle entraîné - défaut: `models/nlp`
- `--n-iter` (optionnel) : Nombre d'itérations d'entraînement - défaut: `20`
- `--dropout` (optionnel) : Taux de dropout - défaut: `0.1`

**Exemples :**
```bash
# Entraînement basique
python -m src.cli.nlp train \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --model spacy

# Entraînement complet avec validation
python -m src.cli.nlp train \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --model spacy \
    --n-iter 30 \
    --dropout 0.2 \
    --output-dir models/nlp/spacy_finetuned
```

**Sortie :**
```
✅ Training complete!
Model saved to: models/nlp/spacy_finetuned/model

To use this fine-tuned model, update your config:
  custom_model_path: models/nlp/spacy_finetuned/model
```

**Utilisation du modèle fine-tuné :**
Créez un fichier `configs/nlp/spacy_finetuned.yaml` :
```yaml
nlp:
  model_name: fr_core_news_md
  custom_model_path: models/nlp/spacy_finetuned/model
```

---

## 🔄 Commandes Pipeline

### Traiter un fichier audio complet (STT → NLP)

Traite un fichier audio complet : transcription puis extraction origine/destination.

```bash
python -m src.cli.pipeline \
    --audio <chemin_audio> \
    [--stt-model <modèle_stt>] \
    [--nlp-model <modèle_nlp>] \
    [--config <fichier_config>] \
    [--output <chemin_sortie>]
```

**Paramètres :**
- `--audio` (requis) : Chemin vers le fichier audio
- `--stt-model` (optionnel) : Modèle STT à utiliser (`whisper`, `vosk`) - défaut: `whisper`
- `--nlp-model` (optionnel) : Modèle NLP à utiliser (`spacy`) - défaut: `spacy`
- `--config` (optionnel) : Chemin vers un fichier de configuration YAML
- `--output` (optionnel) : Chemin pour sauvegarder les résultats JSON (sinon généré automatiquement)

**Exemples :**
```bash
# Pipeline basique
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav

# Pipeline avec modèles spécifiques
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --config configs/nlp/spacy_finetuned.yaml

# Pipeline avec sortie personnalisée
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --output results/pipeline/mon_resultat.json
```

**Sortie :**
```
=== Résultats ===
Transcription: Je veux voyager de Toulouse à Bordeaux.
Origine: Toulouse
Destination: Bordeaux
Valide: True
Confidence: 1.00

Résultats JSON sauvegardés dans: results/pipeline/sample_000160_result.json
Rapport markdown généré: results/pipeline/sample_000160_result.md
```

**Messages d'erreur possibles :**
- `⚠️ Attention : La ville de départ est manquante. Veuillez préciser d'où vous partez.`
- `⚠️ Attention : La ville d'arrivée est manquante. Veuillez préciser votre destination.`
- `❌ Erreur : Aucune ville détectée. Veuillez préciser une ville de départ et/ou d'arrivée.`

**Fichiers générés :**
- `{audio_name}_result.json` : Résultats au format JSON
- `{audio_name}_result.md` : Rapport markdown détaillé

---

## 🛠️ Scripts utilitaires

### Générer un dataset STT

Génère un dataset STT avec diverses phrases et variations.

```bash
PYTHONPATH=. python3 scripts/generate_stt_dataset.py \
    [--output-dir <dossier_sortie>] \
    [--num-samples <nombre>] \
    [--audio-dir <dossier_audio>] \
    [--seed <graine>]
```

**Paramètres :**
- `--output-dir` (optionnel) : Dossier de sortie - défaut: `data/splits`
- `--num-samples` (optionnel) : Nombre d'échantillons à générer - défaut: `1000`
- `--audio-dir` (optionnel) : Dossier pour les fichiers audio - défaut: `data/raw/audio`
- `--seed` (optionnel) : Graine aléatoire pour reproductibilité - défaut: `42`

**Exemple :**
```bash
PYTHONPATH=. python3 scripts/generate_stt_dataset.py \
    --num-samples 500 \
    --output-dir data/splits
```

---

### Générer un dataset NLP

Génère un dataset NLP massif avec nombreuses variations de phrases.

```bash
PYTHONPATH=. python3 scripts/generate_nlp_dataset.py \
    [--output-dir <dossier_sortie>] \
    [--num-samples <nombre>] \
    [--seed <graine>]
```

**Paramètres :**
- `--output-dir` (optionnel) : Dossier de sortie - défaut: `data/splits`
- `--num-samples` (optionnel) : Nombre d'échantillons à générer - défaut: `10000`
- `--seed` (optionnel) : Graine aléatoire pour reproductibilité - défaut: `42`

**Exemple :**
```bash
PYTHONPATH=. python3 scripts/generate_nlp_dataset.py \
    --num-samples 5000 \
    --output-dir data/splits
```

**Fichiers générés :**
- `train/train_nlp.jsonl` : Dataset d'entraînement
- `valid/valid_nlp.jsonl` : Dataset de validation
- `test/test_nlp.jsonl` : Dataset de test
- `full_nlp_dataset.jsonl` : Dataset complet

---

### Générer des fichiers audio

Génère des fichiers audio à partir d'un dataset JSONL en utilisant TTS.

```bash
PYTHONPATH=. python3 scripts/generate_audio.py \
    --dataset <chemin_dataset> \
    [--audio-dir <dossier_audio>] \
    [--tts-engine <moteur>] \
    [--no-skip-existing]
```

**Paramètres :**
- `--dataset` (requis) : Chemin vers le fichier JSONL du dataset
- `--audio-dir` (optionnel) : Dossier de sortie pour les fichiers audio - défaut: `data/raw/audio`
- `--tts-engine` (optionnel) : Moteur TTS à utiliser (`gtts`, `pyttsx3`) - défaut: `gtts`
- `--no-skip-existing` (optionnel) : Ne pas ignorer les fichiers existants

**Exemple :**
```bash
PYTHONPATH=. python3 scripts/generate_audio.py \
    --dataset data/splits/full_dataset.jsonl \
    --audio-dir data/raw/audio \
    --tts-engine gtts
```

---

### Préparer des splits train/test/valid

Divise un dataset complet en splits train/test/valid.

```bash
PYTHONPATH=. python3 scripts/prepare_splits.py \
    --input <fichier_entrée> \
    --output <dossier_sortie> \
    [--train-ratio <ratio>] \
    [--valid-ratio <ratio>] \
    [--test-ratio <ratio>] \
    [--no-shuffle] \
    [--seed <graine>]
```

**Paramètres :**
- `--input` (requis) : Fichier JSONL d'entrée
- `--output` (requis) : Dossier de sortie
- `--train-ratio` (optionnel) : Ratio pour train - défaut: `0.7`
- `--valid-ratio` (optionnel) : Ratio pour validation - défaut: `0.15`
- `--test-ratio` (optionnel) : Ratio pour test - défaut: `0.15`
- `--no-shuffle` (optionnel) : Ne pas mélanger les données
- `--seed` (optionnel) : Graine aléatoire - défaut: `42`

**Exemple :**
```bash
PYTHONPATH=. python3 scripts/prepare_splits.py \
    --input data/splits/full_dataset.jsonl \
    --output data/splits \
    --train-ratio 0.7 \
    --valid-ratio 0.15 \
    --test-ratio 0.15
```

---

### Tester le pipeline sur plusieurs exemples

Teste le pipeline sur plusieurs fichiers audio ou textes.

```bash
PYTHONPATH=. python3 scripts/test_pipeline_examples.py \
    [--audio-dir <dossier_audio>] \
    [--audio-files <fichier1> <fichier2> ...] \
    [--texts <texte1> <texte2> ...] \
    [--dataset <chemin_dataset>] \
    [--config <fichier_config>] \
    [--output <fichier_sortie>] \
    [--num-samples <nombre>]
```

**Paramètres :**
- `--audio-dir` (optionnel) : Dossier contenant des fichiers audio à tester
- `--audio-files` (optionnel) : Liste de fichiers audio à tester
- `--texts` (optionnel) : Liste de textes à tester
- `--dataset` (optionnel) : Fichier JSONL avec phrases à tester
- `--config` (optionnel) : Fichier de configuration
- `--output` (optionnel) : Fichier JSON de sortie pour les résultats
- `--num-samples` (optionnel) : Nombre d'échantillons depuis le dataset - défaut: `10`

**Exemples :**
```bash
# Tester sur plusieurs textes
PYTHONPATH=. python3 scripts/test_pipeline_examples.py \
    --texts "Je veux aller à Paris" "Je souhaite voyager de Lyon à Marseille" \
    --config configs/nlp/spacy_finetuned.yaml

# Tester sur plusieurs fichiers audio
PYTHONPATH=. python3 scripts/test_pipeline_examples.py \
    --audio-files data/raw/audio/sample_000001.wav data/raw/audio/sample_000002.wav \
    --config configs/nlp/spacy_finetuned.yaml

# Tester sur un dataset
PYTHONPATH=. python3 scripts/test_pipeline_examples.py \
    --dataset data/splits/test/test_nlp.jsonl \
    --num-samples 20 \
    --config configs/nlp/spacy_finetuned.yaml \
    --output results/pipeline_test.json
```

---

### Nettoyer le projet

Supprime les fichiers inutiles (__pycache__, fichiers temporaires, etc.).

```bash
PYTHONPATH=. python3 scripts/clean_project.py
```

**Supprime :**
- Tous les dossiers `__pycache__`
- Fichiers temporaires (`.pyc`, `.py~`, `.DS_Store`)
- Dossiers vides
- Fichiers de test individuels (garde les rapports)

---

## ⚙️ Configuration

### Fichiers de configuration

Les fichiers de configuration sont au format YAML et se trouvent dans `configs/`.

**Structure :**
```
configs/
  base.yaml              # Configuration de base
  stt/
    whisper_small.yaml   # Configuration Whisper
  nlp/
    spacy_finetuned.yaml # Configuration spaCy fine-tuné
  pipeline/
    full.yaml            # Configuration pipeline complet
```

**Exemple de configuration NLP fine-tunée :**
```yaml
nlp:
  model_name: fr_core_news_md
  custom_model_path: models/nlp/spacy_finetuned/model
```

**Exemple de configuration STT :**
```yaml
stt:
  model_size: small
  language: fr
  device: cpu
```

---

## 📝 Variables d'environnement

Vous pouvez utiliser `PYTHONPATH=.` avant les commandes pour s'assurer que les modules sont trouvés :

```bash
PYTHONPATH=. python3 -m src.cli.stt transcribe --audio audio.wav
```

Ou définir dans votre shell :
```bash
export PYTHONPATH=.
```

---

## 🔍 Format des datasets

### Dataset STT (JSONL)

Chaque ligne contient :
```json
{
  "id": "sample_001",
  "audio_path": "data/raw/audio/sample_001.wav",
  "transcript": "Je veux aller à Paris depuis Lyon"
}
```

### Dataset NLP (JSONL)

Chaque ligne contient :
```json
{
  "id": "nlp_000001",
  "sentence": "Je veux aller à Paris depuis Lyon",
  "origin": "Lyon",
  "destination": "Paris",
  "is_valid": true
}
```

---

## 📊 Résultats générés

### Structure des résultats

```
results/
  stt/
    <model>_test/
      metrics.json          # Métriques agrégées
      predictions.jsonl     # Prédictions détaillées
      predictions.csv       # Format CSV
      report.md             # Rapport markdown
      errors_top.csv        # Top erreurs (si analyse activée)
  
  nlp/
    <model>_test/
      metrics.json          # Métriques agrégées
      predictions.jsonl     # Prédictions détaillées
      predictions.csv       # Format CSV
      report.md             # Rapport markdown
  
  pipeline/
    <audio_name>_result.json  # Résultats JSON
    <audio_name>_result.md     # Rapport markdown
```

---

## 🚀 Exemples de workflows complets

### Workflow 1 : Évaluer un modèle STT

```bash
# 1. Générer le dataset
PYTHONPATH=. python3 scripts/generate_stt_dataset.py --num-samples 500

# 2. Évaluer le modèle
python -m src.cli.stt evaluate \
    --dataset data/splits/test/test.jsonl \
    --model whisper \
    --config configs/stt/whisper_small.yaml \
    --output-dir results/stt/whisper_test \
    --analyze-errors
```

### Workflow 2 : Entraîner et évaluer un modèle NLP

```bash
# 1. Générer le dataset NLP
PYTHONPATH=. python3 scripts/generate_nlp_dataset.py --num-samples 5000

# 2. Entraîner le modèle
python -m src.cli.nlp train \
    --train-dataset data/splits/train/train_nlp.jsonl \
    --valid-dataset data/splits/valid/valid_nlp.jsonl \
    --model spacy \
    --n-iter 30 \
    --output-dir models/nlp/spacy_finetuned

# 3. Évaluer le modèle fine-tuné
python -m src.cli.nlp evaluate \
    --dataset data/splits/test/test_nlp.jsonl \
    --model spacy \
    --config configs/nlp/spacy_finetuned.yaml \
    --output-dir results/nlp/spacy_finetuned_test
```

### Workflow 3 : Pipeline complet

```bash
# Traiter un fichier audio complet
python -m src.cli.pipeline \
    --audio data/raw/audio/sample_000160.wav \
    --stt-model whisper \
    --nlp-model spacy \
    --config configs/nlp/spacy_finetuned.yaml
```

---

## 💡 Conseils

1. **Utilisez toujours `PYTHONPATH=.`** avec les scripts Python
2. **Les rapports markdown** sont générés automatiquement après chaque évaluation
3. **Les modèles fine-tunés** doivent être configurés dans un fichier YAML
4. **Les messages d'erreur** indiquent clairement les villes manquantes
5. **La confiance** varie de 0.0 à 1.0 selon la qualité de l'extraction

---

## 📞 Aide

Pour obtenir l'aide d'une commande :
```bash
python -m src.cli.stt --help
python -m src.cli.nlp --help
python -m src.cli.pipeline --help
```

Pour obtenir l'aide d'une sous-commande :
```bash
python -m src.cli.stt transcribe --help
python -m src.cli.nlp train --help
```

---

**Dernière mise à jour :** 2026-01-09

