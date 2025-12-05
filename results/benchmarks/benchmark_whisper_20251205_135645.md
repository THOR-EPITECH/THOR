# Rapport de Benchmark Whisper

**Date**: 2025-12-05 13:56:45

**Source**: Microphone

**Modèles testés**: 5 | **Réussis**: 5 | **Échoués**: 0

## Résultats

| Modèle | Taille | Temps (s) | Mémoire (MB) | CPU (%) | Confiance | Texte |
|--------|--------|-----------|--------------|---------|-----------|-------|
| whisper-tiny | tiny | 4.25 | 373.70 | 25.8 | 96.19% | `Je veux aller de Paris à Marse...` |
| whisper-base | base | 0.87 | 429.73 | 156.1 | 95.98% | `Je veux aller de Paris à Marse...` |
| whisper-small | small | 2.10 | 1537.48 | 156.9 | 98.47% | `Je veux aller de Paris à Marse...` |
| whisper-medium | medium | 6.53 | 3619.05 | 187.1 | 84.83% | `Je veux aller de Paris à Marse...` |
| whisper-large | large | 14.41 | 5510.47 | 192.4 | 83.60% | `Je veux aller de Paris à Marse...` |

## Comparaison

### Performance

- **Plus rapide**: `whisper-base` (0.87s)
- **Plus lent**: `whisper-large` (14.41s)
- **Différence**: 13.54s (1558.3% plus lent)

### Mémoire

- **Moins de mémoire**: `whisper-tiny` (373.70 MB)
- **Plus de mémoire**: `whisper-large` (5510.47 MB)
- **Différence**: 5136.77 MB

### Précision

- **Meilleure confiance**: `whisper-small` (98.47%)
- **Moins bonne confiance**: `whisper-large` (83.60%)
- **Différence**: 14.9 points de pourcentage

### Recommandation

- Pour la **vitesse**: `whisper-base`
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
- ⏱️ Temps de transcription: `4.25s`
- 💾 Utilisation mémoire: `373.70 MB`
- 🔄 Utilisation CPU: `25.8%`

**Qualité**
- ✅ Confiance: `96.19%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-base (base)

**Performance**
- ⏱️ Temps de transcription: `0.87s`
- 💾 Utilisation mémoire: `429.73 MB`
- 🔄 Utilisation CPU: `156.1%`

**Qualité**
- ✅ Confiance: `95.98%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-small (small)

**Performance**
- ⏱️ Temps de transcription: `2.10s`
- 💾 Utilisation mémoire: `1537.48 MB`
- 🔄 Utilisation CPU: `156.9%`

**Qualité**
- ✅ Confiance: `98.47%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-medium (medium)

**Performance**
- ⏱️ Temps de transcription: `6.53s`
- 💾 Utilisation mémoire: `3619.05 MB`
- 🔄 Utilisation CPU: `187.1%`

**Qualité**
- ✅ Confiance: `84.83%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

### whisper-large (large)

**Performance**
- ⏱️ Temps de transcription: `14.41s`
- 💾 Utilisation mémoire: `5510.47 MB`
- 🔄 Utilisation CPU: `192.4%`

**Qualité**
- ✅ Confiance: `83.60%`
- 📝 Longueur texte: `35 caractères`

**Texte transcrit**
> Je veux aller de Paris à Marseille.

