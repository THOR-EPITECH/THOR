import {
  ArrowRight,
  Mic,
  Brain,
  Route,
  Layers,
  CheckCircle2,
  XCircle,
  Trophy,
  Zap,
  Target,
  Database,
  GitBranch,
  Box,
  ArrowDown,
  Train,
} from "lucide-react";

function Badge({ variant }: { variant: "chosen" | "tested" | "rejected" }) {
  const styles = {
    chosen: "bg-green-500/20 text-green-400 border-green-500/30",
    tested: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    rejected: "bg-red-500/20 text-red-400 border-red-500/30",
  };
  const labels = {
    chosen: "Choisi",
    tested: "Testé",
    rejected: "Non retenu",
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs border ${styles[variant]}`}>
      {labels[variant]}
    </span>
  );
}

function ProgressBar({
  value,
  max,
  color = "green",
}: {
  value: number;
  max: number;
  color?: string;
}) {
  const percentage = (value / max) * 100;
  const colorClasses: Record<string, string> = {
    green: "bg-green-500",
    yellow: "bg-yellow-500",
    red: "bg-red-500",
    blue: "bg-blue-500",
    purple: "bg-purple-500",
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

function MetricRow({
  label,
  value,
  percentage,
  best = false,
}: {
  label: string;
  value: string;
  percentage: number;
  best?: boolean;
}) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-40 text-sm text-neutral-400">{label}</div>
      <div className="flex-1">
        <ProgressBar
          value={percentage}
          max={100}
          color={best ? "green" : "yellow"}
        />
      </div>
      <div
        className={`w-24 text-right text-sm font-mono ${best ? "text-green-400" : "text-neutral-300"}`}
      >
        {value}
      </div>
    </div>
  );
}

function DiagramBox({
  children,
  className = "",
  highlight = false,
}: {
  children: React.ReactNode;
  className?: string;
  highlight?: boolean;
}) {
  return (
    <div
      className={`p-3 rounded-lg border text-center text-sm ${
        highlight
          ? "bg-green-500/10 border-green-500/30 text-green-400"
          : "bg-white/5 border-white/10 text-neutral-300"
      } ${className}`}
    >
      {children}
    </div>
  );
}

function DiagramArrow({
  direction = "right",
}: {
  direction?: "right" | "down";
}) {
  if (direction === "down") {
    return (
      <div className="flex justify-center py-2">
        <ArrowDown className="w-4 h-4 text-neutral-500" />
      </div>
    );
  }
  return (
    <div className="flex items-center px-2">
      <ArrowRight className="w-4 h-4 text-neutral-500" />
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
        <code className="text-sm text-neutral-300 whitespace-pre">
          {children}
        </code>
      </pre>
    </div>
  );
}

function JustificationCard({
  title,
  description,
  points,
}: {
  title: string;
  description: string;
  points: string[];
}) {
  return (
    <div className="p-4 rounded-lg bg-white/5 border border-white/10">
      <h4 className="font-medium text-white mb-2">{title}</h4>
      <p className="text-sm text-neutral-400 mb-3">{description}</p>
      <ul className="space-y-1">
        {points.map((point, i) => (
          <li
            key={i}
            className="flex items-start gap-2 text-xs text-neutral-400"
          >
            <CheckCircle2 className="w-3 h-3 text-green-400 mt-0.5 shrink-0" />
            <span>{point}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function DocsDecisions() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Recherche</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Justification des choix</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Justification des Choix</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Documentation détaillée des décisions architecturales et techniques du
          projet THOR, avec métriques comparatives et justifications basées sur
          les benchmarks.
        </p>
      </div>

      {/* Section 1: Architecture Pipeline */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Layers className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold">Architecture Pipeline</h2>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-neutral-400" />
            Flux de données
          </h3>

          {/* Pipeline Diagram */}
          <div className="p-6 rounded-lg bg-[#0d0d0d] border border-white/10 mb-6">
            <div className="flex flex-col lg:flex-row items-center justify-center gap-2 lg:gap-0">
              <DiagramBox className="w-full lg:w-auto">
                <div className="flex items-center gap-2 justify-center mb-1">
                  <Mic className="w-4 h-4 text-blue-400" />
                  <span className="font-medium">Audio</span>
                </div>
                <div className="text-xs text-neutral-500">WAV / WebM</div>
              </DiagramBox>

              <DiagramArrow />

              <DiagramBox className="w-full lg:w-auto">
                <div className="flex items-center gap-2 justify-center mb-1">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  <span className="font-medium">STT</span>
                </div>
                <div className="text-xs text-neutral-500">Whisper</div>
              </DiagramBox>

              <DiagramArrow />

              <DiagramBox className="w-full lg:w-auto">
                <div className="flex items-center gap-2 justify-center mb-1">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <span className="font-medium">NLP</span>
                </div>
                <div className="text-xs text-neutral-500">spaCy fine-tuné</div>
              </DiagramBox>

              <DiagramArrow />

              <DiagramBox className="w-full lg:w-auto" highlight>
                <div className="flex items-center gap-2 justify-center mb-1">
                  <Route className="w-4 h-4 text-green-400" />
                  <span className="font-medium">Pathfinding</span>
                </div>
                <div className="text-xs text-green-400/70">Dijkstra</div>
              </DiagramBox>
            </div>

            {/* Output types */}
            <div className="mt-6 grid grid-cols-1 lg:grid-cols-4 gap-4 text-xs">
              <div className="p-2 rounded bg-white/5 text-center">
                <div className="text-neutral-500 mb-1">Entrée</div>
                <code className="text-blue-400">audio_file</code>
              </div>
              <div className="p-2 rounded bg-white/5 text-center">
                <div className="text-neutral-500 mb-1">STTResult</div>
                <code className="text-yellow-400">text, confidence</code>
              </div>
              <div className="p-2 rounded bg-white/5 text-center">
                <div className="text-neutral-500 mb-1">NLPExtraction</div>
                <code className="text-purple-400">origin, destination</code>
              </div>
              <div className="p-2 rounded bg-white/5 text-center">
                <div className="text-neutral-500 mb-1">Route</div>
                <code className="text-green-400">steps[], total_time</code>
              </div>
            </div>
          </div>

          <h3 className="font-semibold mb-4">Principes architecturaux</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <JustificationCard
              title="Séparation modulaire"
              description="Interfaces abstraites STTModel, NLPModel, PathfindingModel"
              points={[
                "Test unitaire de chaque module en isolation",
                "Échange de modèles sans modifier le code client",
                "Complexité divisée par 3 (debug facilité)",
              ]}
            />
            <JustificationCard
              title="Registry dynamique"
              description="ModelRegistry avec lazy loading des modèles"
              points={[
                "Startup rapide (~200ms vs ~3s sans lazy loading)",
                "Configuration YAML sans recompilation",
                "Ajout de nouveaux modèles = 1 décorateur",
              ]}
            />
            <JustificationCard
              title="Types standardisés"
              description="Dataclasses STTResult, NLPExtraction, Route"
              points={[
                "Contrat explicite entre modules",
                "Validation automatique des données",
                "Sérialisation JSON native (API)",
              ]}
            />
            <JustificationCard
              title="Validation en couches"
              description="TranscriptValidator, CityValidator, ExtractionValidator"
              points={[
                "Détection précoce des erreurs",
                "Suggestions de correction automatiques",
                "Métriques de confiance explicables",
              ]}
            />
          </div>
        </div>

        {/* Registry diagram */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-4">Système de Registry</h3>
          <CodeBlock title="src/common/registry.py">{`class ModelRegistry:
    _registry = {
        "stt": {
            "whisper": WhisperModel,      # GPU optionnel
            "vosk": VoskModel,            # CPU only
            "dummy": DummySTTModel
        },
        "nlp": {
            "spacy_finetuned": SpacyNLPModel,   # ◀ CHOISI
            "regex_advanced": RegexAdvancedModel,
            "transformers": TransformersNERModel
        },
        "pathfinding": {
            "dijkstra": DijkstraModel     # Temps pondéré
        }
    }
    
    @classmethod
    def get(cls, module_type: str, model_name: str):
        return cls._registry[module_type][model_name]`}</CodeBlock>
        </div>
      </section>

      {/* Section 2: STT Choice */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Mic className="w-5 h-5 text-blue-400" />
          </div>
          <h2 className="text-2xl font-bold">Choix STT : Whisper vs Vosk</h2>
        </div>

        {/* Process comparison diagram */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6">Comparaison des processus</h3>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Whisper process */}
            <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-medium text-green-400">Whisper (small)</h4>
                <Badge variant="chosen" />
              </div>

              <div className="space-y-2">
                <DiagramBox>Audio (tout format)</DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>librosa → 16kHz mono</DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>Transformer Encoder-Decoder</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    39M → 1.5B paramètres
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox highlight>
                  <div>"Je veux aller de Paris."</div>
                  <div className="text-xs text-green-400/70 mt-1">
                    Ponctuation + Majuscules
                  </div>
                </DiagramBox>
              </div>
            </div>

            {/* Vosk process */}
            <div className="p-4 rounded-lg bg-yellow-500/5 border border-yellow-500/20">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-medium text-yellow-400">Vosk</h4>
                <Badge variant="tested" />
              </div>

              <div className="space-y-2">
                <DiagramBox>
                  <div>Audio (WAV 16kHz uniquement)</div>
                  <div className="text-xs text-red-400 mt-1">
                    ⚠ Format strict
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>Chunks de 4000 samples</DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>Kaldi (CTC + HMM-GMM)</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    Modèle français pré-entraîné
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>"je veux aller de paris"</div>
                  <div className="text-xs text-yellow-400/70 mt-1">
                    Texte brut uniquement
                  </div>
                </DiagramBox>
              </div>
            </div>
          </div>
        </div>

        {/* Metrics comparison */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <Target className="w-4 h-4 text-neutral-400" />
            Métriques comparatives (30 échantillons)
          </h3>

          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium">Whisper (small)</span>
                <Badge variant="chosen" />
              </div>
              <div className="space-y-2">
                <MetricRow
                  label="WER (erreur mots)"
                  value="29.13%"
                  percentage={70.87}
                  best
                />
                <MetricRow
                  label="CER (erreur caractères)"
                  value="12.24%"
                  percentage={87.76}
                  best
                />
                <MetricRow
                  label="Transcriptions parfaites"
                  value="16.7%"
                  percentage={16.7}
                  best
                />
                <MetricRow
                  label="Latence moyenne"
                  value="387ms"
                  percentage={60}
                />
              </div>
            </div>

            <div className="border-t border-white/5 pt-6">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium">Vosk</span>
                <Badge variant="tested" />
              </div>
              <div className="space-y-2">
                <MetricRow
                  label="WER (erreur mots)"
                  value="48.12%"
                  percentage={51.88}
                />
                <MetricRow
                  label="CER (erreur caractères)"
                  value="16.05%"
                  percentage={83.95}
                />
                <MetricRow
                  label="Transcriptions parfaites"
                  value="0%"
                  percentage={0}
                />
                <MetricRow
                  label="Latence moyenne"
                  value="118ms"
                  percentage={90}
                  best
                />
              </div>
            </div>
          </div>
        </div>

        {/* Justification */}
        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div>
              <h4 className="font-medium text-green-400 mb-3">
                Justification du choix Whisper
              </h4>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    1. Précision critique pour le NLP
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    Les erreurs STT se propagent au NLP : une erreur de
                    transcription peut rendre l'extraction d'entités impossible.
                  </p>
                  <div className="p-2 rounded bg-white/5 text-xs font-mono">
                    <div className="text-green-400">
                      WER 29% vs 48% = <strong>40% moins d'erreurs</strong>
                    </div>
                    <div className="text-neutral-500 mt-1">
                      transmises au module NLP
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    2. Transcriptions parfaites
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    Seul Whisper produit des transcriptions sans aucune erreur.
                  </p>
                  <div className="p-2 rounded bg-white/5 text-xs font-mono">
                    <div className="text-green-400">
                      Whisper: 16.7% parfaites (5/30)
                    </div>
                    <div className="text-red-400">
                      Vosk: 0% parfaites (0/30)
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    3. Post-traitement automatique
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    Whisper ajoute ponctuation et majuscules, facilitant la
                    détection des noms propres.
                  </p>
                  <div className="space-y-1 text-xs font-mono">
                    <div className="text-green-400">
                      "Je veux aller de Paris à Lyon."
                    </div>
                    <div className="text-yellow-400">
                      "je veux aller de paris à lyon"
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    4. Trade-off latence acceptable
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    387ms reste bien inférieur au seuil de perception humaine
                    (~500ms).
                  </p>
                  <div className="p-2 rounded bg-white/5 text-xs font-mono">
                    <div className="text-neutral-300">
                      RTF = 0.16 (6× plus rapide que temps réel)
                    </div>
                    <div className="text-neutral-500 mt-1">
                      GPU optionnel pour applications critiques
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: NLP Choice */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-purple-500/10">
            <Brain className="w-5 h-5 text-purple-400" />
          </div>
          <h2 className="text-2xl font-bold">
            Choix NLP : spaCy fine-tuné vs Regex vs Transformers
          </h2>
        </div>

        {/* Process comparison */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6">
            Comparaison des approches d'extraction
          </h3>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Regex */}
            <div className="p-4 rounded-lg bg-yellow-500/5 border border-yellow-500/20">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-medium text-yellow-400">Regex Advanced</h4>
                <Badge variant="tested" />
              </div>

              <div className="space-y-2">
                <DiagramBox>"Je veux aller de Paris à Lyon"</DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>100+ patterns prédéfinis</div>
                  <div className="text-xs text-neutral-500 mt-1 font-mono">
                    /depuis (\w+)/, /de (\w+) à/
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>Match dans liste de ~100 villes</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    Hardcodé, non extensible
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>origin="Paris", dest="Lyon"</div>
                  <div className="text-xs text-red-400 mt-1">
                    ⚠ Limité aux patterns connus
                  </div>
                </DiagramBox>
              </div>
            </div>

            {/* spaCy fine-tuned */}
            <div className="p-4 rounded-lg bg-green-500/5 border border-green-500/20">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-medium text-green-400">spaCy fine-tuné</h4>
                <Badge variant="chosen" />
              </div>

              <div className="space-y-2">
                <DiagramBox>"Je veux aller de Paris à Lyon"</DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>Tokenization + POS tagging</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    Analyse syntaxique complète
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>Embeddings fr_core_news_md</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    40MB, contexte sémantique
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox>
                  <div>NER: labels ORIGIN + DESTINATION</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    Fine-tuné 20 iter, dropout 0.1
                  </div>
                </DiagramBox>
                <DiagramArrow direction="down" />
                <DiagramBox highlight>
                  <div>origin="Paris", dest="Lyon"</div>
                  <div className="text-xs text-green-400/70 mt-1">
                    ✓ Apprend de nouveaux patterns
                  </div>
                </DiagramBox>
              </div>
            </div>
          </div>
        </div>

        {/* Training process diagram */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6">Processus d'entraînement spaCy</h3>

          <div className="p-4 rounded-lg bg-[#0d0d0d] border border-white/10">
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <DiagramBox>
                <Database className="w-4 h-4 text-blue-400 mx-auto mb-1" />
                <div>Données annotées</div>
                <div className="text-xs text-neutral-500">
                  JSONL, 438 samples
                </div>
              </DiagramBox>
              <DiagramBox>
                <Box className="w-4 h-4 text-purple-400 mx-auto mb-1" />
                <div>Modèle de base</div>
                <div className="text-xs text-neutral-500">fr_core_news_md</div>
              </DiagramBox>
              <DiagramBox highlight>
                <Brain className="w-4 h-4 text-green-400 mx-auto mb-1" />
                <div>Modèle fine-tuné</div>
                <div className="text-xs text-green-400/70">
                  ORIGIN + DESTINATION
                </div>
              </DiagramBox>
            </div>

            <div className="p-4 rounded bg-white/5 text-sm">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <div className="text-neutral-500 mb-2">Configuration</div>
                  <div className="space-y-1 font-mono text-xs">
                    <div>
                      <span className="text-purple-400">n_iter:</span> 20
                    </div>
                    <div>
                      <span className="text-purple-400">dropout:</span> 0.1
                    </div>
                    <div>
                      <span className="text-purple-400">batch_size:</span> 4 →
                      32 (compounding)
                    </div>
                    <div>
                      <span className="text-purple-400">labels:</span>{" "}
                      ["ORIGIN", "DESTINATION"]
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-neutral-500 mb-2">Processus</div>
                  <div className="space-y-1 text-xs text-neutral-400">
                    <div>1. Charger fr_core_news_md</div>
                    <div>2. Ajouter labels ORIGIN/DESTINATION au NER</div>
                    <div>3. Créer Examples à partir du JSONL</div>
                    <div>4. 20 itérations SGD avec validation</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Metrics table */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <Target className="w-4 h-4 text-neutral-400" />
            Métriques comparatives (test_nlp.jsonl)
          </h3>

          <div className="rounded-xl border border-white/10 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-white/5">
                  <th className="text-left p-4 font-medium">Modèle</th>
                  <th className="text-left p-4 font-medium">F1-Score</th>
                  <th className="text-left p-4 font-medium">Origine</th>
                  <th className="text-left p-4 font-medium">Destination</th>
                  <th className="text-left p-4 font-medium">Les 2</th>
                  <th className="text-left p-4 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <tr className="bg-green-500/5">
                  <td className="p-4 flex items-center gap-2">
                    <Trophy className="w-4 h-4 text-green-400" />
                    <span className="font-medium">spaCy fine-tuné</span>
                  </td>
                  <td className="p-4 text-green-400 font-mono font-bold">
                    0.621
                  </td>
                  <td className="p-4 text-green-400 font-mono">94.98%</td>
                  <td className="p-4 text-green-400 font-mono">83.90%</td>
                  <td className="p-4 text-green-400 font-mono">83.68%</td>
                  <td className="p-4">
                    <Badge variant="chosen" />
                  </td>
                </tr>
                <tr>
                  <td className="p-4">regex_advanced</td>
                  <td className="p-4 font-mono text-neutral-400">0.430</td>
                  <td className="p-4 font-mono text-neutral-400">80.82%</td>
                  <td className="p-4 font-mono text-red-400">29.57%</td>
                  <td className="p-4 font-mono text-red-400">27.05%</td>
                  <td className="p-4">
                    <Badge variant="tested" />
                  </td>
                </tr>
                <tr>
                  <td className="p-4">spaCy (base)</td>
                  <td className="p-4 font-mono text-neutral-400">0.407</td>
                  <td className="p-4 font-mono text-neutral-400">72.60%</td>
                  <td className="p-4 font-mono text-neutral-400">42.24%</td>
                  <td className="p-4 font-mono text-neutral-400">40.75%</td>
                  <td className="p-4">
                    <Badge variant="tested" />
                  </td>
                </tr>
                <tr>
                  <td className="p-4 text-neutral-500">
                    Transformers (CamemBERT)
                  </td>
                  <td className="p-4 text-red-400">Erreur</td>
                  <td className="p-4 text-neutral-500">-</td>
                  <td className="p-4 text-neutral-500">-</td>
                  <td className="p-4 text-neutral-500">-</td>
                  <td className="p-4">
                    <Badge variant="rejected" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Justification */}
        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-green-400 mb-3">
                Justification du choix spaCy fine-tuné
              </h4>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    1. Amélioration F1 de +53%
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    Le fine-tuning permet au modèle d'apprendre les labels
                    ORIGIN/DESTINATION spécifiques à notre cas d'usage.
                  </p>
                  <div className="p-2 rounded bg-white/5 text-xs font-mono">
                    <div>
                      Regex: <span className="text-yellow-400">F1 = 0.43</span>
                    </div>
                    <div>
                      spaCy finetuned:{" "}
                      <span className="text-green-400">F1 = 0.62</span> (+53%)
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    2. Précision destination corrigée
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    La regex échoue sur les destinations complexes ou
                    implicites.
                  </p>
                  <div className="p-2 rounded bg-white/5 text-xs font-mono">
                    <div>
                      Regex: <span className="text-red-400">29.57%</span>{" "}
                      destinations
                    </div>
                    <div>
                      spaCy: <span className="text-green-400">83.90%</span>{" "}
                      (+183%)
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    3. Compréhension contextuelle
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    spaCy comprend le contexte sémantique, pas seulement les
                    patterns.
                  </p>
                  <div className="space-y-1 text-xs">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3 h-3 text-green-400" />
                      <span className="text-neutral-300">
                        "de Paris" → ORIGIN
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <XCircle className="w-3 h-3 text-red-400" />
                      <span className="text-neutral-400">
                        "le Paris-Brest express" → ignoré
                      </span>
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    4. Pourquoi pas Transformers ?
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    CamemBERT a échoué sur notre dataset de test.
                  </p>
                  <div className="space-y-1 text-xs text-neutral-400">
                    <div>• Erreur à l'exécution</div>
                    <div>• Empreinte mémoire 10× supérieure (~400MB)</div>
                    <div>• Nécessite GPU pour latence acceptable</div>
                  </div>
                </div>
              </div>

              {/* Limitations regex détaillées */}
              <div className="mt-4 p-4 rounded-lg bg-red-500/5 border border-red-500/20">
                <h5 className="text-sm font-medium text-red-400 mb-3">
                  Pourquoi le Regex est insuffisant
                </h5>
                <div className="grid md:grid-cols-2 gap-4 text-xs">
                  <div>
                    <div className="text-neutral-500 mb-2">Cas non gérés :</div>
                    <ul className="space-y-1 text-neutral-400">
                      <li>• Typos : "parir" → Paris non reconnu</li>
                      <li>• Destinations implicites : "vers chez moi"</li>
                      <li>• Structures complexes : "en passant par Avignon"</li>
                      <li>• Variations régionales : "sur Marseille"</li>
                    </ul>
                  </div>
                  <div>
                    <div className="text-neutral-500 mb-2">
                      Limites structurelles :
                    </div>
                    <ul className="space-y-1 text-neutral-400">
                      <li>• ~100 villes hardcodées seulement</li>
                      <li>• Recall 39% vs 62% (−37%)</li>
                      <li>• Pas d'apprentissage possible</li>
                      <li>• Maintenance manuelle des patterns</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 4: Pathfinding Choice */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Route className="w-5 h-5 text-green-400" />
          </div>
          <h2 className="text-2xl font-bold">
            Choix Pathfinding : Dijkstra avec pénalités
          </h2>
        </div>

        {/* Algorithm diagram */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6">Algorithme de Dijkstra</h3>

          <div className="p-4 rounded-lg bg-[#0d0d0d] border border-white/10">
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <div className="p-3 rounded bg-white/5">
                <div className="text-xs text-neutral-500 mb-1">
                  Complexité temps
                </div>
                <div className="font-mono text-blue-400">O((V + E) log V)</div>
              </div>
              <div className="p-3 rounded bg-white/5">
                <div className="text-xs text-neutral-500 mb-1">
                  Nœuds (gares)
                </div>
                <div className="font-mono text-green-400">2,782</div>
              </div>
              <div className="p-3 rounded bg-white/5">
                <div className="text-xs text-neutral-500 mb-1">
                  Arêtes (liaisons)
                </div>
                <div className="font-mono text-purple-400">7,852</div>
              </div>
            </div>

            <CodeBlock title="Pseudo-code Dijkstra avec pénalités">{`function dijkstra(graph, origin, destination):
    distances = {node: ∞ for all nodes}
    distances[origin] = 0
    parent = {}
    priority_queue = [(0, origin)]
    
    while priority_queue not empty:
        current_dist, current = pop_min(priority_queue)
        
        if current == destination:
            return reconstruct_path(parent)
        
        for neighbor, edge_data in graph.neighbors(current):
            # ◀ PÉNALITÉ : temps × multiplicateur selon type de train
            weight = edge_data.temps_min × PENALTY[edge_data.type_train]
            
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = current
                push(priority_queue, (new_dist, neighbor))
    
    return None  # Pas de chemin trouvé`}</CodeBlock>
          </div>
        </div>

        {/* Penalty system */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <Train className="w-4 h-4 text-neutral-400" />
            Système de pénalités par type de train
          </h3>

          <div className="rounded-xl border border-white/10 overflow-hidden mb-6">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-white/5">
                  <th className="text-left p-4 font-medium">Type de train</th>
                  <th className="text-left p-4 font-medium">Pénalité</th>
                  <th className="text-left p-4 font-medium">Justification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                <tr className="bg-green-500/5">
                  <td className="p-4 font-medium">
                    TGV, OUIGO, Lyria, Eurostar
                  </td>
                  <td className="p-4 font-mono text-green-400">×1.0</td>
                  <td className="p-4 text-neutral-400">
                    Priorité maximale : rapide, confortable
                  </td>
                </tr>
                <tr>
                  <td className="p-4">Intercités</td>
                  <td className="p-4 font-mono text-yellow-400">×1.3</td>
                  <td className="p-4 text-neutral-400">
                    +30% pour favoriser TGV quand disponible
                  </td>
                </tr>
                <tr>
                  <td className="p-4">Train de nuit</td>
                  <td className="p-4 font-mono text-yellow-400">×1.5</td>
                  <td className="p-4 text-neutral-400">
                    Lent mais utile pour longues distances
                  </td>
                </tr>
                <tr>
                  <td className="p-4">TER, Navette</td>
                  <td className="p-4 font-mono text-orange-400">×2.0</td>
                  <td className="p-4 text-neutral-400">
                    Régional, nombreux arrêts
                  </td>
                </tr>
                <tr>
                  <td className="p-4">Auto-train</td>
                  <td className="p-4 font-mono text-red-400">×2.5</td>
                  <td className="p-4 text-neutral-400">
                    Très lent, cas spécifique
                  </td>
                </tr>
                <tr className="bg-blue-500/5">
                  <td className="p-4">Correspondance (métro)</td>
                  <td className="p-4 font-mono text-blue-400">×1.0</td>
                  <td className="p-4 text-neutral-400">
                    Transfert inter-gare, neutre
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Example */}
          <div className="p-4 rounded-lg bg-white/5">
            <h4 className="font-medium text-white mb-3">
              Exemple : Paris → Lyon
            </h4>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="p-3 rounded bg-green-500/10 border border-green-500/30">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-green-400">TGV</span>
                  <span className="text-xs text-green-400">◀ CHOISI</span>
                </div>
                <div className="text-sm font-mono">
                  120 min × 1.0 ={" "}
                  <span className="text-green-400 font-bold">120</span>
                </div>
              </div>
              <div className="p-3 rounded bg-white/5 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-neutral-400">TER</span>
                  <span className="text-xs text-neutral-500">Non retenu</span>
                </div>
                <div className="text-sm font-mono">
                  180 min × 2.0 = <span className="text-neutral-400">360</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Graph construction */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6 flex items-center gap-2">
            <Database className="w-4 h-4 text-neutral-400" />
            Construction du graphe depuis les données SNCF
          </h3>

          <div className="p-4 rounded-lg bg-[#0d0d0d] border border-white/10">
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <DiagramBox>
                <div className="font-medium mb-1">stop_times.txt</div>
                <div className="text-xs text-neutral-500">
                  Horaires réels GTFS
                </div>
              </DiagramBox>
              <DiagramBox>
                <div className="font-medium mb-1">dataset_gares.json</div>
                <div className="text-xs text-neutral-500">UIC, GPS, noms</div>
              </DiagramBox>
              <DiagramBox>
                <div className="font-medium mb-1">shapes.json</div>
                <div className="text-xs text-neutral-500">
                  Géométries GeoJSON
                </div>
              </DiagramBox>
            </div>

            <DiagramArrow direction="down" />

            <div className="p-4 rounded bg-white/5 mb-4">
              <div className="text-sm font-medium text-center mb-2">
                scripts/generate_enhanced_graph.py
              </div>
              <div className="grid md:grid-cols-2 gap-4 text-xs text-neutral-400">
                <div>
                  <div className="text-neutral-500 mb-1">Extraction :</div>
                  <ul className="space-y-1">
                    <li>• Codes UIC (8 chiffres) via regex</li>
                    <li>• Arrêts consécutifs par trip_id</li>
                    <li>• Type train : OCETGV, OCEOUIGO, OCETER...</li>
                  </ul>
                </div>
                <div>
                  <div className="text-neutral-500 mb-1">
                    Agrégation par liaison :
                  </div>
                  <ul className="space-y-1">
                    <li>• temps_moyen_min : moyenne observée</li>
                    <li>• temps_min_min : minimum observé</li>
                    <li>• nb_trains : fréquence journalière</li>
                  </ul>
                </div>
              </div>
            </div>

            <DiagramArrow direction="down" />

            <DiagramBox highlight>
              <div className="font-medium mb-1">NetworkX Graph</div>
              <div className="text-xs text-green-400/70">
                2,782 nœuds × 7,852 arêtes
              </div>
              <div className="text-xs text-neutral-500 mt-1">
                Poids = temps (min) × pénalité
              </div>
            </DiagramBox>
          </div>
        </div>

        {/* Multi-station handling */}
        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5 mb-6">
          <h3 className="font-semibold mb-6">Gestion des villes multi-gares</h3>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-white mb-3">
                Système de scoring
              </h4>
              <div className="p-4 rounded-lg bg-white/5">
                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-neutral-400">Nom exact</span>
                    <span className="text-green-400">+200</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">
                      Préfixe ville + station
                    </span>
                    <span className="text-green-400">+100</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">
                      Gare principale (Part-Dieu, St-Charles)
                    </span>
                    <span className="text-blue-400">+50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">Station TGV</span>
                    <span className="text-blue-400">+30</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">Par connexion</span>
                    <span className="text-neutral-500">+2</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">
                      Aéroport / banlieue
                    </span>
                    <span className="text-red-400">-20</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-white mb-3">
                Exemple : Paris
              </h4>
              <div className="p-4 rounded-lg bg-white/5">
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between items-center">
                    <span>Paris Gare de Lyon</span>
                    <span className="font-mono text-green-400">+350</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Paris Montparnasse</span>
                    <span className="font-mono text-green-400">+340</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Paris Nord</span>
                    <span className="font-mono text-blue-400">+320</span>
                  </div>
                  <div className="flex justify-between items-center text-neutral-500">
                    <span>Paris Bercy</span>
                    <span className="font-mono">+180</span>
                  </div>
                  <div className="flex justify-between items-center text-neutral-500">
                    <span>Paris CDG Aéroport</span>
                    <span className="font-mono">+80</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Justification */}
        <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
          <div className="flex items-start gap-3">
            <Trophy className="w-5 h-5 text-green-400 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-medium text-green-400 mb-3">
                Justification du choix Dijkstra
              </h4>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    1. Optimalité garantie
                  </h5>
                  <p className="text-xs text-neutral-400">
                    Dijkstra trouve toujours le chemin de poids minimal. Crucial
                    pour un système de recommandation de trajets.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    2. Pourquoi pas A* ?
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    A* nécessite une heuristique admissible.
                  </p>
                  <div className="text-xs text-red-400">
                    Problème : temps ≠ distance euclidienne
                    <br />→ Heuristique invalide → perte d'optimalité
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    3. Optimisation par le temps
                  </h5>
                  <p className="text-xs text-neutral-400">
                    Les utilisateurs optimisent leur{" "}
                    <strong className="text-white">temps de trajet</strong>, pas
                    les kilomètres. Le système de pénalités encode cette
                    préférence.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-white/5">
                  <h5 className="text-sm font-medium text-white mb-2">
                    4. Performance suffisante
                  </h5>
                  <p className="text-xs text-neutral-400 mb-2">
                    Avec 2,782 nœuds et 7,852 arêtes :
                  </p>
                  <div className="text-xs font-mono text-green-400">
                    Temps moyen: {"<"}50ms par recherche
                  </div>
                </div>
              </div>

              {/* Correspondances Paris */}
              <div className="mt-4 p-4 rounded-lg bg-blue-500/5 border border-blue-500/20">
                <h5 className="text-sm font-medium text-blue-400 mb-3">
                  Correspondances inter-gares Paris
                </h5>
                <p className="text-xs text-neutral-400 mb-3">
                  Arêtes spéciales pour les transferts métro entre gares
                  parisiennes :
                </p>
                <div className="grid md:grid-cols-3 gap-2 text-xs">
                  <div className="p-2 rounded bg-white/5 text-center">
                    <div className="text-neutral-300">Montparnasse ↔ Lyon</div>
                    <div className="text-neutral-500">~15 min</div>
                  </div>
                  <div className="p-2 rounded bg-white/5 text-center">
                    <div className="text-neutral-300">Lyon ↔ Nord</div>
                    <div className="text-neutral-500">~15 min</div>
                  </div>
                  <div className="p-2 rounded bg-white/5 text-center">
                    <div className="text-neutral-300">Montparnasse ↔ Nord</div>
                    <div className="text-neutral-500">~20 min</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 5: Data Pipeline */}
      <section className="mb-16">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-orange-500/10">
            <Database className="w-5 h-5 text-orange-400" />
          </div>
          <h2 className="text-2xl font-bold">Données et prétraitement</h2>
        </div>

        <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
          <h3 className="font-semibold mb-6">Pipeline de données complète</h3>

          <div className="p-4 rounded-lg bg-[#0d0d0d] border border-white/10">
            {/* Sources */}
            <div className="mb-4">
              <div className="text-xs text-neutral-500 mb-2">
                1. SOURCES BRUTES
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                <DiagramBox>
                  <div className="font-medium text-blue-400">GTFS SNCF</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    stop_times.txt, stops.txt
                  </div>
                  <div className="text-xs text-neutral-400 mt-1">
                    Horaires officiels
                  </div>
                </DiagramBox>
                <DiagramBox>
                  <div className="font-medium text-purple-400">
                    OpenData Gares
                  </div>
                  <div className="text-xs text-neutral-500 mt-1">
                    dataset_gares.csv
                  </div>
                  <div className="text-xs text-neutral-400 mt-1">
                    2,782 gares France
                  </div>
                </DiagramBox>
                <DiagramBox>
                  <div className="font-medium text-green-400">Géométries</div>
                  <div className="text-xs text-neutral-500 mt-1">
                    shapes.json
                  </div>
                  <div className="text-xs text-neutral-400 mt-1">
                    LineString GeoJSON
                  </div>
                </DiagramBox>
              </div>
            </div>

            <DiagramArrow direction="down" />

            {/* Processing */}
            <div className="mb-4">
              <div className="text-xs text-neutral-500 mb-2">
                2. SCRIPTS DE TRAITEMENT
              </div>
              <div className="p-4 rounded bg-white/5">
                <div className="grid md:grid-cols-2 gap-4 text-xs">
                  <div>
                    <code className="text-purple-400">
                      generate_enhanced_graph.py
                    </code>
                    <ul className="mt-2 space-y-1 text-neutral-400">
                      <li>• Extraction codes UIC depuis stop_id</li>
                      <li>• Calcul temps trajet entre arrêts consécutifs</li>
                      <li>• Identification type train (TGV, TER, etc.)</li>
                    </ul>
                  </div>
                  <div>
                    <code className="text-purple-400">
                      train_station_converter.py
                    </code>
                    <ul className="mt-2 space-y-1 text-neutral-400">
                      <li>• Normalisation noms de villes</li>
                      <li>• Construction aliases (Saint/St, etc.)</li>
                      <li>• Index ville → [gares]</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <DiagramArrow direction="down" />

            {/* Outputs */}
            <div>
              <div className="text-xs text-neutral-500 mb-2">
                3. DONNÉES PRODUITES
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                <DiagramBox highlight>
                  <div className="font-medium">
                    dataset_liaisons_enhanced.json
                  </div>
                  <div className="text-xs text-green-400/70 mt-1">
                    7,852 liaisons
                  </div>
                  <div className="text-xs text-neutral-500 mt-1">
                    temps min/moy/max, type train
                  </div>
                </DiagramBox>
                <DiagramBox highlight>
                  <div className="font-medium">dataset_gares.json</div>
                  <div className="text-xs text-green-400/70 mt-1">
                    2,782 gares
                  </div>
                  <div className="text-xs text-neutral-500 mt-1">
                    UIC, GPS, commune
                  </div>
                </DiagramBox>
                <DiagramBox highlight>
                  <div className="font-medium">dataset_villes.json</div>
                  <div className="text-xs text-green-400/70 mt-1">
                    Aliases + index
                  </div>
                  <div className="text-xs text-neutral-500 mt-1">
                    Recherche fuzzy
                  </div>
                </DiagramBox>
              </div>
            </div>
          </div>

          {/* Justification */}
          <div className="mt-6 grid md:grid-cols-2 gap-4">
            <JustificationCard
              title="Données SNCF officielles"
              description="Source de vérité pour les temps de trajet"
              points={[
                "Horaires réels (pas estimations)",
                "Couverture nationale exhaustive",
                "Mise à jour régulière (GTFS)",
              ]}
            />
            <JustificationCard
              title="Optimisation par le temps"
              description="Métrique alignée avec les besoins utilisateurs"
              points={[
                "Temps de trajet = critère principal",
                "Distance euclidienne non représentative",
                "TGV Paris-Lyon plus rapide malgré détours",
              ]}
            />
          </div>
        </div>
      </section>

      {/* Summary */}
      <section className="mb-8">
        <div className="p-6 rounded-xl bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-white/10">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-green-400" />
            Résumé des choix finaux
          </h2>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-2">
                <Mic className="w-4 h-4 text-blue-400" />
                <span className="font-medium">STT</span>
              </div>
              <div className="text-lg font-bold text-green-400 mb-1">
                Whisper (small)
              </div>
              <div className="text-xs text-neutral-400">
                WER 29% | 387ms latence
              </div>
            </div>

            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-2">
                <Brain className="w-4 h-4 text-purple-400" />
                <span className="font-medium">NLP</span>
              </div>
              <div className="text-lg font-bold text-green-400 mb-1">
                spaCy fine-tuné
              </div>
              <div className="text-xs text-neutral-400">
                F1 0.62 | 84% destination
              </div>
            </div>

            <div className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center gap-2 mb-2">
                <Route className="w-4 h-4 text-green-400" />
                <span className="font-medium">Pathfinding</span>
              </div>
              <div className="text-lg font-bold text-green-400 mb-1">
                Dijkstra + pénalités
              </div>
              <div className="text-xs text-neutral-400">
                {"<"}50ms | Optimal garanti
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
