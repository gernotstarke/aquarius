# ADR-016: Progressive Web App (PWA) Architektur

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-013 React Frontend](ADR-013-react-typescript-frontend.md), [ADR-015 Turso Database](ADR-015-turso-database.md)

---

## Kontext

Die **Durchführungs-App** muss im Schwimmbad auf Tablets funktionieren:

**Herausforderungen:**
- 🏊 Schwimmbäder haben oft **schlechte/keine Internet**verbindung
- 📱 Verschiedene Geräte: iPads, Android-Tablets, evtl. Laptops
- ⚡ **Live-Bewertung** darf nicht durch Netzwerkprobleme unterbrochen werden
- 👥 Ehrenamtliche Helfer müssen App **ohne Installation** nutzen können

**Anforderungen:**
- Offline-Fähigkeit für kritische Funktionen (Bewertung erfassen)
- App-ähnliches Erlebnis (Home-Screen-Icon, Fullscreen)
- Kein App-Store nötig (keine Kosten, keine Wartezeit)
- Automatische Updates
- Schnelle Ladezeiten trotz mobilem Netz

## Entscheidung

Wir entwickeln die Durchführungs-App als **Progressive Web App (PWA)** mit:
- Service Worker für Offline-Funktionalität
- Workbox für Caching-Strategien
- Web App Manifest für installierbare App
- Embedded Turso Replica für lokale Daten

### PWA-Architektur

```
┌─────────────────────────────────────────────────┐
│            Browser (Safari/Chrome)              │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │         React App (UI Layer)              │ │
│  │  - Bewertungs-Formulare                   │ │
│  │  - Durchgangs-Übersicht                   │ │
│  │  - Offline-Status-Anzeige                 │ │
│  └──────────────┬────────────────────────────┘ │
│                 │                                │
│  ┌──────────────▼────────────────────────────┐ │
│  │      Service Worker (Workbox)             │ │
│  │                                            │ │
│  │  ┌────────────┐   ┌────────────────────┐  │ │
│  │  │  Cache API │   │  Background Sync   │  │ │
│  │  │  (Assets)  │   │  (Pending Writes)  │  │ │
│  │  └────────────┘   └────────────────────┘  │ │
│  └──────────────┬────────────────────────────┘ │
│                 │                                │
│  ┌──────────────▼────────────────────────────┐ │
│  │         IndexedDB / libSQL Replica        │ │
│  │  - Lokale Kopie der Wettkampf-Daten      │ │
│  │  - Offline Writes Queue                   │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                     │
                     │ Sync when online
                     ▼
         ┌───────────────────────┐
         │   Backend API         │
         │   + Turso Cloud       │
         └───────────────────────┘
```

## Begründung

### Pro PWA

**Vorteile:**
- ✅ **Keine Installation nötig**: URL öffnen, „Zum Home-Bildschirm"
- ✅ **Plattform-unabhängig**: iOS, Android, Windows, macOS
- ✅ **Automatische Updates**: Neue Version bei nächstem Laden
- ✅ **Offline-Fähigkeit**: Service Worker cacht App + Daten
- ✅ **Schneller Start**: Assets aus Cache, keine Downloads
- ✅ **App-ähnlich**: Fullscreen, eigenes Icon, keine Browser-UI
- ✅ **Eine Codebasis**: Kein nativer Code pro Plattform
- ✅ **Keine App-Store-Gebühren**: 0€ statt 99€/Jahr (Apple)

**Für Aquarius:**
- ✅ Kleine Liga (20 Kinder) → App Store lohnt sich nicht
- ✅ Ehrenamtliche Helfer → Einfache Nutzung ohne Installation
- ✅ Schwimmbad-Internet → Offline-Fähigkeit kritisch

### Alternative: Native App (Swift/Kotlin)

**Pro:**
- ✅ Beste Performance
- ✅ Voller Zugriff auf Geräte-APIs

**Contra:**
- ❌ **2 Codebasen**: iOS (Swift) + Android (Kotlin/Java)
- ❌ **App-Store-Prozess**: Review-Zeit, Gebühren
- ❌ **Entwicklungsaufwand**: 2-3x länger
- ❌ **Updates**: User müssen manuell aktualisieren

**Entscheidung gegen Native:** Zu hoher Aufwand für kleine Liga

### Alternative: React Native / Flutter

**Pro:**
- ✅ Eine Codebasis für iOS + Android
- ✅ Gute Performance

**Contra:**
- ❌ **Trotzdem App-Store**: Installation + Review nötig
- ❌ **Build-Komplexität**: Xcode, Android Studio
- ❌ **Native-Abhängigkeiten**: Platform-spezifische Bugs
- ❌ **Keine Desktop-Version**: Planungs-App wäre separate Codebasis

**Entscheidung gegen React Native:** PWA reicht aus, weniger Komplexität

### Alternative: Electron App

**Pro:**
- ✅ Desktop-App mit Web-Technologie

**Contra:**
- ❌ **Keine Mobile-Unterstützung**: Tablets ausgeschlossen
- ❌ **Installation nötig**: Download + Setup
- ❌ **Große Bundle-Size**: Chromium mitgeliefert

**Entscheidung gegen Electron:** Mobile ist Hauptfokus

## Konsequenzen

### Positiv

