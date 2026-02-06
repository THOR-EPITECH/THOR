'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Segment } from '@/types';
import type { RailwayTracksData } from '@/types/railway';

interface RouteMapClientProps {
  segments: Segment[];
}

const createStationIcon = (isTerminal: boolean) => {
  const size = isTerminal ? 12 : 8;
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      width: ${size}px;
      height: ${size}px;
      background: ${isTerminal ? '#fff' : '#666'};
      border: 2px solid ${isTerminal ? '#fff' : '#333'};
      border-radius: 50%;
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    "></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
};

function getTrainColor(type: string): string {
  switch (type) {
    case 'TGV': return '#f43f5e';
    case 'OUIGO': return '#06b6d4';
    case 'Intercités': return '#8b5cf6';
    case 'TER': return '#f59e0b';
    default: return '#6b7280';
  }
}

const MIN_GEOMETRY_POINTS = 10;

export default function RouteMapClient({ segments }: RouteMapClientProps) {
  const mapRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [railwayTracks, setRailwayTracks] = useState<RailwayTracksData | null>(null);

  useEffect(() => {
    fetch('/api/railway-tracks')
      .then(res => res.json())
      .then(data => setRailwayTracks(data))
      .catch(err => console.error('Failed to load railway tracks:', err));
  }, []);

  useEffect(() => {
    if (!containerRef.current) return;

    if (mapRef.current) {
      mapRef.current.remove();
      mapRef.current = null;
    }

    const validSegments = segments.filter(
      seg => seg.geometry?.coordinates && seg.geometry.coordinates.length >= MIN_GEOMETRY_POINTS
    );

    if (validSegments.length === 0) return;

    const map = L.map(containerRef.current, {
      zoomControl: false,
      attributionControl: false,
    });
    mapRef.current = map;

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
    }).addTo(map);

    if (railwayTracks) {
      const trackLines = Object.values(railwayTracks.lines);
      trackLines.forEach(line => {
        const coords: L.LatLngExpression[] = line.geometry.coordinates.map(
          coord => [coord[1], coord[0]] as L.LatLngExpression
        );
        
        L.polyline(coords, {
          color: '#475569',
          weight: 1,
          opacity: 0.25,
          interactive: false,
        }).addTo(map);
      });
    }

    const bounds = L.latLngBounds([]);

    validSegments.forEach((segment, index) => {
      const coords = segment.geometry!.coordinates;
      const color = getTrainColor(segment.type_train);
      
      const routeCoords: L.LatLngExpression[] = coords.map(
        coord => [coord[1], coord[0]] as L.LatLngExpression
      );
      
      routeCoords.forEach(coord => bounds.extend(coord));

      L.polyline(routeCoords, {
        color: color,
        weight: 3,
        opacity: 0.8,
        lineJoin: 'round',
        lineCap: 'round',
      }).addTo(map);

      const firstCoord = routeCoords[0];
      const lastCoord = routeCoords[routeCoords.length - 1];
      
      if (index === 0) {
        L.marker(firstCoord, { icon: createStationIcon(true) })
          .bindPopup(`<strong>${segment.from}</strong>`)
          .addTo(map);
      }
      
      L.marker(lastCoord, { icon: createStationIcon(index === validSegments.length - 1) })
        .bindPopup(`<strong>${segment.to}</strong>`)
        .addTo(map);
    });

    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [40, 40] });
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [segments, railwayTracks]);

  return (
    <div 
      ref={containerRef} 
      className="w-full h-[400px] rounded-xl overflow-hidden border border-white/5"
    />
  );
}
