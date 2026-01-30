'use client';

import { useState } from 'react';
import { PipelineResult } from '@/types';
import SearchInput from '@/components/SearchInput';
import RouteDetails from '@/components/RouteDetails';
import RouteMap from '@/components/RouteMap';
import { ArrowRight, Github, Loader2 } from 'lucide-react';

export default function Home() {
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (text: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 503) {
          throw new Error('Backend non disponible');
        }
        throw new Error(data.error || 'Erreur lors de la recherche');
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setResult(data as PipelineResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceResult = (data: PipelineResult) => {
    setError(null);
    setResult(data);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-lg font-semibold tracking-tight">THOR</span>
            <span className="text-xs text-neutral-500 hidden sm:block">Train Horaires Optimisés Routes</span>
          </div>
          
          <a 
            href="https://github.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="p-2 text-neutral-500 hover:text-white transition-colors"
          >
            <Github className="w-5 h-5" />
          </a>
        </div>
      </header>

      {/* Main */}
      <main className="pt-32 pb-24 px-6">
        <div className="max-w-2xl mx-auto">
          {/* Hero */}
          <div className="text-center mb-12">
            <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight mb-4">
              Trouvez votre trajet
            </h1>
            <p className="text-neutral-400 text-lg">
              Recherchez un itinéraire entre deux gares françaises
            </p>
          </div>

          {/* Search */}
          <div className="mb-16">
            <SearchInput 
              onSearch={handleSearch} 
              onVoiceResult={handleVoiceResult}
              isLoading={isLoading} 
            />
          </div>

          {/* Loading */}
          {isLoading && (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-6 h-6 animate-spin text-neutral-500" />
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="text-center py-8 animate-fade-in">
              <p className="text-red-400 mb-2">{error}</p>
              <p className="text-sm text-neutral-500">Vérifiez votre saisie et réessayez</p>
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="space-y-8 animate-fade-in">
              {/* Query confirmation */}
              <div className="text-center pb-6 border-b border-white/5">
                <p className="text-sm text-neutral-500 mb-2">Votre recherche</p>
                <p className="text-lg">"{result.transcript}"</p>
                {result.origin && result.destination && (
                  <div className="flex items-center justify-center gap-3 mt-3 text-neutral-400">
                    <span>{result.origin}</span>
                    <ArrowRight className="w-4 h-4" />
                    <span>{result.destination}</span>
                  </div>
                )}
              </div>

              {/* Route */}
              {result.route && result.route.steps && result.route.steps.length > 0 ? (
                <div className="space-y-8 stagger-children">
                  <RouteDetails route={result.route} />
                  <RouteMap segments={result.route.metadata?.segments || []} />
                </div>
              ) : result.error_message ? (
                <div className="text-center py-8">
                  <p className="text-neutral-400">{result.error_message}</p>
                </div>
              ) : null}
            </div>
          )}

          {/* Empty state */}
          {!isLoading && !error && !result && (
            <div className="text-center py-16 text-neutral-500">
              <p className="mb-8">Exemples de recherches</p>
              <div className="flex flex-wrap gap-3 justify-center">
                {['Paris → Bordeaux', 'Lyon → Marseille', 'Bordeaux → Toulouse'].map((example) => (
                  <button
                    key={example}
                    onClick={() => handleSearch(`Je veux aller de ${example.replace(' → ', ' à ')}`)}
                    className="px-4 py-2 text-sm border border-white/10 rounded-full hover:border-white/30 hover:text-white transition-all"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 left-0 right-0 border-t border-white/5 bg-[#0a0a0a]/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-12 flex items-center justify-between text-xs text-neutral-500">
          <span>THOR — Projet EPITECH 2026</span>
          <span>Données SNCF</span>
        </div>
      </footer>
    </div>
  );
}
