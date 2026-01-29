'use client';

import { useEffect, useState } from 'react';
import { Segment } from '@/types';
import { getStationPosition } from '@/data/stations';

interface RouteMapProps {
  segments: Segment[];
  steps: string[];
}

export default function RouteMap({ segments, steps }: RouteMapProps) {
  const [MapComponent, setMapComponent] = useState<React.ComponentType<RouteMapProps> | null>(null);

  useEffect(() => {
    // Import dynamique pour éviter les erreurs SSR
    import('./RouteMapClient').then((mod) => {
      setMapComponent(() => mod.default);
    });
  }, []);

  if (!MapComponent) {
    return (
      <div className="w-full h-[400px] bg-slate-900/50 rounded-xl flex items-center justify-center border border-slate-700/50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-slate-400 text-sm">Chargement de la carte...</span>
        </div>
      </div>
    );
  }

  return <MapComponent segments={segments} steps={steps} />;
}

// Fonction utilitaire pour obtenir les positions
export function getRoutePositions(steps: string[]): Array<{ name: string; lat: number; lon: number }> {
  return steps
    .map(step => {
      const pos = getStationPosition(step);
      if (pos) {
        return { name: step, ...pos };
      }
      return null;
    })
    .filter((p): p is { name: string; lat: number; lon: number } => p !== null);
}
