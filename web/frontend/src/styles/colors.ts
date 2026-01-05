/**
 * Color constants for Grunddaten tiles
 * Used to maintain visual consistency and allow easy color updates
 */

export const GRUNDDATEN_COLORS = {
  saisons: {
    bg: 'bg-blue-50',
    hover: 'hover:bg-blue-100',
    full: 'bg-blue-50 hover:bg-blue-100',
  },
  schwimmbaeder: {
    bg: 'bg-cyan-50',
    hover: 'hover:bg-cyan-100',
    full: 'bg-cyan-50 hover:bg-cyan-100',
  },
  figuren: {
    bg: 'bg-teal-50',
    hover: 'hover:bg-teal-100',
    full: 'bg-teal-50 hover:bg-teal-100',
  },
  vereine: {
    bg: 'bg-emerald-50',
    hover: 'hover:bg-emerald-100',
    full: 'bg-emerald-50 hover:bg-emerald-100',
  },
} as const;
