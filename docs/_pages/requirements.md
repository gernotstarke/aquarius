---
permalink: /requirements/
title: "Anforderungen"
layout: single
toc: true
toc_label: "Inhalt"
toc_icon: "list"
---

# Aquarius - Anforderungsdokument
## Bewertungssystem für Kunstschwimmen-Wettkämpfe

**Version:** 1.0  
**Datum:** 2025-12-17  
**Status:** Initial Draft

---

## 1. Einführung und Ziele

### 1.1 Aufgabenstellung
Entwicklung eines computerunterstützten Bewertungssystems für eine regionale Kinderliga im Kunstschwimmen. Das System unterstützt die komplette Wettkampforganisation von der Saisonplanung über die Anmeldung bis zur Live-Bewertung und Ergebnisauswertung.

**Fokus:** Das System berücksichtigt primär das **Figurenschwimmen** (nicht Synchronschwimmen).

### 1.2 Qualitätsziele

| Priorität | Qualitätsziel | Beschreibung |
|-----------|---------------|--------------|
| 1 | **Benutzbarkeit** | Einfachste Bedienung für nicht-computer-affine Benutzer |
| 2 | **Verfügbarkeit** | Offline-Fähigkeit im Schwimmbad, Cloud-Synchronisation |
| 3 | **Korrektheit** | Fehlerfreie Bewertungsberechnung nach vorgegebenen Regeln |
| 4 | **Performance** | Schnelle Reaktionszeiten bei der Live-Bewertung |
| 5 | **Wartbarkeit** | Modulare Architektur für einfache Erweiterungen |

### 1.3 Stakeholder

| Rolle | Beschreibung | Erwartungen |
|-------|--------------|-------------|
| **Präsident** | Leiter der Kinderliga | Saisonplanung, Wettkampforganisation, Reporting |
| **Assistent des Präsidenten** | Unterstützung bei Verwaltung | Figurenkatalog verwalten, Stammdaten pflegen |
| **Verein** | Sportverein mit Teams | Kinder anmelden, Teamdaten verwalten |
| **Kind** | Teilnehmer | Sich zu Wettkämpfen anmelden |
| **Offizieller** | Kampf-/Punktrichter | Wettkampfplanung, Durchführung, Bewertung |
| **Punktrichter** | Stationsverantwortlicher | Reibungsloser Ablauf an Station, Endpunkte berechnen |
| **Schwimmverband** | Übergeordnete Organisation | Statusänderungen, Katalogaktualisierung |

---

## 2. Randbedingungen

### 2.1 Technische Randbedingungen

| ID | Randbedingung | Beschreibung |
|----|---------------|--------------|
| TR-01 | Web-Anwendung | Moderne Web-App (keine Desktop-Installation) |
| TR-02 | Mobile-First | Touch-optimiert für Tablets/Smartphones im Schwimmbad |
| TR-03 | Progressive Web App | Installierbar, Offline-Fähigkeit |
| TR-04 | Cloud-Datenbank | Turso (libSQL) mit Sync-Funktionalität |
| TR-05 | Responsive Design | Eine Codebasis für Desktop (Büro) und Mobile (Schwimmbad) |
| TR-06 | Browser-Kompatibilität | Moderne Browser (Chrome, Firefox, Safari, Edge) |

### 2.2 Organisatorische Randbedingungen

| ID | Randbedingung | Beschreibung |
|----|---------------|--------------|
| OR-01 | Zwei Betriebsmodi | Planung (Büro/Desktop) und Durchführung (Schwimmbad/Mobile) |
| OR-02 | Zentral gehostet | Planungs-App muss nicht offline-fähig sein |
| OR-03 | Offline-Fähigkeit | Durchführungs-App muss im Schwimmbad ohne Internet funktionieren |
| OR-04 | Datensynchronisation | Automatische Sync zwischen Büro und Schwimmbad |

---

## 3. Kontextabgrenzung

### 3.1 Fachlicher Kontext

```
[Verein] ──> AQUARIUS <── [Präsident/Assistent]
[Kind] ──> AQUARIUS <── [Offizieller]
[Punktrichter] ──> AQUARIUS
[Schwimmverband] ──> AQUARIUS
```

### 3.2 System-Scope

**Im Scope:**
- ✅ Figurenschwimmen-Bewertung
- ✅ Saisonplanung und Wettkampforganisation
- ✅ Anmeldungsverwaltung
- ✅ Live-Bewertung mit Punkteerfassung
- ✅ Einzel- und Teamwertung (nur Figuren)
- ✅ Stammdatenverwaltung

