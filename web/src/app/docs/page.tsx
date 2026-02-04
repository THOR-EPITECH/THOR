import { Mic, Brain, Route, ArrowRight, Zap } from 'lucide-react';
import Link from 'next/link';

export default function DocsIntroduction() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Introduction</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">
          Documentation THOR
        </h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Bienvenue dans la documentation de THOR (Train Horaires Optimisés Routes). 
          Un système intelligent de recherche d'itinéraires ferroviaires français.
        </p>
      </div>

      {/* Quick intro */}
      <div className="prose prose-invert max-w-none mb-12">
        <p className="text-neutral-300 leading-relaxed">
          THOR est un projet qui combine reconnaissance vocale, traitement du langage naturel 
          et algorithmes de pathfinding pour offrir une expérience de recherche d'itinéraires 
          ferroviaires unique et optimisée.
        </p>
      </div>

      {/* Features grid */}
      <div className="grid gap-4 mb-12">
        <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-blue-500/10">
              <Mic className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h3 className="font-semibold mb-2">Reconnaissance Vocale</h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Utilisez votre voix pour rechercher un itinéraire. Le modèle Whisper d'OpenAI 
                transcrit votre demande avec une précision remarquable en français.
              </p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-purple-500/10">
              <Brain className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h3 className="font-semibold mb-2">Traitement du Langage Naturel</h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                spaCy analyse votre texte pour extraire intelligemment l'origine et la destination 
                de votre voyage, quelle que soit la formulation utilisée.
              </p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-green-500/10">
              <Route className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <h3 className="font-semibold mb-2">Pathfinding Intelligent</h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                L'algorithme de Dijkstra optimisé trouve le meilleur itinéraire en privilégiant 
                les TGV et en utilisant les temps de trajet réels.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-12">
        <div className="text-center p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="text-3xl font-bold text-white mb-1">3000+</div>
          <div className="text-xs text-neutral-500">Gares SNCF</div>
        </div>
        <div className="text-center p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="text-3xl font-bold text-white mb-1">50k+</div>
          <div className="text-xs text-neutral-500">Connexions</div>
        </div>
        <div className="text-center p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="text-3xl font-bold text-white mb-1">&lt;2s</div>
          <div className="text-xs text-neutral-500">Temps de réponse</div>
        </div>
      </div>

      {/* Quick start CTA */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-white/5 to-white/[0.02] border border-white/10">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold mb-1">Prêt à commencer ?</h3>
            <p className="text-sm text-neutral-400">
              Suivez le guide d'installation pour démarrer en quelques minutes.
            </p>
          </div>
          <Link 
            href="/docs/installation"
            className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg text-sm font-medium hover:bg-neutral-200 transition-colors"
          >
            Installation
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Architecture overview */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6">Architecture</h2>
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="flex items-center justify-between gap-4 overflow-x-auto pb-2">
            <div className="flex flex-col items-center min-w-[100px]">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-2">
                <Mic className="w-6 h-6 text-blue-400" />
              </div>
              <span className="text-xs text-neutral-400">Audio</span>
            </div>
            
            <ArrowRight className="w-4 h-4 text-neutral-600 flex-shrink-0" />
            
            <div className="flex flex-col items-center min-w-[100px]">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-2">
                <Zap className="w-6 h-6 text-blue-400" />
              </div>
              <span className="text-xs text-neutral-400">Whisper STT</span>
            </div>
            
            <ArrowRight className="w-4 h-4 text-neutral-600 flex-shrink-0" />
            
            <div className="flex flex-col items-center min-w-[100px]">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mb-2">
                <Brain className="w-6 h-6 text-purple-400" />
              </div>
              <span className="text-xs text-neutral-400">spaCy NLP</span>
            </div>
            
            <ArrowRight className="w-4 h-4 text-neutral-600 flex-shrink-0" />
            
            <div className="flex flex-col items-center min-w-[100px]">
              <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center mb-2">
                <Route className="w-6 h-6 text-green-400" />
              </div>
              <span className="text-xs text-neutral-400">Dijkstra</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
