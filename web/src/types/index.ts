// Types pour l'application THOR

export interface Segment {
  from: string;
  to: string;
  temps_min: number;
  distance_km: number;
  nb_trains_jour: number;
  type_train: 'TGV' | 'OUIGO' | 'Intercités' | 'TER' | 'Autre';
  types_details?: Record<string, number>;
}

export interface RouteMetadata {
  origin_uic: string;
  destination_uic: string;
  path_uic: string[];
  num_stations: number;
  mode: string;
  segments: Segment[];
  error?: string;
}

export interface Route {
  origin: string;
  destination: string;
  steps: string[];
  total_distance: number;
  total_time: number;
  metadata: RouteMetadata;
}

export interface Station {
  name: string;
  uic: string;
  lat: number;
  lon: number;
}

export interface PipelineResult {
  audio_path?: string;
  transcript: string;
  origin: string | null;
  destination: string | null;
  is_valid: boolean;
  confidence: number;
  route?: Route;
  error_message?: string;
  stt_metadata?: {
    model: string;
    language: string;
    processing_time: number;
  };
  nlp_metadata?: {
    model: string;
    extraction_method: string;
    locations_found: string[];
    entities: Array<{ text: string; label: string }>;
  };
}

export interface SearchRequest {
  text?: string;
  audio?: string; // Base64 encoded audio
}

export interface StationPosition {
  name: string;
  lat: number;
  lon: number;
}
