# Rapport Pipeline - Traitement Audio

**Date**: 2026-01-30 00:09:07  
**Fichier audio**: data/raw/audio/sample_000193.wav

## 🔧 Configuration

- **Modèle STT**: whisper
- **Modèle NLP**: spacy
- **Modèle Pathfinding**: dijkstra

---

## 📝 Transcription (STT)

```
Comment puis-je me rendre de bordeaux à Marseille ?
```

### Métadonnées STT
- **Modèle**: whisper
- **Langue détectée**: fr
- **Segments**: 1
- **Temps de traitement**: N/A

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: bordeaux
- **Destination**: Marseille
- **Demande valide**: ✅ Oui
- **Confiance**: 0.70

### Métadonnées NLP
- **Modèle**: spacy
- **Méthode d'extraction**: ner_patterns
- **Lieux détectés**: bordeaux, Marseille

---

## 🗺️ Itinéraire (Pathfinding)

### Résultats
- **Distance totale**: 1185.99 km
- **Nombre d'étapes**: 6
- **Temps estimé**: 347.5 minutes

### Étapes du trajet
1. Bordeaux Saint-Jean
2. Massy TGV
3. Marne-la-Vallée Chessy
4. Lyon Saint-Exupéry TGV
5. Aix-en-Provence TGV
6. Marseille Saint-Charles

### Détails techniques
- **UIC départ**: 87581009
- **UIC arrivée**: 87751008
- **Nombre de gares**: 6

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
- bordeaux (LOC)
- Marseille (LOC)


---

## 📁 Fichiers

- **Audio source**: `data/raw/audio/sample_000193.wav`
- **Rapport généré**: `sample_000193_whisper_spacy_dijkstra_result.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio data/raw/audio/sample_000193.wav --stt-model whisper --nlp-model spacy --pathfinding-model dijkstra
```
