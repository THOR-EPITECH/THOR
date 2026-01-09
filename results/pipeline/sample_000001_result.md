# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-09 14:24:50  
**Fichier audio**: data/raw/audio/sample_000001.wav

---

## 📝 Transcription (STT)

```
Je voudrais bien aller à Paris.
```

### Métadonnées STT
- **Modèle**: whisper-small
- **Langue détectée**: fr
- **Segments**: 1
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: Non détectée
- **Destination**: Paris
- **Demande valide**: ✅ Oui
- **Confiance**: 0.60

### ⚠️ Message d'erreur
⚠️ Attention : La ville de départ est manquante. Veuillez préciser d'où vous partez.

### Métadonnées NLP
- **Modèle**: spacy-fr_core_news_md
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: Paris

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
- Paris (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000001.wav`
- **Rapport généré**: `sample_000001_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement :
```bash
python -m src.cli.pipeline --audio data/raw/audio/sample_000001.wav --stt-model whisper --nlp-model spacy
```
