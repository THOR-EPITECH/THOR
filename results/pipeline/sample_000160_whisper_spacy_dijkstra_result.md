# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-30 00:27:10  
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
- **Lieux détectés**: Bordeaux, Toulouse

---

## 🗺️ Itinéraire (Pathfinding)

### Résultats
- **⏱️ Temps de trajet**: 2h23 (143 min)
- **📏 Distance totale**: 209.5 km
- **🛤️ Nombre d'étapes**: 2

### 📊 Détails du trajet

| # | Type | Départ | Arrivée | Temps | Distance | Trains/jour |
|---|------|--------|---------|-------|----------|-------------|
| 1 | 🚄 TGV | Toulouse Matabiau | Bordeaux Saint-Jean | 143 min | 209.5 km | 17 |

### 🚂 Types de trains utilisés
- 🚄 **TGV**: 1 segment(s)

### 🔧 Détails techniques
- **Mode**: temps_reel
- **UIC départ**: 87611004
- **UIC arrivée**: 87581009
- **Nombre de gares**: 2

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
- Bordeaux (LOC)
- Toulouse (LOC)


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
