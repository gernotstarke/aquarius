/**
 * Grunddaten Types - Base data for clubs, associations, and insurance
 *
 * These types align with the Grunddaten domain in the backend.
 */

export interface Verein {
  id: number;
  name: string;
  ort: string;
  register_id: string;
  contact: string;
}

export interface VereinCreate {
  name: string;
  ort: string;
  register_id: string;
  contact: string;
}

export interface Verband {
  id: number;
  name: string;
  abkuerzung: string;
  land: string;
  ort: string;
  nomination_count?: number;
}

export interface Versicherung {
  id: number;
  name: string;
  kurz: string;
  land: string;
  hauptsitz: string;
}
