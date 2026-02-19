'use client';

import { 
  Lightbulb, 
  Mic, 
  Brain, 
  Route, 
  Zap,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Target,
  Layers,
  Map,
  Database,
  Globe,
  Sparkles,
  ArrowRight
} from 'lucide-react';

function ImprovementCard({ 
  icon: Icon, 
  title, 
  priority,
  difficulty,
  impact,
  description,
  steps,
  color = 'blue'
}: {
  icon: any;
  title: string;
  priority: 'Haute' | 'Moyenne' | 'Basse';
  difficulty: 'Facile' | 'Moyenne' | 'Difficile';
  impact: string;
  description: string;
  steps: string[];
  color?: string;
}) {
  const priorityColors = {
    'Haute': 'bg-red-500/20 text-red-400',
    'Moyenne': 'bg-yellow-500/20 text-yellow-400',
    'Basse': 'bg-green-500/20 text-green-400',
  };
  
  const difficultyColors = {
    'Facile': 'bg-green-500/20 text-green-400',
    'Moyenne': 'bg-yellow-500/20 text-yellow-400',
    'Difficile': 'bg-red-500/20 text-red-400',
  };

  return (
    <div className="p-5 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-colors">
      <div className="flex items-start gap-4">
        <div className={`p-2 rounded-lg bg-${color}-500/10`}>
          <Icon className={`w-5 h-5 text-${color}-400`} />
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium">{title}</h4>
            <div className="flex gap-2">
              <span className={`px-2 py-0.5 rounded text-xs ${priorityColors[priority]}`}>
                {priority}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs ${difficultyColors[difficulty]}`}>
                {difficulty}
              </span>
            </div>
          </div>
          <p className="text-sm text-neutral-400 mb-3">{description}</p>
          <div className="text-xs text-neutral-500 mb-3">
            <strong className="text-neutral-300">Impact :</strong> {impact}
          </div>
          <div className="space-y-1">
            {steps.map((step, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-neutral-400">
                <span className="text-neutral-600 mt-0.5">{i + 1}.</span>
                <span>{step}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricComparison({ current, potential, unit, label }: {
  current: string;
  potential: string;
  unit: string;
  label: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-white/5 text-center">
      <div className="text-xs text-neutral-500 mb-2">{label}</div>
      <div className="flex items-center justify-center gap-2">
        <span className="text-lg font-medium text-neutral-400">{current}</span>
        <TrendingUp className="w-4 h-4 text-green-400" />
        <span className="text-lg font-medium text-green-400">{potential}</span>
      </div>
      <div className="text-xs text-neutral-500 mt-1">{unit}</div>
    </div>
  );
}

export default function DocsImprovements() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Améliorations</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Améliorations</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Pistes d'amélioration pour optimiser chaque composant de la pipeline THOR.
        </p>
      </div>

      <section className="mb-12">
        <h2 className="text-xl font-semibold mb-4">État actuel</h2>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <Mic className="w-6 h-6 text-blue-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-blue-400">4.8%</div>
            <div className="text-xs text-neutral-500">WER (Whisper)</div>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <Brain className="w-6 h-6 text-purple-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-purple-400">96.3%</div>
            <div className="text-xs text-neutral-500">F1 (spaCy)</div>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <Route className="w-6 h-6 text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-green-400">98%</div>
            <div className="text-xs text-neutral-500">Routes trouvées</div>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 text-center">
            <Clock className="w-6 h-6 text-orange-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-orange-400">~400ms</div>
            <div className="text-xs text-neutral-500">Latence totale</div>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Mic className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold">Speech-to-Text (STT)</h2>
        </div>

        <div className="mb-6 p-4 rounded-lg bg-blue-500/5 border border-blue-500/20">
          <h4 className="font-medium text-blue-400 mb-3">Potentiel d'amélioration</h4>
          <div className="grid md:grid-cols-3 gap-4">
            <MetricComparison current="4.8%" potential="2-3%" unit="WER" label="Taux d'erreur" />
            <MetricComparison current="387ms" potential="~100ms" unit="latence" label="Temps de traitement" />
            <MetricComparison current="1 lang" potential="Multi" unit="langues" label="Support" />
          </div>
        </div>

        <div className="space-y-4">
          <ImprovementCard
            icon={Zap}
            title="Utiliser Whisper Large v3"
            priority="Haute"
            difficulty="Facile"
            impact="WER réduit de 4.8% à ~2.5%, meilleure reconnaissance des noms de gares"
            description="Le modèle Whisper Large v3 offre une précision significativement meilleure, surtout pour les noms propres français."
            steps={[
              "Télécharger le modèle large-v3 (~3GB)",
              "Modifier configs/stt/whisper_small.yaml → whisper_large.yaml",
              "Augmenter la RAM GPU recommandée à 8GB+",
              "Tester sur le dataset de validation"
            ]}
            color="blue"
          />

          <ImprovementCard
            icon={Sparkles}
            title="Fine-tuner Whisper sur le domaine ferroviaire"
            priority="Haute"
            difficulty="Difficile"
            impact="Reconnaissance quasi-parfaite des noms de gares et vocabulaire SNCF"
            description="Entraîner Whisper sur un dataset de phrases ferroviaires améliorerait considérablement la reconnaissance des termes spécifiques."
            steps={[
              "Générer 10,000+ samples audio avec TTS (noms de gares, villes)",
              "Préparer le dataset au format HuggingFace",
              "Fine-tuner avec LoRA pour réduire les ressources",
              "Évaluer sur un test set séparé",
              "Comparer WER avant/après fine-tuning"
            ]}
            color="blue"
          />

          <ImprovementCard
            icon={Zap}
            title="Implémenter Whisper.cpp ou Faster-Whisper"
            priority="Moyenne"
            difficulty="Moyenne"
            impact="Latence réduite de 387ms à ~100ms, CPU-only possible"
            description="Les implémentations optimisées de Whisper offrent des gains de performance significatifs sans perte de qualité."
            steps={[
              "Installer faster-whisper (pip install faster-whisper)",
              "Adapter src/stt/models/whisper.py pour utiliser l'API",
              "Benchmarker latence et précision",
              "Configurer la quantification INT8 pour les déploiements CPU"
            ]}
            color="blue"
          />

          <ImprovementCard
            icon={Globe}
            title="Support multilingue"
            priority="Basse"
            difficulty="Facile"
            impact="Permettre les requêtes en anglais, espagnol, etc."
            description="Whisper supporte nativement 99 langues. Activer la détection automatique de langue permettrait des requêtes internationales."
            steps={[
              "Retirer le paramètre language='fr' dans la config",
              "Adapter le prompt NLP pour les variations linguistiques",
              "Ajouter un mapping des noms de villes internationaux"
            ]}
            color="blue"
          />
        </div>
      </section>

      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-purple-500/10">
            <Brain className="w-5 h-5 text-purple-400" />
          </div>
          <h2 className="text-2xl font-bold">Natural Language Processing (NLP)</h2>
        </div>

        <div className="mb-6 p-4 rounded-lg bg-purple-500/5 border border-purple-500/20">
          <h4 className="font-medium text-purple-400 mb-3">Potentiel d'amélioration</h4>
          <div className="grid md:grid-cols-3 gap-4">
            <MetricComparison current="96.3%" potential="99%+" unit="F1-Score" label="Extraction" />
            <MetricComparison current="10ms" potential="~5ms" unit="latence" label="Temps NLP" />
            <MetricComparison current="2" potential="5+" unit="entités" label="Types extraits" />
          </div>
        </div>

        <div className="space-y-4">
          <ImprovementCard
            icon={Target}
            title="Utiliser un modèle Transformer (CamemBERT)"
            priority="Haute"
            difficulty="Moyenne"
            impact="F1-Score 99%+, meilleure généralisation aux formulations inconnues"
            description="Les modèles Transformer comme CamemBERT offrent une compréhension contextuelle supérieure à spaCy."
            steps={[
              "Installer transformers et adapter le code existant dans src/nlp/models/",
              "Fine-tuner CamemBERT-NER sur le dataset train_nlp.jsonl",
              "Implémenter un fallback vers spaCy si latence critique",
              "Comparer F1 et latence sur le test set"
            ]}
            color="purple"
          />

          <ImprovementCard
            icon={Layers}
            title="Extraire plus d'entités (date, heure, classe)"
            priority="Moyenne"
            difficulty="Moyenne"
            impact="Permettre des requêtes comme 'demain à 14h en première classe'"
            description="Actuellement seules ORIGIN et DESTINATION sont extraites. Ajouter DATE, TIME, CLASS enrichirait les fonctionnalités."
            steps={[
              "Annoter le dataset existant avec les nouvelles entités",
              "Ajouter les labels dans la config spaCy",
              "Re-entraîner le modèle NER",
              "Adapter le pathfinding pour utiliser ces contraintes"
            ]}
            color="purple"
          />

          <ImprovementCard
            icon={Sparkles}
            title="Ajouter un intent classifier"
            priority="Moyenne"
            difficulty="Facile"
            impact="Distinguer 'itinéraire' de 'horaires' de 'prix' de 'infos gare'"
            description="Un classifieur d'intention permettrait d'étendre THOR à d'autres cas d'usage que la recherche d'itinéraire."
            steps={[
              "Créer un dataset d'intents (ROUTE, SCHEDULE, PRICE, INFO)",
              "Entraîner un classifieur simple (LogisticRegression ou petit Transformer)",
              "Router vers différents handlers selon l'intent détecté"
            ]}
            color="purple"
          />

          <ImprovementCard
            icon={Database}
            title="Augmenter le dataset d'entraînement"
            priority="Haute"
            difficulty="Facile"
            impact="Meilleure robustesse aux variations de formulation"
            description="Le dataset actuel contient ~1000 exemples. L'augmenter avec des paraphrases améliorerait la généralisation."
            steps={[
              "Utiliser GPT/Claude pour générer des variations de phrases",
              "Ajouter des exemples avec fautes d'orthographe courantes",
              "Inclure du langage oral (abréviations, contractions)",
              "Valider manuellement les annotations générées"
            ]}
            color="purple"
          />
        </div>
      </section>

      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Route className="w-5 h-5 text-green-400" />
          </div>
          <h2 className="text-2xl font-bold">Pathfinding</h2>
        </div>

        <div className="mb-6 p-4 rounded-lg bg-green-500/5 border border-green-500/20">
          <h4 className="font-medium text-green-400 mb-3">Potentiel d'amélioration</h4>
          <div className="grid md:grid-cols-3 gap-4">
            <MetricComparison current="98%" potential="99.9%" unit="couverture" label="Routes trouvées" />
            <MetricComparison current="5ms" potential="~1ms" unit="latence" label="Temps calcul" />
            <MetricComparison current="Temps" potential="Multi" unit="critères" label="Optimisation" />
          </div>
        </div>

        <div className="space-y-4">
          <ImprovementCard
            icon={Clock}
            title="Intégrer les horaires réels (time-dependent routing)"
            priority="Haute"
            difficulty="Difficile"
            impact="Itinéraires avec heures de départ/arrivée, correspondances réalistes"
            description="Actuellement le pathfinding utilise des temps moyens. Intégrer les horaires GTFS permettrait des itinéraires temporels."
            steps={[
              "Parser calendar_dates.txt et stop_times.txt complet",
              "Implémenter un algorithme time-expanded ou time-dependent",
              "Gérer les correspondances avec temps de changement minimum",
              "Afficher les horaires exacts dans les résultats"
            ]}
            color="green"
          />

          <ImprovementCard
            icon={Zap}
            title="Utiliser A* avec heuristique géographique"
            priority="Moyenne"
            difficulty="Facile"
            impact="Pathfinding 2-3x plus rapide sur les longues distances"
            description="L'algorithme A* avec distance Haversine comme heuristique serait plus efficace que Dijkstra pur."
            steps={[
              "Implémenter A* dans src/pathfinding/models/",
              "Utiliser la distance à vol d'oiseau comme heuristique h(n)",
              "Benchmarker vs Dijkstra sur différentes distances",
              "Ajouter option dans la config pour choisir l'algorithme"
            ]}
            color="green"
          />

          <ImprovementCard
            icon={Target}
            title="Optimisation multi-critères (Pareto)"
            priority="Moyenne"
            difficulty="Moyenne"
            impact="Proposer plusieurs itinéraires : le plus rapide, le moins cher, le moins de correspondances"
            description="Au lieu d'un seul itinéraire optimal, proposer un front de Pareto avec différents compromis."
            steps={[
              "Définir les critères : temps, correspondances, confort, CO2",
              "Implémenter un algorithme multi-objectif (NAMOA*, MOSP)",
              "Retourner 3-5 alternatives dans l'API",
              "Adapter le frontend pour afficher les alternatives"
            ]}
            color="green"
          />

          <ImprovementCard
            icon={Map}
            title="Améliorer la couverture des géométries"
            priority="Basse"
            difficulty="Moyenne"
            impact="100% des trajets avec tracé réaliste sur la carte (actuellement ~60%)"
            description="Certaines liaisons n'ont pas de géométrie associée. Améliorer le matching ou interpoler les tracés manquants."
            steps={[
              "Analyser les liaisons sans géométrie (type de train, distance)",
              "Améliorer l'algorithme de matching (tolérance, multi-segments)",
              "Pour les cas restants, interpoler avec une courbe de Bézier",
              "Utiliser des données OSM Railway comme source alternative"
            ]}
            color="green"
          />

          <ImprovementCard
            icon={Globe}
            title="Étendre au réseau européen"
            priority="Basse"
            difficulty="Difficile"
            impact="Itinéraires Paris-Londres, Paris-Bruxelles, etc."
            description="Intégrer les données GTFS des réseaux voisins (Eurostar, Thalys, DB, SBB) pour des itinéraires internationaux."
            steps={[
              "Collecter les GTFS européens (EU Open Data Portal)",
              "Harmoniser les formats et codes UIC",
              "Créer des liaisons de correspondance aux frontières",
              "Gérer les fuseaux horaires"
            ]}
            color="green"
          />
        </div>
      </section>

      <section className="mb-12">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-orange-500/10">
            <Layers className="w-5 h-5 text-orange-400" />
          </div>
          <h2 className="text-2xl font-bold">Infrastructure & UX</h2>
        </div>

        <div className="space-y-4">
          <ImprovementCard
            icon={Zap}
            title="Streaming de la réponse STT"
            priority="Haute"
            difficulty="Moyenne"
            impact="Feedback instantané pendant l'enregistrement vocal"
            description="Afficher la transcription en temps réel pendant que l'utilisateur parle, comme les assistants vocaux modernes."
            steps={[
              "Implémenter WebSocket pour le streaming audio",
              "Utiliser Whisper en mode streaming (chunks de 30s)",
              "Afficher la transcription partielle côté frontend",
              "Lancer le NLP dès que la phrase est complète"
            ]}
            color="orange"
          />

          <ImprovementCard
            icon={Database}
            title="Cache des résultats fréquents"
            priority="Moyenne"
            difficulty="Facile"
            impact="Réponse instantanée pour Paris-Lyon, Paris-Marseille, etc."
            description="Les trajets populaires représentent 80% des requêtes. Les mettre en cache réduirait la latence à ~10ms."
            steps={[
              "Identifier les 100 trajets les plus demandés",
              "Implémenter un cache Redis ou in-memory",
              "Définir une politique d'invalidation (TTL 24h)",
              "Mesurer le hit rate et ajuster"
            ]}
            color="orange"
          />

          <ImprovementCard
            icon={Globe}
            title="Progressive Web App (PWA)"
            priority="Basse"
            difficulty="Facile"
            impact="Application installable, mode offline partiel"
            description="Transformer le site en PWA permettrait une utilisation hors-ligne et une expérience native sur mobile."
            steps={[
              "Ajouter un manifest.json et service worker",
              "Cacher les assets statiques et le dataset des gares",
              "Permettre la recherche offline (suggestions)",
              "Ajouter les notifications pour les alertes trafic"
            ]}
            color="orange"
          />

          <ImprovementCard
            icon={Target}
            title="Tests end-to-end automatisés"
            priority="Haute"
            difficulty="Moyenne"
            impact="Détection automatique des régressions, CI/CD robuste"
            description="Actuellement les tests sont manuels. Automatiser avec Playwright et un test set golden."
            steps={[
              "Configurer Playwright pour le frontend",
              "Créer un golden test set de 50 requêtes avec résultats attendus",
              "Intégrer dans GitHub Actions",
              "Alerter si WER ou F1 se dégradent"
            ]}
            color="orange"
          />
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-4">Matrice de priorité</h2>
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-green-400 mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Quick Wins (Facile + Impact élevé)
              </h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>• Whisper Large v3</li>
                <li>• Augmentation du dataset NLP</li>
                <li>• Cache des trajets fréquents</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-blue-400 mb-3 flex items-center gap-2">
                <Target className="w-4 h-4" /> Projets majeurs (Difficile + Impact élevé)
              </h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>• Fine-tuning Whisper ferroviaire</li>
                <li>• Horaires temps réel</li>
                <li>• CamemBERT NER</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-yellow-400 mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" /> Nice to have (Facile + Impact faible)
              </h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>• Support multilingue</li>
                <li>• PWA</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-neutral-400 mb-3 flex items-center gap-2">
                <Clock className="w-4 h-4" /> Long terme (Difficile + Impact faible)
              </h4>
              <ul className="space-y-2 text-sm text-neutral-400">
                <li>• Réseau européen</li>
                <li>• Optimisation Pareto complète</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
