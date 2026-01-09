# Rapport d'évaluation NLP - SpacyFRModel

**Date**: 2026-01-09 12:25:32  
**Modèle**: SpacyFRModel  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre d'échantillons**: 30

---

## 📊 Métriques globales

### Precision, Recall, F1
- **Precision**: 0.6000 ± 0.4726
- **Recall**: 0.6333 ± 0.4819
- **F1-Score**: 0.6111 ± 0.4721

### Précision par entité
- **Origine correcte**: 27/30 (90.0%)
- **Destination correcte**: 17/30 (56.7%)
- **Les deux correctes**: 17/30 (56.7%)

### Validation
- **Précision de validation**: 1.0000 ± 0.0000

---

## 📈 Statistiques

- **Total d'échantillons**: 30
- **Extractions parfaites (origine + destination)**: 17 (56.7%)
- **Origine correcte**: 27 (90.0%)
- **Destination correcte**: 17 (56.7%)

---

## ✅ Meilleures extractions (F1 le plus élevé)

### 1. F1: 1.0000

- **Texte**: Je veux voyager de Toulouse à Bordeaux
- **Reference**: Toulouse → Bordeaux
- **Prediction**: Toulouse → Bordeaux
- **Precision**: 1.0000, **Recall**: 1.0000

### 2. F1: 1.0000

- **Texte**: Je veux aller à Paris
- **Reference**: None → Paris
- **Prediction**: None → Paris
- **Precision**: 1.0000, **Recall**: 1.0000

### 3. F1: 1.0000

- **Texte**: je veux aller a paris depuis lyon
- **Reference**: Lyon → Paris
- **Prediction**: lyon → paris
- **Precision**: 1.0000, **Recall**: 1.0000

### 4. F1: 1.0000

- **Texte**: Je souhaite un trajet de Nantes à Rennes
- **Reference**: Nantes → Rennes
- **Prediction**: Nantes → Rennes
- **Precision**: 1.0000, **Recall**: 1.0000

### 5. F1: 1.0000

- **Texte**: Je veux aller à Paris depuis Lyon
- **Reference**: Lyon → Paris
- **Prediction**: Lyon → Paris
- **Precision**: 1.0000, **Recall**: 1.0000

---

## ❌ Pires extractions (F1 le plus bas)

### 1. F1: 0.0000

- **Texte**: Je connais quelqu'un qui habite à Toulouse
- **Reference**: None → None
- **Prediction**: None → Toulouse
- **Precision**: 0.0000, **Recall**: 0.0000

### 2. F1: 0.0000

- **Texte**: Je dois me rendre à Lille en partant de Reims
- **Reference**: Reims → Lille
- **Prediction**: Lille → Reims
- **Precision**: 0.0000, **Recall**: 0.0000

### 3. F1: 0.0000

- **Texte**: Comment faire pour quitter Toulouse ?
- **Reference**: Toulouse → None
- **Prediction**: None → Toulouse
- **Precision**: 0.0000, **Recall**: 0.0000

### 4. F1: 0.0000

- **Texte**: Marseille a un beau port
- **Reference**: None → None
- **Prediction**: None → Marseille
- **Precision**: 0.0000, **Recall**: 0.0000

### 5. F1: 0.0000

- **Texte**: Mon ami habite à Bordeaux
- **Reference**: None → None
- **Prediction**: None → Bordeaux
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
