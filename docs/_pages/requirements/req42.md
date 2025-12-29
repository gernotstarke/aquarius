---
permalink: /requirements/req42/
title: "Req42 Framework"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-requirements-header-1500.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
  caption: "Basiert auf einer Idee von [Dr. Peter Hruschka](https://b-agile.de)"

---


<small>
**Version:** 1.1 vom 28. Dezember 2025  
**Status:** Auf req42 adaptiert.<br>
Hinweis: Dieses Dokument entspricht von der Struktur dem [req42 Template](https://req42.de) von Peter Hruschka und Markus Meuthen.
</small>

{% include toc title="Inhalt" %}


## 1. Vision/Ziele

### Aufgabenstellung

Ein computerunterstütztes Bewertungssystems für eine regionale Kinderliga im Kunstschwimmen. 
Das System unterstützt die komplette Wettkampforganisation von der Saisonplanung über die Anmeldung bis zur Live-Bewertung und Ergebnisauswertung.

Das gesamte System ist als Fallstudie für Schulungen in Softwarearchitektur und -engineering geplant.

>**Hinweis zur Fallgestaltung**:
>Diese Fallstudie verfolgt primär didaktische Ziele und ist vernachlässigt daher (möglicherweise)  organisatorische, sportliche oder wirtschaftliche Realitätsnähe.
>Sie dient dazu, Prinzipien, Methoden und Entscheidungsprozesse der Softwarearchitektur und des Software Engineerings nachvollziehbar zu veranschaulichen.
>Sowohl Vereinfachungen wie auch übermässig kompliziert anmutende Anforderungen sind deswegen beabsichtigt.

**Fokus:** Das System berücksichtigt primär das **Figurenschwimmen** einzelner Kinder (kein Synchronschwimmen).


---

## 2. Stakeholder

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

## 3. Scope-Abgrenzung

### Fachlicher Kontext
```
[Verein] ──> AQUARIUS <── [Präsident/Assistent]
[Kind] ──> AQUARIUS <── [Offizieller]
[Punktrichter] ──> AQUARIUS
[Schwimmverband] ──> AQUARIUS
```

### Scope
**In Scope:**
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

## 4. Product Backlog

### 4.1 Epics
- **E01 Saison- & Stammdatenverwaltung**: Alles rund um die Vorbereitung einer Saison (Figuren, Vereine, Wettkämpfe).
- **E02 Anmeldung & Teilnehmer**: Verwaltung der Anmeldungen durch Vereine/Kinder.
- **E03 Wettkampfplanung**: Konfiguration des konkreten Wettkampftages (Stationen, Gruppen).
- **E04 Durchführung & Bewertung**: Die Live-Applikation im Schwimmbad.
- **E05 Auswertung & Reporting**: Ergebnisse berechnen, Ranglisten, Urkunden.

### 4.2 Features

**F01 Saisonplanung** (zu E01)
Der Präsident plant die Saison, legt Wettkämpfe fest und definiert den Figurenkatalog.

**F02 Stammdatenpflege** (zu E01)
Verwaltung von Vereinen, Teams, Schwimmbädern und Offiziellen.

**F03 Anmeldungsmanagement** (zu E02)
Registrierung von Kindern, Prüfung der Startberechtigung und Durchführung der Wettkampfanmeldung inkl. Figurenwahl.

**F04 Stations- & Gruppenplanung** (zu E03)
Einteilung der Kinder in Gruppen, Zuweisung zu Stationen und Erstellung von Rotationsplänen.

**F05 Live-Bewertung** (zu E04)
Digitale Erfassung der Wertungen durch Kampfrichter, sofortige Berechnung der Endpunkte pro Start.

**F06 Ergebnisdienst** (zu E05)
Berechnung von Gesamtpunkten, Erstellung von Ranglisten nach Altersgruppen und Export der Ergebnisse.

### 4.3 User-Storys (Anforderungen)

#### Zu F01 Saisonplanung
* **FA-01**: Als Präsident möchte ich eine Saison mit Zeitraum anlegen.
* **FA-02**: Als Präsident möchte ich die Figuren für die Saison definieren.
* **FA-03**: Als System muss ich sicherstellen, dass Figuren einen Schwierigkeitsfaktor haben.
* **FA-04**: Als Präsident möchte ich Wettkämpfe mit Datum und Schwimmbad planen.
* **FA-05**: Als Präsident möchte ich den Wettkampfplan exportieren/drucken.
* **FA-06**: Als System möchte ich Kinder rechtzeitig über die Saison informieren.

#### Zu F02 Stammdatenpflege
* **FA-10**: Als Assistent möchte ich den Figurenkatalog verwalten.
* **FA-11**: Als Assistent möchte ich einen neuen Figurenkatalog importieren.
* **FA-12**: Als Assistent möchte ich alte Kataloge durch neue ersetzen.
* **FA-13**: Als Assistent möchte ich Vereine anlegen und verwalten.
* **FA-14**: Als Assistent möchte ich Teams verwalten.
* **FA-15**: Als Assistent möchte ich Schwimmbäder mit Adresse verwalten.
* **FA-16**: Als Assistent möchte ich Offizielle registrieren.

#### Zu F03 Anmeldungsmanagement
* **FA-20**: Als Verein möchte ich Kinder registrieren (Name, Alter, Adresse, Team).
* **FA-21**: Als System muss ich die Vereinszugehörigkeit speichern.
* **FA-30**: Als System muss ich Kinder eindeutig identifizieren können.
* **FA-40**: Als Kind möchte ich verfügbare Wettkämpfe sehen.
* **FA-42**: Als Kind möchte ich Figuren für den Wettkampf auswählen.
* **FA-46**: Als System muss ich die Figurenwahl validieren (altersgerecht).
* **FA-48**: Als System muss ich Doppelmeldungen erkennen.
* **FA-50**: Als System muss ich eine freie Startnummer finden und vergeben.

#### Zu F04 Stations- & Gruppenplanung
* **FA-60**: Als Offizieller möchte ich Stationen anlegen (z.B. 4 Ecken).
* **FA-61**: Als Offizieller möchte ich Kampfrichter den Stationen zuweisen.
* **FA-64**: Als System muss ich angemeldete Kinder in Gruppen einteilen.
* **FA-65**: Als System muss ich Durchgänge planen (Figur, Station, Gruppe).
* **FA-67**: Als System sollte ich einen Rotationsplan erstellen.

#### Zu F05 Live-Bewertung
* **FA-70**: Als Punktrichter möchte ich Durchgänge an Stationen starten.
* **FA-71**: Als System muss ich die Startnummer des nächsten Kindes anzeigen.
* **FA-74**: Als Kampfrichter möchte ich vorläufige Punkte eingeben.
* **FA-75**: Die Eingabe muss touch-optimiert sein (große Buttons).
* **FA-77**: Als System muss ich die höchste und niedrigste Punktzahl streichen.
* **FA-79**: Als System muss ich die Endpunkte berechnen (Durchschnitt x Schwierigkeit).

#### Zu F06 Ergebnisdienst
* **FA-90**: Als System muss ich Gesamtpunkte pro Kind berechnen.
* **FA-91**: Als System muss ich Einzelranglisten pro Altersgruppe erstellen.
* **FA-97**: Als Offizieller möchte ich Endergebnisse exportieren/drucken.
* **FA-98**: Als Offizieller möchte ich Urkunden generieren.

---

## 5. Modelle zur Unterstützung

### 5.1 Prozessmodelle

**Anmeldungsprozess:**
```
START -> [Kind identifizieren] -> [Wettkampf prüfen] -> [Anmeldung registrieren] -> ENDE
```

**Wettkampfdurchführung:**
Vorbereitung -> Durchführung (Startnummer aufrufen, Figur vorführen, Bewertung eingeben, Punkte berechnen) -> Auswertung

### 5.2 Datenmodell (Logisch)

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
```

---

## 6. Qualitätsanforderungen

| ID | Qualitätsmerkmal | Anforderung / Messkriterium |
|----|------------------|-----------------------------|
| QA-01 | **Benutzbarkeit** | Intuitive Bedienung ohne Schulung (80% Erfolgsrate beim ersten Versuch). |
| QA-02 | **Benutzbarkeit** | Touch-optimierte Oberfläche: Buttons mind. 44x44px. |
| QA-10 | **Verfügbarkeit** | Offline-Fähigkeit: 100% der Durchführungs-Funktionen müssen ohne Netz funktionieren. |
| QA-11 | **Verfügbarkeit** | Sync innerhalb 30s nach Verbindungsaufbau. |
| QA-20 | **Performance** | Initial Load < 3 Sekunden. |
| QA-22 | **Performance** | Bewertungsberechnung < 100ms. |
| QA-30 | **Korrektheit** | 100% Testabdeckung der Berechnungslogik. |
| QA-31 | **Korrektheit** | Transaktionale Speicherung, keine Datenverluste. |


---

## 7. Randbedingungen

### Technische Randbedingungen
* **TR-01**: Web-Anwendung (keine Installation).
* **TR-02**: Mobile-First / Touch-Optimiert.
* **TR-03**: PWA (Offline-fähig).
* **TR-04**: Cloud-Datenbank (Turso/libSQL).
* **TR-06**: Browser-Kompatibilität (Chrome, Firefox, Safari, Edge).

### Organisatorische Randbedingungen
* **OR-01**: Zwei Betriebsmodi (Planung/Büro vs. Durchführung/Schwimmbad).
* **OR-03**: Durchführung muss offline funktionieren.
* **OR-04**: Automatische Datensynchronisation.

---

## 8. Domänen-Terminologie

| Begriff | Definition |
|---------|------------|
| **Anmeldung** | Wunsch eines Kindes, an einem Wettkampf teilzunehmen. |
| **Durchgang** | Teil eines Wettkampfes: Eine Gruppe führt eine Figur an einer Station vor. |
| **Figur** | Vorgeschriebener Bewegungsablauf mit Schwierigkeitsfaktor. |
| **Gruppe** | Zusammengefasste Kinder für den Wettkampfablauf. |
| **Kampfrichter** | Offizieller, der die Ausführung bewertet (Notenvergabe). |
| **Kind** | Startberechtigter Teilnehmer. |
| **Punktrichter** | Stationsverantwortlicher, leitet den Durchgang, validiert Punkte. |
| **Start (Versuch)** | Einmaliges Vorführen einer Figur durch ein Kind. |
| **Station** | Ort am Becken (z.B. "Ecke 1"), wo bewertet wird. |

---

## 9. Betriebsmittel & Personal

> absichtlich frei gelassen

---

## 10. Teamstruktur

> absichtlich frei gelassen

---

## 11. Roadmaps

> absichtlich frei gelassen

---

## 12. Risiken/Annahmen

### Risiken
* **R-01 Offline-Sync-Konflikte**: Konflikte bei gleichzeitiger Bearbeitung. *Mitigation*: Last-Write-Wins für Bewertungen.
* **R-02 Komplexe Gruppenbildung**: Algorithmus könnte scheitern. *Mitigation*: Fallback auf manuelle Zuweisung.
* **R-03 Touch-Bedienung**: Stresssituation im Wettkampf. *Mitigation*: Große Buttons, Usability-Tests.
* **R-04 Netzwerkausfall**: Kein Sync möglich. *Mitigation*: Queueing und Retry-Mechanismus.

### Offene Punkte
* Genaue Anzahl Kampfrichter pro Station?
* Details zur Synchronschwimmen-Wertung (falls später relevant)?
* Authentifizierungskonzept im Detail?