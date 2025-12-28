# Quality Requirements

This document specifies the quality requirements for the Aquarius system using quality scenarios with measurable acceptance criteria.

## Quality Scenario Format

Each scenario follows this structure:
- **ID**: Unique identifier
- **Quality Attribute**: Category (Performance, Availability, Security, etc.)
- **Scenario**: Description of the situation
- **Acceptance Criteria**: Measurable success criteria

---

## Quality Scenarios

| ID | Quality Attribute | Scenario | Acceptance Criteria |
|---|---|---|---|
| **QS-01** | **Availability** | Ein Kampfrichter bewertet eine Darbietung während das WLAN im Schwimmbad ausfällt (30 Sekunden bis 5 Minuten). Die Bewertung muss gespeichert und später synchronisiert werden. | • Bewertungs-App funktioniert >99,9% der Zeit offline<br>• Alle offline erfassten Bewertungen werden innerhalb von 10 Sekunden nach Verbindungswiederherstellung synchronisiert<br>• Kein Datenverlust bei Netzausfall |
| **QS-02** | **Consistency** | Zwei Kampfrichter bewerten dieselbe Darbietung offline mit unterschiedlichen Punkten (z.B. 8.5 vs 8.7). Nach Wiederverbindung müssen beide Bewertungen konfliktfrei gespeichert werden. | • Split-Brain Konflikte werden automatisch erkannt<br>• Konfliktauflösungs-Strategie (Last-Write-Wins oder CRDT) ist dokumentiert und implementiert<br>• Konflikt-Log im Admin-Panel einsehbar<br>• Keine Bewertung geht verloren |
| **QS-03** | **Security (Privacy)** | Ein Administrator exportiert Wettkampf-Ergebnisse. Persönliche Daten (Geburtsdatum, Adresse) von minderjährigen Teilnehmern dürfen nicht in öffentlichen Exporten enthalten sein. | • GDPR-konforme Datenminimierung implementiert<br>• Öffentliche Exporte enthalten nur: Name, Verein, Startnummer, Punkte<br>• Vollständige Daten nur für autorisierte Rollen (Wettkampfleiter)<br>• Audit-Log dokumentiert jeden Datenzugriff<br>• DSGVO "Right to be Forgotten" innerhalb 30 Tage umsetzbar |
| **QS-04** | **Security (Authentication)** | Ein nicht-autorisierter Benutzer versucht auf Teilnehmer-Daten zuzugreifen. | • Zugriff wird verweigert (HTTP 401/403)<br>• Fehlgeschlagene Login-Versuche werden geloggt<br>• Nach 5 fehlgeschlagenen Versuchen: Account-Sperre für 15 Minuten<br>• Passwörter mit bcrypt (min. 10 rounds) gehasht |
| **QS-05** | **Reliability** | Während der Anmeldephase registrieren 3 Sachbearbeiter gleichzeitig Teilnehmer. Jeder Teilnehmer muss eine eindeutige Startnummer erhalten. | • Keine Duplikate bei parallelen Registrierungen (0% Fehlerrate)<br>• Atomare Startnummern-Vergabe via Database Locks<br>• Race Conditions durch Transaktions-Isolation verhindert<br>• Bei Fehler: Retry mit Exponential Backoff (max. 3 Versuche) |
| **QS-06** | **Availability (Failover)** | Der zentrale Server fällt während eines laufenden Wettkampfs aus. | • Mobile Apps arbeiten mindestens 4 Stunden autark weiter<br>• Nach Server-Wiederherstellung: Automatische Sync innerhalb 60 Sekunden<br>• RTO (Recovery Time Objective) ≤ 5 Minuten<br>• RPO (Recovery Point Objective) ≤ 1 Minute |
| **QS-07** | **Performance (Latency)** | Ein Kampfrichter gibt eine Bewertung ein und drückt "Submit". Die Bewertung muss an andere Geräte übertragen und die Ergebnis-Anzeige aktualisiert werden. | • Lokale Bestätigung innerhalb 200ms<br>• Synchronisation an Server innerhalb 1 Sekunde (bei Verbindung)<br>• Leaderboard-Update innerhalb 2 Sekunden nach letzter Kampfrichter-Bewertung<br>• WebSocket Push an Public Display: <500ms Latenz |
| **QS-08** | **Performance (Throughput)** | 100 Zuschauer greifen gleichzeitig auf die Live-Ergebnisse zu. | • System unterstützt ≥150 gleichzeitige Benutzer<br>• API Response Time p95 <500ms unter Last<br>• Frontend lädt innerhalb 2 Sekunden (LCP - Largest Contentful Paint)<br>• CDN-Caching für statische Assets (Cache-Hit-Rate >90%) |
| **QS-09** | **Interoperability** | Das System muss Wettkampf-Ergebnisse an die DSV-API (Deutscher Schwimm-Verband) übermitteln. Die API hat Rate-Limits (10 req/min) und ist gelegentlich nicht verfügbar. | • Retry-Logik mit Exponential Backoff implementiert<br>• Circuit Breaker nach 5 Fehlversuchen (30s Wartezeit)<br>• Request-Queue mit max. 100 wartenden Anfragen<br>• Erfolgreiche Übermittlung innerhalb 24h garantiert (99%)<br>• Manuelle Retry-Option im Admin-Panel |
| **QS-10** | **Maintainability (Versioning)** | Der Figuren-Katalog wird für die Saison 2026 aktualisiert (neue Figuren, geänderte Schwierigkeitsgrade). Wettkämpfe aus 2025 müssen mit dem alten Katalog anzeigbar bleiben. | • Figuren-Katalog ist versioniert (gültig-von/gültig-bis Datum)<br>• Wettkampf referenziert Katalog-Version beim Anlegen<br>• Historische Wettkämpfe zeigen korrekte Figuren + Schwierigkeitsgrade<br>• Katalog-Migration via Admin-Tool (mit Rollback-Option)<br>• Breaking Changes werden als neue Major-Version gespeichert |
| **QS-11** | **Traceability (Audit)** | Ein Kampfrichter ändert nachträglich eine bereits gespeicherte Bewertung. Diese Änderung muss nachvollziehbar sein (wer, wann, alt vs. neu). | • Jede Änderung erzeugt Event im Audit-Log<br>• Log enthält: User-ID, Timestamp, alte Werte, neue Werte, Grund (optional)<br>• Audit-Log ist append-only (keine Löschung/Änderung möglich)<br>• Admin kann Audit-Trail pro Teilnehmer/Wettkampf einsehen<br>• Logs werden 10 Jahre aufbewahrt (Compliance) |
| **QS-12** | **Usability (Learnability)** | Ein technisch unerfahrener Wettkampf-Planer soll ohne Schulung einen neuen Wettkampf anlegen können (Teilnehmer, Datum, Figuren-Katalog). | • Workflow ist wizard-basiert (Schritt-für-Schritt)<br>• Kontextsensitive Hilfe-Texte bei jedem Eingabefeld<br>• Erfolgreiche Task-Completion ohne Hilfe: ≥80% der Testpersonen<br>• Time-on-Task für Wettkampf-Anlage: ≤5 Minuten (Durchschnitt)<br>• Fehlerrate bei Eingaben: <5% |
| **QS-13** | **Usability (Error Tolerance)** | Ein Sachbearbeiter gibt versehentlich ein ungültiges Geburtsdatum ein (z.B. "32.13.2010"). | • Eingabe wird sofort validiert (Client-side + Server-side)<br>• Fehlermeldung ist klar und handlungsorientiert ("Bitte gültiges Datum im Format TT.MM.JJJJ eingeben")<br>• Fehlerhafte Felder werden visuell markiert (rot umrandet)<br>• Korrekte Eingaben bleiben erhalten (kein Formular-Reset)<br>• Undo-Funktion für letzte 5 Aktionen verfügbar |
| **QS-14** | **Scalability (Data Volume)** | Nach 5 Jahren Betrieb enthält die Datenbank 10.000 Wettkämpfe, 50.000 Teilnehmer, 500.000 Bewertungen. | • Datenbankabfragen bleiben performant (p95 <500ms)<br>• Indexierung auf relevanten Spalten (wettkampf_id, teilnehmer_id, timestamp)<br>• Archivierung alter Wettkämpfe (>3 Jahre) in separates Schema<br>• Backup-Größe: <5 GB (komprimiert)<br>• Restore-Zeit: <30 Minuten |
| **QS-15** | **Scalability (Concurrent Users)** | Ein nationaler Wettkampf mit 500 Teilnehmern und 20 Kampfrichtern findet statt. | • System unterstützt ≥30 gleichzeitige Kampfrichter-Bewertungen<br>• ≥500 gleichzeitige Zuschauer-Zugriffe auf Ergebnisse<br>• Auto-Scaling bei >70% CPU-Auslastung (fly.io)<br>• Database Connection Pool: min 10, max 50 Verbindungen<br>• Keine Timeouts während Peak-Load |
| **QS-16** | **Portability (Offline Capability)** | Ein Kampfrichter nutzt die Mobile App an einem Ort ohne Internet (3 Stunden Offline-Zeit). | • Vollständige Funktionalität offline (Bewertungen, Zeitplan, Teilnehmerliste)<br>• Lokale SQLite-Datenbank speichert alle relevanten Daten<br>• Storage-Bedarf: <100 MB pro Wettkampf<br>• Battery Drain: <20% Akku-Verbrauch pro Stunde aktiver Nutzung<br>• Sync-Payload komprimiert (gzip): <1 MB für typischen Wettkampf |
| **QS-17** | **Testability (Integration)** | Ein Entwickler integriert eine neue Bewertungs-Regel (z.B. "Bonus für Synchronität"). Die Änderung muss testbar sein ohne echten Wettkampf. | • Unit-Tests für Bewertungs-Logik (Code Coverage ≥80%)<br>• Integrationstests mit Test-Datenbank (SQLite in-memory)<br>• E2E-Tests mit Mock-Kampfrichtern (Playwright/Cypress)<br>• CI/CD Pipeline: Alle Tests in <5 Minuten<br>• Test-Fixtures für typische Wettkampf-Szenarien vorhanden |
| **QS-18** | **Modifiability (Configuration)** | Ein Wettkampf-Organisator möchte die Scoring-Methode ändern (von "Average" zu "Drop Highest/Lowest"). | • Scoring-Methode ist per Wettkampf konfigurierbar (keine Code-Änderung)<br>• Admin-UI bietet Dropdown mit verfügbaren Methoden<br>• Änderung wirkt sich nur auf zukünftige Bewertungen aus (Historische bleiben unverändert)<br>• Plugin-Architektur erlaubt neue Scoring-Methoden ohne Core-Änderung<br>• Änderung ist in <2 Minuten umsetzbar |
| **QS-19** | **Recoverability (Data Loss)** | Durch einen Fehler werden versehentlich Bewertungen gelöscht. | • Point-in-Time Recovery möglich (Turso Backup jede Stunde)<br>• Soft-Delete (Daten werden markiert, nicht physisch gelöscht)<br>• Wiederherstellung innerhalb 15 Minuten möglich<br>• Event-Sourcing Log erlaubt Replay bis zu bestimmtem Zeitpunkt<br>• Automatische Backups: täglich (behalten 7 Tage), wöchentlich (behalten 4 Wochen) |
| **QS-20** | **Security (Authorization)** | Ein Kampfrichter versucht Teilnehmer-Stammdaten zu ändern (darf nur bewerten). | • Rollen-basierte Zugriffskontrolle (RBAC) implementiert<br>• Kampfrichter-Rolle hat nur Lese-Zugriff auf Teilnehmer<br>• Schreib-Zugriff nur für Rollen: Admin, Wettkampfleiter<br>• API validiert Berechtigungen serverseitig (nie nur clientseitig)<br>• Unauthorized Access wird geloggt und alarmiert |

