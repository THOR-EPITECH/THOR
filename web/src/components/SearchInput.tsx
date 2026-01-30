'use client';

import { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, ArrowRight, Loader2 } from 'lucide-react';

interface SearchInputProps {
  onSearch: (text: string) => void;
  onVoiceResult: (result: any) => void;
  isLoading: boolean;
}

export default function SearchInput({ onSearch, onVoiceResult, isLoading }: SearchInputProps) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  // Vérifier si MediaRecorder est supporté
  const [recordingSupported, setRecordingSupported] = useState(false);
  
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setRecordingSupported(!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
    }
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Essayer d'abord webm, sinon fallback sur le format par défaut
      let mimeType = 'audio/webm;codecs=opus';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'audio/webm';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
          mimeType = ''; // Utiliser le format par défaut du navigateur
        }
      }
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: mimeType || undefined
      });
      
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        // Arrêter tous les tracks
        stream.getTracks().forEach(track => track.stop());
        
        // Convertir en blob puis en base64
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendAudioToPipeline(audioBlob);
      };
      
      mediaRecorder.start();
      mediaRecorderRef.current = mediaRecorder;
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Impossible d\'accéder au microphone. Vérifiez les permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Convertir un blob audio en WAV
  const convertToWav = async (audioBlob: Blob): Promise<Blob> => {
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    
    // Paramètres WAV
    const sampleRate = audioBuffer.sampleRate;
    const numberOfChannels = audioBuffer.numberOfChannels;
    const length = audioBuffer.length;
    
    // Créer le buffer WAV
    const wavBuffer = new ArrayBuffer(44 + length * numberOfChannels * 2);
    const view = new DataView(wavBuffer);
    
    // En-tête WAV
    const writeString = (offset: number, string: string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };
    
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + length * numberOfChannels * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true); // Taille du format
    view.setUint16(20, 1, true); // Format PCM
    view.setUint16(22, numberOfChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numberOfChannels * 2, true);
    view.setUint16(32, numberOfChannels * 2, true);
    view.setUint16(34, 16, true); // Bits par sample
    writeString(36, 'data');
    view.setUint32(40, length * numberOfChannels * 2, true);
    
    // Convertir les données audio en 16-bit PCM
    let offset = 44;
    for (let i = 0; i < length; i++) {
      for (let channel = 0; channel < numberOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, audioBuffer.getChannelData(channel)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
    }
    
    return new Blob([wavBuffer], { type: 'audio/wav' });
  };

  const sendAudioToPipeline = async (audioBlob: Blob) => {
    setIsProcessing(true);
    
    try {
      // Convertir en WAV
      const wavBlob = await convertToWav(audioBlob);
      
      // Convertir le blob WAV en base64
      const base64Audio = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          const result = reader.result as string;
          // Enlever le préfixe data:audio/wav;base64,
          const base64 = result.includes(',') ? result.split(',')[1] : result;
          resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(wavBlob);
      });
      
      const response = await fetch('/api/pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          audio: base64Audio,
          format: 'wav'
        }),
      });

      // Vérifier le Content-Type avant de parser
      const contentType = response.headers.get('content-type');
      let data;
      
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Réponse non-JSON:', text);
        throw new Error(`Réponse invalide du serveur (${response.status}): ${text.substring(0, 200)}`);
      }

      data = await response.json();

      if (!response.ok) {
        console.error('Erreur API:', data);
        throw new Error(data.error || data.message || `Erreur ${response.status} lors du traitement audio`);
      }

      // Afficher la transcription dans le champ
      if (data.transcript) {
        setText(data.transcript);
      }

      // Passer le résultat complet au parent
      onVoiceResult(data);
    } catch (error) {
      console.error('Error processing audio:', error);
      const errorMessage = error instanceof Error ? error.message : 'Erreur lors du traitement audio';
      alert(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSearch(text.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={isRecording ? "🎤 Enregistrement en cours..." : isProcessing ? "⏳ Traitement..." : "De Paris à Bordeaux..."}
          disabled={isLoading || isRecording || isProcessing}
          className="w-full h-14 px-5 pr-28 bg-white/5 border border-white/10 rounded-xl text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition-colors"
        />
        
        <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
          {/* Mic button - enregistrement audio */}
          <button
            type="button"
            onClick={toggleRecording}
            disabled={isLoading || isProcessing || !recordingSupported}
            title={recordingSupported ? (isRecording ? "Arrêter l'enregistrement" : "Parler (enregistrement audio)") : "Enregistrement audio non supporté"}
            className={`p-2.5 rounded-lg transition-colors ${
              !recordingSupported
                ? 'text-neutral-700 cursor-not-allowed'
                : isRecording 
                  ? 'bg-red-500/20 text-red-400 animate-pulse' 
                  : isProcessing
                    ? 'text-neutral-600 cursor-not-allowed'
                    : 'text-neutral-500 hover:text-white hover:bg-white/5'
            }`}
          >
            {isRecording ? (
              <MicOff className="w-5 h-5" />
            ) : (
              <Mic className="w-5 h-5" />
            )}
          </button>
          
          {/* Submit button */}
          <button
            type="submit"
            disabled={!text.trim() || isLoading || isRecording || isProcessing}
            className="p-2.5 rounded-lg bg-white text-black hover:bg-neutral-200 disabled:opacity-30 disabled:hover:bg-white transition-all"
          >
            {isLoading || isProcessing ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <ArrowRight className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>

      {/* Recording indicator */}
      {isRecording && (
        <div className="flex items-center justify-center gap-1.5 mt-4">
          <span className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
          <span className="text-sm text-neutral-500">Enregistrement en cours... Cliquez sur le micro pour arrêter</span>
        </div>
      )}
      
      {isProcessing && (
        <div className="flex items-center justify-center gap-1.5 mt-4">
          <Loader2 className="w-4 h-4 animate-spin text-neutral-500" />
          <span className="text-sm text-neutral-500">Traitement audio avec Whisper...</span>
        </div>
      )}
    </form>
  );
}
