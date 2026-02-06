/**
 * Composant de saisie de recherche avec support vocal.
 * 
 * Ce composant permet à l'utilisateur de :
 * - Saisir manuellement une requête de trajet
 * - Utiliser la reconnaissance vocale via le microphone
 * - Soumettre la recherche
 * 
 * L'enregistrement audio est converti en WAV avant l'envoi au backend.
 * 
 * @module components/SearchInput
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { Mic, ArrowRight, Loader2 } from 'lucide-react';

/**
 * Props du composant SearchInput.
 * 
 * @interface SearchInputProps
 * @property {Function} onSearch - Callback appelé lors de la soumission d'une recherche textuelle
 * @property {Function} onVoiceResult - Callback appelé avec le résultat complet du traitement vocal
 * @property {boolean} isLoading - Indique si une recherche est en cours
 */
interface SearchInputProps {
  onSearch: (text: string) => void;
  onVoiceResult: (result: any) => void;
  isLoading: boolean;
}

/**
 * Composant de recherche avec saisie textuelle et vocale.
 * 
 * @param {SearchInputProps} props - Props du composant
 * @returns {JSX.Element} Formulaire de recherche
 * 
 * @example
 * <SearchInput 
 *   onSearch={(text) => console.log('Search:', text)}
 *   onVoiceResult={(result) => console.log('Voice result:', result)}
 *   isLoading={false}
 * />
 */
export default function SearchInput({ onSearch, onVoiceResult, isLoading }: SearchInputProps) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  /** Indique si l'enregistrement audio est supporté par le navigateur */
  const [recordingSupported, setRecordingSupported] = useState(false);
  
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setRecordingSupported(!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
    }
  }, []);

  /**
   * Démarre l'enregistrement audio via le microphone.
   * 
   * Demande l'accès au microphone, configure le MediaRecorder avec le format
   * webm/opus si supporté, et commence l'enregistrement.
   * 
   * @async
   * @throws {Error} Si l'accès au microphone est refusé
   */
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Déterminer le meilleur format audio supporté
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
        stream.getTracks().forEach(track => track.stop());
        
        // Convertir l'audio en blob et l'envoyer au backend
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

  /**
   * Arrête l'enregistrement audio en cours.
   * 
   * Déclenche l'événement onstop du MediaRecorder qui envoie l'audio au backend.
   */
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  /**
   * Convertit un Blob audio (webm, etc) en format WAV.
   * 
   * Utilise l'API Web Audio pour décoder l'audio et le réencoder en WAV PCM 16-bit.
   * 
   * @param {Blob} audioBlob - Blob audio source à convertir
   * @returns {Promise<Blob>} Blob audio au format WAV
   */
  const convertToWav = async (audioBlob: Blob): Promise<Blob> => {
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    
    // Configuration de l'encodage WAV
    const sampleRate = audioBuffer.sampleRate;
    const numberOfChannels = audioBuffer.numberOfChannels;
    const length = audioBuffer.length;
    
    // Allouer le buffer pour le fichier WAV (44 bytes header + audio data)
    const wavBuffer = new ArrayBuffer(44 + length * numberOfChannels * 2);
    const view = new DataView(wavBuffer);
    
    // Écrire l'en-tête WAV (format RIFF)
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
    
    // Encoder les samples audio en PCM 16-bit
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

  /**
   * Envoie l'audio enregistré au pipeline backend pour traitement.
   * 
   * L'audio est converti en WAV, encodé en base64, puis envoyé via l'API /api/pipeline.
   * Le résultat complet (transcription + itinéraire) est retourné via onVoiceResult.
   * 
   * @param {Blob} audioBlob - Blob audio à traiter
   * @async
   */
  const sendAudioToPipeline = async (audioBlob: Blob) => {
    setIsProcessing(true);
    
    try {
      // Étape 1: Conversion en format WAV
      const wavBlob = await convertToWav(audioBlob);
      
      // Étape 2: Encodage en base64 pour transmission
      const base64Audio = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          const result = reader.result as string;
          // Retirer le préfixe data URL pour n'avoir que le base64
          const base64 = result.includes(',') ? result.split(',')[1] : result;
          resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(wavBlob);
      });
      
      // Étape 3: Envoi au backend pour traitement
      const response = await fetch('/api/pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          audio: base64Audio,
          format: 'wav'
        }),
      });

      // Validation de la réponse
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

      // Mise à jour de l'UI avec la transcription
      if (data.transcript) {
        setText(data.transcript);
      }

      // Transmission du résultat complet au composant parent
      onVoiceResult(data);
    } catch (error) {
      console.error('Error processing audio:', error);
      const errorMessage = error instanceof Error ? error.message : 'Erreur lors du traitement audio';
      alert(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * Bascule l'état d'enregistrement (démarrer/arrêter).
   */
  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  /**
   * Gère la soumission du formulaire de recherche textuelle.
   * 
   * @param {React.FormEvent} e - Événement de soumission du formulaire
   */
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
          placeholder={isRecording ? "Enregistrement en cours..." : isProcessing ? "Traitement..." : "De Paris à Bordeaux..."}
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
              <span className="relative flex h-5 w-5 items-center justify-center">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75" />
                <span className="relative inline-flex h-3 w-3 rounded-full bg-red-500" />
              </span>
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
