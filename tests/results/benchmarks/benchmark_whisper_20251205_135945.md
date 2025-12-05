# Rapport de Benchmark Whisper

**Date**: 2025-12-05 13:59:45

**Source**: Microphone

**Modèles testés**: 5 | **Réussis**: 5 | **Échoués**: 0

## Résultats

| Modèle | Taille | Temps (s) | Mémoire (MB) | CPU (%) | Confiance | Texte |
|--------|--------|-----------|--------------|---------|-----------|-------|
| whisper-tiny | tiny | 0.64 | 373.41 | 166.7 | 97.60% | `Je veux aller de Paris à Marse...` |
| whisper-base | base | 0.87 | 426.83 | 155.4 | 97.40% | `Je veux aller de Paris à Marse...` |
| whisper-small | small | 2.09 | 1537.00 | 155.4 | 98.20% | `Je veux aller de Paris à Marse...` |
| whisper-medium | medium | 6.55 | 3622.33 | 181.3 | 84.93% | `Je veux aller de Paris à Marse...` |
| whisper-large | large | 14.07 | 5304.61 | 194.9 | 73.77% | `Je veux aller de Paris à Marse...` |

## Comparaison

### Performance

- **Plus rapide**: `whisper-tiny` (0.64s)
- **Plus lent**: `whisper-large` (14.07s)
- **Différence**: 13.43s (2096.4% plus lent)

### Mémoire

- **Moins de mémoire**: `whisper-tiny` (373.41 MB)
- **Plus de mémoire**: `whisper-large` (5304.61 MB)
- **Différence**: 4931.20 MB

### Précision

- **Meilleure confiance**: `whisper-small` (98.20%)
- **Moins bonne confiance**: `whisper-large` (73.77%)
- **Différence**: 24.4 points de pourcentage

### Recommandation

- Pour la **vitesse**: `whisper-tiny`
- Pour la **mémoire**: `whisper-tiny`
- Pour la **précision**: `whisper-small`

## Transcriptions

### whisper-tiny

> Je veux aller de Paris à Marseille.

### whisper-base

> Je veux aller de Paris à Marseille.

### whisper-small

> Je veux aller de Paris à Marseille.

### whisper-medium

> Je veux aller de Paris à Marseille.

### whisper-large

> Je veux aller de Paris à Marseille.


## Statistiques détaillées

### whisper-tiny (tiny)

**Performance**
- ⏱️ Temps de transcription: `0.64s`
- 💾 Utilisation mémoire: `373.41 MB`
- 🔄 Utilisation CPU: `166.7%`

**Qualité**
- ✅ Confiance: `97.60%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-base (base)

**Performance**
- ⏱️ Temps de transcription: `0.87s`
- 💾 Utilisation mémoire: `426.83 MB`
- 🔄 Utilisation CPU: `155.4%`

**Qualité**
- ✅ Confiance: `97.40%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-small (small)

**Performance**
- ⏱️ Temps de transcription: `2.09s`
- 💾 Utilisation mémoire: `1537.00 MB`
- 🔄 Utilisation CPU: `155.4%`

**Qualité**
- ✅ Confiance: `98.20%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-medium (medium)

**Performance**
- ⏱️ Temps de transcription: `6.55s`
- 💾 Utilisation mémoire: `3622.33 MB`
- 🔄 Utilisation CPU: `181.3%`

**Qualité**
- ✅ Confiance: `84.93%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-large (large)

**Performance**
- ⏱️ Temps de transcription: `14.07s`
- 💾 Utilisation mémoire: `5304.61 MB`
- 🔄 Utilisation CPU: `194.9%`

**Qualité**
- ✅ Confiance: `73.77%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

