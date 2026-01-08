/**
 * Kind Types - Child/participant management
 *
 * These types align with the Kind domain in the backend.
 */

import { Verein, Verband, Versicherung } from './grunddaten';

export interface Kind {
  id: number;
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  geschlecht?: string;
  verein_id?: number;
  verein?: Verein;
  verband_id?: number;
  verband?: Verband;
  versicherung_id?: number;
  versicherung?: Versicherung;
  vertrag?: string;
}

export interface KindCreate {
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  geschlecht?: string;
  verein_id?: number;
  verband_id?: number;
  versicherung_id?: number;
  vertrag?: string;
}
