'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Segment } from '@/types';

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
    case 'Correspondance': return '#fbbf24';
    default: return '#6b7280';
  }
}

const MIN_GEOMETRY_POINTS = 2;

function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function splitIntoValidSegments(coords: number[][]): number[][][] {
  const segments: number[][][] = [];
  let currentSegment: number[][] = [];
  
  for (let i = 0; i < coords.length; i++) {
    if (currentSegment.length === 0) {
      currentSegment.push(coords[i]);
    } else {
      const prevPoint = currentSegment[currentSegment.length - 1];
      const [lon1, lat1] = prevPoint;
      const [lon2, lat2] = coords[i];
      const distance = calculateDistance(lat1, lon1, lat2, lon2);
      
      if (distance > 50) {
        if (currentSegment.length > 1) {
          segments.push(currentSegment);
        }
        currentSegment = [coords[i]];
      } else {
        currentSegment.push(coords[i]);
      }
    }
  }
  
  if (currentSegment.length > 1) {
    segments.push(currentSegment);
  }
  
  return segments;
}

export default function RouteMapClient({ segments }: RouteMapClientProps) {
  const mapRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

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

    const franceBounds = L.latLngBounds(
      L.latLng(41.0, -5.5),
      L.latLng(51.5, 10.0)
    );
    
    const map = L.map(containerRef.current, {
      zoomControl: false,
      attributionControl: false,
      minZoom: 5,
      maxZoom: 19,
      maxBounds: franceBounds,
      maxBoundsViscosity: 1.0,
    });
    mapRef.current = map;

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
    }).addTo(map);

    const bounds = L.latLngBounds([]);
    const displayedEndpoints: Map<number, { last: L.LatLngExpression }> = new Map();

    validSegments.forEach((segment, index) => {
      const coords = segment.geometry!.coordinates;
      const firstGeomPoint = coords[0];
      const lastGeomPoint = coords[coords.length - 1];
      
      const fromCoord: L.LatLngExpression = segment.from_lat && segment.from_lon
        ? [segment.from_lat, segment.from_lon]
        : [firstGeomPoint[1], firstGeomPoint[0]];
      
      const toCoord: L.LatLngExpression = segment.to_lat && segment.to_lon
        ? [segment.to_lat, segment.to_lon]
        : [lastGeomPoint[1], lastGeomPoint[0]];
      
      const color = getTrainColor(segment.type_train);
      const isCorrespondance = segment.type_train === 'Correspondance';
      
      if (isCorrespondance) {
        let startPoint: L.LatLngExpression = [coords[0][1], coords[0][0]];
        let endPoint: L.LatLngExpression = [coords[1][1], coords[1][0]];
        
        if (index > 0 && displayedEndpoints.has(index - 1)) {
          startPoint = displayedEndpoints.get(index - 1)!.last;
        }
        
        if (index + 1 < validSegments.length) {
          const nextSegment = validSegments[index + 1];
          const nextCoords = nextSegment.geometry!.coordinates;
          const nextValidSegments = splitIntoValidSegments(nextCoords);
          if (nextValidSegments.length > 0 && nextValidSegments[0].length > 0) {
            const firstPoint = nextValidSegments[0][0];
            endPoint = [firstPoint[1], firstPoint[0]];
          }
        }
        
        const routeCoords: L.LatLngExpression[] = [startPoint, endPoint];
        
        routeCoords.forEach(coord => bounds.extend(coord));
        
        const invisibleLine = L.polyline(routeCoords, {
          color: color,
          weight: 15,
          opacity: 0,
        }).addTo(map);
        
        const visibleLine = L.polyline(routeCoords, {
          color: color,
          weight: 4,
          opacity: 0.9,
          dashArray: '10, 10',
          lineJoin: 'round',
          lineCap: 'round',
        }).addTo(map);
        
        const popupContent = `<div style="text-align: center;">
          <strong>🚇 ${segment.from} → ${segment.to}</strong><br/>
          <span style="color: ${color}; font-size: 12px;">Correspondance métro/RER</span><br/>
          <span style="color: #999; font-size: 11px;">${segment.distance_km} km • ${segment.temps_min} min</span>
        </div>`;
        
        invisibleLine.bindPopup(popupContent);
        visibleLine.bindPopup(popupContent);
      } else {
        let validSegmentsList = splitIntoValidSegments(coords);
        
        if (validSegmentsList.length > 0) {
          const firstSegment = validSegmentsList[0];
          const lastSegment = validSegmentsList[validSegmentsList.length - 1];
          const firstPoint = firstSegment[0];
          const lastPoint = lastSegment[lastSegment.length - 1];
          
          const distFirstToFrom = calculateDistance(fromCoord[0], fromCoord[1], firstPoint[1], firstPoint[0]);
          const distLastToFrom = calculateDistance(fromCoord[0], fromCoord[1], lastPoint[1], lastPoint[0]);
          const distFirstToTo = calculateDistance(toCoord[0], toCoord[1], firstPoint[1], firstPoint[0]);
          const distLastToTo = calculateDistance(toCoord[0], toCoord[1], lastPoint[1], lastPoint[0]);
          
          if (distLastToFrom < distFirstToFrom && distFirstToTo < distLastToTo) {
            validSegmentsList = validSegmentsList.map(seg => [...seg].reverse()).reverse();
          }
          
          const finalLastSegment = validSegmentsList[validSegmentsList.length - 1];
          const finalLastPoint = finalLastSegment[finalLastSegment.length - 1];
          displayedEndpoints.set(index, { last: [finalLastPoint[1], finalLastPoint[0]] });
          
          validSegmentsList.forEach(segmentCoords => {
            const routeCoords: L.LatLngExpression[] = segmentCoords.map(
              coord => [coord[1], coord[0]] as L.LatLngExpression
            );
            
            routeCoords.forEach(coord => bounds.extend(coord));

            const invisibleLine = L.polyline(routeCoords, {
              color: color,
              weight: 15,
              opacity: 0,
            }).addTo(map);
            
            const visibleLine = L.polyline(routeCoords, {
              color: color,
              weight: 3,
              opacity: 0.8,
              lineJoin: 'round',
              lineCap: 'round',
            }).addTo(map);
            
            const popupContent = `<div style="text-align: center;">
              <strong>${segment.from} → ${segment.to}</strong><br/>
              <span style="color: ${color}; font-size: 12px;">${segment.type_train}</span><br/>
              <span style="color: #999; font-size: 11px;">${segment.distance_km} km • ${segment.temps_min} min</span>
            </div>`;
            
            invisibleLine.bindPopup(popupContent);
            visibleLine.bindPopup(popupContent);
          });
          
          const totalPointsInValidSegments = validSegmentsList.reduce((sum, seg) => sum + seg.length, 0);
          const percentageValid = (totalPointsInValidSegments / coords.length) * 100;
          
          if (percentageValid < 80) {
            
            const invisibleLine = L.polyline([fromCoord, toCoord], {
              color: color,
              weight: 15,
              opacity: 0,
            }).addTo(map);
            
            const dashedLine = L.polyline([fromCoord, toCoord], {
              color: color,
              weight: 3,
              opacity: 0.6,
              dashArray: '10, 15',
              lineCap: 'round',
            }).addTo(map);
            
            const popupContent = `<div style="text-align: center;">
              <strong>${segment.from} → ${segment.to}</strong><br/>
              <span style="color: #999; font-size: 12px;">Tracé indisponible</span>
            </div>`;
            
            invisibleLine.bindPopup(popupContent);
            dashedLine.bindPopup(popupContent);
          }
        }
      }
      
      bounds.extend(fromCoord);
      bounds.extend(toCoord);
      
      let actualFromCoord = fromCoord;
      let actualToCoord: L.LatLngExpression = toCoord;
      
      if (!isCorrespondance && displayedEndpoints.has(index)) {
        actualToCoord = displayedEndpoints.get(index)!.last;
      }
      
      if (index === 0) {
        L.marker(actualFromCoord, { icon: createStationIcon(true) })
          .bindPopup(`<strong>${segment.from}</strong>`)
          .addTo(map);
      }
      
      L.marker(actualToCoord, { icon: createStationIcon(index === validSegments.length - 1) })
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
  }, [segments]);

  return (
    <div 
      ref={containerRef} 
      className="w-full h-[400px] rounded-xl overflow-hidden border border-white/5"
    />
  );
}
