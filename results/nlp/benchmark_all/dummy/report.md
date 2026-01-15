# Rapport d'évaluation NLP - DummyNLPModel

**Date**: 2026-01-09 16:24:19  
**Modèle**: DummyNLPModel  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre d'échantillons**: 876

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: 0.2751 ± 0.4362
- **Recall**: 0.2078 ± 0.3490
- **F1-Score**: 0.2302 ± 0.3717

### Précision par entité
- **Origine correcte**: 700/876 (79.9%)
- **Destination correcte**: 500/876 (57.1%)
- **Les deux correctes**: 438/876 (50.0%)

### Validation
- **Précision de validation**: 0.6381 ± 0.4805

---

## 📈 Statistiques

- **Total d'échantillons**: 876
- **Extractions parfaites (origine + destination)**: 438 (50.0%)
- **Origine correcte**: 700 (79.9%)
- **Destination correcte**: 500 (57.1%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

### 1. F1: 1.0000

- **Texte**: Je veux voyager vers Lyon depuis Toulouse
- **Reference**: Toulouse → Lyon
- **Prediction**: Toulouse → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 2. F1: 1.0000

- **Texte**: Je veux se rendre vers Le Havre ?
- **Reference**: None → Le Havre
- **Prediction**: None → Le Havre
- **Precision**: 1.0000, **Recall**: 1.0000

### 3. F1: 1.0000

- **Texte**: Je veux se rendre à Lyon depuis Lille
- **Reference**: Lille → Lyon
- **Prediction**: Lille → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 4. F1: 1.0000

- **Texte**: Je veux voyager à Lyon depuis Saint-Étienne
- **Reference**: Saint-Étienne → Lyon
- **Prediction**: Saint-étienne → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 5. F1: 1.0000

- **Texte**: Je veux aller à Paris depuis Toulon
- **Reference**: Toulon → Paris
- **Prediction**: Toulon → Paris
- **Precision**: 1.0000, **Recall**: 1.0000

---

## ❌ Pires extractions (F1 le plus bas)

### 1. F1: 0.0000

- **Texte**: Je veux se rendre pour Lyon de Toulouse
- **Reference**: Toulouse → Lyon
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 2. F1: 0.0000

- **Texte**: J'ai visité Nancy
- **Reference**: None → None
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 3. F1: 0.0000

- **Texte**: Je veux partir vers Nice
- **Reference**: None → Nice
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 4. F1: 0.0000

- **Texte**: Mon ami habite à Dunkerque
- **Reference**: None → None
- **Prediction**: None → None
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
