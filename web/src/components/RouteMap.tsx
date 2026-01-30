'use client';

import { useEffect, useState } from 'react';
import { Segment } from '@/types';
import { Loader2 } from 'lucide-react';

interface RouteMapProps {
  segments: Segment[];
}

export default function RouteMap({ segments }: RouteMapProps) {
  const [MapComponent, setMapComponent] = useState<React.ComponentType<RouteMapProps> | null>(null);

  useEffect(() => {
    import('./RouteMapClient').then((mod) => {
      setMapComponent(() => mod.default);
    });
  }, []);

  if (!MapComponent) {
    return (
      <div className="w-full h-[400px] bg-white/[0.02] border border-white/5 rounded-xl flex items-center justify-center">
        <Loader2 className="w-5 h-5 animate-spin text-neutral-500" />
      </div>
    );
  }

  return <MapComponent segments={segments} />;
}
