---
title: "Aquarius: Architektur"
layout: protected
permalink: /architecture/overview
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
  caption: "Überblick über die Lösung"
  actions:
    - label: "Zur Startseite"
      url: "/"
    - label: "Zu den Anforderungen"
      url: "/requirements/"
    - label: "Zur Anwendung"
      url: "/app/"
---

## Drei User-Gruppen, drei _Apps_

Wie in der [Aquarius-Story](/requirements/story) beschrieben, haben wir es bei Aquarius mit drei verschiedenen User-Gruppen zu tun:

* Backoffice, für gesamte Verwaltung von Grunddaten. Das lösen wir mit [Aquarius-Control](#aquacontrol), der zentralen App für alle Planungs- und Verwaltungsaufgaben.
* Offizielle, primär für die Bewertung von Starts während der Wettkämpfe. Sie bekommen mit [Aquarius-Score](#aquascore) eine mobile App für ihr eigenes Mobiltelefon oder Tablet.
* Kinder melden sich an und können zeitnah Ergebnisse (und ihre Urkunden) einsehen. Dafür gibt es mit [Aquarius-Splash](#aquasplash) eine modern gestaltete Mobil-App für alle Arten von Mobilgeräten.

![Drei Apps](/assets/images/requirements/aquarius-die-apps-nobg.webp)

## Aquarius Control
* Das zentrale Programm, für Saison- und Wettkampfplanung sowie alle Grunddaten (Kinder, Schwimmbäder, Vereine, Verbände etc)

## Aquarius Score
* Eine App für Mobilgeräte, zur Unterstützung der Punkt- und Kampfrichter

## Aquarius Splash

Die App für Kinder und Eltern, zur Anmeldung sowie zur Anzeige von Ranglisten und Ergebnissen der Wettkämpfe: 

> "Splash: Dein Wettkampf. Deine Platzierung."



Am Anfang einer **Saison** aktualisieren die Verantwortlichen (Präsident und Backoffice-Mitarbeitende) die Daten der Kinder und erstellen einen Saisonplan.
Aus dem geht hervor, welche Figuren bei welchem Wettkampf bewertet werden.

Vor einem Wettkampf wird das System zur Bearbeitung der Anmeldungen verwendet. 
Während des Wettkampfs erfasst es die Punkte und ermittelt die Ranglisten, druckt Urkunden.
