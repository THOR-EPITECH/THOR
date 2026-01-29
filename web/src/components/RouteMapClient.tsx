'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Segment } from '@/types';
import { getStationPosition } from '@/data/stations';

interface RouteMapClientProps {
  segments: Segment[];
  steps: string[];
}

// Icônes personnalisées pour les gares
const createStationIcon = (isTerminal: boolean) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div class="relative">
        <div class="${isTerminal ? 'w-5 h-5 bg-cyan-500' : 'w-3 h-3 bg-amber-500'} rounded-full border-2 border-white shadow-lg ${isTerminal ? 'animate-pulse' : ''}"></div>
        ${isTerminal ? '<div class="absolute -inset-1 bg-cyan-500/30 rounded-full animate-ping"></div>' : ''}
      </div>
    `,
    iconSize: [isTerminal ? 20 : 12, isTerminal ? 20 : 12],
    iconAnchor: [isTerminal ? 10 : 6, isTerminal ? 10 : 6],
  });
};

export default function RouteMapClient({ segments, steps }: RouteMapClientProps) {
  const mapRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    // Obtenir les positions des gares
    const positions = steps
      .map(step => {
        const pos = getStationPosition(step);
        return pos ? { name: step, ...pos } : null;
      })
      .filter((p): p is { name: string; lat: number; lon: number } => p !== null);

    if (positions.length === 0) return;

    // Créer la carte
    const map = L.map(containerRef.current, {
      zoomControl: false,
      attributionControl: false,
    });
    mapRef.current = map;

    // Ajouter les contrôles de zoom en bas à droite
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Tuile sombre pour le style
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
    }).addTo(map);

    // Ajouter les marqueurs et la ligne du trajet
    const bounds = L.latLngBounds([]);
    const routeCoords: L.LatLngExpression[] = [];

    positions.forEach((pos, index) => {
      const latLng: L.LatLngExpression = [pos.lat, pos.lon];
      bounds.extend(latLng);
      routeCoords.push(latLng);

      const isTerminal = index === 0 || index === positions.length - 1;
      const marker = L.marker(latLng, { icon: createStationIcon(isTerminal) });
      
      // Popup avec les infos de la gare
      const segment = segments[index];
      const popupContent = `
        <div class="font-sans">
          <strong class="text-cyan-400">${pos.name}</strong>
          ${segment ? `<br><span class="text-xs text-slate-400">${segment.type_train} • ${segment.temps_min} min</span>` : ''}
        </div>
      `;
      marker.bindPopup(popupContent, {
        className: 'dark-popup',
      });
      
      marker.addTo(map);
    });

    // Tracer la ligne du trajet avec un dégradé
    if (routeCoords.length > 1) {
      // Ligne principale
      L.polyline(routeCoords, {
        color: '#06b6d4',
        weight: 4,
        opacity: 0.8,
        lineJoin: 'round',
      }).addTo(map);

      // Ligne de lueur
      L.polyline(routeCoords, {
        color: '#06b6d4',
        weight: 8,
        opacity: 0.3,
        lineJoin: 'round',
      }).addTo(map);
    }

    // Ajuster la vue
    map.fitBounds(bounds, { padding: [50, 50] });

    // Cleanup
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [segments, steps]);

  return (
    <div 
      ref={containerRef} 
      className="w-full h-[400px] rounded-xl overflow-hidden border border-slate-700/50"
      style={{ background: '#0f172a' }}
    />
  );
}
