# ADR-017: TailwindCSS für Styling

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-013 React Frontend](ADR-013-react-typescript-frontend.md)

---

## Kontext

Aquarius benötigt zwei UI-Varianten mit unterschiedlichen Design-Anforderungen:

**1. Planungs-App (Desktop)**
- Komplexe Formulare mit vielen Feldern
- Tabellen für Daten-Übersichten
- Standard Desktop-UI (Maus + Tastatur)

**2. Durchführungs-App (Mobile/Tablet)**
- **Touch-optimiert**: Mindestens 44×44px Touch-Targets
- **Große Buttons**: Gut drückbar auch mit nassen Händen
- **Hoher Kontrast**: Lesbar in heller Schwimmbad-Umgebung
- **Einfache Navigation**: Minimale UI, fokussierte Workflows

**Anforderungen:**
- Responsive Design (Desktop + Tablet + Mobile)
- Konsistentes Design-System zwischen beiden Apps
- Schnelle Entwicklung (Ehrenamtliche, begrenztes Budget)
- Wartbarkeit (kein CSS-Experte im Team erforderlich)
- Dark Mode (optional, für Abendveranstaltungen)

## Entscheidung

Wir verwenden **TailwindCSS** als Utility-First CSS Framework.

### Styling-Stack

```
Styling Stack:
├── TailwindCSS 3.x          # Utility-First CSS
├── PostCSS                   # CSS-Processing
├── Autoprefixer              # Browser-Kompatibilität
└── Custom Design Tokens      # aquarius-theme.js
    ├── Colors (Liga-Branding)
    ├── Spacing (Touch-Targets)
    └── Typography
```

### Design-System-Struktur

```
packages/ui/
├── src/
│   ├── components/
│   │   ├── Button.tsx         # <Button variant="primary" size="lg" />
│   │   ├── Input.tsx          # <Input label="Name" />
│   │   ├── Card.tsx
│   │   └── ...
│   └── tailwind.config.js     # Shared Config
└── package.json

apps/planning/
└── tailwind.config.js         # Extends shared config

apps/execution/
└── tailwind.config.js         # Extends shared config + Touch-optimizations
```

## Begründung

### Pro TailwindCSS

**Vorteile:**
- ✅ **Utility-First**: Styling direkt im JSX, keine CSS-Dateien
- ✅ **Design-System**: Konsistente Spacing/Colors out-of-the-box
- ✅ **Responsive**: Mobile-First Breakpoints (sm, md, lg, xl)
- ✅ **Purge**: Ungenutztes CSS wird automatisch entfernt (kleine Bundle-Size)
- ✅ **IntelliSense**: VS Code Plugin mit Autovervollständigung
- ✅ **Keine Naming-Konflikte**: Kein BEM, keine CSS-Module nötig
- ✅ **Schnelle Iteration**: Änderungen direkt sichtbar, kein CSS-Switching

**Für Aquarius:**
- ✅ Touch-Targets: `min-h-[44px] min-w-[44px]` als Utility
- ✅ Shared Components: `@aquarius/ui` Package
- ✅ Theming: Custom Colors für Liga-Branding
- ✅ Dark Mode: `dark:bg-gray-900` out-of-the-box

### Alternative: Plain CSS / CSS Modules

**Pro:**
- ✅ Kein Build-Step nötig
- ✅ Standard-Technologie

**Contra:**
- ❌ Naming-Konflikte (BEM ist verbose)
- ❌ CSS-Dateien getrennt von Komponenten
- ❌ Kein Design-System (muss selbst gebaut werden)
- ❌ Responsive Design manuell

**Entscheidung gegen Plain CSS:** Zu viel Boilerplate

### Alternative: Styled-Components / Emotion

**Pro:**
- ✅ CSS-in-JS, Styling bei Komponente
- ✅ Dynamic Styling (Props → Styles)

**Contra:**
- ❌ Runtime-Overhead (CSS wird zur Laufzeit generiert)
- ❌ Größere Bundle-Size
- ❌ SSR-Komplexität
- ❌ Kein Design-System out-of-the-box

**Entscheidung gegen CSS-in-JS:** Performance-Overhead, Tailwind reicht

### Alternative: Material UI / Chakra UI

**Pro:**
- ✅ Fertige Komponenten-Library
- ✅ Accessibility eingebaut

**Contra:**
- ❌ Größere Bundle-Size (100+ KB)
- ❌ Weniger Flexibilität (eigenes Design schwieriger)
- ❌ Lernkurve für Component-API
- ❌ Mobile-First nicht optimal (Material = Desktop-first)

**Entscheidung gegen Component-Libraries:** Zu groß, zu wenig Kontrolle

### Alternative: Bootstrap

**Pro:**
- ✅ Weit verbreitet, bekannt

**Contra:**
- ❌ jQuery-Abhängigkeit (historisch, nicht mehr)
- ❌ „Bootstrap-Look" (generisch)
- ❌ Schwerer zu customizen als Tailwind
- ❌ Größere Bundle-Size

**Entscheidung gegen Bootstrap:** Tailwind ist moderner

## Konsequenzen

### Positiv

