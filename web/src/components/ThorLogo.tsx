/**
 * Logo THOR : Mjölnir dont le manche est un éclair.
 * Hérite de la couleur du texte (currentColor).
 */
export default function ThorLogo({ className = "w-6 h-6" }: { className?: string }) {
  return (
    <svg viewBox="0 0 48 48" fill="currentColor" className={className} aria-hidden="true">
      <rect x="7" y="5" width="34" height="15" rx="3" />
      <path d="M27 20 22 31h5l-8 13 13-16h-6l7-8z" />
    </svg>
  );
}
