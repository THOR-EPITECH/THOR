'use client';

import { Route, Segment } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Train, 
  Clock, 
  MapPin, 
  ArrowRight,
  Zap,
  Timer,
  TrainFront,
  Train as TrainIcon,
  TramFront
} from 'lucide-react';

interface RouteDetailsProps {
  route: Route;
}

function TrainTypeIcon({ type, className = "w-4 h-4" }: { type: string; className?: string }) {
  switch (type) {
    case 'TGV':
      return <TrainFront className={`${className} text-rose-400`} />;
    case 'OUIGO':
      return <TrainFront className={`${className} text-cyan-400`} />;
    case 'Intercités':
      return <TrainIcon className={`${className} text-violet-400`} />;
    case 'TER':
      return <TramFront className={`${className} text-amber-400`} />;
    default:
      return <Train className={`${className} text-slate-400`} />;
  }
}

function getTrainColor(type: string) {
  switch (type) {
    case 'TGV':
      return 'bg-gradient-to-r from-rose-500 to-pink-600 text-white border-0';
    case 'OUIGO':
      return 'bg-gradient-to-r from-cyan-500 to-teal-600 text-white border-0';
    case 'Intercités':
      return 'bg-gradient-to-r from-violet-500 to-purple-600 text-white border-0';
    case 'TER':
      return 'bg-gradient-to-r from-amber-500 to-orange-600 text-white border-0';
    default:
      return 'bg-slate-600 text-white border-0';
  }
}

function formatTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  if (hours === 0) return `${mins} min`;
  return `${hours}h${mins.toString().padStart(2, '0')}`;
}

export default function RouteDetails({ route }: RouteDetailsProps) {
  const segments = route.metadata?.segments || [];
  
  // Compter les types de trains
  const trainTypes: Record<string, number> = {};
  segments.forEach(seg => {
    trainTypes[seg.type_train] = (trainTypes[seg.type_train] || 0) + 1;
  });

  return (
    <div className="space-y-6">
      {/* Résumé du trajet */}
      <Card className="bg-slate-900/80 border-slate-700/50 backdrop-blur-sm overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5" />
        <CardHeader className="relative pb-2">
          <CardTitle className="flex items-center gap-3 text-xl">
            <div className="p-2 rounded-lg bg-cyan-500/10">
              <Train className="w-5 h-5 text-cyan-400" />
            </div>
            <span className="text-white">Itinéraire</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="relative">
          {/* Origine → Destination */}
          <div className="flex items-center gap-4 mb-6">
            <div className="flex-1">
              <div className="text-sm text-slate-400 mb-1">Départ</div>
              <div className="text-lg font-semibold text-white flex items-center gap-2">
                <MapPin className="w-4 h-4 text-emerald-400" />
                {route.steps[0]}
              </div>
            </div>
            <ArrowRight className="w-6 h-6 text-cyan-400 flex-shrink-0" />
            <div className="flex-1 text-right">
              <div className="text-sm text-slate-400 mb-1">Arrivée</div>
              <div className="text-lg font-semibold text-white flex items-center gap-2 justify-end">
                {route.steps[route.steps.length - 1]}
                <MapPin className="w-4 h-4 text-rose-400" />
              </div>
            </div>
          </div>

          <Separator className="bg-slate-700/50 mb-4" />

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 rounded-lg bg-slate-800/50">
              <Clock className="w-5 h-5 text-cyan-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{formatTime(route.total_time)}</div>
              <div className="text-xs text-slate-400">Durée totale</div>
            </div>
            <div className="text-center p-3 rounded-lg bg-slate-800/50">
              <Zap className="w-5 h-5 text-amber-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{route.total_distance.toFixed(0)}</div>
              <div className="text-xs text-slate-400">km</div>
            </div>
            <div className="text-center p-3 rounded-lg bg-slate-800/50">
              <Timer className="w-5 h-5 text-emerald-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white">{route.steps.length - 1}</div>
              <div className="text-xs text-slate-400">{route.steps.length - 1 > 1 ? 'correspondances' : 'correspondance'}</div>
            </div>
          </div>

          {/* Types de trains utilisés */}
          {Object.keys(trainTypes).length > 0 && (
            <div className="flex flex-wrap gap-2 mt-4 justify-center">
              {Object.entries(trainTypes).map(([type, count]) => (
                <Badge key={type} className={getTrainColor(type)}>
                  <TrainTypeIcon type={type} className="w-3 h-3 mr-1" /> {type} × {count}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Détails des segments */}
      {segments.length > 0 && (
        <Card className="bg-slate-900/80 border-slate-700/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-lg text-white">Détails du trajet</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {segments.map((segment, index) => (
                <SegmentCard key={index} segment={segment} index={index} isLast={index === segments.length - 1} />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function SegmentCard({ segment, isLast }: { segment: Segment; index: number; isLast: boolean }) {
  return (
    <div className="relative">
      {/* Ligne de connexion */}
      {!isLast && (
        <div className="absolute left-[23px] top-[56px] bottom-[-16px] w-0.5 bg-gradient-to-b from-cyan-500/50 to-slate-700/50" />
      )}
      
      <div className="flex gap-4">
        {/* Icône du segment */}
        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-cyan-500/20 to-purple-500/20 border border-cyan-500/30 flex items-center justify-center">
          <TrainTypeIcon type={segment.type_train} className="w-5 h-5" />
        </div>
        
        {/* Détails */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <Badge className={getTrainColor(segment.type_train)}>
              {segment.type_train}
            </Badge>
            <span className="text-slate-400 text-sm">
              {formatTime(segment.temps_min)} • {segment.distance_km.toFixed(0)} km
            </span>
          </div>
          
          <div className="mt-2 flex items-center gap-2 text-sm">
            <span className="text-white font-medium truncate">{segment.from}</span>
            <ArrowRight className="w-4 h-4 text-slate-500 flex-shrink-0" />
            <span className="text-white font-medium truncate">{segment.to}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
