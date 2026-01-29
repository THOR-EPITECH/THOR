# Rapport d'évaluation STT - VoskModel

**Date**: 2026-01-29 15:33:32  
**Modèle**: VoskModel  
**Dataset**: data/splits/test/test.jsonl  
**Nombre d'échantillons**: 30

---

## 📊 Métriques globales

### Word Error Rate (WER)
- **Moyenne**: 0.4812
- **Écart-type**: 0.1973

### Character Error Rate (CER)
- **Moyenne**: 0.1605
- **Écart-type**: 0.1726

### Performance
- **Latency moyenne**: 0.1175 secondes
- **Écart-type**: 0.1572 secondes
- **Real-Time Factor (RTF) moyen**: 0.0419
- **Écart-type RTF**: 0.0532

### Confiance (si disponible)
- **Moyenne**: N/A
- **Écart-type**: N/A

---

## 📈 Statistiques

- **Total d'échantillons**: 30
- **Transcriptions parfaites (WER = 0.0)**: 0 (0.0%)
- **Erreurs importantes (WER > 0.5)**: 5 (16.7%)

---

## ✅ Meilleures transcriptions (WER le plus bas)

### 1. WER: 0.1818

- **Reference**: Je me demande s'il y a un moyen d'aller à Nice
- **Prediction**: je me demande s'il y a un moyen d'aller à nice
- **CER**: 0.0435
- **Latency**: 0.0606s
- **ID**: sample_000156

### 2. WER: 0.3000

- **Reference**: Je dois me rendre à Lille en partant de Reims
- **Prediction**: je dois me rendre à l'île en partant de reims
- **CER**: 0.1111
- **Latency**: 0.0676s
- **ID**: sample_000089

### 3. WER: 0.3000

- **Reference**: Je voudrais un billet pour aller de Nice à Cannes
- **Prediction**: je voudrais un billet pour aller de nice à cannes
- **CER**: 0.0612
- **Latency**: 0.0630s
- **ID**: sample_000010

### 4. WER: 0.3333

- **Reference**: Je voudrais me rendre à Bordeaux
- **Prediction**: je voudrais me rendre à bordeaux
- **CER**: 0.0625
- **Latency**: 0.0449s
- **ID**: sample_000176

### 5. WER: 0.3333

- **Reference**: Je voudrais bien aller à Paris
- **Prediction**: je voudrais bien aller à paris
- **CER**: 0.0667
- **Latency**: 0.0521s
- **ID**: sample_000001

---

## ❌ Pires transcriptions (WER le plus élevé)

### 1. WER: 1.0000

- **Reference**: Marseille a un beau port
- **Prediction**: merci iran boycott
- **CER**: 0.6667
- **Latency**: 0.1695s
- **ID**: sample_000066

### 2. WER: 1.0000

- **Reference**: Me gustaría viajar de Burdeos a Toulouse
- **Prediction**: mais story avait dit atteler
- **CER**: 0.7250
- **Latency**: 0.3856s
- **ID**: sample_000171

### 3. WER: 0.9286

- **Reference**: A quelle heure y a-t-il des trains vers Paris en partance de Toulouse ?
- **Prediction**: aqua white hilda transvase pearson partons de toulouse
- **CER**: 0.4930
- **Latency**: 0.4250s
- **ID**: sample_000081

### 4. WER: 0.8333

- **Reference**: J'ai un rendez-vous à Paris demain
- **Prediction**: giant rendez vous paris demain
- **CER**: 0.2941
- **Latency**: 0.2561s
- **ID**: sample_000187

### 5. WER: 0.6000

- **Reference**: Marseille est une belle ville
- **Prediction**: marseille est une bmw
- **CER**: 0.3793
- **Latency**: 0.0991s
- **ID**: sample_000112

---

## 🔍 Analyse détaillée

### Distribution des erreurs

- **Parfait (0.0)**: 0 échantillons (0.0%)
- **Excellent (0.0-0.1)**: 0 échantillons (0.0%)
- **Bon (0.1-0.3)**: 1 échantillons (3.3%)
- **Moyen (0.3-0.5)**: 24 échantillons (80.0%)
- **Mauvais (>0.5)**: 5 échantillons (16.7%)
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
