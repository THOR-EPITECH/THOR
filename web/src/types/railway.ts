export interface RailwayLine {
  code_ligne: string;
  num_segments: number;
  geometry: {
    type: 'LineString';
    coordinates: number[][];
  };
  metadata: {
    ligne: string;
    pk_debut: string;
    pk_fin: string;
    num_tracks: number;
    num_vpa: number;
  };
}

export interface RailwayTracksData {
  metadata: {
    source: string;
    num_lines: number;
    simplification_factor?: number;
  };
  lines: Record<string, RailwayLine>;
}
