import { ArrowRight, Mic, CheckCircle2, Settings, Zap, Clock, AlertCircle } from 'lucide-react';

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

export default function DocsSTT() {
  return (
    <div>
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center gap-2 text-sm text-neutral-500 mb-4">
          <span>Docs</span>
          <ArrowRight className="w-3 h-3" />
          <span>Pipeline</span>
          <ArrowRight className="w-3 h-3" />
          <span className="text-white">STT (Whisper)</span>
        </div>
        <h1 className="text-4xl font-bold mb-4">Speech-to-Text</h1>
        <p className="text-xl text-neutral-400 leading-relaxed">
          Module de reconnaissance vocale utilisant le modèle Whisper d'OpenAI 
          pour une transcription précise du français.
        </p>
      </div>

      {/* What is Whisper */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Qu'est-ce que Whisper ?</h2>
        <div className="prose prose-invert max-w-none">
          <p className="text-neutral-400">
            Whisper est un modèle de reconnaissance vocale automatique (ASR) développé par OpenAI. 
            Il a été entraîné sur 680 000 heures d'audio multilingue et multitâche, ce qui lui 
            permet de transcrire l'audio en texte avec une précision remarquable.
          </p>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/10">
            <CheckCircle2 className="w-5 h-5 text-blue-400 mb-2" />
            <h4 className="font-medium mb-1">Multilingue</h4>
            <p className="text-xs text-neutral-400">Supporte 99+ langues dont le français</p>
          </div>
          <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/10">
            <Zap className="w-5 h-5 text-blue-400 mb-2" />
            <h4 className="font-medium mb-1">Robuste</h4>
            <p className="text-xs text-neutral-400">Résistant au bruit et aux accents</p>
          </div>
        </div>
      </div>

      {/* Model sizes */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Tailles de modèle</h2>
        <div className="rounded-xl border border-white/10 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-white/5">
                <th className="text-left p-4 font-medium">Modèle</th>
                <th className="text-left p-4 font-medium">Paramètres</th>
                <th className="text-left p-4 font-medium">VRAM</th>
                <th className="text-left p-4 font-medium">Vitesse</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              <tr>
                <td className="p-4"><code className="text-blue-400">tiny</code></td>
                <td className="p-4 text-neutral-400">39M</td>
                <td className="p-4 text-neutral-400">~1 GB</td>
                <td className="p-4"><span className="text-green-400">~32x</span></td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-blue-400">base</code></td>
                <td className="p-4 text-neutral-400">74M</td>
                <td className="p-4 text-neutral-400">~1 GB</td>
                <td className="p-4"><span className="text-green-400">~16x</span></td>
              </tr>
              <tr className="bg-green-500/5">
                <td className="p-4">
                  <code className="text-green-400">small</code>
                  <span className="ml-2 px-2 py-0.5 rounded text-xs bg-green-500/20 text-green-400">recommandé</span>
                </td>
                <td className="p-4 text-neutral-400">244M</td>
                <td className="p-4 text-neutral-400">~2 GB</td>
                <td className="p-4"><span className="text-yellow-400">~6x</span></td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-blue-400">medium</code></td>
                <td className="p-4 text-neutral-400">769M</td>
                <td className="p-4 text-neutral-400">~5 GB</td>
                <td className="p-4"><span className="text-orange-400">~2x</span></td>
              </tr>
              <tr>
                <td className="p-4"><code className="text-blue-400">large</code></td>
                <td className="p-4 text-neutral-400">1550M</td>
                <td className="p-4 text-neutral-400">~10 GB</td>
                <td className="p-4"><span className="text-red-400">1x</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="text-sm text-neutral-500 mt-4">
          * Vitesse relative par rapport au modèle "large". Plus le nombre est élevé, plus c'est rapide.
        </p>
      </div>

      {/* Configuration */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Settings className="w-6 h-6 text-neutral-400" />
          Configuration
        </h2>
        
        <CodeBlock title="configs/stt/whisper_small.yaml">{`name: whisper
model_size: small
language: fr
device: cpu  # ou "cuda" pour GPU
compute_type: float32`}</CodeBlock>

        <div className="mt-6 space-y-4">
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center justify-between mb-2">
              <code className="text-sm text-blue-400">model_size</code>
              <span className="text-xs text-neutral-500">string</span>
            </div>
            <p className="text-sm text-neutral-400">
              Taille du modèle Whisper à utiliser. Options : tiny, base, small, medium, large.
            </p>
          </div>
          
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center justify-between mb-2">
              <code className="text-sm text-blue-400">language</code>
              <span className="text-xs text-neutral-500">string</span>
            </div>
            <p className="text-sm text-neutral-400">
              Code de langue ISO 639-1. Utiliser "fr" pour le français.
            </p>
          </div>
          
          <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
            <div className="flex items-center justify-between mb-2">
              <code className="text-sm text-blue-400">device</code>
              <span className="text-xs text-neutral-500">string</span>
            </div>
            <p className="text-sm text-neutral-400">
              Device de calcul. "cpu" pour processeur, "cuda" pour GPU NVIDIA.
            </p>
          </div>
        </div>
      </div>

      {/* Usage */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Utilisation</h2>
        
        <h3 className="font-semibold mb-3">Via la CLI</h3>
        <CodeBlock title="Terminal">{`python3 -m src.cli.stt \\
  --audio data/raw/audio/sample.wav \\
  --model whisper \\
  --output results/stt/`}</CodeBlock>

        <h3 className="font-semibold mb-3 mt-6">Via Python</h3>
        <CodeBlock title="Python">{`from src.stt.models.whisper import WhisperSTT

# Initialiser le modèle
stt = WhisperSTT(model_size="small", language="fr")

# Transcrire un fichier audio
result = stt.transcribe("path/to/audio.wav")

print(result.text)       # Texte transcrit
print(result.confidence) # Score de confiance`}</CodeBlock>
      </div>

      {/* Formats */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Formats audio supportés</h2>
        <div className="grid grid-cols-4 gap-3">
          {['WAV', 'MP3', 'M4A', 'FLAC', 'OGG', 'WEBM', 'MP4', 'MPEG'].map((format) => (
            <div key={format} className="p-3 rounded-lg bg-white/[0.02] border border-white/5 text-center">
              <code className="text-sm text-neutral-300">{format}</code>
            </div>
          ))}
        </div>
        <div className="mt-4 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-yellow-400 mt-0.5" />
            <div className="text-sm">
              <p className="text-yellow-300 font-medium">Recommandation</p>
              <p className="text-yellow-200/70">
                Pour de meilleurs résultats, utilisez le format WAV 16kHz mono.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Performance */}
      <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5 text-neutral-400" />
          Performance
        </h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-white mb-1">~0.5s</div>
            <div className="text-neutral-500">Temps de transcription (5s audio, small)</div>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <div className="text-2xl font-bold text-white mb-1">98%+</div>
            <div className="text-neutral-500">Précision WER français</div>
          </div>
        </div>
      </div>
    </div>
  );
}