1. **Schnelle Entwicklung**: Eine Codebasis für alle Plattformen
2. **Offline-First**: Bewertung funktioniert ohne Internet
3. **Einfache Distribution**: URL teilen statt App Store
4. **Automatische Updates**: Neue Features sofort verfügbar
5. **Niedrige Kosten**: Kein App Store, keine Device-Testing-Farm

### Negativ

1. **iOS-Limitierungen**: Safari hat eingeschränkte PWA-Features
2. **Kein App-Store-Listing**: Discoverability schlechter (aber irrelevant für geschlossene Liga)
3. **Browser-Abhängigkeit**: Safari/Chrome Updates können App brechen
4. **Storage-Limits**: IndexedDB hat Größenbeschränkungen (aber ausreichend)

### iOS-spezifische Einschränkungen

| Feature | iOS Safari | Android Chrome |
|---------|-----------|---------------|
| Installierbar | ✅ (seit iOS 11.3) | ✅ |
| Service Worker | ✅ (seit iOS 11.3) | ✅ |
| Background Sync | ❌ | ✅ |
| Push Notifications | ❌ (Stand 2024) | ✅ |
| Fullscreen | ⚠️ (Partial) | ✅ |
| Offline Storage | ✅ (50 MB Limit) | ✅ (Quota-based) |

**Mitigation:** Background Sync nicht kritisch, da Sync manuell getriggert werden kann

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| iOS löscht Cache zu aggressiv | Mittel | Hoch | Embedded Turso Replica statt nur Cache |
| Storage-Quota überschritten | Niedrig | Mittel | Alte Daten periodisch löschen |
| Service Worker Bugs | Niedrig | Hoch | Gründliches Testing, Fallback auf Online-Modus |

## Implementierung

### 1. Web App Manifest

```json
// apps/execution/public/manifest.json
{
  "name": "Aquarius Durchführung",
  "short_name": "Aquarius",
  "description": "Wettkampf-Durchführung und Live-Bewertung",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0ea5e9",
  "theme_color": "#0ea5e9",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["sports", "utilities"],
  "screenshots": [
    {
      "src": "/screenshots/bewertung.png",
      "sizes": "1170x2532",
      "type": "image/png"
    }
  ]
}
```

### 2. Service Worker (Workbox)

```typescript
// apps/execution/src/service-worker.ts
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { NetworkFirst, CacheFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Precache all build assets
precacheAndRoute(self.__WB_MANIFEST);

// API Requests: Network First (mit Cache-Fallback)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60, // 5 Minuten
      }),
    ],
  })
);

// Bilder: Cache First
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Tage
      }),
    ],
  })
);

// HTML: Stale While Revalidate
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new StaleWhileRevalidate({
    cacheName: 'pages-cache',
  })
);
```

### 3. Offline-Status-Komponente

```typescript
// apps/execution/src/components/OfflineIndicator.tsx
import { useEffect, useState } from 'react';

export function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (isOnline) return null;

  return (
    <div className="fixed top-0 left-0 right-0 bg-yellow-500 text-white px-4 py-2 text-center">
      ⚠️ Offline-Modus: Daten werden lokal gespeichert und später synchronisiert
    </div>
  );
}
```

### 4. Installation-Prompt

```typescript
// apps/execution/src/hooks/useInstallPrompt.ts
import { useState, useEffect } from 'react';

export function useInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [isInstallable, setIsInstallable] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setIsInstallable(true);
    };

    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const promptInstall = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === 'accepted') {
      setIsInstallable(false);
    }
    setDeferredPrompt(null);
  };

  return { isInstallable, promptInstall };
}
```

### 5. Vite PWA Plugin

```typescript
// apps/execution/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'icons/*.png'],
      manifest: {
        name: 'Aquarius Durchführung',
        short_name: 'Aquarius',
        theme_color: '#0ea5e9',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.aquarius\..*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 300 },
            },
          },
        ],
      },
    }),
  ],
});
```

## Validierung

### Success Criteria

- ✅ **Lighthouse PWA Score > 90**
- ✅ **Installierbar** auf iOS Safari und Chrome
- ✅ **Offline-Funktionalität**: Bewertung ohne Internet möglich
- ✅ **Service Worker**: Registriert und aktiv
- ✅ **Manifest**: Valide, alle erforderlichen Felder
- ✅ **HTTPS**: Deployment auf HTTPS (erforderlich für PWA)

### Testing-Checkliste

```bash
# Lighthouse PWA Audit
lighthouse https://aquarius.app/execution --view

# Service Worker registriert?
# Chrome DevTools → Application → Service Workers

# Offline-Test
# Chrome DevTools → Network → Offline
# App sollte weiterhin funktionieren

# iOS Installation
# Safari → Share → Add to Home Screen

# Android Installation
# Chrome → Menu → Install App
```

### Metriken

| Metrik | Zielwert | Aktuell |
|--------|----------|---------|
| Lighthouse PWA Score | > 90 | TBD |
| Offline Funktionalität | 100% kritische Features | TBD |
| Service Worker Cache Hit Rate | > 80% | TBD |
| Time to Interactive (3G) | < 5s | TBD |

## Referenzen

- [PWA Documentation (web.dev)](https://web.dev/progressive-web-apps/)
- [Workbox Documentation](https://developer.chrome.com/docs/workbox/)
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/)
- [iOS PWA Support](https://webkit.org/blog/8090/workers-at-your-service/)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |
