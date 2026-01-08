/**
 * Saison Types - Season management
 *
 * These types align with the Saison domain in the backend.
 */

export interface Saison {
  id: number;
  name: string;
  from_date: string;
  to_date: string;
}

export interface SaisonCreate {
  name: string;
  from_date: string;
  to_date: string;
}
