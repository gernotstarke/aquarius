# ADR-015: Turso (libSQL) als Datenbank

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-014 FastAPI Backend](ADR-014-python-fastapi-backend.md), [ADR-016 PWA Architecture](ADR-016-pwa-architecture.md)

---

## Kontext

Die Aquarius-Anwendung benötigt eine Datenbanklösung, die zwei gegensätzliche Anforderungen erfüllt:
1.  **Zentrale Datenhaltung** für die Planung (Web-App).
2.  **Offline-Fähigkeit** für die Durchführung am Beckenrand (Mobile App).

Kritisch ist, dass die Bewertung im Schwimmbad auch bei Netzwerkausfällen unterbrechungsfrei weiterlaufen muss, die Daten aber später automatisch synchronisiert werden sollen.

## Entscheidung

Wir verwenden **Turso (libSQL)** als Datenbanktechnologie.

*   Siehe **[Architekturkonzept: Persistenz mit Turso](../architecture/08-persistence-with-turso.adoc)** für Details zu Architektur und Betrieb.

## Begründung

### Pro Turso (libSQL)

*   **Offline-First**: Durch *Embedded Replicas* kann die Datenbank lokal auf dem Endgerät (Tablet) laufen und sich im Hintergrund synchronisieren.
*   **SQLite-Kompatibilität**: Ermöglicht einfache lokale Entwicklung (mit Standard-SQLite-Dateien) und nutzt das etablierte SQL-Ökosystem.
*   **Edge-Replication**: Sorgt für niedrige Latenzen bei Online-Zugriffen.
*   **Managed Service**: Geringer Betriebsaufwand im Vergleich zu selbst gehosteten Replikationslösungen.

### Alternativen

*   **PostgreSQL**: Hat keinen nativen Offline-Sync für Endgeräte. Sync-Logik müsste selbst implementiert werden (hoher Aufwand/Risiko).
*   **CouchDB/PouchDB**: Wäre eine gute Offline-Lösung, ist aber NoSQL. Das Domänenmodell von Aquarius ist stark relational (Wettkampf -> Station -> Durchgang -> Wertung), was SQL prädestiniert.

## Konsequenzen

### Positiv
*   Entwicklung bleibt einfach (lokales SQLite).
*   Das "Split-Brain"-Problem (Netzwerk weg) ist architektonisch gelöst.
*   Kostenloser Einstieg (Free Tier).

### Negativ
*   Vendor Lock-in bezüglich der Sync-Technologie.
*   Technologie ist noch relativ jung ("Bleeding Edge").

### Risiken & Mitigation
*   **Sync-Konflikte**: Werden durch "Last-Write-Wins" Strategie oder fachliche Partitionierung (nur ein Punktrichter pro Station) minimiert.