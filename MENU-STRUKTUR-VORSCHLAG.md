# Arqua42 - Vorschlag für geschachtelte Menüstruktur

## Hauptnavigation (Top-Level)

### 1. 📅 **Stammdaten**
Grundlegende Daten, die für alle Wettkämpfe benötigt werden:
- Saisons (bestehend)
- Schwimmbäder (bestehend)
- Figuren (neu)
  - Liste aller verfügbaren Schwimmfiguren
  - Name, Beschreibung, Schwierigkeitsgrad
  - Kategorisierung (z.B. nach Alter, Können)

### 2. 👶 **Kinder**
Teilnehmerverwaltung:
- Kinder (bestehend)
- Vereine
  - Liste aller Vereine
  - Kontaktdaten, Verantwortliche

### 3. 🏆 **Wettkampfplanung**
Planung und Organisation von Wettkämpfen:

#### 3.1 Wettkampf-Übersicht
- Liste aller Wettkämpfe
- Filter nach Saison, Status (geplant/laufend/abgeschlossen)

#### 3.2 Wettkampf bearbeiten → führt zu Untermenu
Bei Auswahl eines Wettkampfs:

**Basis-Informationen**
- Name, Datum, Schwimmbad, Max. Teilnehmer
- Saison-Zuordnung

**Figuren für diesen Wettkampf**
- Auswahl der erlaubten Figuren aus Stammdaten
- Editierbare Liste (Hinzufügen/Entfernen)

**Stationen planen**
- Anzahl der Stationen
- Pro Station: Name, Verantwortliche
- Pro Station: Erlaubte Figuren (Subset der Wettkampf-Figuren)

**Zeitplanung**
- Gruppen definieren (z.B. Altersgruppen)
- Pro Gruppe: Zeitslot zuweisen
- Pro Gruppe: Station zuweisen
- Rotationsplan erstellen

**Anmeldungen (read-only)**
- Liste aller angemeldeten Kinder
- Filter nach Verein, Altersgruppe
- Status der Anmeldung
- Welche Figuren jedes Kind zeigen will

### 4. 📝 **Anmeldung**
Für Vereine/Präsident zum Anmelden von Kindern:

#### 4.1 Wettkampf auswählen
- Liste der offenen Wettkämpfe
- Zeigt: Name, Datum, freie Plätze

#### 4.2 Anmeldung durchführen
- Kind auswählen
- Figuren auswählen (aus den für den Wettkampf erlaubten)
- Optional: Präferenz für Zeitslot/Gruppe
- Bestätigung

#### 4.3 Meine Anmeldungen
- Übersicht aller Anmeldungen
- Nach Wettkampf gruppiert
- Bearbeiten/Stornieren möglich (bis Anmeldeschluss)

### 5. 🎯 **Wettkampf-Durchführung**
Für Helfer während des Wettkampfs:

#### 5.1 Station auswählen
- Auswahl der aktuellen Station

#### 5.2 Bewertung erfassen
- Aktuelle Gruppe anzeigen
- Kind auswählen
- Pro Figur: Bewertung eingeben
- Schnelle Navigation zum nächsten Kind

### 6. 📊 **Auswertung**
Nach dem Wettkampf:

#### 6.1 Ergebnisse
- Rangliste pro Altersgruppe
- Detailansicht pro Kind
- Export-Funktion (PDF, CSV)

#### 6.2 Statistiken
- Verteilung der Bewertungen
- Beliebte Figuren
- Vereins-Statistiken

---

## Vorschlag für Navigation-Komponente

### Variante A: Mega-Menu (Desktop)
```
┌─────────────────────────────────────────────────────────┐
│ [Arqua42]  Stammdaten ▼  Kinder  Wettkämpfe ▼  ...     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐                               │
│  │ Stammdaten           │                               │
│  ├──────────────────────┤                               │
│  │ • Saisons            │                               │
│  │ • Schwimmbäder       │                               │
│  │ • Figuren            │                               │
│  └──────────────────────┘                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Variante B: Sidebar (Mobile & Desktop)
```
┌──────────┬──────────────────────────────────┐
│          │                                   │
│ 📅       │  Hauptinhalt                     │
│ Stamm-   │                                   │
│ daten ▼  │                                   │
│  • Saison│                                   │
│  • Bad   │                                   │
│  • Figur │                                   │
│          │                                   │
│ 🏆       │                                   │
│ Wett-    │                                   │
│ kämpfe ▼ │                                   │
│  • Neu   │                                   │
│  • Liste │                                   │
│          │                                   │
└──────────┴──────────────────────────────────┘
```

### Variante C: Breadcrumb-Navigation (Empfohlen)
Für tiefe Hierarchien gut geeignet:
```
Home > Wettkämpfe > Herbstcup 2024 > Stationen > Station 1 > Bewertung
```

---

## Empfehlung für die Implementierung

**Phase 1 (aktuell):**
- Flaches Top-Menu wie jetzt
- Stammdaten + Kinder + Wettkämpfe + Anmeldung

**Phase 2 (nächster Schritt):**
- Sidebar-Navigation mit Kollaps-Bereichen
- Breadcrumbs für Kontext
- Wettkampf-Detail als eigene View mit Tabs:
  - Tab "Basis"
  - Tab "Figuren"
  - Tab "Stationen"
  - Tab "Zeitplanung"
  - Tab "Anmeldungen"

**Phase 3 (später):**
- Durchführungs-Modus (vereinfachte UI)
- Auswertungs-Views

---

## Mobile-First Überlegungen

Für ehrenamtliche Helfer sollte die App auf Tablets/Phones gut funktionieren:

- **Große Touch-Targets** (min 44px) ✓ bereits implementiert
- **Hamburger-Menu** für Hauptnavigation auf Mobile
- **Bottom-Navigation** für wichtigste Funktionen während Wettkampf
- **Swipe-Gesten** für Navigation zwischen Kindern
- **Offline-Fähigkeit** (PWA) für Bewertungs-Modus

---

## Technische Umsetzung

### React Router Setup
```typescript
/                           → Home
/stammdaten
  /saisons                  → SaisonList
  /schwimmbaeder            → SchwimmbadList
  /figuren                  → FigurenList
/kinder                     → KindList
/wettkämpfe                 → WettkampfList
/wettkämpfe/:id
  /basis                    → WettkampfForm
  /figuren                  → WettkampfFigurenEdit
  /stationen                → StationenPlan
  /zeitplanung              → ZeitplanEdit
  /anmeldungen              → AnmeldungenView (read-only)
/anmeldung
  /wettkampf-wählen         → WettkampfSelect
  /durchführen/:wkId        → AnmeldungForm
  /meine                    → MyAnmeldungen
```

### Navigation Component
```typescript
<Navigation>
  <NavSection title="Stammdaten" icon="📅">
    <NavItem to="/stammdaten/saisons">Saisons</NavItem>
    <NavItem to="/stammdaten/schwimmbaeder">Schwimmbäder</NavItem>
    <NavItem to="/stammdaten/figuren">Figuren</NavItem>
  </NavSection>

  <NavSection title="Wettkämpfe" icon="🏆">
    <NavItem to="/wettkämpfe">Übersicht</NavItem>
    <NavItem to="/wettkämpfe/new">Neu anlegen</NavItem>
  </NavSection>

  <NavSection title="Anmeldung" icon="📝">
    <NavItem to="/anmeldung/wettkampf-wählen">Neue Anmeldung</NavItem>
    <NavItem to="/anmeldung/meine">Meine Anmeldungen</NavItem>
  </NavSection>
</Navigation>
```