**Out of Scope:**
- ❌ Synchronschwimmen-Bewertung (erwähnt für Teamwertung, aber nicht im Detail)
- ❌ Finanzielle Abwicklung
- ❌ Externe Schnittstellen zu anderen Systemen

---

## 4. Fachliche Domäne

### 4.1 Glossar

| Begriff | Definition |
|---------|------------|
| **Anmeldung** | Wunsch eines Kindes, bei einem Wettkampf teilzunehmen und ausgewählte Figuren vorzuzeigen |
| **Durchgang** | Teil eines Wettkampfes, bei dem alle Kinder einer Gruppe eine Figur nacheinander vorführen und bewertet werden |
| **Figur** | Vorgeschriebener Bewegungsablauf mit Bewertungsregeln und Schwierigkeitsfaktor |
| **Gruppe** | Zusammengefasste Kinder für optimalen Wettkampfablauf |
| **Kampfrichter** | Offizieller, der Starts mit vorläufigen Punkten bewertet |
| **Kind** | Startberechtigtes Mitglied der Kinderschwimmliga |
| **Offizieller** | Ehrenamtlicher für Organisation und Abwicklung |
| **Punktrichter** | Offizieller, verantwortlich für reibungslosen Ablauf an einer Station |
| **Saison** | Zeitraum mit geplanten Wettkämpfen |
| **Schwimmbad** | Austragungsort für Wettkämpfe |
| **Start (Versuch)** | Antreten eines Kindes zur Vorführung einer Figur |
| **Station** | Ort am Becken, wo Durchgänge ausgeführt und bewertet werden |
| **Team** | Gruppierung von Kindern eines Vereins |
| **Verein** | Zusammenschluss von Sportbegeisterten |
| **Wettkampf** | Sportliche Veranstaltung zum Leistungsvergleich |

### 4.2 Domänenmodell

```
Saison (1) ──┬── (*) Wettkampf
             └── (*) Figur

Verein (1) ──── (*) Team (1) ──── (*) Kind

Wettkampf (1) ──┬── (*) Station
                ├── (*) Anmeldung
                ├── (*) Gruppe
                └── (1) Schwimmbad

Station (1) ──┬── (*) Durchgang
              ├── (*) Kampfrichter
              └── (1) Punktrichter

Durchgang (1) ──┬── (1) Figur
                ├── (1) Gruppe
                └── (*) Start

Start (1) ──┬── (1) Kind
            ├── (1) Figur
            └── (*) Bewertung

Kind (1) ──┬── (*) Anmeldung
           └── (*) Start
```

---

## 5. Funktionale Anforderungen

### 5.1 Saisonplanung (Use Case: Saisonplanung)

**Akteur:** Präsident

**Beschreibung:** Der Präsident plant 6 Monate vor Saisonbeginn die kommende Saison.

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-01 | System muss Saison mit Zeitraum anlegen können | MUSS |
| FA-02 | System muss Figuren für die Saison definieren können | MUSS |
| FA-03 | Figuren müssen Schwierigkeitsfaktor haben | MUSS |
| FA-04 | System muss Wettkämpfe mit Datum und Schwimmbad planen | MUSS |
| FA-05 | System muss Wettkampfplan exportieren/drucken können | SOLLTE |
| FA-06 | System muss Kinder rechtzeitig über Saison informieren können | SOLLTE |

### 5.2 Stammdatenverwaltung

**Akteur:** Assistent des Präsidenten, Schwimmverband

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-10 | System muss Figurenkatalog verwalten können | MUSS |
| FA-11 | System muss neuen Figurenkatalog importieren können | MUSS |
| FA-12 | System muss alten Katalog durch neuen ersetzen können | MUSS |
| FA-13 | System muss Vereine anlegen und verwalten können | MUSS |
| FA-14 | System muss Teams verwalten können | MUSS |
| FA-15 | System muss Schwimmbäder mit Adresse verwalten können | MUSS |
| FA-16 | System muss Offizielle registrieren können | MUSS |
| FA-17 | System muss Statusänderungen vornehmen können | SOLLTE |

### 5.3 Startberechtigte aktualisieren

**Akteur:** Verein

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-20 | System muss Kinder registrieren können (Name, Alter, Adresse, Team) | MUSS |
| FA-21 | System muss Vereinszugehörigkeit speichern | MUSS |
| FA-22 | System muss Kinder eines Vereins auflisten können | MUSS |
| FA-23 | System muss Altersgruppen automatisch berechnen | MUSS |
| FA-24 | System muss Änderungen an Kinderdaten ermöglichen | MUSS |

