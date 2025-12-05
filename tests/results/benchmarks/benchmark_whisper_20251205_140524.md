# Rapport de Benchmark Whisper

**Date**: 2025-12-05 14:05:24

**Source**: Microphone

**Modèles testés**: 5 | **Réussis**: 5 | **Échoués**: 0

## Résultats

| Modèle | Taille | Temps (s) | Mémoire (MB) | CPU (%) | Confiance | Texte |
|--------|--------|-----------|--------------|---------|-----------|-------|
| whisper-tiny | tiny | 0.70 | 375.06 | 178.1 | 96.16% | `Je veux aller à Marseille avec...` |
| whisper-base | base | 0.96 | 428.03 | 162.0 | 91.27% | `Je veux aller à Marseille avec...` |
| whisper-small | small | 2.50 | 1535.38 | 163.7 | 96.37% | `Je veux aller à Marseille avec...` |
| whisper-medium | medium | 8.06 | 3622.16 | 190.0 | 92.48% | `Je veux aller à Marseille avec...` |
| whisper-large | large | 16.14 | 5320.94 | 190.6 | 93.26% | `Je veux aller à Marseille avec...` |

## Comparaison

### Performance

- **Plus rapide**: `whisper-tiny` (0.70s)
- **Plus lent**: `whisper-large` (16.14s)
- **Différence**: 15.44s (2210.3% plus lent)

### Mémoire

- **Moins de mémoire**: `whisper-tiny` (375.06 MB)
- **Plus de mémoire**: `whisper-large` (5320.94 MB)
- **Différence**: 4945.88 MB

### Précision

- **Meilleure confiance**: `whisper-small` (96.37%)
- **Moins bonne confiance**: `whisper-base` (91.27%)
- **Différence**: 5.1 points de pourcentage

### Recommandation

- Pour la **vitesse**: `whisper-tiny`
- Pour la **mémoire**: `whisper-tiny`
- Pour la **précision**: `whisper-small`

## Transcriptions

### whisper-tiny

> Je veux aller à Marseille avec Kevin en partant de Lyon.

### whisper-base

> Je veux aller à Marseille avec Kevin en portant de Lyon.

### whisper-small

> Je veux aller à Marseille avec Kévin en portant de Lyon.

### whisper-medium

> Je veux aller à Marseille avec Kevin en portant de Lyon.

### whisper-large

> Je veux aller à Marseille avec Kevin en portant de Lyon.


## Statistiques détaillées

### whisper-tiny (tiny)

**Performance**
- ⏱️ Temps de transcription: `0.70s`
- 💾 Utilisation mémoire: `375.06 MB`
- 🔄 Utilisation CPU: `178.1%`

**Qualité**
- ✅ Confiance: `96.16%`
- 📝 Longueur texte: `56 caractères`

**Texte transcrit**
> Je veux aller à Marseille avec Kevin en partant de Lyon.

### whisper-base (base)

**Performance**
- ⏱️ Temps de transcription: `0.96s`
- 💾 Utilisation mémoire: `428.03 MB`
- 🔄 Utilisation CPU: `162.0%`

**Qualité**
- ✅ Confiance: `91.27%`
- 📝 Longueur texte: `56 caractères`

**Texte transcrit**
> Je veux aller à Marseille avec Kevin en portant de Lyon.

### whisper-small (small)

**Performance**
- ⏱️ Temps de transcription: `2.50s`
- 💾 Utilisation mémoire: `1535.38 MB`
- 🔄 Utilisation CPU: `163.7%`

**Qualité**
- ✅ Confiance: `96.37%`
- 📝 Longueur texte: `56 caractères`

**Texte transcrit**
> Je veux aller à Marseille avec Kévin en portant de Lyon.

### whisper-medium (medium)

**Performance**
- ⏱️ Temps de transcription: `8.06s`
- 💾 Utilisation mémoire: `3622.16 MB`
- 🔄 Utilisation CPU: `190.0%`

**Qualité**
- ✅ Confiance: `92.48%`
- 📝 Longueur texte: `56 caractères`

**Texte transcrit**
> Je veux aller à Marseille avec Kevin en portant de Lyon.

### whisper-large (large)

**Performance**
- ⏱️ Temps de transcription: `16.14s`
- 💾 Utilisation mémoire: `5320.94 MB`
- 🔄 Utilisation CPU: `190.6%`

**Qualité**
- ✅ Confiance: `93.26%`
- 📝 Longueur texte: `56 caractères`

**Texte transcrit**
> Je veux aller à Marseille avec Kevin en portant de Lyon.

