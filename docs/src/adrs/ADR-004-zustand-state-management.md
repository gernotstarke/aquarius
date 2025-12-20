# ADR-004: Zustand für lokales State Management

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Neben Server-State (TanStack Query) benötigen wir lokales State Management für UI-State wie Formulareingaben, Modal-Zustände, Filteroptionen und temporäre Daten.

## Entscheidung

Wir verwenden **Zustand** als minimale State Management Library für lokalen UI-State.

## Begründung

### Vorteile

- **Minimale API** - Extrem einfach zu lernen
- **Keine Boilerplate** - Kein Redux-ähnliches Setup erforderlich
- **Hooks-basiert** - Natürliche React-Integration
- **TypeScript-First** - Exzellente Type-Inferenz
- **Kleine Bundle-Size** - Nur ~1KB gzipped
- **DevTools** - Redux DevTools kompatibel
- **Middleware** - Persist, Immer, DevTools integrierbar

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Redux Toolkit** | Zu viel Overhead für UI-State |
| **Jotai** | Atomic Approach nicht benötigt |
| **Recoil** | Komplexer, Meta-Abhängigkeit |
| **Context API** | Performance-Probleme bei häufigen Updates |
| **useState only** | Nicht skalierbar für komplexere Zustände |

## Konsequenzen

### Positiv

- Sehr einfache Lernkurve für Team
- Minimaler Overhead im Bundle
- Klare Trennung: Zustand = UI-State, TanStack Query = Server-State
- Schnelle Entwicklungsgeschwindigkeit

### Negativ

- Nicht geeignet für komplexe State-Maschinen (aktuell nicht benötigt)
- Bei sehr großen State-Trees weniger strukturiert als Redux

## Technische Details

```typescript
// Store Definition
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  sidebarOpen: boolean;
  filterOptions: FilterOptions;
  toggleSidebar: () => void;
  setFilter: (options: FilterOptions) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      filterOptions: {},
      toggleSidebar: () => set((state) => ({
        sidebarOpen: !state.sidebarOpen
      })),
      setFilter: (options) => set({ filterOptions: options }),
    }),
    {
      name: 'ui-storage', // LocalStorage key
    }
  )
);

// Usage
const { sidebarOpen, toggleSidebar } = useUIStore();
```

**Dependencies:**
```json
{
  "zustand": "^4.4.0"
}
```

## State-Architektur

- **Server-State** → TanStack Query (cached, synchronized)
- **UI-State** → Zustand (local, ephemeral or persisted)
- **Form-State** → React Hook Form (component-local)
