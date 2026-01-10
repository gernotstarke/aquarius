# Self-Service-Konzept (Kinder/Eltern und Offizielle)

## Zielbild
Eine eingeschraenkte Web-Oberflaeche fuer Self-Service-Registrierung und
Stammdatenpflege. Zunaechst fuer Kinder/Eltern, spaeter fuer Offizielle
(Kampfrichter/Punktrichter).

## Rollen und Rechte
- **Kind/Elternteil**: Registrierung, eigene Stammdaten, Einsicht in eigene
  Meldungen und aktuelle Status (z. B. angemeldet, geloescht).
- **Offizielle**: Registrierung, eigene Stammdaten, ggf. Verfuegbarkeiten.
- **Admin/Planung**: Freigabe/Pruefung, Zuordnung zu Vereinen/Teams,
  Sperren/Entziehen von Accounts.

## Registrierung und Onboarding
1. **Einladung oder Self-Signup**
   - Variante A: Einladung per E-Mail (Token-Link, zeitlich begrenzt).
   - Variante B: Self-Signup mit E-Mail-Verifikation und nachtraeglicher
     Admin-Freigabe.
2. **E-Mail-Bestaetigung**
   - Einmaliger Link zur Verifikation der E-Mail-Adresse.
   - Optional: Zwei-Faktor-Setup spaeter.
3. **Profilanlage**
   - Minimaldaten erfassen (Name, Geburtsjahr, Verein/Team, Kontakt).
   - Freigabeprozess durch Admin, falls erforderlich.

## Datenmodell (grob)
- **User**: id, email, role, status, created_at, last_login
- **Person**: name, adresse, kontakt, bezug zu Verein/Team
- **Kind**: person_id, geburtsjahr, team_id
- **Offizieller**: person_id, lizenz/stufe, rolle
- **Registration**: kind_id, wettkampf_id, status

## Authentifizierung
- Session-basiert (Cookie) oder JWT.
- Passwort-Reset per E-Mail.
- Rate-Limit und Captcha bei Self-Signup.

## Self-Service-Oberflaeche (MVP)
- Login/Logout
- Profil bearbeiten (nur eigene Stammdaten)
- Eigene Anmeldungen anzeigen
- Admin-Hinweise (z. B. "wartet auf Freigabe")

## E-Mail-Versand von fly.io
### Optionen
1. **SMTP ueber externen Provider**
   - Provider: z. B. Postmark, Mailgun, SendGrid, Amazon SES.
   - Nutzung ueber SMTP-Credentials als Secrets in Fly.
   - Vorteil: robust, einfache Integration, Zustellberichte.
2. **HTTP-API eines Providers**
   - Provider-API per HTTPS ansprechen.
   - Vorteil: bessere Telemetrie, Templates, Webhooks.

### Umsetzungsempfehlung
- Start mit **SMTP** (einfach, schnell), spaeter ggf. API.
- Secrets in Fly.io setzen: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`,
  `SMTP_PASS`, `SMTP_FROM`.
- E-Mail-Template fuer:
  - Verifikation
  - Passwort-Reset
  - Einladung

## Sicherheit und Compliance
- E-Mail-Adresse als eindeutiger Login-Identifier.
- DSGVO-konforme Loeschung und Export der Personendaten.
- Audit-Log fuer Profilaenderungen (minimal).

## Rollout
1. Kinder/Eltern Self-Service (Invite oder Self-Signup + Freigabe).
2. Offizielle Self-Service (Invite, spaeter Self-Signup).
3. Erweiterung um Benachrichtigungen (Wettkampfzeiten, Ergebnisse).

## Offene Fragen
- Soll Self-Signup ohne Admin-Freigabe moeglich sein?
- Wie werden Vereine/Teams beim Self-Service zugeordnet?
- Welche Daten duerfen Eltern fuer Kinder aendern?
