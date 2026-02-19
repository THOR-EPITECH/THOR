import { ArrowRight, Route, Zap, Timer, Map, Train, Plane, Settings, CheckCircle2, AlertCircle, Target } from 'lucide-react';

function CodeBlock({ children, title }: { children: string; title?: string }) {
  return (
    <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0d0d0d]">
      {title && (
        <div className="px-4 py-2 bg-white/5 border-b border-white/5 text-xs text-neutral-400">
          {title}
        </div>
      )}
      <pre className="p-4 overflow-x-auto">
        <code className="text-sm text-neutral-300">{children}</code>
      </pre>
    </div>
  );
}

export default function DocsPathfinding() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Pipeline</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Pathfinding</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Pathfinding (Dijkstra)</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Algorithme de recherche du plus court chemin optimisé pour le réseau ferroviaire français, 
          avec système de pénalités intelligentes favorisant les trains rapides (TGV) et temps de trajet réels.
        </p>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Concepts de base</h2>
        
        <div className="p-6 rounded-xl bg-blue-500/5 border border-blue-500/20 mb-6">
          <h3 className="font-semibold text-blue-400 mb-4">Qu'est-ce qu'un graphe ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Un <strong className="text-white">graphe</strong> est une structure mathématique composée de deux éléments :
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-4 h-4 rounded-full bg-blue-500" />
                <span className="font-medium">Nœuds (ou sommets)</span>
              </div>
              <p className="text-xs text-neutral-400">
                Les <strong className="text-blue-300">points</strong> du graphe. Dans THOR, chaque nœud représente une <strong className="text-blue-300">gare</strong>.
              </p>
              <div className="mt-2 text-xs text-neutral-500">
                Ex: Paris Gare de Lyon, Lyon Part Dieu, Marseille Saint-Charles...
              </div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-0.5 bg-green-500" />
                <span className="font-medium">Arêtes (ou liaisons)</span>
              </div>
              <p className="text-xs text-neutral-400">
                Les <strong className="text-green-300">connexions</strong> entre les nœuds. Dans THOR, chaque arête représente une <strong className="text-green-300">liaison ferroviaire</strong> directe.
              </p>
              <div className="mt-2 text-xs text-neutral-500">
                Ex: Paris ↔ Lyon, Lyon ↔ Marseille...
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-purple-500/5 border border-purple-500/20 mb-6">
          <h3 className="font-semibold text-purple-400 mb-4">Qu'est-ce qu'un graphe pondéré ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Un graphe <strong className="text-white">pondéré</strong> est un graphe où chaque arête possède un <strong className="text-purple-300">poids</strong> (ou coût).
            Ce poids représente le "coût" pour parcourir cette liaison.
          </p>
          <div className="p-4 rounded-lg bg-white/5 mb-4">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-blue-500" />
                <span>Paris</span>
              </div>
              <div className="flex-1 mx-4 relative">
                <div className="h-0.5 bg-green-500" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 px-2 py-0.5 rounded bg-green-500/20 text-green-400 text-xs font-mono">
                  117 min
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span>Lyon</span>
                <div className="w-3 h-3 rounded-full bg-blue-500" />
              </div>
            </div>
          </div>
          <p className="text-xs text-neutral-500">
            Dans THOR, le poids = <strong className="text-purple-300">temps de trajet en minutes</strong>. 
            L'algorithme cherche donc le chemin avec le <strong>temps total le plus court</strong>.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-4">Visualisation du graphe THOR</h3>
          <div className="grid md:grid-cols-3 gap-4 text-center text-sm">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-3xl font-bold text-blue-400 mb-1">2,782</div>
              <div className="text-neutral-500">Nœuds (gares)</div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-3xl font-bold text-green-400 mb-1">7,852</div>
              <div className="text-neutral-500">Arêtes (liaisons)</div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-3xl font-bold text-purple-400 mb-1">Temps</div>
              <div className="text-neutral-500">Poids (minutes)</div>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">L'algorithme de Dijkstra</h2>
        <div className="prose prose-invert max-w-none mb-6">
          <p className="text-neutral-400">
            L'algorithme de Dijkstra est un algorithme de recherche du <strong className="text-white">plus court chemin</strong> dans un graphe pondéré. 
            Il a été inventé par Edsger Dijkstra en 1956.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Comment ça fonctionne ?</h3>
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-sm font-mono text-green-400 shrink-0">1</div>
              <div>
                <div className="font-medium">Initialisation</div>
                <div className="text-sm text-neutral-400">
                  On assigne une distance <code className="text-green-400">0</code> au nœud de départ, et <code className="text-red-400">∞</code> (infini) à tous les autres.
                </div>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-sm font-mono text-green-400 shrink-0">2</div>
              <div>
                <div className="font-medium">Exploration</div>
                <div className="text-sm text-neutral-400">
                  On visite le nœud non-visité ayant la <strong className="text-white">plus petite distance</strong>. 
                  On met à jour les distances de ses voisins si on trouve un chemin plus court.
                </div>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-sm font-mono text-green-400 shrink-0">3</div>
              <div>
                <div className="font-medium">Répétition</div>
                <div className="text-sm text-neutral-400">
                  On répète l'étape 2 jusqu'à atteindre la destination ou avoir visité tous les nœuds accessibles.
                </div>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-sm font-mono text-green-400 shrink-0">4</div>
              <div>
                <div className="font-medium">Résultat</div>
                <div className="text-sm text-neutral-400">
                  On remonte le chemin depuis la destination vers l'origine pour obtenir l'itinéraire optimal.
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20 mb-6">
          <h3 className="font-semibold text-green-400 mb-4">Complexité algorithmique</h3>
          <p className="text-sm text-neutral-400 mb-4">
            La <strong className="text-white">complexité</strong> mesure les ressources nécessaires (temps, mémoire) en fonction de la taille du problème.
          </p>
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-1">Complexité temporelle</div>
              <code className="text-lg text-green-400">O((V + E) × log V)</code>
              <div className="mt-2 text-xs text-neutral-400">
                Avec <strong className="text-blue-300">V</strong> = nombre de nœuds (gares) et <strong className="text-green-300">E</strong> = nombre d'arêtes (liaisons)
              </div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-1">Complexité spatiale</div>
              <code className="text-lg text-green-400">O(V)</code>
              <div className="mt-2 text-xs text-neutral-400">
                On stocke la distance minimale connue pour chaque nœud
              </div>
            </div>
          </div>
          <div className="p-3 rounded-lg bg-green-500/10 text-xs">
            <strong className="text-green-300">En pratique pour THOR :</strong>
            <span className="text-neutral-400"> Avec 2,782 gares et 7,852 liaisons, le calcul prend environ <strong className="text-white">5ms</strong>.</span>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Exemple détaillé : Paris → Marseille</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Suivons l'algorithme de Dijkstra pas à pas pour trouver le trajet Paris → Marseille.
          </p>
          
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400">0</div>
                <span className="font-medium text-blue-400">Initialisation</span>
              </div>
              <div className="grid grid-cols-5 gap-2 text-xs text-center">
                <div className="p-2 rounded bg-green-500/20 border border-green-500/30">
                  <div className="font-medium text-green-400">Paris</div>
                  <div className="text-green-300 font-mono">0</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Lyon</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Marseille</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Bordeaux</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Lille</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                On commence avec Paris à distance 0, tous les autres à l'infini.
              </div>
            </div>

            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400">1</div>
                <span className="font-medium text-blue-400">Visite de Paris</span>
                <span className="text-xs text-neutral-500 ml-auto">Nœud avec plus petite distance = Paris (0)</span>
              </div>
              <div className="grid grid-cols-5 gap-2 text-xs text-center">
                <div className="p-2 rounded bg-neutral-500/20 border border-neutral-500/30">
                  <div className="font-medium text-neutral-400">Paris</div>
                  <div className="text-neutral-300 font-mono">0 ✓</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20 border border-yellow-500/30">
                  <div className="font-medium text-yellow-400">Lyon</div>
                  <div className="text-yellow-300 font-mono">117</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Marseille</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20 border border-yellow-500/30">
                  <div className="font-medium text-yellow-400">Bordeaux</div>
                  <div className="text-yellow-300 font-mono">130</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20 border border-yellow-500/30">
                  <div className="font-medium text-yellow-400">Lille</div>
                  <div className="text-yellow-300 font-mono">62</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                On met à jour les voisins de Paris : Lyon (0+117=117), Bordeaux (0+130=130), Lille (0+62=62)
              </div>
            </div>

            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400">2</div>
                <span className="font-medium text-blue-400">Visite de Lille</span>
                <span className="text-xs text-neutral-500 ml-auto">Nœud avec plus petite distance = Lille (62)</span>
              </div>
              <div className="grid grid-cols-5 gap-2 text-xs text-center">
                <div className="p-2 rounded bg-neutral-500/20">
                  <div className="font-medium text-neutral-400">Paris</div>
                  <div className="text-neutral-300 font-mono">0 ✓</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20 border border-yellow-500/30">
                  <div className="font-medium text-yellow-400">Lyon</div>
                  <div className="text-yellow-300 font-mono">117</div>
                </div>
                <div className="p-2 rounded bg-white/5">
                  <div className="font-medium text-neutral-400">Marseille</div>
                  <div className="text-red-400 font-mono">∞</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20 border border-yellow-500/30">
                  <div className="font-medium text-yellow-400">Bordeaux</div>
                  <div className="text-yellow-300 font-mono">130</div>
                </div>
                <div className="p-2 rounded bg-neutral-500/20 border border-neutral-500/30">
                  <div className="font-medium text-neutral-400">Lille</div>
                  <div className="text-neutral-300 font-mono">62 ✓</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                Lille n'améliore aucun chemin vers nos destinations (pas de TGV direct vers Lyon/Marseille).
              </div>
            </div>

            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400">3</div>
                <span className="font-medium text-blue-400">Visite de Lyon</span>
                <span className="text-xs text-neutral-500 ml-auto">Nœud avec plus petite distance = Lyon (117)</span>
              </div>
              <div className="grid grid-cols-5 gap-2 text-xs text-center">
                <div className="p-2 rounded bg-neutral-500/20">
                  <div className="font-medium text-neutral-400">Paris</div>
                  <div className="text-neutral-300 font-mono">0 ✓</div>
                </div>
                <div className="p-2 rounded bg-neutral-500/20 border border-neutral-500/30">
                  <div className="font-medium text-neutral-400">Lyon</div>
                  <div className="text-neutral-300 font-mono">117 ✓</div>
                </div>
                <div className="p-2 rounded bg-green-500/20 border border-green-500/30">
                  <div className="font-medium text-green-400">Marseille</div>
                  <div className="text-green-300 font-mono">117+100=217</div>
                </div>
                <div className="p-2 rounded bg-yellow-500/20">
                  <div className="font-medium text-yellow-400">Bordeaux</div>
                  <div className="text-yellow-300 font-mono">130</div>
                </div>
                <div className="p-2 rounded bg-neutral-500/20">
                  <div className="font-medium text-neutral-400">Lille</div>
                  <div className="text-neutral-300 font-mono">62 ✓</div>
                </div>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                On met à jour Marseille : 117 (Paris→Lyon) + 100 (Lyon→Marseille) = <strong className="text-green-400">217 min</strong>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle2 className="w-5 h-5 text-green-400" />
                <span className="font-medium text-green-400">Résultat final</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="px-2 py-1 rounded bg-blue-500/20 text-blue-400">Paris</span>
                <ArrowRight className="w-4 h-4 text-neutral-500" />
                <span className="text-xs text-neutral-400">117 min</span>
                <ArrowRight className="w-4 h-4 text-neutral-500" />
                <span className="px-2 py-1 rounded bg-purple-500/20 text-purple-400">Lyon</span>
                <ArrowRight className="w-4 h-4 text-neutral-500" />
                <span className="text-xs text-neutral-400">100 min</span>
                <ArrowRight className="w-4 h-4 text-neutral-500" />
                <span className="px-2 py-1 rounded bg-green-500/20 text-green-400">Marseille</span>
              </div>
              <div className="mt-3 text-xs text-neutral-400">
                Temps total : <strong className="text-green-400">217 min</strong> (3h37) — Chemin optimal trouvé !
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-cyan-500/5 border border-cyan-500/20">
          <h3 className="font-semibold text-cyan-400 mb-4">Structures de données utilisées</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="font-medium mb-2">File de priorité (Min-Heap)</div>
              <p className="text-xs text-neutral-400 mb-2">
                Permet de toujours récupérer le nœud avec la <strong className="text-cyan-300">plus petite distance</strong> en temps O(log V).
              </p>
              <CodeBlock>{`# Python : heapq
import heapq
heap = [(0, 'Paris')]  # (distance, nœud)
heapq.heappush(heap, (117, 'Lyon'))
next_node = heapq.heappop(heap)  # (0, 'Paris')`}</CodeBlock>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="font-medium mb-2">Dictionnaires</div>
              <p className="text-xs text-neutral-400 mb-2">
                Stockent les distances connues et le chemin pour reconstruire l'itinéraire.
              </p>
              <CodeBlock>{`distances = {
  'Paris': 0,
  'Lyon': 117,
  'Marseille': 217
}
predecesseurs = {
  'Lyon': 'Paris',
  'Marseille': 'Lyon'
}`}</CodeBlock>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Système de pondération</h2>
        
        <div className="p-6 rounded-xl bg-orange-500/5 border border-orange-500/20 mb-6">
          <h3 className="font-semibold text-orange-400 mb-4">Qu'est-ce que la pondération ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            La <strong className="text-white">pondération</strong> est le système qui attribue un <strong className="text-orange-300">poids</strong> (coût) à chaque liaison.
            L'algorithme de Dijkstra cherche à <strong className="text-white">minimiser la somme des poids</strong> sur tout le trajet.
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Pondération simple (temps réel)</div>
              <div className="flex items-center gap-2 text-sm">
                <code className="text-orange-400">poids</code>
                <span className="text-neutral-500">=</span>
                <code className="text-blue-400">temps_trajet</code>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                Paris → Lyon : poids = <strong className="text-white">117 min</strong>
              </div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Pondération THOR (avec pénalité)</div>
              <div className="flex items-center gap-2 text-sm">
                <code className="text-orange-400">poids</code>
                <span className="text-neutral-500">=</span>
                <code className="text-blue-400">temps</code>
                <span className="text-neutral-500">×</span>
                <code className="text-purple-400">pénalité</code>
              </div>
              <div className="mt-2 text-xs text-neutral-500">
                Paris → Lyon TGV : <strong className="text-white">117 × 1.0 = 117</strong>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-purple-500/5 border border-purple-500/20 mb-6">
          <h3 className="font-semibold text-purple-400 mb-4">Pourquoi utiliser des pénalités ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Sans pénalité, l'algorithme choisirait parfois des TER lents mais directs au lieu de TGV avec correspondance.
            Les pénalités permettent de <strong className="text-white">favoriser les trains rapides</strong>, tout en restant flexible 
            si un train "lent" direct est vraiment plus rapide que plusieurs TGV avec correspondances.
          </p>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-xs text-neutral-500 mb-3">Exemple : Bordeaux → Marseille</div>
            <div className="space-y-3 text-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-red-400">❌</span>
                  <span className="text-neutral-400">TER direct</span>
                </div>
                <div className="text-neutral-400">
                  <span>6h (360 min)</span>
                  <span className="mx-2">×</span>
                  <span className="text-red-400">2.0</span>
                  <span className="mx-2">=</span>
                  <span className="text-red-400 font-mono">720</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-green-400">✓</span>
                  <span className="text-neutral-300">TGV via Paris</span>
                </div>
                <div className="text-neutral-400">
                  <span>5h30 (330 min)</span>
                  <span className="mx-2">×</span>
                  <span className="text-green-400">1.0</span>
                  <span className="mx-2">=</span>
                  <span className="text-green-400 font-mono">330</span>
                </div>
              </div>
            </div>
            <div className="mt-3 text-xs text-neutral-500">
              → Dans cet exemple, l'algorithme choisit le TGV via Paris (poids <strong className="text-green-400">330</strong> &lt; <strong className="text-red-400">720</strong>)
            </div>
          </div>
        </div>

        <h3 className="font-semibold mb-4">Tableau des pénalités par type de train</h3>
        <div className="rounded-xl border border-white/10 overflow-hidden mb-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Type de train</th>
                <th className="text-left p-4 font-medium">Multiplicateur</th>
                <th className="text-left p-4 font-medium">Effet sur le calcul</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr className="bg-green-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-green-400" />
                  <span className="text-green-400 font-medium">TGV / OUIGO</span>
                </td>
                <td className="p-4"><code className="text-green-400">×1.0</code></td>
                <td className="p-4 text-neutral-400">Aucune pénalité — temps réel utilisé</td>
              </tr>
              <tr className="bg-green-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-green-400" />
                  <span className="text-green-400">Lyria / Eurostar</span>
                </td>
                <td className="p-4"><code className="text-green-400">×1.0</code></td>
                <td className="p-4 text-neutral-400">TGV internationaux — aucune pénalité</td>
              </tr>
              <tr className="bg-yellow-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-yellow-400" />
                  <span className="text-yellow-400">Correspondance</span>
                </td>
                <td className="p-4"><code className="text-yellow-400">×1.0</code></td>
                <td className="p-4 text-neutral-400">Transfert inter-gare (métro/RER)</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-yellow-400" />
                  <span className="text-yellow-400">Intercités</span>
                </td>
                <td className="p-4"><code className="text-yellow-400">×1.3</code></td>
                <td className="p-4 text-neutral-400">+30% sur le temps réel</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-orange-400" />
                  <span className="text-orange-400">Train de nuit</span>
                </td>
                <td className="p-4"><code className="text-orange-400">×1.5</code></td>
                <td className="p-4 text-neutral-400">+50% sur le temps réel</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Train className="w-4 h-4 text-red-400" />
                  <span className="text-red-400">TER / Navette</span>
                </td>
                <td className="p-4"><code className="text-red-400">×2.0</code></td>
                <td className="p-4 text-neutral-400">×2 sur le temps réel — forte pénalité</td>
              </tr>
            </tbody>
          </table>
        </div>

        <CodeBlock title="Formule de pondération">{`# Formule appliquée dans THOR :
poids_pondere = temps_reel_minutes × coefficient_penalite

# Exemple 1 : Paris → Lyon en TGV (117 min)
poids = 117 × 1.0 = 117  ✓ Chemin probable

# Exemple 2 : Liaison TER (180 min)
poids = 180 × 2.0 = 360  ✗ Pénalisé (×2)

# L'algorithme choisit TOUJOURS le chemin avec le PLUS PETIT poids total`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Zap className="w-6 h-6 text-yellow-400" />
          Dijkstra Multi-source
        </h2>
        
        <div className="p-6 rounded-xl bg-yellow-500/5 border border-yellow-500/20 mb-6">
          <h3 className="font-semibold text-yellow-400 mb-4">Pourquoi Multi-source ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Les grandes villes ont <strong className="text-white">plusieurs gares</strong> avec des liaisons différentes. 
            Par exemple, Paris a 7 gares principales. Si l'utilisateur demande "Paris → Lyon", 
            quelle gare choisir ?
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Approche naïve</div>
              <p className="text-xs text-neutral-400">
                Choisir une gare "par défaut" (ex: la plus grande) → <strong className="text-red-400">Résultat sous-optimal</strong>
              </p>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Approche THOR (Multi-source)</div>
              <p className="text-xs text-neutral-400">
                Tester <strong className="text-yellow-300">toutes les combinaisons</strong> et garder la meilleure → <strong className="text-green-400">Optimal garanti</strong>
              </p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Exemple : Paris → Lyon</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Paris a 7 gares, Lyon en a 3. L'algorithme teste les <strong className="text-white">21 combinaisons possibles</strong> (7×3) et retourne la meilleure.
          </p>
          
          <div className="mb-4">
            <div className="text-xs text-neutral-500 mb-2">Gares de Paris testées :</div>
            <div className="flex flex-wrap gap-2">
              {['Gare de Lyon', 'Montparnasse', 'Saint-Lazare', 'Nord', 'Est', 'Bercy', 'Austerlitz'].map((g) => (
                <span key={g} className="px-2 py-1 rounded bg-blue-500/10 text-blue-400 text-xs">{g}</span>
              ))}
            </div>
          </div>
          
          <div className="mb-4">
            <div className="text-xs text-neutral-500 mb-2">Gares de Lyon testées :</div>
            <div className="flex flex-wrap gap-2">
              {['Part Dieu', 'Perrache', 'Saint-Exupéry'].map((g) => (
                <span key={g} className="px-2 py-1 rounded bg-purple-500/10 text-purple-400 text-xs">{g}</span>
              ))}
            </div>
          </div>

          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3 p-2 rounded-lg bg-green-500/10">
              <CheckCircle2 className="w-4 h-4 text-green-400" />
              <span className="text-green-300 font-medium">Paris Gare de Lyon → Lyon Part Dieu</span>
              <span className="ml-auto text-green-400 font-mono">117 min ✓</span>
            </div>
            <div className="flex items-center gap-3 p-2 rounded-lg bg-white/5">
              <div className="w-4 h-4 rounded-full border border-neutral-600" />
              <span className="text-neutral-500">Paris Gare de Lyon → Lyon Perrache</span>
              <span className="ml-auto text-neutral-500 font-mono">125 min</span>
            </div>
            <div className="flex items-center gap-3 p-2 rounded-lg bg-white/5">
              <div className="w-4 h-4 rounded-full border border-neutral-600" />
              <span className="text-neutral-500">Paris Bercy → Lyon Part Dieu</span>
              <span className="ml-auto text-neutral-500 font-mono">135 min</span>
            </div>
            <div className="flex items-center gap-3 p-2 rounded-lg bg-white/5">
              <div className="w-4 h-4 rounded-full border border-neutral-600" />
              <span className="text-neutral-500">Paris Montparnasse → Lyon Perrache</span>
              <span className="ml-auto text-neutral-500 font-mono">145 min</span>
            </div>
            <div className="text-xs text-neutral-500 text-center">... et 17 autres combinaisons testées</div>
          </div>
        </div>

        <CodeBlock title="Algorithme Multi-source">{`def find_route(origin_city: str, destination_city: str):
    # Récupérer toutes les gares de chaque ville
    origin_stations = get_stations_for_city(origin_city)      # Ex: 7 gares
    destination_stations = get_stations_for_city(dest_city)   # Ex: 3 gares
    
    best_route = None
    best_time = float('inf')
    
    # Tester toutes les combinaisons
    for start in origin_stations:           # 7 itérations
        for end in destination_stations:    # 3 itérations → 21 tests
            route = dijkstra(start, end)
            if route.total_time < best_time:
                best_route = route
                best_time = route.total_time
    
    return best_route  # Meilleure des 21 routes`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Train className="w-6 h-6 text-yellow-400" />
          Correspondances inter-gare
        </h2>
        
        <div className="p-6 rounded-xl bg-yellow-500/5 border border-yellow-500/20 mb-6">
          <h3 className="font-semibold text-yellow-400 mb-4">Qu'est-ce qu'une correspondance inter-gare ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Certaines villes comme <strong className="text-white">Paris</strong> ont plusieurs gares non-connectées directement par voie ferrée. 
            Pour optimiser les trajets, THOR peut proposer des <strong className="text-yellow-300">correspondances métro/RER</strong> entre ces gares.
          </p>
          <div className="p-4 rounded-lg bg-white/5 mb-4">
            <div className="text-xs text-neutral-500 mb-3">Exemple : Biarritz → Marseille</div>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="px-2 py-1 rounded bg-rose-500/20 text-rose-400 text-xs">TGV</span>
                <span className="text-neutral-400">Biarritz → Paris Montparnasse</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-1 rounded bg-yellow-500/20 text-yellow-400 text-xs"> Correspondance</span>
                <span className="text-neutral-400">Paris Montparnasse → Paris Gare de Lyon (métro, 40-60 min)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-1 rounded bg-rose-500/20 text-rose-400 text-xs">TGV</span>
                <span className="text-neutral-400">Paris Gare de Lyon → Marseille</span>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Gares concernées</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Les correspondances inter-gare sont définies manuellement pour les principales gares parisiennes :
          </p>
          <div className="grid md:grid-cols-3 gap-3">
            {['Paris Montparnasse', 'Paris Gare de Lyon', 'Paris Nord'].map((g) => (
              <span key={g} className="px-3 py-2 rounded-lg bg-yellow-500/10 text-yellow-400 text-sm text-center">{g}</span>
            ))}
          </div>
          <div className="mt-4 text-xs text-neutral-500">
            Les temps de transfert incluent le trajet en métro/RER + marges de sécurité.
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Pénalité des correspondances</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Les correspondances inter-gare ont un <strong className="text-white">multiplicateur de 1.0</strong>, 
            identique aux TGV. Cela permet à l'algorithme de les considérer comme une option viable sans les pénaliser.
          </p>
          <CodeBlock>{`TRAIN_TYPE_PENALTY = {
    'TGV': 1.0,
    'OUIGO': 1.0,
    'Correspondance': 1.0,  # ← Traité comme TGV
    'Intercités': 1.3,
    'TER': 2.0
}`}</CodeBlock>
        </div>

        <div className="p-6 rounded-xl bg-yellow-500/5 border border-yellow-500/20">
          <h3 className="font-semibold text-yellow-400 mb-4">Affichage sur la carte</h3>
          <p className="text-sm text-neutral-400 mb-3">
            Les correspondances sont affichées différemment des trains :
          </p>
          <ul className="space-y-2 text-sm text-neutral-400">
            <li className="flex items-center gap-2">
              <div className="w-4 h-1 bg-yellow-400" style={{backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 5px, currentColor 5px, currentColor 10px)'}} />
              <span>Ligne jaune <strong className="text-yellow-400">pointillée</strong></span>
            </li>
            <li className="flex items-center gap-2">
              <span>Badge <strong className="text-yellow-400">"Correspondance"</strong> dans les détails</span>
            </li>
          </ul>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Plane className="w-6 h-6 text-red-400" />
          Exclusion des aéroports
        </h2>
        
        <div className="p-6 rounded-xl bg-red-500/5 border border-red-500/20 mb-6">
          <h3 className="font-semibold text-red-400 mb-4">Pourquoi exclure les gares d'aéroport ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Quand un utilisateur demande "Paris → Lyon", il s'attend à arriver en <strong className="text-white">centre-ville</strong>, 
            pas à l'aéroport. Les gares d'aéroport sont donc <strong className="text-red-300">exclues des origines/destinations par défaut</strong>.
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-red-400 mb-2">❌ Sans exclusion</div>
              <div className="text-sm text-neutral-400">
                "Lyon" pourrait retourner <strong className="text-red-300">Lyon Saint-Exupéry TGV</strong> (à 30km du centre)
              </div>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-green-400 mb-2">✓ Avec exclusion</div>
              <div className="text-sm text-neutral-400">
                "Lyon" retourne <strong className="text-green-300">Lyon Part Dieu</strong> ou <strong className="text-green-300">Lyon Perrache</strong> (centre-ville)
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h4 className="font-medium mb-4">Mots-clés utilisés pour la détection</h4>
          <p className="text-sm text-neutral-400 mb-4">
            Une gare est considérée comme "aéroport" si son nom contient l'un de ces termes :
          </p>
          <div className="flex flex-wrap gap-2 mb-4">
            {['Aéroport', 'CDG', 'Charles de Gaulle', 'Saint-Exupéry', 'Orly'].map((term) => (
              <span key={term} className="px-3 py-1.5 rounded-lg bg-red-500/10 text-red-400 text-sm font-mono">
                "{term}"
              </span>
            ))}
          </div>
          <div className="text-xs text-neutral-500">
            <strong>Note :</strong> Ces gares restent accessibles comme <strong>correspondances</strong> (passage), 
            mais pas comme origine ou destination finale.
          </div>
        </div>

        <CodeBlock title="Logique d'exclusion">{`AIRPORT_KEYWORDS = ['Aéroport', 'CDG', 'Saint-Exupéry', 'Orly']

def is_airport_station(station_name: str) -> bool:
    return any(keyword.lower() in station_name.lower() 
               for keyword in AIRPORT_KEYWORDS)

def get_stations_for_city(city: str, exclude_airports: bool = True):
    stations = find_all_stations(city)
    if exclude_airports:
        stations = [s for s in stations if not is_airport_station(s.name)]
    return stations`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Target className="w-6 h-6 text-blue-400" />
          Sélection intelligente des villes
        </h2>
        
        <div className="p-6 rounded-xl bg-blue-500/5 border border-blue-500/20 mb-6">
          <h3 className="font-semibold text-blue-400 mb-4">Problématique des homonymes</h3>
          <p className="text-neutral-400 text-sm mb-4">
            La France compte plusieurs villes avec des noms similaires. Par exemple, "Marseille" peut faire référence à :
          </p>
          <ul className="list-disc list-inside space-y-2 text-sm text-neutral-400 mb-4">
            <li><strong className="text-white">Marseille</strong> (13) - 2ème ville de France, 870 000 habitants</li>
            <li><strong className="text-neutral-500">Marseille-en-Beauvaisis</strong> (60) - Petit village, 800 habitants</li>
          </ul>
          <p className="text-neutral-400 text-sm">
            Sans système intelligent, l'algorithme pourrait choisir le village par erreur (car plus proche de Paris). 
            THOR utilise un <strong className="text-blue-300">système de scoring</strong> pour privilégier automatiquement les grandes villes.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Système de scoring des gares</h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-green-500/20 text-green-400 text-xs font-mono shrink-0">+200</span>
              <span className="text-neutral-400">Nom exact de la gare (ex: cherche "Paris Gare de Lyon" → trouve exactement)</span>
            </div>
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-green-500/20 text-green-400 text-xs font-mono shrink-0">+100</span>
              <span className="text-neutral-400">Grande ville majeure (Marseille, Lyon, Toulouse, Nice, Bordeaux, Lille...)</span>
            </div>
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-green-500/20 text-green-400 text-xs font-mono shrink-0">+50</span>
              <span className="text-neutral-400">Gare principale reconnue (Saint-Charles, Part-Dieu, Saint-Jean, Montparnasse...)</span>
            </div>
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-green-500/20 text-green-400 text-xs font-mono shrink-0">+30</span>
              <span className="text-neutral-400">Gare TGV ou centrale</span>
            </div>
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-blue-500/20 text-blue-400 text-xs font-mono shrink-0">+2×N</span>
              <span className="text-neutral-400">Nombre de connexions (N) dans le réseau ferroviaire</span>
            </div>
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 rounded bg-red-500/20 text-red-400 text-xs font-mono shrink-0">-20</span>
              <span className="text-neutral-400">Gare secondaire (banlieue, aéroport, RER...)</span>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Exclusion automatique des homonymes</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Pour les recherches <strong className="text-white">simples</strong> (sans tiret), THOR exclut automatiquement les homonymes indésirables :
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-2 px-3 text-neutral-400 font-medium">Recherche</th>
                  <th className="text-left py-2 px-3 text-green-400 font-medium">✅ Trouve</th>
                  <th className="text-left py-2 px-3 text-red-400 font-medium">❌ Exclut</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <tr>
                  <td className="py-3 px-3">
                    <code className="text-blue-400">"marseille"</code>
                  </td>
                  <td className="py-3 px-3 text-green-400">Marseille Saint-Charles (13)</td>
                  <td className="py-3 px-3 text-red-400/70">Marseille-en-Beauvaisis (60)</td>
                </tr>
                <tr>
                  <td className="py-3 px-3">
                    <code className="text-blue-400">"lyon"</code>
                  </td>
                  <td className="py-3 px-3 text-green-400">Lyon Part-Dieu / Perrache</td>
                  <td className="py-3 px-3 text-red-400/70">Lyon-Dagneux (01)</td>
                </tr>
                <tr>
                  <td className="py-3 px-3">
                    <code className="text-blue-400">"paris"</code>
                  </td>
                  <td className="py-3 px-3 text-green-400">Paris Gare de Lyon, Nord...</td>
                  <td className="py-3 px-3 text-red-400/70">Paris-Plage</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 p-3 rounded-lg bg-blue-500/10 text-xs text-blue-400">
            <strong>Note :</strong> Si l'utilisateur cherche explicitement l'homonyme avec tirets 
            (ex: <code className="bg-white/10 px-1 rounded">"marseille-en-beauvaisis"</code>), le système trouvera bien cette ville.
          </div>
        </div>

        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
          <h3 className="font-semibold text-green-400 mb-4">Exemple de calcul de score</h3>
          <CodeBlock>{`# Recherche: "marseille"

Marseille Saint-Charles:
  - ville_nom == "marseille" : +80
  - "marseille" in MAJOR_CITIES : +100
  - "saint-charles" in gare_nom : +50
  - nb_connections × 2 : +120
  → Score total : 350

Marseille-en-Beauvaisis:
  - EXCLU automatiquement (homonyme indésirable)
  → Non considéré

✅ L'algorithme choisit Marseille Saint-Charles`}</CodeBlock>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Settings className="w-6 h-6 text-neutral-400" />
          Configuration
        </h2>
        
        <CodeBlock title="Paramètres du pathfinding">{`{
  "pathfinding": {
    "path_gares": "data/train_station/dataset_gares.json",
    "path_liaisons": "data/train_station/dataset_liaisons_enhanced.json",
    "path_shapes": "data/train_station/dataset_liaisons_with_shapes.json",
    "mode": "time",
    "penalty_system": "enabled",
    "exclude_airports": true
  }
}`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Utilisation</h2>
        
        <h3 className="font-semibold mb-3">Via la CLI</h3>
        <CodeBlock title="Terminal">{`python3 -m src.cli.pathfinding \\
  --origin "Paris" \\
  --destination "Marseille" \\
  --model dijkstra`}</CodeBlock>

        <h3 className="font-semibold mb-3 mt-6">Via Python</h3>
        <CodeBlock title="Python">{`from src.pathfinding.models.dijkstra import DijkstraPathfinder

# Initialiser le pathfinder
pathfinder = DijkstraPathfinder()

# Trouver un itinéraire
route = pathfinder.find_route("Paris", "Lyon")

print(route.steps)         # ['Paris Gare de Lyon', 'Lyon Part Dieu']
print(route.total_time)    # 117
print(route.total_distance)# 390.79
print(route.metadata)      # Détails des segments, géométries, etc.`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Exemple de résultat</h2>
        <CodeBlock title="Route Paris → Lyon">{`{
  "origin": "Paris",
  "destination": "Lyon",
  "steps": ["Paris Gare de Lyon", "Lyon Part Dieu"],
  "total_time": 117,
  "total_distance": 390.79,
  "metadata": {
    "origin_uic": "87686006",
    "destination_uic": "87723197",
    "path_uic": ["87686006", "87723197"],
    "segments": [
      {
        "from": "Paris Gare de Lyon",
        "to": "Lyon Part Dieu",
        "temps_min": 117,
        "distance_km": 390.79,
        "nb_trains_jour": 120,
        "type_train": "TGV",
        "geometry": {
          "type": "LineString",
          "coordinates": [[2.37396, 48.8447], ...]
        }
      }
    ]
  }
}`}</CodeBlock>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Map className="w-6 h-6 text-blue-400" />
          Géométries des voies ferrées
        </h2>

        <div className="p-6 rounded-xl bg-blue-500/5 border border-blue-500/20 mb-6">
          <h3 className="font-semibold text-blue-400 mb-4">Qu'est-ce qu'une géométrie ?</h3>
          <p className="text-neutral-400 text-sm mb-4">
            Chaque liaison entre deux gares possède une <strong className="text-white">géométrie</strong> : 
            une liste de coordonnées GPS qui trace le <strong className="text-blue-300">parcours réel de la voie ferrée</strong>.
          </p>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-xs text-neutral-500 mb-2">Format GeoJSON LineString</div>
            <CodeBlock>{`{
  "type": "LineString",
  "coordinates": [
    [2.373, 48.844],   // Paris Gare de Lyon
    [2.401, 48.831],   // Point intermédiaire
    [2.456, 48.792],   // Point intermédiaire
    [4.859, 45.760]    // Lyon Part Dieu
  ]
}`}</CodeBlock>
            <div className="mt-2 text-xs text-neutral-500">
              <strong>Format :</strong> [longitude, latitude] — Attention, Leaflet utilise [lat, lon] !
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-1">~60%</div>
            <div className="text-sm text-neutral-500">Liaisons avec géométrie</div>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <div className="text-3xl font-bold text-green-400 mb-1">~300</div>
            <div className="text-sm text-neutral-500">Points par segment (moy.)</div>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <div className="text-3xl font-bold text-purple-400 mb-1">3,348</div>
            <div className="text-sm text-neutral-500">Lignes dans shapes.json</div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-orange-500/5 border border-orange-500/20 mb-6">
          <h3 className="font-semibold text-orange-400 mb-4">La distance Haversine</h3>
          <p className="text-neutral-400 text-sm mb-4">
            La <strong className="text-white">formule de Haversine</strong> calcule la distance entre deux points sur une sphère 
            (la Terre) à partir de leurs coordonnées GPS (latitude, longitude). C'est la distance "à vol d'oiseau" 
            en tenant compte de la <strong className="text-orange-300">courbure terrestre</strong>.
          </p>
          
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Pourquoi pas Pythagore ?</div>
              <p className="text-xs text-neutral-400">
                La formule de Pythagore (√(x² + y²)) fonctionne sur un plan <strong className="text-red-400">plat</strong>. 
                Mais la Terre est une <strong className="text-orange-300">sphère</strong> ! Sur de grandes distances, 
                Pythagore donne des résultats faux.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-white/5">
              <div className="text-xs text-neutral-500 mb-2">Précision de Haversine</div>
              <p className="text-xs text-neutral-400">
                Haversine suppose une Terre parfaitement sphérique (rayon = 6,371 km). 
                Erreur &lt; <strong className="text-green-400">0.5%</strong> pour la plupart des calculs.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-lg bg-white/5 mb-4">
            <div className="text-xs text-neutral-500 mb-2">Formule mathématique</div>
            <div className="text-center py-4">
              <div className="text-sm text-neutral-300 font-mono">
                a = sin²(Δlat/2) + cos(lat₁) × cos(lat₂) × sin²(Δlon/2)
              </div>
              <div className="text-sm text-neutral-300 font-mono mt-2">
                d = 2 × R × arctan2(√a, √(1−a))
              </div>
            </div>
            <div className="text-xs text-neutral-500 text-center">
              Où <strong className="text-orange-300">R</strong> = rayon de la Terre (6,371 km), 
              <strong className="text-orange-300">Δlat</strong> = différence de latitudes, 
              <strong className="text-orange-300">Δlon</strong> = différence de longitudes
            </div>
          </div>

          <CodeBlock title="Implémentation Python">{`import math

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calcule la distance en km entre deux points GPS."""
    R = 6371  # Rayon de la Terre en km
    
    # Convertir en radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Différences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Formule de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c  # Distance en km

# Exemple : Paris → Lyon
distance = haversine(2.349, 48.853, 4.835, 45.764)
print(f"Distance : {distance:.1f} km")  # → 391.2 km`}</CodeBlock>

          <div className="mt-4 p-3 rounded-lg bg-orange-500/10 text-xs">
            <strong className="text-orange-300">Utilisation dans THOR :</strong>
            <span className="text-neutral-400"> Haversine est utilisé pour (1) calculer les distances entre gares, 
            (2) matcher les géométries aux liaisons (seuil &lt; 5km), (3) trier les résultats par proximité.</span>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-4">Processus de matching géométrie ↔ liaison</h3>
          <p className="text-sm text-neutral-400 mb-4">
            Les géométries proviennent du fichier <code className="text-blue-400">shapes.json</code> (RFN). 
            Le script <code className="text-blue-400">generate_railway_shapes.py</code> associe chaque liaison à sa géométrie.
          </p>
          <div className="space-y-3">
            <div className="flex items-start gap-4">
              <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400 shrink-0">1</div>
              <div className="text-sm text-neutral-400">
                Pour chaque liaison (ex: Paris → Lyon), on cherche dans shapes.json les lignes passant près des deux gares.
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400 shrink-0">2</div>
              <div className="text-sm text-neutral-400">
                On calcule la <strong className="text-white">distance Haversine</strong> entre chaque point de la ligne et les coordonnées des gares.
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400 shrink-0">3</div>
              <div className="text-sm text-neutral-400">
                Si une ligne passe à moins de <strong className="text-yellow-400">5km</strong> des deux gares, on extrait le segment correspondant.
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-xs font-mono text-blue-400 shrink-0">4</div>
              <div className="text-sm text-neutral-400">
                La géométrie extraite est ajoutée à <code className="text-green-400">dataset_liaisons_with_shapes.json</code>.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
        <h2 className="text-xl font-bold mb-4">Résumé du Pathfinding THOR</h2>
        <div className="grid md:grid-cols-2 gap-6 text-sm">
          <div>
            <h4 className="font-medium text-green-400 mb-2">Points forts</h4>
            <ul className="space-y-1 text-neutral-400">
              <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-green-400" /> Temps de trajet réels (GTFS)</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-green-400" /> Système de pénalités intelligent (favorise TGV)</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-green-400" /> Multi-source pour villes à plusieurs gares</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-green-400" /> Géométries pour affichage carte</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-green-400" /> Latence ~5ms</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-blue-400 mb-2">Données utilisées</h4>
            <ul className="space-y-1 text-neutral-400">
              <li className="flex items-center gap-2"><span className="text-blue-400">→</span> dataset_gares.json (2,782 gares)</li>
              <li className="flex items-center gap-2"><span className="text-blue-400">→</span> dataset_liaisons_enhanced.json (7,852 liaisons)</li>
              <li className="flex items-center gap-2"><span className="text-blue-400">→</span> dataset_liaisons_with_shapes.json (géométries)</li>
              <li className="flex items-center gap-2"><span className="text-blue-400">→</span> shapes.json (3,348 lignes RFN)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
