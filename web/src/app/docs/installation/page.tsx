import { ArrowRight, CheckCircle2, AlertCircle, Terminal } from 'lucide-react';

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

function Step({ number, title, children }: { number: number; title: string; children: React.ReactNode }) {
  return (
    <div className="relative pl-12 pb-8 border-l border-white/10 last:border-0 last:pb-0">
      <div className="absolute left-0 -translate-x-1/2 w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm font-mono">
        {number}
      </div>
      <h3 className="font-semibold mb-3 text-lg">{title}</h3>
      <div className="space-y-4 text-neutral-400">{children}</div>
    </div>
  );
}

export default function DocsInstallation() {
  return (
    <div>
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">Installation</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Installation</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Guide complet pour installer et configurer THOR sur votre machine.
        </p>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Prérequis</h2>
        <div className="grid gap-3">
          {[
            { name: 'Python', version: '3.9 ou supérieur', required: true },
            { name: 'Node.js', version: '18 ou supérieur', required: true },
            { name: 'Git', version: 'Dernière version', required: true },
            { name: 'FFmpeg', version: 'Optionnel (pour Whisper)', required: false },
          ].map((item) => (
            <div 
              key={item.name}
              className="flex items-center justify-between p-4 rounded-lg bg-white/[0.02] border border-white/5"
            >
              <div className="flex items-center gap-3">
                {item.required ? (
                  <CheckCircle2 className="w-4 h-4 text-green-400" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-yellow-400" />
                )}
                <span className="font-medium">{item.name}</span>
              </div>
              <span className="text-sm text-neutral-500">{item.version}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-8">Étapes d'installation</h2>
        
        <div className="space-y-2">
          <Step number={1} title="Cloner le dépôt">
            <p>Clonez le projet depuis GitHub :</p>
            <CodeBlock title="Terminal">{`git clone https://github.com/THOR-EPITECH/THOR.git
cd THOR`}</CodeBlock>
          </Step>

          <Step number={2} title="Configurer l'environnement Python">
            <p>Créez et activez un environnement virtuel :</p>
            <CodeBlock title="Terminal">{`python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\\Scripts\\activate    # Windows`}</CodeBlock>
            <p>Installez les dépendances :</p>
            <CodeBlock title="Terminal">{`pip install -r requirements.txt`}</CodeBlock>
          </Step>

          <Step number={3} title="Télécharger le modèle spaCy">
            <p>Le modèle français de spaCy est nécessaire pour le NLP :</p>
            <CodeBlock title="Terminal">{`python -m spacy download fr_core_news_md`}</CodeBlock>
          </Step>

          <Step number={4} title="Générer les datasets">
            <p>Les scripts de génération préparent les données pour le pathfinding :</p>
            <CodeBlock title="Terminal">{`# Générer le graphe des liaisons avec temps réels
python3 scripts/generate_enhanced_graph.py

# Générer les tracés géographiques des voies
python3 scripts/generate_railway_shapes.py`}</CodeBlock>
          </Step>

          <Step number={5} title="Lancer le backend Flask">
            <p>Démarrez l'API Python avec préchargement des modèles :</p>
            <CodeBlock title="Terminal">{`python3 api/app.py --preload`}</CodeBlock>
            <div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/20">
              <div className="flex items-start gap-3">
                <Terminal className="w-4 h-4 text-blue-400 mt-0.5" />
                <div className="text-sm">
                  <p className="text-blue-300 font-medium">Note</p>
                  <p className="text-blue-200/70">
                    L'option <code className="px-1.5 py-0.5 bg-blue-500/20 rounded">--preload</code> charge 
                    Whisper au démarrage pour des réponses plus rapides.
                  </p>
                </div>
              </div>
            </div>
          </Step>

          <Step number={6} title="Lancer le frontend Next.js">
            <p>Dans un nouveau terminal, installez et lancez le frontend :</p>
            <CodeBlock title="Terminal">{`cd web
npm install
npm run dev`}</CodeBlock>
            <p>
              L'application sera accessible sur{' '}
              <code className="px-2 py-1 bg-white/5 rounded text-green-400">
                http://localhost:3000
              </code>
            </p>
          </Step>
        </div>
      </div>

      <div className="p-6 rounded-xl bg-green-500/5 border border-green-500/20">
        <h3 className="font-semibold text-green-400 mb-3 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5" />
          Vérification
        </h3>
        <p className="text-sm text-neutral-400 mb-4">
          Pour vérifier que tout fonctionne, testez l'API health check :
        </p>
        <CodeBlock>{`curl http://localhost:8000/api/health`}</CodeBlock>
        <p className="text-sm text-neutral-500 mt-4">
          Vous devriez recevoir une réponse JSON avec le statut "ok" et les modèles chargés.
        </p>
      </div>
    </div>
  );
}
