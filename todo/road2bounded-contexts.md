# Weg zu Bounded Contexts (Planung vs. Durchführung)

## Ziel
Einen eigenen Bounded Context für die mobile Durchführung am Beckenrand
einführen – mit eigener Datenbank und klarer Synchronisation zur
Planungs-/Web-Anwendung.

## Namensvorschlag
- **Planung** (Web, Anmeldung/Administration)
- **Durchführung** (Mobile, Wettkampfabwicklung vor Ort)

Alternativen, falls ihr es noch präziser wollt:
- **Wettkampfplanung** / **Wettkampfdurchführung**
- **Organisation** / **Ausführung**

## Plan
1. **Bounded-Context-Skizze**
   - Zwei Kontexte definieren: „Planung“ (Web, Admin/Anmeldung) und
     „Durchführung“ (Mobile, Poolbetrieb).
   - Kerndomänen je Kontext festlegen; gemeinsame Begriffe als „Published
     Language“ markieren (z. B. Wettkampf, Kind, Team, Start, Bewertung).
   - Ownership-Regeln klären: Welche Aggregate liegen ausschließlich in
     welchem Kontext?
   - Betriebsregeln festlegen: Während der Durchführung sind **keine neuen
     Anmeldungen** erlaubt; **Löschungen von Anmeldungen** müssen möglich sein.

2. **Integrationsstrategie**
   - Sync-Ansatz wählen: Event-basierte Replikation vs. periodischer Pull/Push.
   - Datenhoheit pro Attribut definieren (Source of Truth).
   - Konfliktlösung festlegen (z. B. last-write-wins oder domänenspezifisch).
   - Bewertungsdaten sind in „Durchführung“ führend und müssen zuverlässig in
     „Planung“ ankommen (Auswertung/Siegerlisten).

3. **Datenverträge**
   - Ein-/Ausgehende Datenverträge zwischen den Kontexten spezifizieren.
   - Versioniertes Sync-Schema definieren (Events oder Snapshots).
   - Stabile IDs für kontextübergreifende Referenzen festlegen.
   - Bewertungsworkflow abbilden: Kind führt Figur an Station aus -> Bewertung
     erfassen -> Wertungen zurück synchronisieren.

4. **Technische Architektur**
   - Mobile Datenbanktopologie festlegen (lokal SQLite/Turso-Replikat).
   - Sync-Infrastruktur definieren (Background-Job, Queue, oder direkte API).
   - Betriebsanforderungen klären (Offline-Modus, Retry/Backoff, Telemetrie).

5. **MVP-Rollout**
   - Start mit Read-only-Replikation von Planung -> Durchführung.
   - Danach Write-back für Wertungen (Durchführung -> Planung) und Löschungen
     von Anmeldungen.
   - Pilot-Wettkampf als End-to-End-Validierung.

6. **Doku & ADRs**
   - ADRs ergänzen: Kontext-Schnitt und Synchronisationsstrategie.
   - Architektur-Doku um Context Map und Integrationsmuster erweitern.
