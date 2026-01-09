# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-09 12:24:44  
**Fichier audio**: data/raw/audio/sample_000160.wav

---

## 📝 Transcription (STT)

```
Je veux voyager de Toulouse à Bordeaux.
```

### Métadonnées STT
- **Modèle**: whisper-small
- **Langue détectée**: fr
- **Segments**: 1
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: Toulouse
- **Destination**: Bordeaux
- **Demande valide**: ✅ Oui
- **Confiance**: 0.70

### Métadonnées NLP
- **Modèle**: spacy-fr_core_news_md
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: Bordeaux, Toulouse

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
- Bordeaux (LOC)
- Toulouse (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000160.wav`
- **Rapport généré**: `sample_000160_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement :
```bash
python -m src.cli.pipeline --audio data/raw/audio/sample_000160.wav --stt-model whisper --nlp-model spacy
```
