---
title: "Aquarius: Die Lösung"
layout: protected
permalink: /architecture/overview/
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
  caption: "Überblick über Anwendungen"
  actions:
    - label: "Zur Startseite"
      url: "/"
    - label: "Anforderungen"
      url: "/requirements/"
    - label: "Anwendungen"
      url: "/app/"
---

## Drei User-Gruppen, drei _Apps_

Wie in der [Aquarius-Story](/requirements/story) beschrieben, haben wir es bei Aquarius mit drei verschiedenen User-Gruppen zu tun.
Zusätzlich muss es aus rein praktisch-pragmatischen Gründen noch eine Rolle "Admin" geben.
Weil der Ligapräsident Fritz Flosse in IT-Dingen wenig bewandert ist, sollten wir sie typischen Admin-Aufgaben einer anderen Person/Rolle geben.

* Backoffice, für gesamte Verwaltung von Grunddaten. Das lösen wir mit [Aquarius-Control](#aquacontrol), der zentralen App für alle Planungs- und Verwaltungsaufgaben.
* Offizielle, primär für die Bewertung von Starts während der Wettkämpfe. Sie bekommen mit [Aquarius-Score](#aquascore) eine mobile App für ihr eigenes Mobiltelefon oder Tablet.
* Kinder melden sich an und können zeitnah Ergebnisse (und ihre Urkunden) einsehen. Dafür gibt es mit [Aquarius-Splash](#aquasplash) eine modern gestaltete Mobil-App für alle Arten von Mobilgeräten.

![Drei Apps](/assets/images/architecture/aquarius-die-apps-nobg.webp)

>Für die praktisch notwendigen administrativen Aufgaben, etwa User- und Rechteverwaltung, Monitoring, DB-Pflege und Backup  gibt es noch eine weitere App namens [Aquarius Pulse](#aquapulse)

<a id="aquacontrol"></a>
## Aquarius Control

![](/assets/images/architecture/app-logos/aquarius-control-logo-nobg-200.webp){: .align-left}
Das zentrale Programm, für Saison- und Wettkampfplanung sowie alle Grunddaten (Kinder, Schwimmbäder, Vereine, Verbände etc).

Am Anfang einer **Saison** aktualisieren die Verantwortlichen (Präsident oder Backoffice-Mitarbeitende) die Daten der Kinder, Vereine und Schwimmbäder.
Dann planen sie mit Aquarius-Control die kommende Saison.
Sie legen die Daten und Orte der Wettkämpfe fest und bestimmen, welche Figuren bei welchem Wettkampf bewertet werden.

Vor einem Wettkampf wird das System zur Bearbeitung der Anmeldungen verwendet. 
Während des Wettkampfs kann es die vergebenen Punkte (Bewertungen) erfassen, ermittelt die Ranglisten, druckt Urkunden.


Wir entwickeln das als Web-Anwendung, mit Fokus auf einfachste Bedienung und hohe Zuverlässigkeit.

<a id="aquascore"></a>
## Aquarius Score

![](/assets/images/architecture/app-logos/aquarius-score-logo-nobg-200.webp){: .align-left}
Eine App für Mobilgeräte, zur Unterstützung der Punkt- und Kampfrichter.

Die Offiziellen melden sich mit genau einem Gerät an (damit sie nicht mehrfach abstimmen können).
Sie wählen den gewünschten Wettkampf aus, und können jetzt gemäß ihrer Rolle **Starts** bewerten.

Die Bewertung wird gespeichert, und kann ab diesem Moment nicht mehr nachträglich geändert werden.
Falls ihr Gerät zu diesem Zeitpunkt online ist (d.h. eine Verbindung zu Aquarius-Control herstellen kann), überträgt die App die aktuelle Bewertung. 
Ansonsten speichert es die Bewertung(en) lokal und synchronisiert mit Aquarius-Control, sobald wieder eine Verbindung besteht.

{: .notice--warning}
Hier gibt es eine besondere Herausforderung: Offizelle dürfen zu jedem Zeitpunkt auf höchstens EINEM Gerät angemeldet sein.
Das ist insofern schwierig, als das Aquarius-Score ja auch offline funktionieren muss, ein Offizieller aber auf einem zweiten Gerät online sein kann. 

Offizielle müssen einmalig im [Aquarius-Control](#aquacontrol) als User mit der Rolle "_offizielle_" eingerichtet werden.

>Aktuell ist in Diskussion, ob der Zugang zu Aquarius-Score über eine 2-Faktor-Authentisierung abgesichert werden soll, oder ob alternative Mechanismen (Passwort, Token) zum Einsatz kommen werden.

---

<a id="aquasplash"></a>
## Aquarius Splash

![](/assets/images/architecture/app-logos/aquarius-splash-logo-nobg-200.webp){: .align-left}
Die App für Kinder und Eltern, zur Anmeldung sowie zur Anzeige von Ranglisten und Ergebnissen der Wettkämpfe: 

> "Splash: Dein Wettkampf. Deine Platzierung."

Kinder und Eltern können auf dieser schicken Mobile-App Anmeldungen für Wettkämpfe vornehmen und wichtige Grunddaten ändern.
Dazu kommen Resultate und Ranglisten während der Wettkämpfe - zeitnah aktualisiert, stets am Puls des Geschehens.

Diese App läuft auf den relevanten Betriebssystemen Android und iOS, sowohl auf Mobiltelefonen wie auch Tablets.

Zur Nutzung ist einmalig die Registrierung im [Aquarius-Control](#aquacontrol) notwendig, um Mißbrauch durch unberechtigte Dritte zu verhindern.

---

<a id="aquapulse"></a>
## Aquarius Pulse


![](/assets/images/architecture/aquarius-admin-scenario-400.webp){: .align-right}
>User einrichten und Rechte vergeben gehört zu den kritischen und sensiblen Aufgaben beim Betrieb von IT-Systemen, insbesondere wenn diese schutz- und vertrauenswürdige Daten speichern - dafür gibt es die Rolle _Admin_.


![](/assets/images/architecture/app-logos/aquarius-pulse-logo-nobg-200.webp){: .align-left}
Im Umfeld Aquarius gehören dazu insbesondere die personenbezogenen Daten der Kinder.
Die müssen einerseits vor unberechtigtem Zugriff geschützt werden, andererseits 

Aufgaben wie Datensicherung, das einspielen neuer Figurenkataloge sowie die Diagnose und Behandlung möglicher Fehler zählt ebenfalls zu den administrativen Aufgaben von Aquarius-Pulse.

Deswegen kommt bei Aquarius-Pulse ein _security-bootstraping_ Verfahren zum Einsatz:

* Admins müssen sich zwangsweise mit 2-Faktor-Authentication am System anmelden, für Details siehe [ADR-27](/architecture/adrs/ADR-027/)
