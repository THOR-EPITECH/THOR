"""
Génération de rapports markdown pour les résultats du pipeline.
"""
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def generate_pipeline_report(result: Dict[str, Any], output_path: str | Path, stt_model_name: str = None, nlp_model_name: str = None, pathfinding_model_name: str = None) -> Path:
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
    error_message = result.get("error_message")
    
    stt_metadata = result.get("stt_metadata", {})
    nlp_metadata = result.get("nlp_metadata", {})
    
    # Récupère les noms des modèles
    stt_model = stt_model_name or stt_metadata.get('model', 'N/A')
    nlp_model = nlp_model_name or nlp_metadata.get('model', 'N/A')
    pathfinding_model = pathfinding_model_name or "Non utilisé"
    
    route = result.get("route")
    
    # Formate les valeurs
    confidence_str = f"{confidence:.2f}" if confidence is not None else "N/A"
    processing_time = stt_metadata.get('processing_time')
    processing_time_str = f"{processing_time:.2f}s" if processing_time else "N/A"
    
    # Génère le rapport
    report = f"""# Rapport Pipeline - Traitement Audio

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Fichier audio**: {audio_path}

## 🔧 Configuration

- **Modèle STT**: {stt_model}
- **Modèle NLP**: {nlp_model}
- **Modèle Pathfinding**: {pathfinding_model}

---

## 📝 Transcription (STT)

```
{transcript}
```

### Métadonnées STT
- **Modèle**: {stt_model}
- **Langue détectée**: {stt_metadata.get('detected_language', stt_metadata.get('language', 'N/A'))}
- **Segments**: {stt_metadata.get('segments', 'N/A')}
- **Temps de traitement**: {processing_time_str}

---

## 🎯 Extraction NLP

### Résultats
- **Origine**: {origin if origin else "Non détectée"}
- **Destination**: {destination if destination else "Non détectée"}
- **Demande valide**: {"✅ Oui" if is_valid else "❌ Non"}
- **Confiance**: {confidence_str}
"""
    
    # Ajoute le message d'erreur si présent
    if error_message:
        report += f"""
### ⚠️ Message d'erreur
{error_message}
"""
    
    report += f"""
### Métadonnées NLP
- **Modèle**: {nlp_model}
- **Méthode d'extraction**: {nlp_metadata.get('extraction_method', 'N/A')}
- **Lieux détectés**: {', '.join(nlp_metadata.get('locations_found', [])) if nlp_metadata.get('locations_found') else 'Aucun'}

---
"""
    
    # Section Pathfinding
    if route:
        if route.get('steps'):
            total_time = route.get('total_time', 0)
            hours = int(total_time // 60) if total_time else 0
            minutes = int(total_time % 60) if total_time else 0
            time_str = f"{hours}h{minutes:02d} ({total_time:.0f} min)" if total_time else "N/A"
            
            report += f"""
## 🗺️ Itinéraire (Pathfinding)

### Résultats
- **⏱️ Temps de trajet**: {time_str}
- **📏 Distance totale**: {route['total_distance']:.1f} km
- **🛤️ Nombre d'étapes**: {len(route['steps'])}
"""
            
            # Détails des segments si disponibles
            segments = route.get('metadata', {}).get('segments', [])
            if segments:
                report += """
### 📊 Détails du trajet

| # | Type | Départ | Arrivée | Temps | Distance | Trains/jour |
|---|------|--------|---------|-------|----------|-------------|
"""
                for i, seg in enumerate(segments, 1):
                    train_type = seg.get('type_train', 'Autre')
                    if train_type == 'TGV':
                        type_emoji = '🚄 TGV'
                    elif train_type == 'OUIGO':
                        type_emoji = '🟢 OUIGO'
                    elif train_type == 'Intercités':
                        type_emoji = '🚃 Intercités'
                    elif train_type == 'TER':
                        type_emoji = '🚈 TER'
                    else:
                        type_emoji = f'🚂 {train_type}'
                    
                    temps = seg.get('temps_min', 0)
                    distance = seg.get('distance_km', 0)
                    nb_trains = seg.get('nb_trains_jour', 0)
                    
                    report += f"| {i} | {type_emoji} | {seg['from']} | {seg['to']} | {temps:.0f} min | {distance:.1f} km | {nb_trains} |\n"
                
                # Résumé par type de train
                train_types = {}
                for seg in segments:
                    t = seg.get('type_train', 'Autre')
                    train_types[t] = train_types.get(t, 0) + 1
                
                report += "\n### 🚂 Types de trains utilisés\n"
                for t, count in sorted(train_types.items(), key=lambda x: -x[1]):
                    if t == 'TGV':
                        report += f"- 🚄 **TGV**: {count} segment(s)\n"
                    elif t == 'OUIGO':
                        report += f"- 🟢 **OUIGO**: {count} segment(s)\n"
                    elif t == 'Intercités':
                        report += f"- 🚃 **Intercités**: {count} segment(s)\n"
                    elif t == 'TER':
                        report += f"- 🚈 **TER**: {count} segment(s)\n"
                    else:
                        report += f"- 🚂 **{t}**: {count} segment(s)\n"
            else:
                report += "\n### Étapes du trajet\n"
                for i, step in enumerate(route['steps'], 1):
                    report += f"{i}. {step}\n"
            
            if route.get('metadata', {}).get('path_uic'):
                report += f"""
### 🔧 Détails techniques
- **Mode**: {route['metadata'].get('mode', 'N/A')}
- **UIC départ**: {route['metadata'].get('origin_uic', 'N/A')}
- **UIC arrivée**: {route['metadata'].get('destination_uic', 'N/A')}
- **Nombre de gares**: {route['metadata'].get('num_stations', 'N/A')}
"""
        elif route.get('metadata', {}).get('error'):
            report += f"""
## 🗺️ Itinéraire (Pathfinding)

⚠️ **Erreur**: {route['metadata']['error']}
"""
        else:
            report += """
## 🗺️ Itinéraire (Pathfinding)

❌ **Aucun itinéraire trouvé**
"""
    
    report += """
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
2. **NLP** : Extraction origine/destination depuis le texte"""
    
    if pathfinding_model_name:
        report += """
3. **Pathfinding** : Recherche d'itinéraire entre origine et destination"""
    
    report += """

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

Pour relancer le traitement avec les mêmes modèles :
```bash
python3 -m src.cli.pipeline --audio {audio_path} --stt-model {stt_model} --nlp-model {nlp_model}"""
    
    if pathfinding_model_name:
        report += f" --pathfinding-model {pathfinding_model_name}"
    
    report += """
```
"""
    
    # Sauvegarde
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_path

