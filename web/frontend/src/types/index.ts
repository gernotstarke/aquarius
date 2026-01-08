/**
 * Central type exports - Re-exports all domain types
 *
 * This file maintains backward compatibility while allowing
 * components to import from domain-specific files.
 *
 * Prefer importing from domain-specific files (e.g., import { Kind } from '../types/kind')
 * over importing from this index file.
 */

// Grunddaten domain
export type { Verein, VereinCreate, Verband, Versicherung } from './grunddaten';

// Saison domain
export type { Saison, SaisonCreate } from './saison';

// Schwimmbad domain
export type { Schwimmbad, SchwimmbadCreate } from './schwimmbad';

// Figur domain
export type { Figur, FigurCreate } from './figur';

// Kind domain
export type { Kind, KindCreate } from './kind';

// Wettkampf domain
export type { Wettkampf, WettkampfCreate, WettkampfWithDetails } from './wettkampf';

// Anmeldung domain
export type { Anmeldung, AnmeldungCreate } from './anmeldung';
