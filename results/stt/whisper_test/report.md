# Rapport d'évaluation STT - WhisperModel

**Date**: 2026-01-09 12:04:05  
**Modèle**: WhisperModel  
**Dataset**: data/splits/test/test.jsonl  
**Nombre d'échantillons**: 30

---

## 📊 Métriques globales

### Word Error Rate (WER)
- **Moyenne**: 0.2913
- **Écart-type**: 0.2854

### Character Error Rate (CER)
- **Moyenne**: 0.1224
- **Écart-type**: 0.1682

### Performance
- **Latency moyenne**: 0.3871 secondes
- **Écart-type**: 0.1935 secondes
- **Real-Time Factor (RTF) moyen**: 0.1584
- **Écart-type RTF**: 0.0900

### Confiance (si disponible)
- **Moyenne**: N/A
- **Écart-type**: N/A

---

## 📈 Statistiques

- **Total d'échantillons**: 30
- **Transcriptions parfaites (WER = 0.0)**: 5 (16.7%)
- **Erreurs importantes (WER > 0.5)**: 6 (20.0%)

---

## ✅ Meilleures transcriptions (WER le plus bas)

### 1. WER: 0.0000

- **Reference**: Comment pourrais-je me rendre à Toulouse ?
- **Prediction**: Comment pourrais-je me rendre à Toulouse ?
- **CER**: 0.0000
- **Latency**: 0.3356s
- **ID**: sample_000018

### 2. WER: 0.0000

- **Reference**: Merci beaucoup
- **Prediction**: Merci beaucoup
- **CER**: 0.0000
- **Latency**: 0.2649s
- **ID**: sample_000134

### 3. WER: 0.0000

- **Reference**: Pouvez-vous me dire comment aller de Strasbourg à Nancy ?
- **Prediction**: Pouvez-vous me dire comment aller de Strasbourg à Nancy ?
- **CER**: 0.0000
- **Latency**: 0.3652s
- **ID**: sample_000012

### 4. WER: 0.0000

- **Reference**: Est-ce que je peux aller à Nice depuis Cannes ?
- **Prediction**: Est-ce que je peux aller à Nice depuis Cannes ?
- **CER**: 0.0000
- **Latency**: 0.3473s
- **ID**: sample_000148

### 5. WER: 0.0000

- **Reference**: Pouvez-vous me dire comment aller de Strasbourg à Nancy ?
- **Prediction**: Pouvez-vous me dire comment aller de Strasbourg à Nancy ?
- **CER**: 0.0000
- **Latency**: 0.3679s
- **ID**: sample_000197

---

## ❌ Pires transcriptions (WER le plus élevé)

### 1. WER: 1.0000

- **Reference**: Marseille a un beau port
- **Prediction**: Marseille, Arundbeau Porte
- **CER**: 0.2308
- **Latency**: 0.3304s
- **ID**: sample_000066

### 2. WER: 0.8571

- **Reference**: Me gustaría viajar de Burdeos a Toulouse
- **Prediction**: Mi-Gustaria via Giardin Berdeo's a Toulouse.
- **CER**: 0.2955
- **Latency**: 0.3802s
- **ID**: sample_000171

### 3. WER: 0.8333

- **Reference**: J'ai un rendez-vous à Paris demain
- **Prediction**: Géant Rende's Vusseau Paris Domain
- **CER**: 0.5000
- **Latency**: 0.3453s
- **ID**: sample_000187

### 4. WER: 0.8000

- **Reference**: Quel temps fait-il aujourd'hui ?
- **Prediction**: Qu'est-ce que ça fait ?
- **CER**: 0.6875
- **Latency**: 0.3152s
- **ID**: sample_000085

### 5. WER: 0.7500

- **Reference**: Combien ça coûte ?
- **Prediction**: Combien S'accoute
- **CER**: 0.3333
- **Latency**: 0.2945s
- **ID**: sample_000099

---

## 🔍 Analyse détaillée

### Distribution des erreurs

- **Parfait (0.0)**: 5 échantillons (16.7%)
- **Excellent (0.0-0.1)**: 2 échantillons (6.7%)
- **Bon (0.1-0.3)**: 14 échantillons (46.7%)
- **Moyen (0.3-0.5)**: 3 échantillons (10.0%)
- **Mauvais (>0.5)**: 6 échantillons (20.0%)
---

## 📁 Fichiers générés

- `metrics.json`: Métriques agrégées au format JSON
- `predictions.jsonl`: Toutes les prédictions avec métriques détaillées
- `predictions.csv`: Même contenu en format CSV
- `errors_top.csv`: Top erreurs triées par WER
- `report.md`: Ce rapport

---

## 📝 Notes

Ce rapport a été généré automatiquement par le système d'évaluation THOR.

Pour plus de détails, consultez les fichiers JSON/CSV dans le dossier de résultats.
