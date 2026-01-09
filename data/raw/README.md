# Données brutes (raw)

Ce dossier contient les données brutes avant traitement.

## Structure

```
raw/
  audio/          # Fichiers audio bruts (.wav, .mp3, etc.)
```

## Notes importantes

⚠️ **Les transcripts ne sont PAS dans ce dossier !**

Les transcripts (ground truth) sont directement intégrés dans les fichiers JSONL des splits :
- `data/splits/train/*.jsonl`
- `data/splits/test/*.jsonl`
- `data/splits/valid/*.jsonl`

Chaque ligne JSONL contient :
```json
{
  "id": "sample_001",
  "audio_path": "data/raw/audio/sample_001.wav",
  "transcript": "Je veux aller à Paris depuis Lyon"
}
```

Le champ `transcript` contient la transcription de référence (ground truth) pour l'évaluation.

## Pourquoi cette organisation ?

1. **Simplicité** : Tout est dans un seul fichier JSONL par split
2. **Cohérence** : Audio et transcript sont liés dans la même ligne
3. **Pas de duplication** : Pas besoin de maintenir des fichiers séparés
4. **Facilité d'utilisation** : Le code lit directement le JSONL avec audio_path et transcript

