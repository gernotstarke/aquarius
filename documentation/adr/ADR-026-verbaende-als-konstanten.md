# ADR-026: Verbände als Konstanten

**Status:** Accepted
**Datum:** 2026-01-05
**Entscheider:** Gernot Starke

## Kontext

Die Aquarius-Anwendung muss Verbände (DSV, ÖSV, SSV) verwalten. Es stellt sich die Frage: Sollen Verbände als editierbare Entitäten in der Datenbank gespeichert oder als Konstanten im Code definiert werden?

**Fakten:**
- Die drei Verbände (DSV, ÖSV, SSV) existieren seit Jahrzehnten
- Keine Änderungen in den letzten Jahren
- Neue Verbände sind extrem unwahrscheinlich
- Keine Umbenennung oder Löschung zu erwarten

## Entscheidung

Wir verwenden **Konstanten im Code** statt einer editierbaren Datenbank-Entität.

**Implementierung:**
```python
# Verbände als Python Enum/Konstanten
VERBAENDE = ["DSV", "ÖSV", "SSV"]
```

**Keine Admin-UI** zum Bearbeiten von Verbänden.

## Konsequenzen

### Positiv ✅
- **Einfacher**: Kein CRUD für Verbände nötig (weniger Code)
- **Schneller**: Keine Datenbank-Queries für statische Werte
- **Sicherer**: Keine versehentliche Löschung/Änderung möglich
- **Wartbar**: Änderungen über Code-Review statt Admin-Interface

### Negativ ⚠️
- Bei Änderungen: Code-Anpassung + Deployment nötig (statt Admin-UI)
- Nicht flexibel für hypothetische neue Verbände

### Mitigation
Falls doch Flexibilität nötig wird: Migration zu Datenbank-Entität ist einfach möglich (Enum → Tabelle).

## Offene Fragen
- Sollten wir Verband-Logos/Farben ebenfalls als Konstanten speichern?
