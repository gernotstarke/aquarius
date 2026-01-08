/**
 * Anmeldung Types - Registration management
 *
 * These types align with the Anmeldung domain in the backend.
 */

import { Kind } from './kind';
import { Figur } from './figur';

export interface Anmeldung {
  id: number;
  kind_id: number;
  wettkampf_id: number;
  startnummer: number;
  anmeldedatum: string;
  status: string;
  vorlaeufig: number;
  figuren: Figur[];
  insurance_ok?: boolean;
  kind?: Kind;
}

export interface AnmeldungCreate {
  kind_id: number;
  wettkampf_id: number;
  figur_ids: number[];
}
