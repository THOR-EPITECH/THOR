"""
API Flask pour THOR - Pipeline STT → NLP → Pathfinding.

Cette API expose les fonctionnalités du projet THOR via des endpoints REST.
"""

import os
import sys
import json
import tempfile
import base64
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.stt.models.whisper import WhisperModel
from src.nlp.models.spacy_fr import SpacyFRModel
from src.pathfinding.models.dijkstra import DijkstraPathfindingModel
from src.common.logging import setup_logging

logger = setup_logging(module="api")

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"])

_models = {
    'stt': None,
    'nlp': None,
    'pathfinding': None
}


def get_stt_model():
    """Charge le modèle STT (Whisper) de manière lazy."""
    if _models['stt'] is None:
        logger.info("Chargement du modèle STT (Whisper)...")
        _models['stt'] = WhisperModel({
            'model_size': 'small',
            'language': 'fr',
            'device': 'cpu'
        })
        _models['stt'].initialize()
    return _models['stt']


def get_nlp_model():
    """Charge le modèle NLP (spaCy) de manière lazy."""
    if _models['nlp'] is None:
        logger.info("Chargement du modèle NLP (spaCy)...")
        _models['nlp'] = SpacyFRModel({
            'model_name': 'fr_core_news_md'
        })
        _models['nlp'].initialize()
    return _models['nlp']


def get_pathfinding_model():
    """Charge le modèle Pathfinding (Dijkstra) de manière lazy."""
    if _models['pathfinding'] is None:
        logger.info("Chargement du modèle Pathfinding (Dijkstra)...")
        _models['pathfinding'] = DijkstraPathfindingModel({
            'path_gares': 'data/train_station/dataset_gares.json',
            'path_liaisons_enhanced': 'data/train_station/dataset_liaisons_enhanced.json',
            'mode': 'time'
        })
        _models['pathfinding'].initialize()
    return _models['pathfinding']


_shapes_cache = None

