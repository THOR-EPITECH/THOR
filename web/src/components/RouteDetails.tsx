'use client';

import { Route, Segment } from '@/types';
import { Clock, MapPin, ArrowRight } from 'lucide-react';

interface RouteDetailsProps {
  route: Route;
}

function formatTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  if (hours === 0) return `${mins}min`;
  return `${hours}h${mins.toString().padStart(2, '0')}`;
}

function getTrainTypeStyle(type: string) {
  switch (type) {
    case 'TGV':
      return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
    case 'OUIGO':
      return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
    case 'Intercités':
      return 'bg-violet-500/10 text-violet-400 border-violet-500/20';
    case 'TER':
      return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    default:
      return 'bg-neutral-500/10 text-neutral-400 border-neutral-500/20';
  }
}

export default function RouteDetails({ route }: RouteDetailsProps) {
  const segments = route.metadata?.segments || [];

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="p-6 bg-white/[0.02] border border-white/5 rounded-xl">
        {/* Route */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-xs text-neutral-500 mb-1">Départ</p>
            <p className="font-medium">{route.steps[0]}</p>
          </div>
          <ArrowRight className="w-5 h-5 text-neutral-600" />
          <div className="text-right">
            <p className="text-xs text-neutral-500 mb-1">Arrivée</p>
            <p className="font-medium">{route.steps[route.steps.length - 1]}</p>
          </div>
        </div>

        {/* Stats */}
        <div className="flex items-center justify-center gap-8 py-4 border-t border-white/5">
          <div className="text-center">
            <p className="text-2xl font-semibold">{formatTime(route.total_time)}</p>
            <p className="text-xs text-neutral-500 mt-1">Durée</p>
          </div>
          <div className="w-px h-10 bg-white/10" />
          <div className="text-center">
            <p className="text-2xl font-semibold">{route.total_distance.toFixed(0)}<span className="text-base text-neutral-500 ml-1">km</span></p>
            <p className="text-xs text-neutral-500 mt-1">Distance</p>
          </div>
          <div className="w-px h-10 bg-white/10" />
          <div className="text-center">
            <p className="text-2xl font-semibold">{segments.length}</p>
            <p className="text-xs text-neutral-500 mt-1">{segments.length > 1 ? 'Trains' : 'Train'}</p>
          </div>
        </div>
      </div>

      {/* Segments */}
      {segments.length > 0 && (
        <div className="space-y-3">
          <p className="text-sm text-neutral-500 px-1">Détail du trajet</p>
          
          <div className="space-y-2">
            {segments.map((segment, index) => (
              <SegmentRow key={index} segment={segment} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function SegmentRow({ segment }: { segment: Segment }) {
  return (
    <div className="flex items-center gap-4 p-4 bg-white/[0.02] border border-white/5 rounded-xl">
      {/* Train type */}
      <span className={`px-2.5 py-1 text-xs font-medium rounded-md border ${getTrainTypeStyle(segment.type_train)}`}>
        {segment.type_train}
      </span>

      {/* Route */}
      <div className="flex-1 min-w-0 flex items-center gap-2 text-sm">
        <span className="truncate">{segment.from}</span>
        <ArrowRight className="w-3.5 h-3.5 text-neutral-600 flex-shrink-0" />
        <span className="truncate">{segment.to}</span>
      </div>

      {/* Duration */}
      <div className="flex items-center gap-1.5 text-sm text-neutral-500">
        <Clock className="w-3.5 h-3.5" />
        <span>{formatTime(segment.temps_min)}</span>
      </div>
    </div>
  );
}