### 5.4 Kind identifizieren (Sub-Use-Case)

**Akteur:** System

**Trigger:** Anmeldungsprozess, Wettkampfprüfung

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-30 | System muss Kind eindeutig identifizieren können | MUSS |
| FA-31 | System muss nach Name, Geburtsdatum, Verein suchen | MUSS |
| FA-32 | System muss Vereinszugehörigkeit prüfen | MUSS |
| FA-33 | System muss Kind vorläufig registrieren, wenn nicht vom Verein gemeldet | SOLLTE |
| FA-34 | System muss bei nicht-startberechtigten Kindern Anmeldung ablehnen | MUSS |

### 5.5 Wettkampfanmeldung

**Akteur:** Kind (oder Verein stellvertretend)

**Beschreibung:** Kind meldet sich zu einem Wettkampf an und wählt Figuren aus.

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-40 | System muss verfügbare Wettkämpfe anzeigen | MUSS |
| FA-41 | System muss Figuren des Wettkampfs zur Auswahl anbieten | MUSS |
| FA-42 | System muss Kind Figuren auswählen lassen | MUSS |
| FA-43 | System muss Wettkampfverfügbarkeit prüfen | MUSS |
| FA-44 | System muss bei überfülltem Wettkampf Warteliste anbieten | SOLLTE |
| FA-45 | System muss alternative Wettkämpfe vorschlagen | SOLLTE |
| FA-46 | System muss Figurenwahl validieren (altersgerecht, verfügbar) | MUSS |
| FA-47 | System muss Figurentausch ermöglichen | SOLLTE |
| FA-48 | System muss Doppelmeldungen erkennen | MUSS |
| FA-49 | System muss Wünsche bei Doppelmeldung korrigieren lassen | MUSS |
| FA-50 | System muss freie Startnummer für Kind finden | MUSS |
| FA-51 | System muss Startnummer vergeben und speichern | MUSS |
| FA-52 | System muss Anmeldung bestätigen | MUSS |

### 5.6 Wettkampfplanung

**Akteur:** Offizieller

**Beschreibung:** Offizieller plant Wettkampfdetails vor Ort.

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-60 | System muss Stationen anlegen können (z.B. 4 Ecken des Beckens) | MUSS |
| FA-61 | System muss Kampfrichter Stationen zuweisen können | MUSS |
| FA-62 | System muss Punktrichter Stationen zuweisen können | MUSS |
| FA-63 | System muss Kampfrichter-Wechsel während Wettkampf ermöglichen | MUSS |
| FA-64 | System muss angemeldete Kinder in Gruppen einteilen | MUSS |
| FA-65 | System muss Durchgänge planen (Figur, Station, Gruppe) | MUSS |
| FA-66 | System muss jeder Gruppe eine Startstation zuweisen | MUSS |
| FA-67 | System muss Rotationsplan erstellen (Gruppen wechseln Stationen) | SOLLTE |
| FA-68 | System muss Durchgangsreihenfolge pro Station planen | MUSS |

### 5.7 Versuch bewerten (Wettkampfdurchführung)

**Akteur:** Punktrichter, Kampfrichter

**Beschreibung:** Live-Bewertung während des Wettkampfs.

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-70 | System muss Durchgänge an Stationen starten können | MUSS |
| FA-71 | System muss Startnummer des nächsten Kindes anzeigen | MUSS |
| FA-72 | System muss Kind aufrufen (große Anzeige der Startnummer) | MUSS |
| FA-73 | System muss Pausen bei Unordnung ermöglichen | SOLLTE |
| FA-74 | System muss Kampfrichter vorläufige Punkte eingeben lassen | MUSS |
| FA-75 | Eingabe muss touch-optimiert sein (große Buttons) | MUSS |
| FA-76 | System muss vorläufige Punkte aller Kampfrichter anzeigen | MUSS |
| FA-77 | System muss höchste und niedrigste Punktzahl automatisch streichen | MUSS |
| FA-78 | System muss Durchschnitt der verbleibenden Punkte berechnen | MUSS |
| FA-79 | System muss Endpunkte = Durchschnitt × Schwierigkeitsfaktor berechnen | MUSS |
| FA-80 | System muss Endpunkte für Start speichern | MUSS |
| FA-81 | System muss zum nächsten Kind übergehen können | MUSS |
| FA-82 | System muss Korrekturen an Bewertungen ermöglichen | SOLLTE |