def get_shapes_data():
    """Charge les géométries des voies ferrées."""
    global _shapes_cache
    if _shapes_cache is None:
        shapes_path = Path('data/train_station/dataset_liaisons_with_shapes.json')
        if shapes_path.exists():
            logger.info("Chargement des géométries de voies...")
            with open(shapes_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            _shapes_cache = {}
            for l in data.get('liaisons', []):
                key = (str(l.get('depart')), str(l.get('arrivee')))
                if l.get('geometry'):
                    _shapes_cache[key] = l['geometry']
            logger.info(f"  → {len(_shapes_cache)} géométries chargées")
        else:
            _shapes_cache = {}
    return _shapes_cache


def route_to_dict(route):
    """Convertit un objet Route en dictionnaire JSON-serializable."""
    result = {
        'origin': route.origin,
        'destination': route.destination,
        'steps': route.steps,
        'total_distance': route.total_distance,
        'total_time': route.total_time,
        'metadata': route.metadata
    }
    
    shapes = get_shapes_data()
    if shapes and route.metadata.get('segments'):
        path_uic = route.metadata.get('path_uic', [])
        for i, segment in enumerate(route.metadata['segments']):
            if i < len(path_uic) - 1:
                uic_from = path_uic[i]
                uic_to = path_uic[i + 1]
                
                geometry = shapes.get((uic_from, uic_to))
                
                if geometry:
                    segment['geometry'] = geometry
                else:
                    reverse_geometry = shapes.get((uic_to, uic_from))
                    if reverse_geometry:
                        segment['geometry'] = {
                            'type': 'LineString',
                            'coordinates': list(reversed(reverse_geometry['coordinates']))
                        }
    
    return result


@app.route('/', methods=['GET'])
def home():
    """Page d'accueil avec la liste des endpoints."""
    return jsonify({
        'name': 'THOR API',
        'version': '1.0.0',
        'description': 'Travel Order Resolver - API pour extraire des commandes de voyage',
        'endpoints': {
            'GET /': 'Cette page',
            'GET /api/health': 'Health check',
            'POST /api/search': 'Analyser un texte et trouver un itineraire',
            'POST /api/route': 'Trouver un itineraire entre deux villes',
            'POST /api/transcribe': 'Transcrire un audio en texte',
            'POST /api/pipeline': 'Pipeline complet (audio -> route)',
            'GET /api/stations': 'Liste des gares disponibles',
            'POST /api/preload': 'Precharger les modeles'
        },
        'docs': 'https://github.com/THOR-EPITECH/THOR'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifie l'etat de l'API."""
    return jsonify({
        'status': 'ok',
        'message': 'THOR API is running',
        'models': {
            'stt': 'loaded' if _models['stt'] else 'not_loaded',
            'nlp': 'loaded' if _models['nlp'] else 'not_loaded',
            'pathfinding': 'loaded' if _models['pathfinding'] else 'not_loaded'
        }
    })


@app.route('/api/search', methods=['POST'])
def search():
    """
    Analyse un texte pour extraire origine/destination et trouver l'itinéraire.
    
    Body JSON:
        - text: Le texte à analyser (ex: "Je veux aller de Paris à Bordeaux")
    
    Returns:
        - transcript: Le texte d'entrée
        - origin: Ville d'origine détectée
        - destination: Ville de destination détectée
        - is_valid: Si la demande est valide
        - confidence: Score de confiance
        - route: Détails de l'itinéraire
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Le champ "text" est requis'}), 400
        
        nlp_model = get_nlp_model()
        nlp_result = nlp_model.extract(text)
        
        origin = nlp_result.origin
        destination = nlp_result.destination
        
        result = {
            'transcript': text,
            'origin': origin,
            'destination': destination,
            'is_valid': nlp_result.is_valid,
            'confidence': nlp_result.confidence,
            'nlp_metadata': nlp_result.metadata
        }
        
        if origin and destination:
            pathfinding_model = get_pathfinding_model()
            route = pathfinding_model.find_route(origin, destination)
            
            if route.steps and len(route.steps) > 1:
                result['route'] = route_to_dict(route)
            elif route.metadata.get('error'):
                result['error_message'] = route.metadata['error']
        else:
            if not origin and not destination:
                result['error_message'] = "Origine et destination non détectées. Essayez: 'Je veux aller de Paris à Lyon'"
            elif not origin:
                result['error_message'] = "Origine non détectée"
            else:
                result['error_message'] = "Destination non détectée"
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erreur dans /api/search: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/route', methods=['POST'])
def get_route():
    """
    Trouve un itinéraire entre deux villes.
    
    Body JSON:
        - origin: Ville de départ
        - destination: Ville d'arrivée
    
    Returns:
        - route: Détails de l'itinéraire avec segments
    """
    try:
        data = request.get_json()
        origin = data.get('origin', '')
        destination = data.get('destination', '')
        
        if not origin or not destination:
            return jsonify({'error': 'Les champs "origin" et "destination" sont requis'}), 400
        
        pathfinding_model = get_pathfinding_model()
        route = pathfinding_model.find_route(origin, destination)
        
        if route.steps and len(route.steps) > 1:
            return jsonify({
                'success': True,
                'route': route_to_dict(route)
            })
        elif route.metadata.get('error'):
            return jsonify({
                'success': False,
                'error': route.metadata['error']
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Aucun itinéraire trouvé'
            })
            
    except Exception as e:
        logger.error(f"Erreur dans /api/route: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Transcrit un fichier audio en texte.
    
    Body JSON:
        - audio: Audio encodé en base64
        - format: Format audio (wav, mp3, etc.) - optionnel, défaut: wav
    
    Returns:
        - transcript: Texte transcrit
        - metadata: Métadonnées STT
    """
    try:
        data = request.get_json()
        audio_base64 = data.get('audio', '')
        audio_format = data.get('format', 'wav')
        
        if not audio_base64:
            return jsonify({'error': 'Le champ "audio" (base64) est requis'}), 400
        
        audio_bytes = base64.b64decode(audio_base64)
        
        with tempfile.NamedTemporaryFile(suffix=f'.{audio_format}', delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            stt_model = get_stt_model()
            stt_result = stt_model.transcribe(tmp_path)
            
            return jsonify({
                'transcript': stt_result.text,
                'metadata': stt_result.metadata
            })
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        logger.error(f"Erreur dans /api/transcribe: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/pipeline', methods=['POST'])
def pipeline():
    """
    Pipeline complète: Audio → STT → NLP → Pathfinding.
    
    Body JSON:
        - audio: Audio encodé en base64
        - format: Format audio (optionnel, défaut: wav)
    
    Returns:
        - transcript: Texte transcrit
        - origin: Ville d'origine
        - destination: Ville de destination
        - is_valid: Si la demande est valide
        - route: Détails de l'itinéraire
    """
    try:
        data = request.get_json()
        audio_base64 = data.get('audio', '')
        audio_format = data.get('format', 'wav')
        
        if not audio_base64:
            return jsonify({'error': 'Le champ "audio" (base64) est requis'}), 400
        
        audio_bytes = base64.b64decode(audio_base64)
        
        with tempfile.NamedTemporaryFile(suffix=f'.{audio_format}', delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            logger.info(f"Transcription audio: format={audio_format}, taille={len(audio_bytes)} bytes")
            try:
                stt_model = get_stt_model()
                stt_result = stt_model.transcribe(tmp_path)
                transcript = stt_result.text
                logger.info(f"Transcription réussie: '{transcript}'")
            except Exception as e:
                logger.error(f"Erreur lors de la transcription: {e}")
                return jsonify({
                    'error': f'Erreur lors de la transcription audio: {str(e)}',
                    'details': 'Vérifiez que le format audio est supporté (wav, mp3, webm)'
                }), 500
            
            nlp_model = get_nlp_model()
            nlp_result = nlp_model.extract(transcript)
            
            origin = nlp_result.origin
            destination = nlp_result.destination
            
            result = {
                'audio_path': 'uploaded_audio',
                'transcript': transcript,
                'origin': origin,
                'destination': destination,
                'is_valid': nlp_result.is_valid,
                'confidence': nlp_result.confidence,
                'stt_metadata': stt_result.metadata,
                'nlp_metadata': nlp_result.metadata
            }
            
            if origin and destination:
                pathfinding_model = get_pathfinding_model()
                route = pathfinding_model.find_route(origin, destination)
                
                if route.steps and len(route.steps) > 1:
                    result['route'] = route_to_dict(route)
                elif route.metadata.get('error'):
                    result['error_message'] = route.metadata['error']
            else:
                if not origin and not destination:
                    result['error_message'] = "Origine et destination non détectées"
                elif not origin:
                    result['error_message'] = "Origine non détectée"
                else:
                    result['error_message'] = "Destination non détectée"
            
            return jsonify(result)
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            
    except Exception as e:
        logger.error(f"Erreur dans /api/pipeline: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stations', methods=['GET'])
def list_stations():
    """
    Liste les gares disponibles.
    
    Query params:
        - q: Recherche par nom (optionnel)
        - limit: Nombre max de résultats (défaut: 50)
    
    Returns:
        - stations: Liste des gares avec nom et UIC
    """
    try:
        query = request.args.get('q', '').lower()
        limit = int(request.args.get('limit', 50))
        
        pathfinding_model = get_pathfinding_model()
        
        stations = []
        for uic, station in pathfinding_model._stations_by_uic.items():
            name = station.get('nom_gare', '')
            if not query or query in name.lower():
                if uic in pathfinding_model._graph:
                    stations.append({
                        'name': name,
                        'uic': uic,
                        'city': station.get('ville', {}).get('nom_commune', ''),
                        'lat': station.get('position_geographique', {}).get('lat'),
                        'lon': station.get('position_geographique', {}).get('lon')
                    })
        
        stations.sort(key=lambda s: -len(pathfinding_model._graph.get(s['uic'], [])))
        
        return jsonify({
            'count': len(stations[:limit]),
            'total': len(stations),
            'stations': stations[:limit]
        })
        
    except Exception as e:
        logger.error(f"Erreur dans /api/stations: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/preload', methods=['POST'])
def preload_models():
    """Précharge tous les modèles pour accélérer les requêtes suivantes."""
    try:
        models_loaded = []
        
        if request.json.get('stt', True):
            get_stt_model()
            models_loaded.append('stt')
            
        if request.json.get('nlp', True):
            get_nlp_model()
            models_loaded.append('nlp')
            
        if request.json.get('pathfinding', True):
            get_pathfinding_model()
            models_loaded.append('pathfinding')
        
        return jsonify({
            'success': True,
            'models_loaded': models_loaded
        })
        
    except Exception as e:
        logger.error(f"Erreur dans /api/preload: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='THOR API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--preload', action='store_true', help='Preload all models at startup')
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                    🚄 THOR API Server                          ║
╠═══════════════════════════════════════════════════════════════╣
║  Endpoints:                                                    ║
║    GET  /api/health      - Health check                       ║
║    POST /api/search      - Analyze text → find route          ║
║    POST /api/route       - Find route between cities          ║
║    POST /api/transcribe  - Transcribe audio                   ║
║    POST /api/pipeline    - Full pipeline (audio → route)      ║
║    GET  /api/stations    - List available stations            ║
║    POST /api/preload     - Preload models                     ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    if args.preload:
        print("🔄 Préchargement des modèles...")
        get_nlp_model()
        get_pathfinding_model()
        print("✅ Modèles préchargés (STT chargé à la demande)")
    
    print(f"\n🌐 Server running on http://{args.host}:{args.port}\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
