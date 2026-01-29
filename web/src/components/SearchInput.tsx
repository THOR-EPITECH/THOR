'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Mic, MicOff, Search, Loader2, Sparkles } from 'lucide-react';

interface SearchInputProps {
  onSearch: (text: string) => void;
  isLoading: boolean;
}

export default function SearchInput({ onSearch, isLoading }: SearchInputProps) {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  useEffect(() => {
    // Vérifier si la Web Speech API est supportée
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      setSpeechSupported(!!SpeechRecognition);
      
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'fr-FR';
        
        recognition.onresult = (event) => {
          const transcript = Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');
          setText(transcript);
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
        
        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
      }
    }
    
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setText('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSearch(text.trim());
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative group">
        {/* Effet de lueur */}
        <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-pink-500/20 rounded-2xl blur-lg opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />
        
        <div className="relative flex items-center gap-2 p-2 bg-slate-900/90 backdrop-blur-xl rounded-2xl border border-slate-700/50 group-focus-within:border-cyan-500/50 transition-colors">
          {/* Bouton micro */}
          {speechSupported && (
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={toggleListening}
              disabled={isLoading}
              className={`relative rounded-xl transition-all duration-300 ${
                isListening 
                  ? 'bg-rose-500/20 text-rose-400 hover:bg-rose-500/30' 
                  : 'text-slate-400 hover:text-cyan-400 hover:bg-cyan-500/10'
              }`}
            >
              {isListening ? (
                <>
                  <MicOff className="w-5 h-5" />
                  <span className="absolute inset-0 rounded-xl animate-ping bg-rose-500/20" />
                </>
              ) : (
                <Mic className="w-5 h-5" />
              )}
            </Button>
          )}
          
          {/* Input texte */}
          <div className="flex-1 relative">
            <Input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={isListening ? "Je vous écoute..." : "Ex: Je veux aller de Paris à Bordeaux"}
              disabled={isLoading || isListening}
              className="border-0 bg-transparent text-white placeholder:text-slate-500 focus-visible:ring-0 focus-visible:ring-offset-0 text-base py-6"
            />
            {isListening && (
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                <span className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            )}
          </div>
          
          {/* Bouton rechercher */}
          <Button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white px-6 py-6 transition-all duration-300 disabled:opacity-50"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <Search className="w-5 h-5 mr-2" />
                Rechercher
              </>
            )}
          </Button>
        </div>
      </div>
      
      {/* Suggestions */}
      <div className="flex flex-wrap gap-2 mt-4 justify-center">
        {['Paris → Bordeaux', 'Lyon → Marseille', 'Paris → Rennes', 'Toulouse → Bordeaux'].map((suggestion) => (
          <button
            key={suggestion}
            type="button"
            onClick={() => {
              setText(`Je veux aller de ${suggestion.replace(' → ', ' à ')}`);
            }}
            className="px-3 py-1.5 text-sm text-slate-400 bg-slate-800/50 hover:bg-slate-700/50 rounded-full border border-slate-700/50 hover:border-cyan-500/30 transition-all duration-200 flex items-center gap-1.5"
          >
            <Sparkles className="w-3 h-3" />
            {suggestion}
          </button>
        ))}
      </div>
    </form>
  );
}

// Déclaration des types pour la Web Speech API
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}
