# Rapport d'évaluation NLP - RegexAdvancedModel

**Date**: 2026-01-09 16:24:19  
**Modèle**: RegexAdvancedModel  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre d'échantillons**: 876

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: 0.5097 ± 0.4956
- **Recall**: 0.3898 ± 0.4167
- **F1-Score**: 0.4298 ± 0.4330

### Précision par entité
- **Origine correcte**: 708/876 (80.8%)
- **Destination correcte**: 259/876 (29.6%)
- **Les deux correctes**: 237/876 (27.1%)

### Validation
- **Précision de validation**: 0.8596 ± 0.3474

---

## 📈 Statistiques

- **Total d'échantillons**: 876
- **Extractions parfaites (origine + destination)**: 237 (27.1%)
- **Origine correcte**: 708 (80.8%)
- **Destination correcte**: 259 (29.6%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

### 1. F1: 1.0000

- **Texte**: Je veux voyager pour Lyon ?
- **Reference**: None → Lyon
- **Prediction**: None → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 2. F1: 1.0000

- **Texte**: Je veux aller pour Lyon à partir de Dijon
- **Reference**: Dijon → Lyon
- **Prediction**: Dijon → Lyon
- **Precision**: 1.0000, **Recall**: 1.0000

### 3. F1: 1.0000

- **Texte**: Je veux se rendre pour Marseille à partir de Toulouse
- **Reference**: Toulouse → Marseille
- **Prediction**: Toulouse → Marseille
- **Precision**: 1.0000, **Recall**: 1.0000

### 4. F1: 1.0000

- **Texte**: Je veux se rendre vers Le Havre ?
- **Reference**: None → Le Havre
- **Prediction**: None → Le Havre
- **Precision**: 1.0000, **Recall**: 1.0000

### 5. F1: 1.0000

- **Texte**: Je veux quitter pour Paris à partir de Strasbourg
- **Reference**: Strasbourg → Paris
- **Prediction**: Strasbourg → Paris
- **Precision**: 1.0000, **Recall**: 1.0000

---

## ❌ Pires extractions (F1 le plus bas)

### 1. F1: 0.0000

- **Texte**: J'ai visité Nancy
- **Reference**: None → None
- **Prediction**: None → Nancy
- **Precision**: 0.0000, **Recall**: 0.0000

### 2. F1: 0.0000

- **Texte**: Mon ami habite à Dunkerque
- **Reference**: None → None
- **Prediction**: None → Dunkerque
- **Precision**: 0.0000, **Recall**: 0.0000

### 3. F1: 0.0000

- **Texte**: Je veux donner
- **Reference**: None → None
- **Prediction**: None → Je
- **Precision**: 0.0000, **Recall**: 0.0000

### 4. F1: 0.0000

- **Texte**: Je veux réaliser
- **Reference**: None → None
- **Prediction**: None → Je
- **Precision**: 0.0000, **Recall**: 0.0000

### 5. F1: 0.0000

- **Texte**: Je veux quitter en direction de Nice ?
- **Reference**: None → Nice
- **Prediction**: Nice → None
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
