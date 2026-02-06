/**
 * Composant d'affichage des erreurs et suggestions.
 * 
 * Affiche de manière claire et contextuelle :
 * - Le type d'erreur
 * - Les problèmes détectés
 * - Les suggestions pour corriger
 * 
 * @module components/ErrorDisplay
 */

'use client';

import { AlertCircle, AlertTriangle, Lightbulb, X } from 'lucide-react';

/**
 * Props du composant ErrorDisplay.
 * 
 * @interface ErrorDisplayProps
 * @property {string} errorMessage - Message d'erreur principal
 * @property {string} [errorType] - Type d'erreur pour l'icône et le style
 * @property {string[]} [issues] - Liste des problèmes détectés
 * @property {string[]} [suggestions] - Liste des suggestions
 * @property {Function} [onClose] - Callback pour fermer l'erreur
 */
interface ErrorDisplayProps {
  errorMessage: string;
  errorType?: string;
  issues?: string[];
  suggestions?: string[];
  onClose?: () => void;
}

/**
 * Composant d'affichage complet des erreurs avec suggestions.
 * 
 * @param {ErrorDisplayProps} props - Props du composant
 * @returns {JSX.Element} Affichage de l'erreur
 */
export default function ErrorDisplay({ 
  errorMessage, 
  errorType, 
  issues, 
  suggestions,
  onClose 
}: ErrorDisplayProps) {
  const getErrorStyle = () => {
    switch (errorType) {
      case 'transcript_invalid':
      case 'no_cities_detected':
      case 'same_origin_destination':
        return {
          bg: 'bg-red-500/10',
          border: 'border-red-500/30',
          text: 'text-red-400',
          icon: <AlertCircle className="w-5 h-5" />
        };
      case 'extraction_errors':
      case 'no_route_found':
        return {
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/30',
          text: 'text-yellow-400',
          icon: <AlertTriangle className="w-5 h-5" />
        };
      default:
        return {
          bg: 'bg-orange-500/10',
          border: 'border-orange-500/30',
          text: 'text-orange-400',
          icon: <AlertCircle className="w-5 h-5" />
        };
    }
  };

  const style = getErrorStyle();

  return (
    <div className={`rounded-xl border ${style.border} ${style.bg} p-6 animate-fade-in`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 flex-1">
          <div className={`mt-0.5 ${style.text}`}>
            {style.icon}
          </div>
          
          <div className="flex-1 space-y-4">
            <div>
              <h3 className={`font-medium ${style.text} mb-1`}>
                {errorMessage}
              </h3>
            </div>

            {issues && issues.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm text-neutral-400 font-medium">Problèmes détectés :</p>
                <ul className="space-y-1.5">
                  {issues.map((issue, idx) => (
                    <li key={idx} className="text-sm text-neutral-300 flex items-start gap-2">
                      <span className="text-neutral-500 mt-1">•</span>
                      <span>{issue}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {suggestions && suggestions.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-white/5">
                <div className="flex items-center gap-2 text-sm text-neutral-400 font-medium">
                  <Lightbulb className="w-4 h-4" />
                  <span>Suggestions :</span>
                </div>
                <ul className="space-y-2">
                  {suggestions.map((suggestion, idx) => (
                    <li key={idx} className="text-sm text-neutral-300 flex items-start gap-2 bg-white/5 rounded-lg p-3">
                      <span className="text-green-400 font-bold">→</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="text-neutral-500 hover:text-white transition-colors p-1"
            title="Fermer"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}