### 5.8 Wettkampf auswerten

**Akteur:** Punktrichter, Offizieller

**Beschreibung:** Berechnung der Ergebnisse und Preisvergabe.

| ID | Anforderung | Priorität |
|----|-------------|-----------|
| FA-90 | System muss Gesamtpunkte pro Kind berechnen (Summe aller Starts) | MUSS |
| FA-91 | System muss Einzelrangliste pro Altersgruppe erstellen | MUSS |
| FA-92 | System muss Einzelpreise basierend auf Figurenschwimmen vergeben | MUSS |
| FA-93 | System muss Teampunkte berechnen (Figuren + Synchron) | SOLLTE |
| FA-94 | System muss Teamrangliste pro Altersgruppe erstellen | SOLLTE |
| FA-95 | System muss Teampreise vergeben | SOLLTE |
| FA-96 | System muss Zwischenergebnisse während Wettkampf anzeigen | SOLLTE |
| FA-97 | System muss Endergebnisse exportieren/drucken können | MUSS |
| FA-98 | System muss Urkunden generieren können | KANN |

---

## 6. Qualitätsanforderungen

### 6.1 Benutzbarkeit (Höchste Priorität)

| ID | Anforderung | Messkriterium |
|----|-------------|---------------|
| QA-01 | Intuitive Bedienung ohne Schulung | 80% der Benutzer können Kernfunktionen ohne Anleitung nutzen |
| QA-02 | Touch-optimierte Oberfläche im Schwimmbad | Buttons mindestens 44×44px, großer Abstand |
| QA-03 | Klare visuelle Hierarchie | Wichtige Aktionen hervorgehoben |
| QA-04 | Fehlertoleranz | Rückgängig-Funktion für kritische Aktionen |
| QA-05 | Schnelles Feedback | Bestätigungen innerhalb 0,5 Sekunden |

### 6.2 Verfügbarkeit

| ID | Anforderung | Messkriterium |
|----|-------------|---------------|
| QA-10 | Offline-Fähigkeit im Schwimmbad | 100% der Durchführungs-Funktionen offline nutzbar |
| QA-11 | Automatische Synchronisation | Sync innerhalb 30 Sekunden nach Verbindungsaufbau |
| QA-12 | Konfliktauflösung | Eindeutige Strategie bei Sync-Konflikten |

### 6.3 Performance

| ID | Anforderung | Messkriterium |
|----|-------------|---------------|
| QA-20 | Schnelle Ladezeiten | Initial Load < 3 Sekunden |
| QA-21 | Responsive UI | Reaktionszeit < 200ms bei Eingaben |
| QA-22 | Effiziente Bewertungsberechnung | Endpunkte in < 100ms berechnet |

### 6.4 Korrektheit

| ID | Anforderung | Messkriterium |
|----|-------------|---------------|
| QA-30 | Korrekte Bewertungsberechnung | 100% Testabdeckung der Berechnungslogik |
| QA-31 | Keine Datenverluste | Transaktionale Speicherung aller Bewertungen |
| QA-32 | Eindeutige Startnummern | Keine Duplikate pro Wettkampf |

### 6.5 Wartbarkeit

| ID | Anforderung | Messkriterium |
|----|-------------|---------------|
| QA-40 | Modulare Architektur | Klare Trennung von Planung und Durchführung |
| QA-41 | Erweiterbarkeit | Neue Figuren ohne Code-Änderung hinzufügbar |
| QA-42 | Testabdeckung | Mindestens 80% Code Coverage |

---

## 7. Lösungsstrategie

### 7.1 Architektur-Übersicht

**Zwei Module mit gemeinsamer Datenbasis:**

1. **Planungs-Modul** (Desktop-optimiert)
   - Saisonverwaltung
   - Stammdaten (Vereine, Teams, Kinder, Offizielle)
   - Wettkampfvorbereitung
   - Anmeldungsbearbeitung
   - Reporting

2. **Durchführungs-Modul** (Mobile/Touch-optimiert)
   - Punkteerfassung
   - Live-Bewertung
   - Stationsverwaltung
   - Ergebnisanzeige

### 7.2 Technologie-Stack

- **Frontend:** React + TypeScript + Vite + TailwindCSS
- **Backend:** Python FastAPI + Pydantic
- **Datenbank:** Turso (libSQL) mit Cloud-Sync
- **PWA:** Service Worker für Offline-Fähigkeit
- **Deployment:** Zentrales Hosting, responsive Web-App

