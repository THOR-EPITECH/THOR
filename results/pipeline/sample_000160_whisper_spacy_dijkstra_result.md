# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-29 16:01:06  
**Fichier audio**: data/raw/audio/sample_000160.wav

## 🔧 Configuration

- **Modèle STT**: whisper
- **Modèle NLP**: spacy
- **Modèle Pathfinding**: dijkstra

---

## 📝 Transcription (STT)

```
Je veux voyager de Toulouse à Bordeaux.
```

### Métadonnées STT
- **Modèle**: whisper
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
- **Modèle**: spacy
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: Toulouse, Bordeaux

---

## 🗺️ Itinéraire (Pathfinding)

### Résultats
- **Distance totale**: 216.83 km
- **Nombre d'étapes**: 4
- **Temps estimé**: None minutes

### Étapes du trajet
1. Toulouse Matabiau
2. Bordeaux Saint-Jean
3. Mérignac Arlac
4. Caudéran Mérignac

### Détails techniques
- **UIC départ**: 87611004
- **UIC arrivée**: 87581538
- **Nombre de gares**: 4

---

## 📊 Analyse

✅ **Extraction complète** : Origine et destination détectées

✅ La demande est **valide** (demande de trajet détectée)

---

## 🔍 Détails techniques

### Pipeline utilisé
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte
3. **Pathfinding** : Recherche d'itinéraire entre origine et destination

### Entités détectées
- Toulouse (LOC)
- Bordeaux (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000160.wav`
- **Rapport généré**: `sample_000160_whisper_spacy_dijkstra_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio data/raw/audio/sample_000160.wav --stt-model whisper --nlp-model spacy --pathfinding-model dijkstra
```
