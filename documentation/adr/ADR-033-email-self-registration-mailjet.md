# ADR-033: Email-based Self-Registration and Mailjet Integration

**Status:** in preparation  
**Datum:** 2026-01-10  
**Entscheider:** Gernot Starke

## Kontext

Für die geplante Self-Service-Funktionalität (Kinder/Eltern und Offizielle) ist ein Registrierungsprozess erforderlich. 
Dieser soll E-Mail-Verifikation und Einladungsmechanismen unterstützen.

**Anforderungen:**
- Verifikation der E-Mail-Adresse bei Self-Signup.
- Versand von Einladungs-Links mit zeitlich begrenzten Tokens.
- Passwort-Reset-Funktionalität.
- Kosteneffiziente Lösung (Free Tier).
- Einfache Integration in die bestehende FastAPI-Infrastruktur.

## Entscheidung

Wir implementieren die E-Mail-Funktionalität unter Verwendung von **Mailjet**.

### Begründung für Mailjet
- **Kostenlose Nutzung**: Mailjet bietet ein großzügiges kostenloses Kontingent (bis zu 6.000 E-Mails/Monat, 200/Tag), was für die initialen Anforderungen von Aquarius ausreicht.
- **API & SMTP**: Unterstützung sowohl für SMTP (einfacher Start) als auch für eine moderne REST-API (bessere Telemetrie und Template-Management).
- **Sitz in der EU**: Erleichtert die Einhaltung der DSGVO-Anforderungen.

### Technische Umsetzung

1. **Provider-Integration**:
   - Nutzung der Mailjet REST API für transaktionale E-Mails.
   - Konfiguration über Umgebungsvariablen (Secrets in Fly.io):
     ```env
     MAILJET_API_KEY=your_api_key
     MAILJET_SECRET_KEY=your_secret_key
     EMAIL_FROM=noreply@aquarius-app.de
     ```

2. **Backend-Logik**:
   - Einführung eines `EmailService` im Backend.
   - Unterstützung für asynchronen Versand (Background Tasks in FastAPI), um die API-Response-Zeiten nicht zu beeinträchtigen.
   - Jinja2-Templates für HTML-E-Mails (Verifikation, Einladung, Passwort-Reset).

3. **Registrierungs-Workflow**:
   - **Self-Signup**: User registriert sich -> Account-Status `PENDING` -> E-Mail mit Verifikations-Link -> User klickt Link -> Status `ACTIVE` (ggf. nach Admin-Freigabe).
   - **Einladung**: Admin erstellt User-Entwurf -> E-Mail mit Onboarding-Link -> User setzt Passwort -> Status `ACTIVE`.

## Konsequenzen

### Positiv
- **Sicherer Onboarding-Prozess**: Verifizierte E-Mail-Adressen reduzieren Spam und Fehlregistrierungen.
- **Geringe Kosten**: Free Tier deckt den Bedarf kleinerer Vereine und Wettbewerbe ab.
- **Skalierbarkeit**: Einfacher Wechsel auf bezahlte Pläne bei steigendem Volumen möglich.

### Negativ 
- **Externe Abhängigkeit**: Das System ist für die Registrierung auf die Verfügbarkeit von Mailjet angewiesen.
- **Zustellbarkeit**: Erfordert korrekte SPF/DKIM-Konfiguration oder Domain-Authentication für die sendende Domain.

### Offene Frage
- Dürfen wir mit dem kostenfreien Kontingent von MailJet überhaupt von der subdomain aquarius.arc42.org versenden?

## Referenzen

- [ADR-032: App User Authentication & Authorization](ADR-032-app-user-authentication.md) - Basis für die Benutzerverwaltung
