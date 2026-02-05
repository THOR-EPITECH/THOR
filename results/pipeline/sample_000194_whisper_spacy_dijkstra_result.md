# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-30 00:24:30  
**Fichier audio**: data/raw/audio/sample_000194.wav

## 🔧 Configuration

- **Modèle STT**: whisper
- **Modèle NLP**: spacy
- **Modèle Pathfinding**: dijkstra

---

## 📝 Transcription (STT)

```
Excusez-moi.
```

### Métadonnées STT
- **Modèle**: whisper
- **Langue détectée**: fr
- **Segments**: 1
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: Non détectée
- **Destination**: Non détectée
- **Demande valide**: ❌ Non
- **Confiance**: 0.20

### Métadonnées NLP
- **Modèle**: spacy
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: Aucun

---

---

## 📊 Analyse

❌ **Aucune extraction** : Origine et destination non détectées

❌ La demande est **invalide** (pas une demande de trajet)

---

## 🔍 Détails techniques

### Pipeline utilisé
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte
3. **Pathfinding** : Recherche d'itinéraire entre origine et destination

### Entités détectées
- Aucune entité détectée


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000194.wav`
- **Rapport généré**: `sample_000194_whisper_spacy_dijkstra_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio data/raw/audio/sample_000194.wav --stt-model whisper --nlp-model spacy --pathfinding-model dijkstra
```
