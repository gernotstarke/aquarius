/**
 * Wettkampf Types - Competition management
 *
 * These types align with the Wettkampf domain in the backend.
 */

import { Saison } from './saison';
import { Schwimmbad } from './schwimmbad';
import { Figur } from './figur';
import { Anmeldung } from './anmeldung';

export interface Wettkampf {
  id: number;
  name: string;
  datum: string;
  max_teilnehmer?: number;
  saison_id: number;
  schwimmbad_id: number;
}

export interface WettkampfCreate {
  name: string;
  datum: string;
  max_teilnehmer?: number;
  saison_id: number;
  schwimmbad_id: number;
}

export interface WettkampfWithDetails extends Wettkampf {
  figuren: Figur[];
  anmeldungen: Anmeldung[];
  saison?: Saison;
  schwimmbad?: Schwimmbad;
}
