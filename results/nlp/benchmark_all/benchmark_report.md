# Benchmark NLP - Comparaison de modèles

**Date**: 2026-01-09 16:24:32  
**Dataset**: data/splits/test/test_nlp.jsonl  
**Nombre de modèles**: 5

---

## 📊 Résultats comparatifs

### Tableau récapitulatif

| Modèle | F1-Score | Precision | Recall | Origin Acc. | Dest. Acc. | Valid Acc. | Status |
|--------|----------|-----------|--------|-------------|------------|-------------|--------|
| spacy (spacy_finetuned) 🏆 | 0.6214 | 0.6221 | 0.6210 | 0.9498 | 0.8390 | 1.0000 | ✅ |
| regex_advanced  | 0.4298 | 0.5097 | 0.3898 | 0.8082 | 0.2957 | 0.8596 | ✅ |
| spacy  | 0.4066 | 0.4070 | 0.4132 | 0.7260 | 0.4224 | 1.0000 | ✅ |
| dummy  | 0.2302 | 0.2751 | 0.2078 | 0.7991 | 0.5708 | 0.6381 | ✅ |
| transformers | ❌ Erreur | - | - | - | - | - | ❌ |

---

## 📈 Détails par modèle

### spacy (spacy_finetuned)

#### Métriques principales

- **F1-Score**: 0.6214 ± 0.4845
- **Precision**: 0.6221 ± 0.4849
- **Recall**: 0.6210 ± 0.4845

#### Précision par entité

- **Origine**: 0.9498 ± 0.2184
- **Destination**: 0.8390 ± 0.3675
- **Les deux correctes**: 0.8368 ± 0.3696

#### Validation

- **Précision de validation**: 1.0000 ± 0.0000

#### Configuration

```yaml
{
  "model_name": "fr_core_news_md",
  "custom_model_path": "models/nlp/spacy_finetuned/model"
}
```

📄 [Rapport détaillé](./spacy (spacy_finetuned)/report.md)

---

### regex_advanced

#### Métriques principales

- **F1-Score**: 0.4298 ± 0.4330
- **Precision**: 0.5097 ± 0.4956
- **Recall**: 0.3898 ± 0.4167

#### Précision par entité

- **Origine**: 0.8082 ± 0.3937
- **Destination**: 0.2957 ± 0.4563
- **Les deux correctes**: 0.2705 ± 0.4442

#### Validation

- **Précision de validation**: 0.8596 ± 0.3474

📄 [Rapport détaillé](./regex_advanced/report.md)

---

### spacy

#### Métriques principales

- **F1-Score**: 0.4066 ± 0.4686
- **Precision**: 0.4070 ± 0.4714
- **Recall**: 0.4132 ± 0.4759

#### Précision par entité

- **Origine**: 0.7260 ± 0.4460
- **Destination**: 0.4224 ± 0.4939
- **Les deux correctes**: 0.4075 ± 0.4914

#### Validation

- **Précision de validation**: 1.0000 ± 0.0000

📄 [Rapport détaillé](./spacy/report.md)

---

### dummy

#### Métriques principales

- **F1-Score**: 0.2302 ± 0.3717
- **Precision**: 0.2751 ± 0.4362
- **Recall**: 0.2078 ± 0.3490

#### Précision par entité

- **Origine**: 0.7991 ± 0.4007
- **Destination**: 0.5708 ± 0.4950
- **Les deux correctes**: 0.5000 ± 0.5000

#### Validation

- **Précision de validation**: 0.6381 ± 0.4805

📄 [Rapport détaillé](./dummy/report.md)

---

### ❌ transformers

**Erreur**: 'NoneType' object has no attribute 'endswith'

## 🔍 Analyse comparative

### 🏆 Meilleur modèle: **spacy (spacy_finetuned)**

- **F1-Score**: 0.6214

### Comparaison

- **regex_advanced** vs **spacy (spacy_finetuned)**: -0.1916 (-30.8%)
- **spacy** vs **spacy (spacy_finetuned)**: -0.2148 (-34.6%)
- **dummy** vs **spacy (spacy_finetuned)**: -0.3912 (-63.0%)

---

## 📁 Fichiers générés

- `comparison.json`: Résultats comparatifs au format JSON
- `benchmark_report.md`: Ce rapport
- `<model_name>/`: Dossiers individuels avec résultats détaillés (si `save_individual_results=True`)

---

## 📝 Notes

Ce benchmark compare les modèles NLP sur le même dataset pour une évaluation équitable.

Pour plus de détails sur un modèle spécifique, consultez son rapport individuel dans son dossier.
