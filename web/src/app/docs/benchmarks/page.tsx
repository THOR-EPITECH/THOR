import { ArrowRight, CheckCircle2, XCircle, Mic, Brain, Route, Trophy, BarChart3, Target, Clock, Zap, HelpCircle } from 'lucide-react';

function Badge({ variant }: { variant: 'chosen' | 'tested' | 'rejected' }) {
  const styles = {
    chosen: 'bg-green-500/20 text-green-400 border-green-500/30',
    tested: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    rejected: 'bg-red-500/20 text-red-400 border-red-500/30',
  };
  const labels = {
    chosen: 'Choisi',
    tested: 'Testé',
    rejected: 'Non retenu',
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs border ${styles[variant]}`}>
      {labels[variant]}
    </span>
  );
}

function ProgressBar({ value, max, color = 'green' }: { value: number; max: number; color?: string }) {
  const percentage = (value / max) * 100;
  const colorClasses: Record<string, string> = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
  };
  return (
    <div className="h-2 bg-white/10 rounded-full overflow-hidden">
      <div 
        className={`h-full ${colorClasses[color]} transition-all duration-500`}
        style={{ width: `${Math.min(percentage, 100)}%` }}
      />
    </div>
  );
}

function MetricRow({ label, value, percentage, best = false }: { 
  label: string; 
  value: string; 
  percentage: number;
  best?: boolean;
}) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-32 text-sm text-neutral-400">{label}</div>
      <div className="flex-1">
        <ProgressBar value={percentage} max={100} color={best ? 'green' : 'yellow'} />
      </div>
      <div className={`w-20 text-right text-sm font-mono ${best ? 'text-green-400' : 'text-neutral-300'}`}>
        {value}
      </div>
    </div>
  );
}

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

export default function DocsBenchmarks() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Recherche</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Benchmarks</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Benchmarks & Résultats</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Résultats détaillés des tests comparatifs réalisés sur chaque module 
          de la pipeline THOR avec les données réelles du projet.
        </p>
      </div>

      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-8">
        <div className="flex items-center gap-3 mb-4">
          <BarChart3 className="w-5 h-5 text-neutral-400" />
          <h3 className="font-semibold">Méthodologie des tests</h3>
        </div>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div className="p-3 rounded-lg bg-white/5">
            <div className="text-neutral-400 mb-1">Dataset NLP</div>
            <div className="font-mono text-neutral-300">438 échantillons</div>
          </div>
          <div className="p-3 rounded-lg bg-white/5">
            <div className="text-neutral-400 mb-1">Dataset Audio</div>
            <div className="font-mono text-neutral-300">200+ fichiers WAV</div>
          </div>
          <div className="p-3 rounded-lg bg-white/5">
            <div className="text-neutral-400 mb-1">Date du benchmark</div>
            <div className="font-mono text-neutral-300">09/01/2026</div>
          </div>
        </div>
      </div>

      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-12">
        <div className="flex items-center gap-3 mb-6">
          <HelpCircle className="w-5 h-5 text-neutral-400" />
          <h3 className="font-semibold">Glossaire des métriques</h3>
        </div>
        
        <div className="space-y-6">
          <div>
            <h4 className="text-sm font-medium text-blue-400 mb-3 flex items-center gap-2">
              <Mic className="w-4 h-4" />
              Métriques STT (Speech-to-Text)
            </h4>
            <div className="grid gap-3">
              <div className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-blue-400">WER</span>
                  <span className="text-xs text-neutral-500">Word Error Rate</span>
                </div>
                <p className="text-sm text-neutral-400 mb-2">
                  Taux d'erreur au niveau des mots. Mesure le pourcentage de mots incorrects 
                  (substitutions, insertions, suppressions) par rapport à la transcription de référence.
                </p>
                <div className="p-2 rounded bg-white/5 font-mono text-xs text-neutral-500">
                  WER = (Substitutions + Insertions + Suppressions) / Nombre total de mots
                </div>
                <p className="text-xs text-green-400 mt-2">↓ Plus bas = meilleur. Un WER de 0% = transcription parfaite.</p>
              </div>
              
              <div className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-blue-400">CER</span>
                  <span className="text-xs text-neutral-500">Character Error Rate</span>
                </div>
                <p className="text-sm text-neutral-400 mb-2">
                  Taux d'erreur au niveau des caractères. Plus granulaire que le WER, 
                  utile pour détecter les petites erreurs d'orthographe.
                </p>
                <div className="p-2 rounded bg-white/5 font-mono text-xs text-neutral-500">
                  CER = Erreurs de caractères / Nombre total de caractères
                </div>
                <p className="text-xs text-green-400 mt-2">↓ Plus bas = meilleur. Généralement inférieur au WER.</p>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium text-purple-400 mb-3 flex items-center gap-2">
              <Brain className="w-4 h-4" />
              Métriques NLP (Classification/NER)
            </h4>
            <div className="grid gap-3">
              <div className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-purple-400">Precision</span>
                  <span className="text-xs text-neutral-500">Précision</span>
                </div>
                <p className="text-sm text-neutral-400 mb-2">
                  Parmi toutes les prédictions positives du modèle, combien sont correctes ?
                  Mesure la fiabilité des prédictions.
                </p>
                <div className="p-2 rounded bg-white/5 font-mono text-xs text-neutral-500">
                  Precision = Vrais Positifs / (Vrais Positifs + Faux Positifs)
                </div>
                <p className="text-xs text-neutral-500 mt-2">Ex: Sur 100 villes prédites, 92 sont correctes → Precision = 92%</p>
              </div>
              
              <div className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-purple-400">Recall</span>
                  <span className="text-xs text-neutral-500">Rappel</span>
                </div>
                <p className="text-sm text-neutral-400 mb-2">
                  Parmi toutes les vraies instances positives, combien ont été trouvées ?
                  Mesure la capacité à ne rien manquer.
                </p>
                <div className="p-2 rounded bg-white/5 font-mono text-xs text-neutral-500">
                  Recall = Vrais Positifs / (Vrais Positifs + Faux Négatifs)
                </div>
                <p className="text-xs text-neutral-500 mt-2">Ex: Sur 100 villes réelles, 85 sont détectées → Recall = 85%</p>
              </div>
              
              <div className="p-4 rounded-lg bg-purple-500/10 border border-purple-500/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-purple-400 font-bold">F1-Score</span>
                  <span className="text-xs text-purple-300">Métrique principale</span>
                </div>
                <p className="text-sm text-neutral-400 mb-2">
                  Moyenne harmonique de la Precision et du Recall. 
                  Équilibre entre les deux métriques, idéal quand on veut optimiser les deux à la fois.
                </p>
                <div className="p-2 rounded bg-white/5 font-mono text-xs text-neutral-500">
                  F1 = 2 × (Precision × Recall) / (Precision + Recall)
                </div>
                <p className="text-xs text-green-400 mt-2">↑ Plus haut = meilleur. F1 de 1.0 = parfait. F1 de 0.5 = médiocre.</p>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-lg bg-white/5 border border-white/10">
            <h4 className="text-sm font-medium mb-3">Exemple concret</h4>
            <p className="text-sm text-neutral-400 mb-3">
              Pour la phrase <em>"Je veux aller de Paris à Lyon"</em> :
            </p>
            <div className="grid md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-neutral-500">Vérité :</span>
                  <span>origine=Paris, destination=Lyon</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-500">Prédiction :</span>
                  <span>origine=Paris, destination=Lyon</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-green-400">✓ Vrai Positif (TP)</span>
                  <span>2 entités correctes</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Precision = Recall = F1</span>
                  <span className="font-mono">1.0 (100%)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Mic className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold">Speech-to-Text</h2>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <Target className="w-4 h-4 text-neutral-400" />
            Comparaison des métriques
          </h3>
          
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium">Whisper (small)</span>
                <Badge variant="chosen" />
              </div>
              <div className="space-y-2">
                <MetricRow label="WER (erreur)" value="29.1%" percentage={70.9} best />
                <MetricRow label="CER (erreur)" value="12.2%" percentage={87.8} best />
                <MetricRow label="Latence" value="387ms" percentage={60} />
              </div>
            </div>

            <div className="border-t border-white/5 pt-6">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium">Vosk</span>
                <Badge variant="tested" />
              </div>
              <div className="space-y-2">
                <MetricRow label="WER (erreur)" value="48.1%" percentage={51.9} />
                <MetricRow label="CER (erreur)" value="16.1%" percentage={83.9} />
                <MetricRow label="Latence" value="118ms" percentage={90} best />
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <div className="p-4 rounded-xl bg-green-500/5 border border-green-500/20">
            <div className="text-xs text-green-400 font-medium mb-2">Whisper</div>
            <div className="text-sm text-neutral-300 mb-2">Audio: "Je veux voyager de Toulouse à Bordeaux"</div>
            <CodeBlock title="Transcription">{`"Je veux voyager de Toulouse à Bordeaux."`}</CodeBlock>
            <div className="mt-2 text-xs text-green-400">✓ Majuscules, ponctuation, 100% correct</div>
          </div>
          <div className="p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/20">
            <div className="text-xs text-yellow-400 font-medium mb-2">Vosk</div>
            <div className="text-sm text-neutral-300 mb-2">Audio: "Je veux voyager de Toulouse à Bordeaux"</div>
            <CodeBlock title="Transcription">{`"je veux voyager de toulouse à bordeaux"`}</CodeBlock>
            <div className="mt-2 text-xs text-yellow-400">⚠ Pas de majuscules, mais exploitable</div>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <h4 className="font-medium text-green-400 mb-1">Verdict : Whisper</h4>
              <p className="text-sm text-neutral-400">
                WER 19% inférieur à Vosk (29.1% vs 48.1%). Malgré une latence 3x plus élevée, 
                la qualité de transcription justifie ce choix pour éviter les erreurs en cascade.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-purple-500/10">
            <Brain className="w-5 h-5 text-purple-400" />
          </div>
          <h2 className="text-2xl font-bold">Natural Language Processing</h2>
        </div>

        <div className="rounded-xl border border-white/10 overflow-hidden mb-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Modèle</th>
                <th className="text-left p-4 font-medium">F1-Score</th>
                <th className="text-left p-4 font-medium">Origine</th>
                <th className="text-left p-4 font-medium">Destination</th>
                <th className="text-left p-4 font-medium">Les deux</th>
                <th className="text-left p-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr className="bg-green-500/5">
                <td className="p-4 flex items-center gap-2">
                  <Trophy className="w-4 h-4 text-green-400" />
                  <span className="font-medium">spaCy (fine-tuné)</span>
                </td>
                <td className="p-4 text-green-400 font-mono">0.621</td>
                <td className="p-4 text-green-400 font-mono">94.98%</td>
                <td className="p-4 text-green-400 font-mono">83.90%</td>
                <td className="p-4 text-green-400 font-mono">83.68%</td>
                <td className="p-4"><Badge variant="chosen" /></td>
              </tr>
              <tr>
                <td className="p-4">regex_advanced</td>
                <td className="p-4 font-mono text-neutral-400">0.430</td>
                <td className="p-4 font-mono text-neutral-400">80.82%</td>
                <td className="p-4 font-mono text-red-400">29.57%</td>
                <td className="p-4 font-mono text-red-400">27.05%</td>
                <td className="p-4"><Badge variant="tested" /></td>
              </tr>
              <tr>
                <td className="p-4">spaCy (base)</td>
                <td className="p-4 font-mono text-neutral-400">0.407</td>
                <td className="p-4 font-mono text-neutral-400">72.60%</td>
                <td className="p-4 font-mono text-neutral-400">42.24%</td>
                <td className="p-4 font-mono text-neutral-400">40.75%</td>
                <td className="p-4"><Badge variant="tested" /></td>
              </tr>
              <tr>
                <td className="p-4">dummy (baseline)</td>
                <td className="p-4 font-mono text-neutral-400">0.230</td>
                <td className="p-4 font-mono text-neutral-400">79.91%</td>
                <td className="p-4 font-mono text-neutral-400">57.08%</td>
                <td className="p-4 font-mono text-neutral-400">50.00%</td>
                <td className="p-4"><Badge variant="rejected" /></td>
              </tr>
              <tr>
                <td className="p-4 text-neutral-500">transformers</td>
                <td className="p-4 text-red-400">Erreur</td>
                <td className="p-4 text-neutral-500">—</td>
                <td className="p-4 text-neutral-500">—</td>
                <td className="p-4 text-neutral-500">—</td>
                <td className="p-4"><Badge variant="rejected" /></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Comparaison F1-Score</h3>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm">spaCy (fine-tuné)</span>
                <span className="text-sm font-mono text-green-400">0.621</span>
              </div>
              <ProgressBar value={62.1} max={100} color="green" />
            </div>
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-neutral-400">regex_advanced</span>
                <span className="text-sm font-mono text-neutral-400">0.430</span>
              </div>
              <ProgressBar value={43.0} max={100} color="yellow" />
            </div>
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-neutral-400">spaCy (base)</span>
                <span className="text-sm font-mono text-neutral-400">0.407</span>
              </div>
              <ProgressBar value={40.7} max={100} color="yellow" />
            </div>
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-neutral-400">dummy</span>
                <span className="text-sm font-mono text-neutral-400">0.230</span>
              </div>
              <ProgressBar value={23.0} max={100} color="red" />
            </div>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-purple-500/5 border border-purple-500/20 mb-6">
          <div className="flex items-start gap-3">
            <Zap className="w-5 h-5 text-purple-400 mt-0.5" />
            <div>
              <h4 className="font-medium text-purple-400 mb-1">Impact du fine-tuning</h4>
              <p className="text-sm text-neutral-400">
                Le fine-tuning de spaCy sur notre dataset améliore le F1-Score de <strong className="text-white">+52.7%</strong> (0.407 → 0.621).
                La précision sur la destination passe de 42.24% à 83.90%, soit un gain de <strong className="text-white">+98.6%</strong>.
              </p>
            </div>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <h4 className="font-medium text-green-400 mb-1">Verdict : spaCy fine-tuné</h4>
              <p className="text-sm text-neutral-400">
                Le modèle fine-tuné surpasse tous les autres avec un F1 de 0.621.
                Regex échoue sur les destinations (29.57%), Transformers n'a pas pu être évalué (erreur de chargement).
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Route className="w-5 h-5 text-green-400" />
          </div>
          <h2 className="text-2xl font-bold">Pathfinding</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
            <h3 className="font-semibold mb-4">Dijkstra (temps réels)</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                <span className="text-sm text-neutral-400">Précision origine</span>
                <span className="font-mono text-green-400">100%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                <span className="text-sm text-neutral-400">Précision destination</span>
                <span className="font-mono text-green-400">100%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                <span className="text-sm text-neutral-400">Routes trouvées</span>
                <span className="font-mono text-yellow-400">50%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                <span className="text-sm text-neutral-400">Étapes moyennes</span>
                <span className="font-mono text-neutral-300">3.5</span>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
            <h3 className="font-semibold mb-4">Exemple de route</h3>
            <CodeBlock title="Toulouse → Bordeaux">{`{
  "steps": [
    "Toulouse Matabiau",
    "Bordeaux Saint-Jean"
  ],
  "total_time": 143 min (2h23),
  "total_distance": 209.5 km,
  "type_train": "TGV",
  "nb_trains_jour": 17
}`}</CodeBlock>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <h4 className="font-medium text-green-400 mb-1">Verdict : Dijkstra avec temps pondérés</h4>
              <p className="text-sm text-neutral-400">
                100% de précision sur les gares identifiées. Le taux de 50% de routes trouvées 
                s'explique par des gares manquantes dans le dataset de test (gares étrangères, TER locaux).
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-orange-500/10">
            <Zap className="w-5 h-5 text-orange-400" />
          </div>
          <h2 className="text-2xl font-bold">Pipeline End-to-End</h2>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-4">Test complet : Audio → Itinéraire</h3>
          <CodeBlock title="Entrée : sample_000160.wav">{`Audio: "Je veux voyager de Toulouse à Bordeaux"`}</CodeBlock>
          
          <div className="my-4 flex items-center gap-2 text-neutral-500">
            <div className="flex-1 h-px bg-white/10" />
            <span className="text-xs">Pipeline : Whisper → spaCy → Dijkstra</span>
            <div className="flex-1 h-px bg-white/10" />
          </div>

          <CodeBlock title="Sortie">{`{
  "transcript": "Je veux voyager de Toulouse à Bordeaux.",
  "origin": "Toulouse",
  "destination": "Bordeaux",
  "is_valid": true,
  "confidence": 0.70,
  "route": {
    "steps": ["Toulouse Matabiau", "Bordeaux Saint-Jean"],
    "total_time": 143 min,
    "total_distance": 209.5 km,
    "type_train": "TGV",
    "trains_par_jour": 17
  }
}`}</CodeBlock>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/20 text-center">
            <Mic className="w-6 h-6 text-blue-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">387ms</div>
            <div className="text-xs text-neutral-400">STT (Whisper)</div>
          </div>
          <div className="p-4 rounded-lg bg-purple-500/10 border border-purple-500/20 text-center">
            <Brain className="w-6 h-6 text-purple-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">~10ms</div>
            <div className="text-xs text-neutral-400">NLP (spaCy)</div>
          </div>
          <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20 text-center">
            <Route className="w-6 h-6 text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">~5ms</div>
            <div className="text-xs text-neutral-400">Pathfinding</div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-6">Récapitulatif des choix</h2>
        <div className="rounded-xl border border-white/10 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Module</th>
                <th className="text-left p-4 font-medium">Choix</th>
                <th className="text-left p-4 font-medium">Métrique clé</th>
                <th className="text-left p-4 font-medium">vs Alternative</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Mic className="w-4 h-4 text-blue-400" />
                  STT
                </td>
                <td className="p-4 text-green-400 font-medium">Whisper</td>
                <td className="p-4 font-mono">WER 29.1%</td>
                <td className="p-4 text-green-400">-19% vs Vosk</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Brain className="w-4 h-4 text-purple-400" />
                  NLP
                </td>
                <td className="p-4 text-green-400 font-medium">spaCy (fine-tuné)</td>
                <td className="p-4 font-mono">F1 0.621</td>
                <td className="p-4 text-green-400">+53% vs base</td>
              </tr>
              <tr>
                <td className="p-4 flex items-center gap-2">
                  <Route className="w-4 h-4 text-green-400" />
                  Pathfinding
                </td>
                <td className="p-4 text-green-400 font-medium">Dijkstra</td>
                <td className="p-4 font-mono">100% précision</td>
                <td className="p-4 text-neutral-400">Seul testé</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="mt-6 p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-2">Latence totale de la pipeline</h3>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold text-white">~400ms</span>
            <span className="text-neutral-400">pour une requête audio complète</span>
          </div>
          <p className="text-sm text-neutral-500 mt-2">
            387ms (STT) + 10ms (NLP) + 5ms (Pathfinding) = temps de réponse quasi-instantané
          </p>
        </div>
      </section>
    </div>
  );
}
