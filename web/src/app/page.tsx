'use client';

import { useState } from 'react';
import { PipelineResult } from '@/types';
import SearchInput from '@/components/SearchInput';
import RouteDetails from '@/components/RouteDetails';
import RouteMap from '@/components/RouteMap';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Train, 
  Zap, 
  MessageSquare, 
  AlertCircle,
  CheckCircle2,
  Github,
  Mic,
  TrainFront,
  Map
} from 'lucide-react';

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
          throw new Error('Backend Python non disponible. Lancez: python3 api/app.py --preload');
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

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-slate-800/50 backdrop-blur-xl bg-slate-950/50 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                  <Train className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-slate-950" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                  THOR
                </h1>
                <p className="text-xs text-slate-500">Train Horaires Optimisés Routes</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="border-emerald-500/30 text-emerald-400 bg-emerald-500/10">
                <Zap className="w-3 h-3 mr-1" />
                TGV Prioritaire
              </Badge>
              <a 
                href="https://github.com/THOR-EPITECH/THOR" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-white transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 py-8">
        {/* Hero section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
              Trouvez votre trajet
            </span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Parlez ou écrivez votre destination. Notre IA optimise votre itinéraire 
            en privilégiant les TGV pour des trajets plus rapides.
          </p>
        </div>

        {/* Search input */}
        <div className="max-w-3xl mx-auto mb-12">
          <SearchInput onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Results */}
        {isLoading && (
          <div className="max-w-5xl mx-auto">
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="bg-slate-900/80 border-slate-700/50">
                <CardContent className="p-6">
                  <Skeleton className="h-8 w-48 mb-4 bg-slate-800" />
                  <Skeleton className="h-4 w-full mb-2 bg-slate-800" />
                  <Skeleton className="h-4 w-3/4 mb-4 bg-slate-800" />
                  <Skeleton className="h-24 w-full bg-slate-800" />
                </CardContent>
              </Card>
              <Skeleton className="h-[400px] bg-slate-800 rounded-xl" />
            </div>
          </div>
        )}

        {error && (
          <Card className="max-w-2xl mx-auto bg-rose-500/10 border-rose-500/30">
            <CardContent className="p-6 flex items-center gap-4">
              <AlertCircle className="w-8 h-8 text-rose-400 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-rose-400">Erreur</h3>
                <p className="text-slate-300">{error}</p>
              </div>
            </CardContent>
          </Card>
        )}

        {result && (
          <div className="max-w-5xl mx-auto space-y-8">
            {/* Transcription */}
            <Card className="bg-slate-900/80 border-slate-700/50">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="p-2 rounded-lg bg-purple-500/10">
                    <MessageSquare className="w-5 h-5 text-purple-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm text-slate-400">Votre demande</span>
                      {result.is_valid ? (
                        <Badge className="bg-emerald-500/20 text-emerald-400 border-0">
                          <CheckCircle2 className="w-3 h-3 mr-1" />
                          Validée
                        </Badge>
                      ) : (
                        <Badge className="bg-amber-500/20 text-amber-400 border-0">
                          <AlertCircle className="w-3 h-3 mr-1" />
                          Incomplète
                        </Badge>
                      )}
                    </div>
                    <p className="text-lg text-white">&ldquo;{result.transcript}&rdquo;</p>
                    {result.origin && result.destination && (
                      <p className="text-sm text-slate-400 mt-2">
                        Détecté: <span className="text-cyan-400">{result.origin}</span> → <span className="text-cyan-400">{result.destination}</span>
                      </p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Route et carte */}
            {result.route && result.route.steps && result.route.steps.length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                <RouteDetails route={result.route} />
                <div className="space-y-4">
                  <RouteMap 
                    segments={result.route.metadata?.segments || []} 
                    steps={result.route.steps} 
                  />
                </div>
              </div>
            ) : result.error_message ? (
              <Card className="bg-amber-500/10 border-amber-500/30">
                <CardContent className="p-6 flex items-center gap-4">
                  <AlertCircle className="w-8 h-8 text-amber-400 flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold text-amber-400">Information</h3>
                    <p className="text-slate-300">{result.error_message}</p>
                  </div>
                </CardContent>
              </Card>
            ) : null}
          </div>
        )}

        {/* Empty state */}
        {!isLoading && !error && !result && (
          <div className="max-w-3xl mx-auto text-center">
            <div className="py-16">
              <div className="w-24 h-24 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-slate-700/50 flex items-center justify-center">
                <Train className="w-12 h-12 text-cyan-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">
                Prêt à voyager ?
              </h3>
              <p className="text-slate-400">
                Dites-nous votre destination par la voix ou écrivez-la ci-dessus.
              </p>
            </div>
            
            {/* Features */}
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div className="p-6 rounded-xl bg-slate-900/50 border border-slate-800/50">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-rose-500/20 to-pink-500/20 flex items-center justify-center mb-3 mx-auto">
                  <Mic className="w-6 h-6 text-rose-400" />
                </div>
                <h4 className="font-semibold text-white mb-1">Commande vocale</h4>
                <p className="text-sm text-slate-400">Parlez naturellement</p>
              </div>
              <div className="p-6 rounded-xl bg-slate-900/50 border border-slate-800/50">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 flex items-center justify-center mb-3 mx-auto">
                  <TrainFront className="w-6 h-6 text-cyan-400" />
                </div>
                <h4 className="font-semibold text-white mb-1">TGV Prioritaire</h4>
                <p className="text-sm text-slate-400">Trajets optimisés</p>
              </div>
              <div className="p-6 rounded-xl bg-slate-900/50 border border-slate-800/50">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center mb-3 mx-auto">
                  <Map className="w-6 h-6 text-emerald-400" />
                </div>
                <h4 className="font-semibold text-white mb-1">Carte interactive</h4>
                <p className="text-sm text-slate-400">Visualisez votre trajet</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/50 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-500">
            <p>© 2026 THOR - Projet EPITECH</p>
            <p>Propulsé par l&apos;IA • Données SNCF GTFS</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