### 7.3 Deployment-Szenarien

1. **Büro (Planung):**
   - Web-App im Browser
   - Online-Verbindung zur Cloud-Datenbank
   - Desktop-optimierte UI

2. **Schwimmbad (Durchführung):**
   - PWA auf Tablets installiert
   - Offline-Betrieb mit lokaler Datenhaltung
   - Automatische Sync bei Verbindung
   - Touch-optimierte UI

---

## 8. Prozessabläufe

### 8.1 Anmeldungsprozess (Aktivitätsdiagramm)

```
START
  ↓
[Kind identifizieren]
  │
  ├─[nicht startberechtigt]─→ ENDE
  │
  ↓ [Kind identifiziert]
  │
[Wettkampf prüfen]
  │
  ├─[Wettkampf nicht OK]─→ ENDE
  │
  ↓ [Wettkampf OK]
  │
[Anmeldung registrieren]
  │
  ↓
ENDE
```

**Details:**
- **Kind identifizieren:** Vereinszugehörigkeit prüfen, ggf. vorläufig registrieren
- **Wettkampf prüfen:** Verfügbarkeit, Figuren validieren, Alternativen vorschlagen, Warteliste
- **Anmeldung registrieren:** Doppelmeldungen erkennen, Startnummer vergeben

### 8.2 Wettkampfdurchführung

```
Vorbereitung:
1. Stationen einrichten
2. Kampf-/Punktrichter zuweisen
3. Gruppen bilden
4. Durchgänge planen

Durchführung (pro Durchgang):
1. Gruppe zur Station
2. Für jedes Kind:
   a. Startnummer aufrufen
   b. Kind führt Figur vor
   c. Kampfrichter geben vorläufige Punkte
   d. System berechnet Endpunkte
   e. Nächstes Kind
3. Nächster Durchgang

Auswertung:
1. Gesamtpunkte berechnen
2. Ranglisten erstellen (Altersgruppen)
3. Preise vergeben
```

---

## 9. Abnahmekriterien

### 9.1 Planungs-Modul

- [ ] Saison mit Wettkämpfen und Figuren planbar
- [ ] Vereine, Teams, Kinder vollständig verwaltbar
- [ ] Anmeldungen können erfasst und bearbeitet werden
- [ ] Startnummern werden automatisch vergeben
- [ ] Wettkampfplanung mit Stationen und Durchgängen möglich

### 9.2 Durchführungs-Modul

- [ ] Touch-optimierte UI auf Tablet nutzbar
- [ ] Offline-Betrieb im Schwimmbad funktioniert
- [ ] Punkteerfassung durch mehrere Kampfrichter parallel möglich
- [ ] Bewertungsberechnung korrekt nach Regeln
- [ ] Live-Zwischenergebnisse sichtbar
- [ ] Endergebnisse mit Ranglisten generierbar

### 9.3 Qualität

- [ ] 80% Testabdeckung
- [ ] Intuitive Bedienung ohne Schulung
- [ ] Ladezeit < 3 Sekunden
- [ ] Reaktionszeit < 200ms
- [ ] Automatische Datensynchronisation funktioniert

---

## 10. Risiken und Technische Schulden

| ID | Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|----|--------|-------------------|--------|------------|
| R-01 | Offline-Sync-Konflikte | Mittel | Hoch | Klare Konfliktauflösungsstrategie, "Last Write Wins" für Bewertungen |
| R-02 | Komplexe Gruppenbildung | Niedrig | Mittel | Manuelle Gruppenzuweisung als Fallback |
| R-03 | Touch-Bedienung bei Wettkampfstress | Mittel | Hoch | Extensive Usability-Tests, große Buttons |
| R-04 | Netzwerkausfall während Sync | Niedrig | Mittel | Retry-Mechanismus, Queue für ausstehende Syncs |

---

## 11. Offene Punkte

- [ ] Genaue Anzahl Kampfrichter pro Station?
- [ ] Synchronschwimmen-Details für Teamwertung?
- [ ] Authentifizierung und Rechteverwaltung?
- [ ] Backup-Strategie?
- [ ] Reporting-Anforderungen im Detail?
- [ ] Barrierefreiheit (WCAG-Konformität)?

---

**Dokumenthistorie:**

| Version | Datum | Autor | Änderungen |
|---------|-------|-------|------------|
| 1.0 | 2025-12-17 | Claude | Initiale Version basierend auf Use-Cases und Aktivitätsdiagrammen |