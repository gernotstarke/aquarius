/**
 * Figur Types - Figure/routine catalog
 *
 * These types align with the Figur domain in the backend.
 */

export interface Figur {
  id: number;
  name: string;
  beschreibung?: string;
  schwierigkeitsgrad?: number;
  kategorie?: string;
  altersklasse?: string;
  min_alter?: number;
  bild?: string;
}

export interface FigurCreate {
  name: string;
  beschreibung?: string;
  schwierigkeitsgrad?: number;
  kategorie?: string;
  altersklasse?: string;
  min_alter?: number;
  bild?: string;
}
