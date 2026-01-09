"""
Génération de rapports markdown pour les résultats du pipeline.
"""
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def generate_pipeline_report(result: Dict[str, Any], output_path: str | Path) -> Path:
    """
    Génère un rapport markdown pour un résultat de pipeline.
    
    Args:
        result: Résultat du pipeline
        output_path: Chemin où sauvegarder le rapport
    
    Returns:
        Chemin du fichier créé
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    audio_path = result.get("audio_path", "N/A")
    transcript = result.get("transcript", "")
    origin = result.get("origin")
    destination = result.get("destination")
    is_valid = result.get("is_valid", False)
    confidence = result.get("confidence")
    
    stt_metadata = result.get("stt_metadata", {})
    nlp_metadata = result.get("nlp_metadata", {})
    
    # Formate les valeurs
    confidence_str = f"{confidence:.2f}" if confidence is not None else "N/A"
    processing_time = stt_metadata.get('processing_time')
    processing_time_str = f"{processing_time:.2f}s" if processing_time else "N/A"
    
    # Génère le rapport
    report = f"""# Rapport Pipeline - Traitement Audio

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Fichier audio**: {audio_path}

---

## 📝 Transcription (STT)

```
{transcript}
```

### Métadonnées STT
- **Modèle**: {stt_metadata.get('model', 'N/A')}
- **Langue détectée**: {stt_metadata.get('detected_language', 'N/A')}
- **Segments**: {stt_metadata.get('segments', 'N/A')}
- **Temps de traitement**: {processing_time_str}

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: {origin if origin else "Non détectée"}
- **Destination**: {destination if destination else "Non détectée"}
- **Demande valide**: {"✅ Oui" if is_valid else "❌ Non"}
- **Confiance**: {confidence_str}

### Métadonnées NLP
- **Modèle**: {nlp_metadata.get('model', 'N/A')}
- **Méthode d'extraction**: {nlp_metadata.get('extraction_method', 'N/A')}
- **Lieux détectés**: {', '.join(nlp_metadata.get('locations_found', [])) if nlp_metadata.get('locations_found') else 'Aucun'}

---

## 📊 Analyse

"""
    
    # Analyse de la qualité
    if origin and destination:
        report += "✅ **Extraction complète** : Origine et destination détectées\n\n"
    elif origin:
        report += "⚠️ **Origine seulement** : Destination manquante\n\n"
    elif destination:
        report += "⚠️ **Destination seulement** : Origine manquante\n\n"
    else:
        report += "❌ **Aucune extraction** : Origine et destination non détectées\n\n"
    
    if is_valid:
        report += "✅ La demande est **valide** (demande de trajet détectée)\n\n"
    else:
        report += "❌ La demande est **invalide** (pas une demande de trajet)\n\n"
    
    # Détails de l'extraction
    report += """---

## 🔍 Détails techniques

### Pipeline utilisé
1. **STT** : Transcription audio → texte
2. **NLP** : Extraction origine/destination depuis le texte

### Entités détectées
"""
    
    entities = nlp_metadata.get('entities', [])
    if entities:
        for entity in entities:
            report += f"- {entity.get('text', 'N/A')} ({entity.get('label', 'N/A')})\n"
    else:
        report += "- Aucune entité détectée\n"
    
    report += f"""

---

## 📁 Fichiers

- **Audio source**: `{audio_path}`
- **Rapport généré**: `{output_path.name}`

---

## 📝 Notes

Ce rapport a été généré automatiquement par le pipeline THOR.

Pour relancer le traitement :
```bash
python -m src.cli.pipeline --audio {audio_path} --stt-model whisper --nlp-model spacy
```
"""
    
    # Sauvegarde
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_path

