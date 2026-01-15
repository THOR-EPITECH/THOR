# Modèle STT : Dummy

## Vue d'ensemble

Le modèle Dummy est un modèle baseline utilisé pour les tests et le développement. Il ne fait pas de vraie transcription mais simule le comportement d'un modèle STT pour valider le pipeline.

## Caractéristiques

- **Précision** : ❌ (Ne fait pas de transcription réelle)
- **Vitesse** : ⭐⭐⭐⭐⭐ (Instantané)
- **Multilingue** : ❌
- **Offline** : ✅
- **GPU requis** : ❌

## Utilisation

Le modèle Dummy est principalement utilisé pour :
- **Tests unitaires** : Valider le pipeline sans dépendances externes
- **Baseline** : Comparer les performances des vrais modèles
- **Développement** : Tester rapidement sans attendre la transcription

## Modes disponibles

### Mode "empty"
Retourne un texte vide (simule une transcription échouée).

```python
model = DummySTTModel({"mode": "empty"})
result = model.transcribe("audio.wav")
# result.text = ""
```

### Mode "repeat"
Répète le nom du fichier (sans extension).

```python
model = DummySTTModel({"mode": "repeat"})
result = model.transcribe("data/audio/sample_001.wav")
# result.text = "sample_001"
```

## Configuration

```yaml
# configs/stt/dummy.yaml
model: dummy
mode: empty  # ou "repeat"
```

## Utilisation

### Via CLI

```bash
python -m src.cli.stt transcribe \
    --model dummy \
    --audio data/raw/audio/sample.wav
```

### Via Python

```python
from src.stt.models.dummy import DummySTTModel

# Mode empty
model = DummySTTModel({"mode": "empty"})
result = model.transcribe("audio.wav")

# Mode repeat
model = DummySTTModel({"mode": "repeat"})
result = model.transcribe("audio.wav")
```

## Résultat

Le modèle retourne un objet `STTResult` :

```python
STTResult(
    text="",  # ou le nom du fichier selon le mode
    confidence=0.0,
    processing_time=0.1,  # Simule un temps de traitement
    metadata={
        "model": "dummy",
        "mode": "empty"  # ou "repeat"
    }
)
```

## Cas d'usage

1. **Tests de pipeline** : Valider que le pipeline fonctionne sans dépendre d'un vrai modèle STT
2. **Tests NLP** : Tester l'extraction NLP avec un texte contrôlé
3. **Benchmark** : Utiliser comme baseline pour comparer les performances

## Limitations

- Ne fait pas de vraie transcription
- Ne peut pas être utilisé en production
- Utile uniquement pour les tests et le développement
