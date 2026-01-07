# ADR-029: Lokale Playwright E2E-Tests

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Team

## Kontext

Playwright E2E-Tests sind aktuell nur lokal zuverlässig ausführbar (kein Docker/CI-Setup verfügbar).

## Entscheidung

Wir führen Playwright E2E-Tests lokal auf dem Host-System aus und dokumentieren sie als manuellen Schritt.

## Konsequenzen

- E2E-Abdeckung bleibt lokal und wird nicht in CI automatisiert.
- Entwickler müssen Playwright lokal installiert halten.

## Referenzen

- [ADR-009: Testkonzept mit realer Datenbank](ADR-009-testkonzept.md)
