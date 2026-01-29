# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-29 15:43:03  
**Fichier audio**: data/raw/audio/sample_000004.wav

## 🔧 Configuration

- **Modèle STT**: vosk
- **Modèle NLP**: spacy

---

## 📝 Transcription (STT)

```
pourriez-vous m'aider à trouver un trajet vers paris
```

### Métadonnées STT
- **Modèle**: vosk
- **Langue détectée**: N/A
- **Segments**: N/A
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: Non détectée
- **Destination**: paris
- **Demande valide**: ✅ Oui
- **Confiance**: 0.60

### ⚠️ Message d'erreur
⚠️ Attention : La ville de départ est manquante. Veuillez préciser d'où vous partez.

### Métadonnées NLP
- **Modèle**: spacy
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: paris

---

## 📊 Analyse

⚠️ **Destination seulement** : Origine manquante

✅ La demande est **valide** (demande de trajet détectée)

---

## 🔍 Détails techniques

### Pipeline utilisé
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte

### Entités détectées
- paris (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000004.wav`
- **Rapport généré**: `sample_000004_vosk_spacy_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio data/raw/audio/sample_000004.wav --stt-model vosk --nlp-model spacy
```
