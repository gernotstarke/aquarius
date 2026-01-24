# ADR-034: Dockerized Test Runner Strategy

**Status:** Accepted
**Datum:** 2026-01-22
**Kontext:** Test-Automatisierung und Developer Experience (DX)
**Entscheider:** Architekt, Entwicklungsteam

---

## Kontext und Problem

Das Projekt nutzt `make test` als zentralen Einstiegspunkt für Tests (siehe [ADR-010](ADR-010-makefile-build-interface.md)).
Bei der Ausführung dieses Targets wird ein Docker-Container gebaut und gestartet, was beim **ersten Aufruf** (oder nach Änderungen an `requirements.txt`) zu erheblichen Wartezeiten (mehrere Minuten) führt.

**Ursache:**
- Der Container wird von Grund auf gebaut.
- `pip install --no-cache-dir` lädt und kompiliert alle Abhängigkeiten neu.
- Auf macOS/Windows läuft Docker in einer VM, was I/O-intensive Operationen wie Installationen zusätzlich verlangsamt.

**Frage:**
Warum nehmen wir diese initiale Wartezeit in Kauf, statt Tests einfach lokal in einem `venv` auszuführen?

---

## Entscheidung

Wir führen alle Tests (Unit, Integration, E2E) **ausschließlich in Docker-Containern** aus.
Der `make test` Befehl kapselt diese Logik vollständig.

### Begründung

1.  **Garantierte Konsistenz (Dev vs. CI):**
    - Tests laufen lokal in **exakt derselben Umgebung** (OS, Libraries, Python-Version) wie in der CI-Pipeline.
    - Das "Works on my machine"-Problem wird eliminiert.

2.  **Isolierung:**
    - Keine Konflikte mit lokal installierten Python-Versionen oder anderen Projekten.
    - Systemabhängigkeiten (z.B. für `psutil`, `bcrypt` oder Datenbank-Treiber) sind im Image definiert und müssen nicht auf dem Host-System installiert werden.

3.  **Vereinfachtes Onboarding:**
    - Ein neuer Entwickler muss nur Docker und Make installieren.
    - Kein manuelles Setup von `virtualenv`, `pip install`, `pyenv`, etc. notwendig.

---

## Konsequenzen

### Positiv ✅

- **Reproduzierbarkeit:** Ein fehlgeschlagener Test in der CI kann lokal exakt nachgestellt werden.
- **Sauberkeit:** Keine "verunreinigten" lokalen Umgebungen. `make clean` entfernt rückstandslos alle Artefakte.
- **Caching:** Nach dem ersten Build (Initialkosten) nutzen Folgestarts den Docker-Layer-Cache. Der Start dauert dann nur Sekunden.

### Negativ ⚠️

- **Initiale Wartezeit:** Der erste `make test` Lauf dauert lange (Download & Kompilierung der Dependencies).
- **Overhead:** Docker-Startzeit addiert sich zu jeder Testausführung (geringfügig).
- **Ressourcen:** Docker benötigt mehr RAM/CPU als ein lokales `venv`.

### Mitigation (Linderung)

- **Layer Caching:** Das `Dockerfile` ist so optimiert, dass `requirements.txt` vor dem Code kopiert wird. Änderungen am Code führen *nicht* zur Neuinstallation der Dependencies.
- **Volume Mounts:** Der Quellcode wird in den Container gemountet. Für Code-Änderungen ist kein Rebuild nötig.
- **Lokaler Fallback (Optional):** Erfahrene Entwickler *können* manuell ein `venv` nutzen, wenn sie die Risiken kennen, aber der offizielle Weg bleibt Docker.

---

## Alternativen

### 1. Lokales Virtual Environment (venv)

Tests laufen direkt auf dem Host-System.

*   **Vorteil:** Maximale Performance, kein Docker-Overhead.
*   **Nachteil:** Jeder Entwickler muss Python/Libs selbst verwalten. Inkonsistenzen zwischen OS (Mac/Linux/Windows). CI-Fehler schwerer reproduzierbar.

### 2. Hybrid-Ansatz

`make test` prüft, ob ein venv aktiv ist, und nutzt dieses, sonst Docker.

*   **Vorteil:** Flexibilität.
*   **Nachteil:** Komplexes Makefile. Verwirrung ("Warum geht es bei dir und bei mir nicht?").

---

## Fazit

Die **Konsistenz und Stabilität** der Entwicklungsumgebung wird höher gewichtet als die **initiale Einrichtungszeit**. Die Wartezeit ist eine einmalige Investition pro Änderung der Abhängigkeiten.
