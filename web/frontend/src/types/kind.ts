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
  geschlecht?: string | null;
  verein_id?: number | null;
  verband_id?: number | null;
  versicherung_id?: number | null;
  vertrag?: string | null;
}
