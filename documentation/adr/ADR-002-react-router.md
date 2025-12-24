# ADR-002: React Router für Client-seitiges Routing

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Beide Frontend-Anwendungen (Planung und Durchführung) benötigen Client-seitiges Routing für Navigation zwischen verschiedenen Views, ohne dass vollständige Seitenneuladungen erforderlich sind.

## Entscheidung

Wir verwenden **React Router v6** für Client-seitiges Routing in beiden Frontend-Modulen.

## Begründung

### Vorteile

- **De-facto Standard** für React-Routing
- **Deklaratives Routing** mit JSX-Syntax
- **Nested Routes** für hierarchische UI-Strukturen
- **Data Loading** mit Loaders (React Router 6.4+)
- **Type-safe** mit TypeScript-Unterstützung
- **Lazy Loading** von Route-Komponenten
- **Große Community** und umfangreiche Dokumentation

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **TanStack Router** | Zu neu, kleinere Community |
| **Wouter** | Zu minimalistisch für komplexe Anforderungen |
| **Next.js Routing** | Benötigt Next.js Framework (Overkill) |

## Konsequenzen

### Positiv

- SPA-Navigation ohne Seitenneuladungen
- Browser-History funktioniert korrekt
- URL-basierte Navigation ermöglicht Deep-Linking
- Code-Splitting pro Route möglich

### Negativ

- Client-seitiges Routing erfordert zusätzliche Konfiguration beim Deployment (Nginx)
- SEO-Anforderungen müssen separat adressiert werden (aktuell nicht relevant)

## Technische Details

```typescript
// Routing-Struktur Planung-App
const router = createBrowserRouter([
  {
    path: "/",
    element: <PlanningLayout />,
    children: [
      { path: "saison", element: <SaisonPage /> },
      { path: "wettkampf", element: <WettkampfPage /> },
      { path: "anmeldung", element: <AnmeldungPage /> },
    ]
  }
]);

// Routing-Struktur Durchführungs-App
const router = createBrowserRouter([
  {
    path: "/",
    element: <ExecutionLayout />,
    children: [
      { path: "setup", element: <WettkampfSetupPage /> },
      { path: "bewertung", element: <BewertungPage /> },
      { path: "auswertung", element: <AuswertungPage /> },
    ]
  }
]);
```

**Dependencies:**
```json
{
  "react-router-dom": "^6.20.0"
}
```