1. **Rapid Prototyping**: Komponenten schnell stylen ohne CSS-Dateien
2. **Konsistenz**: Design-System über shared Tailwind-Config
3. **Performance**: Purge entfernt ungenutztes CSS (< 10 KB final CSS)
4. **Responsive**: Mobile-First Breakpoints eingebaut
5. **Dark Mode**: `dark:` Prefix für einfache Dark-Mode-Implementierung

### Negativ

1. **Verbose JSX**: className mit vielen Utilities kann lang werden
2. **Lernkurve**: Tailwind-Klassennamen müssen gelernt werden
3. **Tooling-Abhängigkeit**: IntelliSense-Plugin empfohlen
4. **Custom CSS**: Manchmal braucht man doch @apply oder Arbitrary Values

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| className zu lang und unleserlich | Mittel | Niedrig | Komponenten extrahieren, @apply für Patterns |
| Tailwind-Update bricht Styles | Niedrig | Mittel | Semantic Versioning, Tests |
| Große CSS-Datei (Purge fehlgeschlagen) | Niedrig | Mittel | Purge-Config validieren, Bundle-Analyzer |

## Implementierung

### 1. Tailwind-Konfiguration (Shared)

```javascript
// packages/ui/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#0ea5e9',  // Liga-Blau
          900: '#0c4a6e',
        },
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      spacing: {
        '18': '4.5rem',  // Custom spacing
        'touch': '44px',  // Minimum Touch Target
      },
      minHeight: {
        'touch': '44px',
      },
      minWidth: {
        'touch': '44px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),  // Bessere Form-Styles
    require('@tailwindcss/typography'),  // Prose-Styles
  ],
}
```

### 2. Execution-App Touch-Optimierung

```javascript
// apps/execution/tailwind.config.js
const sharedConfig = require('../../packages/ui/tailwind.config.js');

/** @type {import('tailwindcss').Config} */
module.exports = {
  ...sharedConfig,
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',  // Shared Components
  ],
  theme: {
    extend: {
      ...sharedConfig.theme.extend,
      // Execution-App: Größere Touch-Targets
      fontSize: {
        'base': '18px',  // Standard größer als Desktop
        'xl': '24px',
        '3xl': '32px',
      },
    },
  },
}
```

### 3. Button-Komponente (Shared)

```typescript
// packages/ui/src/components/Button.tsx
import { ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base Styles
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
  {
    variants: {
      variant: {
        primary: 'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
        danger: 'bg-danger text-white hover:bg-red-600 focus:ring-red-500',
      },
      size: {
        sm: 'px-3 py-2 text-sm',
        md: 'px-4 py-2.5 text-base',
        lg: 'px-6 py-3 text-lg min-h-touch min-w-touch',  // Touch-optimiert
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size, className })}
      {...props}
    />
  );
}
```

### 4. Responsive Card-Komponente

```typescript
// packages/ui/src/components/Card.tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div
      className={`
        bg-white dark:bg-gray-800
        rounded-lg shadow-md
        p-4 sm:p-6
        border border-gray-200 dark:border-gray-700
        ${className}
      `}
    >
      {children}
    </div>
  );
}
```

### 5. Touch-Optimierte Navigation (Execution-App)

```typescript
// apps/execution/src/components/Navigation.tsx
export function Navigation() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 dark:bg-gray-900 dark:border-gray-700">
      <div className="flex justify-around">
        <button className="flex flex-col items-center py-3 px-4 min-h-touch">
          <HomeIcon className="w-8 h-8 mb-1" />
          <span className="text-sm">Übersicht</span>
        </button>
        <button className="flex flex-col items-center py-3 px-4 min-h-touch">
          <ClipboardIcon className="w-8 h-8 mb-1" />
          <span className="text-sm">Bewertung</span>
        </button>
        <button className="flex flex-col items-center py-3 px-4 min-h-touch">
          <ChartIcon className="w-8 h-8 mb-1" />
          <span className="text-sm">Ergebnisse</span>
        </button>
      </div>
    </nav>
  );
}
```

### 6. Dark Mode Toggle

```typescript
// packages/ui/src/hooks/useDarkMode.ts
import { useEffect, useState } from 'react';

export function useDarkMode() {
  const [isDark, setIsDark] = useState(
    () => window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  return [isDark, setIsDark] as const;
}
```

## Validierung

### Success Criteria

- ✅ **Bundle Size**: Final CSS < 15 KB (gzipped)
- ✅ **Touch-Targets**: Alle interaktiven Elemente ≥ 44×44px (Execution-App)
- ✅ **Kontrast**: WCAG AA (4.5:1 für Text)
- ✅ **Shared Components**: Mindestens 10 wiederverwendbare Komponenten in `@aquarius/ui`
- ✅ **Responsive**: Mobile, Tablet, Desktop ohne Horizontal-Scroll

### Metriken

```bash
# CSS Bundle Size
pnpm build
ls -lh apps/execution/dist/assets/*.css

# Purge-Validation (ungenutzte Klassen?)
pnpm exec tailwindcss -i ./src/index.css -o ./dist/check.css

# Kontrast-Check (Lighthouse Accessibility)
lighthouse https://aquarius.app --view
```

## Referenzen

- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Tailwind UI](https://tailwindui.com/) - Premium Components
- [Headless UI](https://headlessui.com/) - Unstyled Accessible Components
- [Touch Target Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |
