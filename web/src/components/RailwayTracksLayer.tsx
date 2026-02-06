'use client';

import { useEffect, useState } from 'react';
import { Polyline, LayersControl } from 'react-leaflet';
import type { RailwayTracksData } from '@/types/railway';

const { Overlay } = LayersControl;

export default function RailwayTracksLayer() {
  const [tracks, setTracks] = useState<RailwayTracksData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/railway-tracks')
      .then(res => res.json())
      .then(data => {
        setTracks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load railway tracks:', err);
        setLoading(false);
      });
  }, []);

  if (loading || !tracks) {
    return null;
  }

  const trackLines = Object.values(tracks.lines);

  return (
    <Overlay checked name="Réseau ferré complet">
      <>
        {trackLines.map((line, idx) => {
          const positions: [number, number][] = line.geometry.coordinates.map(
            coord => [coord[1], coord[0]]
          );

          return (
            <Polyline
              key={`${line.code_ligne}-${idx}`}
              positions={positions}
              pathOptions={{
                color: '#94a3b8',
                weight: 1.5,
                opacity: 0.4,
              }}
            />
          );
        })}
      </>
    </Overlay>
  );
}