## Quality Attribute Overview

| Quality Attribute | Scenario IDs | Priority |
|---|---|---|
| **Availability** | QS-01, QS-06 | ⭐⭐⭐ Critical |
| **Consistency** | QS-02, QS-05 | ⭐⭐⭐ Critical |
| **Performance** | QS-07, QS-08 | ⭐⭐⭐ Critical |
| **Security** | QS-03, QS-04, QS-20 | ⭐⭐⭐ Critical |
| **Usability** | QS-12, QS-13 | ⭐⭐ High |
| **Scalability** | QS-14, QS-15 | ⭐⭐ High |
| **Reliability** | QS-05 | ⭐⭐⭐ Critical |
| **Interoperability** | QS-09 | ⭐ Medium |
| **Maintainability** | QS-10, QS-18 | ⭐⭐ High |
| **Traceability** | QS-11 | ⭐⭐⭐ Critical |
| **Portability** | QS-16 | ⭐⭐ High |
| **Testability** | QS-17 | ⭐⭐ High |
| **Recoverability** | QS-19 | ⭐⭐⭐ Critical |

## Measurement Approach

All acceptance criteria are measurable through:
- **Automated Tests**: Unit, Integration, E2E tests in CI/CD
- **Performance Monitoring**: APM tools (e.g., Sentry, DataDog)
- **Manual Testing**: User acceptance testing with real organizers and judges
- **Load Testing**: k6, Locust for stress tests
- **Security Audits**: Penetration testing, GDPR compliance reviews
- **Usability Testing**: Task completion rate, time-on-task measurements

---

*These quality scenarios drive the architectural challenges documented in `/challenges/`*
