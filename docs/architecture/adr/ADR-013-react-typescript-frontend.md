# ADR-013: React + TypeScript als Frontend-Framework

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-016 PWA Architecture](ADR-016-pwa-architecture.md), [ADR-017 TailwindCSS](ADR-017-tailwindcss-styling.md)

---

## Kontext

Aquarius benötigt zwei Frontend-Anwendungen:
1. **Planungs-App**: Desktop-optimiert für Büro/Verwaltung
2. **Durchführungs-App**: Mobile/Touch-optimiert für Wettkampf am Schwimmbad

Anforderungen:
- Moderne, komponentenbasierte Architektur
- Typsicherheit zur Fehlerreduzierung
- Gute Mobile-Unterstützung (PWA-fähig)
- Hohe Code-Qualität durch Non-Technical Users (Ehrenamtliche)
- Wiederverwendbare Komponenten zwischen beiden Apps

## Entscheidung

Wir verwenden **React 18** mit **TypeScript** als Frontend-Framework.

### Technologie-Stack

```
Frontend Stack:
├── React 18                  (UI Framework)
├── TypeScript 5.x            (Type System)
├── Vite 5.x                  (Build Tool)
├── React Router 6            (Client-side Routing)
├── TanStack Query v5         (Server State Management)
├── Zustand                   (Local State Management)
└── Workbox                   (Service Worker / PWA)
```

### Projektstruktur

```
frontend/
├── apps/
│   ├── planning/             # Desktop-optimierte Planungs-App
│   │   ├── src/
│   │   │   ├── pages/
│   │   │   ├── components/
│   │   │   └── main.tsx
│   │   └── index.html
│   └── execution/            # Mobile-optimierte Durchführungs-App
│       ├── src/
│       │   ├── pages/
│       │   ├── components/
│       │   └── main.tsx
│       └── index.html
├── packages/
│   ├── ui/                   # Shared UI Components
│   ├── api-client/           # Backend API Client
│   └── types/                # Shared TypeScript Types
└── package.json              # Monorepo Root
```

## Begründung

### Pro React + TypeScript

**React 18:**
- ✅ **Große Community**: Über 220k GitHub Stars, ausgereifte Best Practices
- ✅ **Komponentenbasiert**: Wiederverwendbare UI-Elemente
- ✅ **Moderne Features**: Hooks, Concurrent Features, Suspense
- ✅ **PWA-Unterstützung**: Hervorragende Service Worker Integration
- ✅ **Ökosystem**: Große Auswahl an Libraries (Routing, State, Forms)
- ✅ **Performance**: Virtual DOM, Code Splitting, Lazy Loading

**TypeScript:**
- ✅ **Typsicherheit**: Fehler zur Compile-Zeit statt Runtime
- ✅ **IDE-Support**: IntelliSense, Autovervollständigung
- ✅ **Refactoring**: Sichere Code-Änderungen
- ✅ **Dokumentation**: Types als lebende Dokumentation
- ✅ **API-Kontrakte**: Pydantic (Backend) → TypeScript (Frontend)

**Vite:**
- ✅ **Schnell**: ESM-basiert, < 1s HMR (Hot Module Replacement)
- ✅ **Modern**: Out-of-the-box TypeScript, JSX Support
- ✅ **Optimiert**: Automatisches Code Splitting, Tree Shaking
- ✅ **PWA**: Einfache Workbox-Integration

### Alternative: Vue.js

- ❌ Kleinere Community als React
- ❌ Weniger PWA-Beispiele und Best Practices
- ✅ Einfachere Lernkurve
- ✅ Gute TypeScript-Integration

**Entscheidung gegen Vue:** React-Ökosystem ist ausgereifter für PWAs

### Alternative: Angular

- ❌ Steile Lernkurve (Dependency Injection, RxJS)
- ❌ Overhead für kleinere Anwendung (20 Kinder Liga)
- ✅ TypeScript-First Framework
- ✅ Batteries-included (Routing, Forms, HTTP)

**Entscheidung gegen Angular:** Zu komplex für Projektgröße

### Alternative: Svelte

- ❌ Kleinere Community, weniger Ressourcen
- ❌ Weniger Enterprise-Erfahrung im Team
- ✅ Sehr performant (Compiler statt Virtual DOM)
- ✅ Einfache Syntax

**Entscheidung gegen Svelte:** Zu wenig Community-Support für PWAs

## Konsequenzen

### Positiv

1. **Geteilte Komponenten**: `@aquarius/ui` Package mit gemeinsamen Buttons, Forms, etc.
2. **Type-Safety**: Automatisch generierte TypeScript-Typen aus FastAPI (via openapi-typescript)
3. **Moderne DX**: Vite bietet exzellente Developer Experience
4. **PWA-Ready**: Workbox + React = bewährte Kombination
5. **Team-Skill**: React ist weit verbreitet, einfach neue Entwickler zu finden

### Negativ

1. **Build-Komplexität**: Monorepo mit 2 Apps + Shared Packages erfordert Setup
2. **Bundle-Größe**: React ist größer als Svelte (~45 KB gzipped)
3. **Lernkurve**: Hooks, Concurrent Features benötigen Einarbeitung
4. **State Management**: Zusätzliche Libraries nötig (TanStack Query, Zustand)

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| React-Version-Upgrade bricht Code | Niedrig | Mittel | Gradual Adoption Strategy, gute Test-Coverage |
| Bundle zu groß für Mobile | Niedrig | Hoch | Code Splitting, Lazy Loading, Bundle Analyzer |
| TypeScript-Kompilierung langsam | Niedrig | Niedrig | Vite ist sehr schnell, inkrementelle Compilation |

## Implementierung

### 1. Projekt-Setup

```bash
# Monorepo mit pnpm
pnpm init
pnpm add -D vite @vitejs/plugin-react typescript

# Shared UI Package
cd packages/ui
pnpm add react react-dom
pnpm add -D @types/react @types/react-dom

# Planning App
cd apps/planning
pnpm add react react-dom react-router-dom
pnpm add @tanstack/react-query zustand

# Execution App (PWA)
cd apps/execution
pnpm add react react-dom react-router-dom
pnpm add @tanstack/react-query zustand workbox-precaching
```

### 2. TypeScript-Konfiguration

```json
// tsconfig.json (Root)
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "react-jsx",
    "paths": {
      "@aquarius/ui": ["./packages/ui/src"],
      "@aquarius/types": ["./packages/types/src"]
    }
  }
}
```

### 3. Vite-Konfiguration (PWA)

```typescript
// apps/execution/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.aquarius\.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 300 }
            }
          }
        ]
      }
    })
  ]
})
```

## Validierung

### Success Criteria

- ✅ Beide Apps teilen mindestens 30% der UI-Komponenten
- ✅ TypeScript Strict Mode ohne Errors
- ✅ PWA Lighthouse Score > 90
- ✅ Bundle Size < 500 KB (gzipped)
- ✅ First Contentful Paint < 1.5s

### Metriken

```bash
# Bundle Size
pnpm build
pnpm exec vite-bundle-visualizer

# TypeScript Errors
pnpm exec tsc --noEmit

# Lighthouse Score
lighthouse https://aquarius.local --view
```

## Referenzen

- [React 18 Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [PWA with Vite](https://vite-pwa-org.netlify.app/)
- [TanStack Query](https://tanstack.com/query/latest)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |
