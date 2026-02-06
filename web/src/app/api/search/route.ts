/**
 * API Route pour la recherche d'itinéraire ferroviaire.
 * 
 * Cette route sert de proxy entre le frontend Next.js et le backend Python Flask.
 * Elle gère deux types de requêtes :
 * 1. Recherche par texte libre (analyse NLP + pathfinding)
 * 2. Recherche directe par origine/destination (pathfinding uniquement)
 * 
 * @module api/search
 */

import { NextRequest, NextResponse } from 'next/server';

/** URL du backend Python Flask */
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

/**
 * Gère les requêtes POST pour la recherche d'itinéraire.
 * 
 * @param {NextRequest} request - Requête Next.js contenant { text } ou { origin, destination }
 * @returns {Promise<NextResponse>} Réponse JSON avec l'itinéraire ou un message d'erreur
 * 
 * @example
 * // Recherche par texte
 * POST /api/search
 * { "text": "Je veux aller de Paris à Lyon" }
 * 
 * @example
 * // Recherche directe
 * POST /api/search
 * { "origin": "Paris", "destination": "Lyon" }
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { text, origin, destination } = body;

    if (text) {
      const response = await fetch(`${PYTHON_BACKEND_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Erreur serveur' }));
        return NextResponse.json(
          { error: error.error || 'Erreur lors de la recherche' },
          { status: response.status }
        );
      }

      const data = await response.json();
      return NextResponse.json(data);
    }

    if (origin && destination) {
      const response = await fetch(`${PYTHON_BACKEND_URL}/api/route`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origin, destination }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Erreur serveur' }));
        return NextResponse.json(
          { error: error.error || 'Erreur lors de la recherche d\'itinéraire' },
          { status: response.status }
        );
      }

      const data = await response.json();
      
      return NextResponse.json({
        transcript: `Trajet de ${origin} à ${destination}`,
        origin,
        destination,
        is_valid: true,
        confidence: 1.0,
        route: data.route
      });
    }

    return NextResponse.json(
      { error: 'Le champ "text" ou les champs "origin" et "destination" sont requis' },
      { status: 400 }
    );

  } catch (error) {
    console.error('Erreur API:', error);
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return NextResponse.json(
        { 
          error: 'Backend Python non disponible. Lancez: python3 api/app.py --preload',
          details: 'Impossible de se connecter à http://localhost:8000'
        },
        { status: 503 }
      );
    }
    
    return NextResponse.json(
      { error: 'Erreur lors du traitement de la requête' },
      { status: 500 }
    );
  }
}

/**
 * Endpoint GET pour vérifier la disponibilité du backend Python.
 * 
 * @returns {Promise<NextResponse>} Statut de santé du backend
 * 
 * @example
 * GET /api/search
 * Response: { "status": "ok", "backend": { "version": "1.0" } }
 */
export async function GET() {
  try {
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/health`);
    
    if (response.ok) {
      const data = await response.json();
      return NextResponse.json({
        status: 'ok',
        backend: data
      });
    }
    
    return NextResponse.json(
      { status: 'error', message: 'Backend non disponible' },
      { status: 503 }
    );
  } catch {
    return NextResponse.json(
      { 
        status: 'error', 
        message: 'Backend Python non disponible',
        hint: 'Lancez: python3 api/app.py --preload'
      },
      { status: 503 }
    );
  }
}
