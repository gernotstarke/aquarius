# ADR-032: App User Authentication & Authorization

**Status:** Accepted  
**Datum:** 2026-01-11  
**Entscheider:** Gernot Starke

## Kontext

Aquarius benötigt mehrere unterschiedliche User-Rollen:

1. **Admin**: Verwaltung von Benutzern, Systemkonfiguration, Monitoring 
2. **CLEO**: Chief League & Executive Officer, die Sonder-Rolle für Fritz Flosse, den Liga-Präsidenten.
3. **Verwaltung**: Zugriff auf die Wettkampf-Verwaltungsanwendung mit Lese-/Schreibrechten
4. **Offizielle**: Können Figuren/Durchführungen/Starts bei Wettkämpfen bewerten, und Anmeldungen für den jeweiligen Wettkampf löschen.
5. **Teilnehmende**: Können sich selbst anmelden, ihre eigenen Stammdaten ändern, Ergebnislisten sehen. 

**Anforderungen:**
- Vereinfachte Lokalentwicklung ohne obligatorische Authentifizierung
- Produktionsumgebung mit vollständiger Authentifizierung
- Granulare Berechtigungen (Lesen vs. Schreiben)
- Einfaches Bootstrap-Verfahren für die erste Benutzer-Erstellung

## Entscheidung

Wir implementieren ein **umgebungsgestütztes App-Authentifizierungssystem**:

### Backend-Architektur

1. **User-Modell erweitern** (`app/models/user.py`):
   - `is_app_user: bool` - Markiert App-Benutzer vs. reine Admin-Benutzer
   - `can_read_all: bool` - Lesezugriff auf App-Daten
   - `can_write_all: bool` - Schreib-/Änderungs-/Löschzugriff

2. **Umgebungsvariablen**:
   ```env
   ENABLE_APP_AUTH=false  # Entwicklung: Auto-Login ohne Token
   ENABLE_APP_AUTH=true   # Produktion: Vollständige Authentifizierung erforderlich
   DEFAULT_APP_USER=testuser  # Benutzername für automatischen Login in Entwicklung
   ```

3. **Authentifizierungs-Dependencies** (`app/auth.py`):
   - `get_current_app_user()`: Intelligente Dependency für beide Modi
   - `require_app_read_permission()`: Gatekeeping für Lesezugriff
   - `require_app_write_permission()`: Gatekeeping für Schreibzugriff
   - `get_or_create_default_app_user()`: Automatische Erstellung des Standard-Benutzers in Entwicklung

4. **Endpoint-Schutz**:
   - GET-Operationen: `@Depends(require_app_read_permission)`
   - POST/PUT/DELETE: `@Depends(require_app_write_permission)`
   - Admin (ROOT) umgeht alle Berechtigungsprüfungen

### Frontend-Architektur

1. **Auth-Context** (`src/context/AuthContext.tsx`):
   - Verwaltet Benutzerinfo und Token
   - Stellt `canRead`/`canWrite`-Flags bereit
   - Lädt Benutzer auf App-Startup

2. **Routen-Schutz**:
   - Neue `AppLoginGuard` für App-Routen
   - Fallback zu `/app/login` wenn kein Token vorhanden

3. **Permission-basierte UI-Gates**:
   - Lesevorgänge: Immer aktiviert
   - Schreibzugriff: Buttons/Formulare deaktivieren wenn `!canWrite`
   - Visuelles Feedback: Read-Only-Indikator

4. **Benutzermenü** (Option 1):
   - Top-Right-Ecke mit Benutzerinformationen
   - Link zum Admin-Dashboard (if ROOT)
   - Logout-Button

### Bootstrap-Verfahren

**Entwicklung** (`ENABLE_APP_AUTH=false`):
- Bei `make dev` wird automatisch ein `testuser` mit Passwort `dev-password` erstellt
- Volle Lese-/Schreibrechte
- Keine manuelle Login erforderlich

**Produktion** (`ENABLE_APP_AUTH=true`):
- Beim initialen Deployment: Kein Standard-Benutzer
- Admin erstellt erste App-Benutzer über das Admin-Panel
- User loggen sich dann über `/app/login` ein


## Referenzen

- [ADR-009: Testkonzept](ADR-009-testkonzept.md) - Auswirkungen auf Tests
- [ADR-014: Python FastAPI Backend](ADR-014-python-fastapi-backend.md) - Backend-Framework
- [ADR-002: React Router](ADR-002-react-router.md) - Frontend-Routing
- [09-user-management-admin-concept.adoc](../09-user-management-admin-concept.adoc) - Admin-Benutzer (verwandt)
