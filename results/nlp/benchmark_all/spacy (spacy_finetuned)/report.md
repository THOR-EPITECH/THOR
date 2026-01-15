# Rapport d'évaluation NLP - SpacyFRModel

**Date**: 2026-01-09 16:24:24  
**Modèle**: SpacyFRModel  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre d'échantillons**: 876

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: 0.6221 ± 0.4849
- **Recall**: 0.6210 ± 0.4845
- **F1-Score**: 0.6214 ± 0.4845

### Précision par entité
- **Origine correcte**: 832/876 (95.0%)
- **Destination correcte**: 735/876 (83.9%)
- **Les deux correctes**: 733/876 (83.7%)

### Validation
- **Précision de validation**: 1.0000 ± 0.0000

---

## 📈 Statistiques

- **Total d'échantillons**: 876
- **Extractions parfaites (origine + destination)**: 733 (83.7%)
- **Origine correcte**: 832 (95.0%)
- **Destination correcte**: 735 (83.9%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

### 1. F1: 1.0000

- **Texte**: Je veux se rendre pour Lyon depuis Bordeaux
- **Reference**: Bordeaux → Lyon
- **Prediction**: Bordeaux → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 2. F1: 1.0000

- **Texte**: Je veux quitter Angers
- **Reference**: Angers → None
- **Prediction**: Angers → None
- **Precision**: 1.0000, **Recall**: 1.0000

### 3. F1: 1.0000

- **Texte**: Je veux se rendre en direction de Montpellier ?
- **Reference**: None → Montpellier
- **Prediction**: None → Montpellier
- **Precision**: 1.0000, **Recall**: 1.0000

### 4. F1: 1.0000

- **Texte**: Je veux voyager vers Lyon depuis Toulouse
- **Reference**: Toulouse → Lyon
- **Prediction**: Toulouse → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 5. F1: 1.0000

- **Texte**: Je veux se rendre à Lyon de Villeurbanne
- **Reference**: Villeurbanne → Lyon
- **Prediction**: Villeurbanne → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

---

## ❌ Pires extractions (F1 le plus bas)

### 1. F1: 0.0000

- **Texte**: J'ai visité Nancy
- **Reference**: None → None
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 2. F1: 0.0000

- **Texte**: Mon ami habite à Dunkerque
- **Reference**: None → None
- **Prediction**: None → Dunkerque
- **Precision**: 0.0000, **Recall**: 0.0000

### 3. F1: 0.0000

- **Texte**: Je veux donner
- **Reference**: None → None
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 4. F1: 0.0000

- **Texte**: Je veux réaliser
- **Reference**: None → None
- **Prediction**: None → None
- **Precision**: 0.0000, **Recall**: 0.0000

### 5. F1: 0.0000

- **Texte**: Je veux faire choisir
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
