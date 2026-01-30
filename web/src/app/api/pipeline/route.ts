import { NextRequest, NextResponse } from 'next/server';

// URL du backend Python Flask
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { audio, format } = body;

    if (!audio) {
      return NextResponse.json(
        { error: 'Le champ "audio" (base64) est requis' },
        { status: 400 }
      );
    }

    // Proxy vers le backend Flask
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/pipeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        audio,
        format: format || 'wav'
      }),
    });

    // Vérifier le Content-Type
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const text = await response.text();
      console.error('Réponse non-JSON du backend:', text.substring(0, 200));
      return NextResponse.json(
        { error: 'Réponse invalide du backend', details: text.substring(0, 200) },
        { status: 500 }
      );
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Erreur serveur' }));
      return NextResponse.json(
        { error: error.error || 'Erreur lors du traitement audio' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Erreur API pipeline:', error);
    
    // Vérifier si c'est une erreur de connexion au backend
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
      { error: 'Erreur lors du traitement de la requête audio' },
      { status: 500 }
    );
  }
}
