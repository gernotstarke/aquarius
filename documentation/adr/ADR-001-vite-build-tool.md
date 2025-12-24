# ADR-001: Vite als Build-Tool für Frontend

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Für die beiden Frontend-Anwendungen (Planung und Durchführung) benötigen wir ein modernes Build-Tool, das schnelle Entwicklungszyklen und optimierte Production-Builds ermöglicht.

## Entscheidung

Wir verwenden **Vite** als Build-Tool für beide Frontend-Module.

## Begründung

### Vorteile

- **Extrem schneller Dev-Server** durch natives ES-Modules
- **Instant Hot Module Replacement (HMR)** ohne Neustart
- **Optimierte Production-Builds** mit Rollup
- **Hervorragende TypeScript-Unterstützung** out-of-the-box
- **Einfache Konfiguration** - funktioniert mit Zero-Config
- **Moderne Defaults** - Tree-shaking, Code-splitting automatisch
- **Plugin-Ökosystem** für React, PWA, etc.

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Webpack** | Langsamer Dev-Server, komplexe Konfiguration |
| **Create React App** | Nicht mehr aktiv entwickelt, langsam |
| **Parcel** | Kleineres Ökosystem, weniger Kontrolle |

## Konsequenzen

### Positiv

- Entwickler erhalten sofortiges Feedback bei Code-Änderungen
- Production-Builds sind optimal für Performance
- Gute Developer Experience steigert Produktivität
- Native ESM-Unterstützung zukunftssicher

### Negativ

- Team muss Vite-Konfiguration lernen (minimal)
- Unterschiede zu CRA-Projekten (geringe Migrationskosten)

## Technische Details

```json
{
  "vite": "^5.0.0",
  "plugins": [
    "@vitejs/plugin-react",
    "vite-plugin-pwa"
  ]
}
```

Konfiguration in `vite.config.ts` für jeden Frontend-Workspace im Monorepo.
