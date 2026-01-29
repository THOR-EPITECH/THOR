# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-29 15:43:45  
**Fichier audio**: data/raw/audio/sample_000160.wav

## 🔧 Configuration

- **Modèle STT**: vosk
- **Modèle NLP**: spacy

---

## 📝 Transcription (STT)

```
je veux voyager de toulouse à bordeaux
```

### Métadonnées STT
- **Modèle**: vosk
- **Langue détectée**: N/A
- **Segments**: N/A
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: toulouse
- **Destination**: bordeaux
- **Demande valide**: ✅ Oui
- **Confiance**: 0.70

### Métadonnées NLP
- **Modèle**: spacy
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: bordeaux, toulouse

---

## 📊 Analyse

✅ **Extraction complète** : Origine et destination détectées

✅ La demande est **valide** (demande de trajet détectée)

---

## 🔍 Détails techniques

### Pipeline utilisé
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte

### Entités détectées
- bordeaux (LOC)
- toulouse (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000160.wav`
- **Rapport généré**: `sample_000160_vosk_spacy_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio data/raw/audio/sample_000160.wav --stt-model vosk --nlp-model spacy
```
