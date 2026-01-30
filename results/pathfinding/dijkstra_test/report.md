# Rapport d'évaluation Pathfinding - DijkstraPathfindingModel

**Date**: 2026-01-29 16:03:45  
**Modèle**: DijkstraPathfindingModel  
**Dataset**: data/splits/test/test_pathfinding.jsonl  
**Nombre d'échantillons**: 4

---

## 📊 Métriques globales

### Précision Origine/Destination
- **Précision origine**: 1.0000 ± 0.0000
- **Précision destination**: 1.0000 ± 0.0000

### Taux de succès
- **Itinéraires trouvés**: 2 / 4 (50.0%)
- **Taux de succès moyen**: 0.5000

### Précision du chemin
- **Précision du chemin moyenne**: N/A
- **Écart-type**: N/A

### Distance
- **Erreur de distance moyenne**: N/A km
- **Erreur relative moyenne**: N/A

### Nombre d'étapes
- **Nombre d'étapes moyen**: 3.50 ± 4.73

---

## 📈 Statistiques

- **Total d'échantillons**: 4
- **Itinéraires trouvés**: 2 (50.0%)
- **Itinéraires non trouvés**: 2 (50.0%)

---

## ✅ Exemples d'itinéraires trouvés

### 1. Toulouse → Bordeaux

- **Étapes**: 4
- **Distance**: 216.82580057187113 km
- **Précision du chemin**: None

### 2. Lyon → Marseille

- **Étapes**: 10
- **Distance**: 292.1834256018065 km
- **Précision du chemin**: None

---

## ❌ Exemples d'itinéraires non trouvés

### 1. Paris → Lyon

- **Erreur**: Raison inconnue

### 2. Bordeaux → Paris

- **Erreur**: Raison inconnue


---

## 📁 Fichiers

- **Dataset**: `data/splits/test/test_pathfinding.jsonl`
- **Prédictions**: `predictions.jsonl`
- **Métriques**: `metrics.json`
- **Rapport**: `report.md`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le système d'évaluation THOR.
