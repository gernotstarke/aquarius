# Aquarius - Domänenmodell

## Fachliche Definitionen

### Organisationsstruktur
- **Verein**: Zusammenschluss von Sportbegeisterten zur organisierten Ausübung des Sports
- **Team**: Gruppierung von Kindern eines Vereins nach dessen Kriterien
- **Kind**: Startberechtigtes Mitglied der Kinderschwimmliga
- **Offizieller**: Ehrenamtliches Mitglied der Liga für Organisation und Abwicklung
  - **Kampfrichter**: Bewertet Starts mit vorläufigen Punkten
  - **Punktrichter**: Verantwortlich für reibungslosen Ablauf an einer Station

### Wettkampfstruktur
- **Saison**: Zeitraum mit geplanten Wettkämpfen
- **Wettkampf**: Sportliche Veranstaltung zum Leistungsvergleich (Figuren- und Synchronschwimmen)
- **Schwimmbad**: Austragungsort für Wettkämpfe
- **Station**: Ort am Becken, wo Durchgänge ausgeführt und bewertet werden
- **Durchgang**: Teil eines Wettkampfes, bei dem alle Kinder einer Gruppe eine Figur nacheinander vorführen
- **Gruppe**: Zusammengefasste Kinder für optimalen Wettkampfablauf
- **Figur**: Vorgeschriebener Bewegungsablauf mit Bewertungsregeln und Schwierigkeitsfaktor

### Teilnahme & Bewertung
- **Anmeldung**: Wunsch eines Kindes, bei einem Wettkampf teilzunehmen und ausgewählte Figuren vorzuzeigen
- **Start (Versuch)**: Antreten eines Kindes zur Vorführung einer bestimmten Figur
- **Bewertung**: Kampfrichter geben vorläufige Punkte, Punktrichter berechnet Endpunkte (höchste/niedrigste streichen, Durchschnitt × Schwierigkeitsfaktor)

## Entitäten und Beziehungen

```
Saison (1) ──┬── (*) Wettkampf
             │
             └── (*) Figur (Saisonfiguren)

Verein (1) ──── (*) Team (1) ──── (*) Kind

Wettkampf (1) ──┬── (*) Station
                ├── (*) Anmeldung
                ├── (*) Gruppe
                └── (1) Schwimmbad

Station (1) ──┬── (*) Durchgang
              ├── (*) Kampfrichter-Zuweisung
              └── (1) Punktrichter

Durchgang (1) ──┬── (1) Figur
                ├── (1) Gruppe
                └── (*) Start

Start (1) ──┬── (1) Kind
            ├── (1) Figur
            └── (*) Bewertung (vorläufige Punkte von Kampfrichtern)

Kind (1) ──┬── (*) Anmeldung
           └── (*) Start
```

## Kern-Geschäftsprozesse

### 1. Saisonplanung (Büro)
- Saison anlegen
- Figuren definieren (mit Schwierigkeitsfaktor)
- Wettkämpfe planen (Termine, Schwimmbäder)
- Vereine, Teams, Kinder verwalten
- Offizielle (Kampf-/Punktrichter) registrieren

### 2. Wettkampfvorbereitung (Büro)
- Anmeldungen bearbeiten
- Gruppen einteilen
- Stationen definieren
- Kampf-/Punktrichter zuweisen
- Durchgänge planen (Figur, Station, Gruppe)

### 3. Wettkampfdurchführung (Schwimmbad/Mobile)
- Durchgang starten
- Kind aufrufen (Startnummer)
- Kampfrichter erfassen vorläufige Punkte
- Punktrichter berechnet Endpunkte automatisch
- Zwischenergebnisse anzeigen
- Am Ende: Einzel- und Teampreise nach Altersgruppen

## Bewertungslogik

1. Jeder Kampfrichter gibt vorläufige Punkte (z.B. 0-10)
2. Höchste und niedrigste Punktzahl werden gestrichen
3. Durchschnitt der verbleibenden Punkte wird berechnet
4. Endpunkte = Durchschnitt × Schwierigkeitsfaktor der Figur
5. Einzelwertung: nur Figurenschwimmen, pro Altersgruppe
6. Teamwertung: Figuren- + Synchronschwimmen, pro Altersgruppe
