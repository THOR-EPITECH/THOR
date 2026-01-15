# Rapport d'évaluation NLP - SpacyFRModel

**Date**: 2026-01-09 16:24:22  
**Modèle**: SpacyFRModel  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre d'échantillons**: 876

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: 0.4070 ± 0.4714
- **Recall**: 0.4132 ± 0.4759
- **F1-Score**: 0.4066 ± 0.4686

### Précision par entité
- **Origine correcte**: 636/876 (72.6%)
- **Destination correcte**: 370/876 (42.2%)
- **Les deux correctes**: 357/876 (40.8%)

### Validation
- **Précision de validation**: 1.0000 ± 0.0000

---

## 📈 Statistiques

- **Total d'échantillons**: 876
- **Extractions parfaites (origine + destination)**: 357 (40.8%)
- **Origine correcte**: 636 (72.6%)
- **Destination correcte**: 370 (42.2%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

### 1. F1: 1.0000

- **Texte**: Je veux se rendre pour Lyon depuis Bordeaux
- **Reference**: Bordeaux → Lyon
- **Prediction**: Bordeaux → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 2. F1: 1.0000

- **Texte**: Je veux se rendre en direction de Montpellier ?
- **Reference**: None → Montpellier
- **Prediction**: None → Montpellier
- **Precision**: 1.0000, **Recall**: 1.0000

### 3. F1: 1.0000

- **Texte**: Je veux voyager vers Lyon depuis Toulouse
- **Reference**: Toulouse → Lyon
- **Prediction**: Toulouse → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 4. F1: 1.0000

- **Texte**: Je veux se rendre à Lyon de Villeurbanne
- **Reference**: Villeurbanne → Lyon
- **Prediction**: Villeurbanne → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 5. F1: 1.0000

- **Texte**: Je veux voyager pour Lyon ?
- **Reference**: None → Lyon
- **Prediction**: None → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

---

## ❌ Pires extractions (F1 le plus bas)

### 1. F1: 0.0000

- **Texte**: Je veux se rendre pour Lyon de Toulouse
- **Reference**: Toulouse → Lyon
- **Prediction**: None → Toulouse
- **Precision**: 0.0000, **Recall**: 0.0000

### 2. F1: 0.0000

- **Texte**: J'ai visité Nancy
- **Reference**: None → None
- **Prediction**: None → Nancy
- **Precision**: 0.0000, **Recall**: 0.0000

### 3. F1: 0.0000

- **Texte**: Je veux voyager pour Paris depuis Grenoble
- **Reference**: Grenoble → Paris
- **Prediction**: Paris → Grenoble
- **Precision**: 0.0000, **Recall**: 0.0000

### 4. F1: 0.0000

- **Texte**: Mon ami habite à Dunkerque
- **Reference**: None → None
- **Prediction**: None → Dunkerque
- **Precision**: 0.0000, **Recall**: 0.0000

### 5. F1: 0.0000

- **Texte**: Je veux donner
- **Reference**: None → None
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

---

## 📁 Fichiers générés

- `metrics.json`: Métriques agrégées au format JSON
- `predictions.jsonl`: Toutes les prédictions avec métriques détaillées
- `predictions.csv`: Même contenu en format CSV
- `report.md`: Ce rapport

---

## 📝 Notes

Ce rapport a été généré automatiquement par le système d'évaluation THOR.

Pour plus de détails, consultez les fichiers JSON/CSV dans le dossier de résultats.
