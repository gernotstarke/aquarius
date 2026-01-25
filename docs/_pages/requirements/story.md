---
permalink: /requirements/story/
title: "Aquarius"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-requirements-header-1500.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
  caption: "Schwimmliga: Die Story"
  actions:
    - label: "Startseite"
      url: "/"
    - label: "Anforderungen"
      url: "/requirements/"
    - label: "Architektur"
      url: "/architecture/"
    - label: "Anwendungen"
      url: "/app/"  
---

**Aquarius unterstützt Planung und Durchführungen von Wettkämpfen im Kinder-Figurenschwimmen.**

Verschiedene Teams treffen sich zu Wettkämpfen, bei denen Kinder in zwei Disziplinen konkurrieren, Figuren- und Synchronschwimmen. 
   
In einem Figurendurchgang tritt jeweils ein Kind an und zeigt eine bestimmte Wasserballettfigur, zum Beispiel Rückenschwimmen mit hoch gestrecktem Bein. 

An der Synchrondisziplin nimmt ein ganzes Team teil. 
Gewertet wird sowohl im Figuren- als auch im Synchronschwimmen; 

>Aquarius berücksichtigt aktuell **nur das Figurenschwimmen**.


Die Kinder müssen bei der **Anmeldung** zum Wettkampf ihren Namen, ihr Alter, ihre Adresse und den Namen des Teams angeben. 

>Für die Wettkämpfe besteht für alle teilnehmenden Kinder unbedingte **Versicherungspflicht**:
>Die muss zwingend über einen der folgenden Wege erfolgen:
>
>1. über die Mitgliedschaft in einem der beteilgten Vereine (denn die versichern alle ihre Mitglieder:innen), 
>2. über die Eltern oder sogar eigene Sporthaftpflichtversicherung oder
>3. über einen Sportverband (etwa einen der Landesverbände): Manche Kinder werden über einen Verband in so genannte _Kader_ berufen, und erhalten damit dann die notwendige Versicherung.

Um die Bewertung zu erleichtern, erhält jeder Teilnehmer eine Startnummer.

Bei einem **Wettkampf** werden mehrere **Durchgänge** für unterschiedliche Figuren an mehreren **Stationen** durchgeführt. 

Die Stationen werden um ein Schwimmbecken herum eingerichtet, meistens eine an jeder Ecke. 

![Stationen am Schwimmbecken](/assets/images/requirements/becken-schematisch.webp)

Es gibt freiwillige Kampf- und Punkterichter (_Offizielle_). 
Punkterichter ermüden schnell und müssen deshalb oft ausgewechselt werden. 
Bei einem Wettkampf werden an jeder Station mehrere Kampf- und Punkterichter eingesetzt. 
Im Laufe einer Saison kann jeder Kampfrichter und jeder Punkterichter an verschiedenen Stationen eingesetzt werden. 

Aus Gerechtigkeitsgründen findet jeder Durchgang an genau einer Station mit den gleichen Kampfrichtern statt. 
An einer Station können im Verlauf eines Wettkampfs mehrere Durchgänge stattfinden. 
Die Wettkampfteilnehmer werden in Gruppen aufgeteilt. Jede Gruppe beginnt an einer anderen Station. 
Wenn ein Kind an einer Station fertig ist, macht es an einer anderen Station mit einem anderen Durchgang weiter.

![so funktionieren Start und Bewertung](/assets/images/requirements/so-funktioniert-start+wertung-300.webp){: .align-left}

Wenn an einer Station jedes Kind einen bestimmten Durchgang absolviert hat, wird an dieser Station mit dem nächsten für die Station vorgesehenen Durchgang begonnen.
  
Jedes teilnehmende Kind hat bei jedem Durchgang einen Versuch, d. h. einen **Start**. 
Vor einem Start wird die Nummer des Kindes aufgerufen. 
Manchmal passt ein Kind nicht auf oder die Punktrichter kommen durcheinander, so dass an der betreffenden Station eine Pause eintritt, bis die Ordnung wiederhergestellt ist. 


Jeder **Kampfrichter** zeigt die vorläufige Punktezahl für jeden beobachteten Start an, indem er Zahlenkarten hochhält. 
Die vorläufigen Punktezahlen werden von den Punktrichtern vorgelesen, die sie erfassen und die Endpunkte für den Start berechnen. 
Die höchste und die niedrigste Punktezahl werden gestrichen und der Durchschnitt der verbleibenden Punkte wird mit einem Schwierigkeitsfaktor für die Figur multipliziert. 
Am Ende eines Wettkampfs werden auf der Basis der individuellen und der Teampunktezahl Einzel- und Teampreise vergeben. 
Es gibt verschiedene Altersgruppen und eigene Preise für jede Altersgruppe. 
Einzelpreise werden nur auf der Basis des Figurenschwimmens vergeben. 
Für Teampreise zählen sowohl das Figuren- als auch das Synchronschwimmen.


### Die Aquarius-User

Das Aquarius-System soll dazu dienen, alle Informationen zur Saisonplanung, Wettkämpfen, Kindern, Anmeldungen, Bewertung usw. digital zu verwalten. 

Dafür haben wir drei verschiedene Kategorien von _Usern_: 

* Unser _Backoffice_, im wesentlichen unseren Präsidenten Fritz Flosse. Deren Aufgabe ist die gesamte Planung, Verwaltung aller Grunddaten (Kinder, Vereine, Schwimmbäder u.s.w.). Während der Wettkämpfe können sie noch _last minute_ Aktualisierungen vornehmen, und Ranglisten und Urkunden drucken. Backoffice arbeitet meist im Büro, teilweise auch bei Wettkämpfen lokal vor-Ort.
* Die _Offiziellen_, also Kampf- und Punktrichter. Sie sorgen für geregelten Ablauf an Stationen und bewerten die Starts der Kinder mit Noten.
* Schließlich möchten wir den Kindern und ihren Eltern ermöglichen, Anmeldungen selbst vorzunehmen, und Rang-/Siegerlisten zeitnah (_in Echtzeit_) schon während der Wettkämpfe einzusehen (und natürlich auch danach noch).
