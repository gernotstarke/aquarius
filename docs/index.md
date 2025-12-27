---
layout: splash
title: "Aquarius"
excerpt: "Methodische Architektur in Aktion.<br>Von und mit [arc42](https://arc42.org)."
header:
  overlay_image: /assets/images/aquarius-splash-dark.png
  actions:
    - label: "Auf GitHub ansehen"
      url: "https://github.com/gernotstarke/aquarius"



aquarius_sections:
  - title: "Anforderungen"
    excerpt: "![requirements](/assets/images/aquarius-requirements-logo.jpeg)<br> 
    User Stories, Use Cases und funktionale Anforderungen für Aquarius, das Wettkampf-Management-System für Kunstschwimmen.
    Umfassende und req42-basierte Dokumentation der Stakeholder-Bedürfnisse."
    url: "/requirements/"
    btn_label: "Mehr lesen..."
    btn_class: "btn btn--blue"

  - title: "Architektur"
    excerpt: "![architecture](/assets/images/aquarius-architecture-logo.jpeg)<br>
    Technische Architektur, Designentscheidungen und Lösungsansatz nach dem arc42-Template.
    Bausteine, Laufzeitsichten und Deployment-Szenarien."
    url: "/architecture/"
    btn_label: "Mehr lesen..."
    btn_class: "btn btn--green"

  - title: "Anwendung"
    excerpt: "![application](/assets/images/aquarius-application-logo.jpeg)<br>Deployment-Guide, API-Dokumentation und Benutzerhandbücher für die Aquarius-Anwendung.
    Alles, was Sie für den Betrieb und die Nutzung des Systems benötigen."
    url: "/app/"
    btn_label: "Mehr lesen..."
    btn_class: "btn btn--violet"
---

# Fallstudie für methodische Softwarearchitektur


Aquarius, ein umfassendes Bewertungssystem für Kunstschwimmen, bietet trotz der überschaubaren Aufgabenstellung einige architektonische Herausforderungen.
Das System unterstützt 

* Desktop-/Web-Anwendungen für Organisation und Administration, 
* Echtzeit-Auswwertung (geplant) und 
* synchronisierte Datenverwaltung,
* mobile Apps für die Bewertung vor-Ort 

{% include feature_row id="aquarius_sections" %}

---

## Über diese Fallstudie

- **Die Herausforderung**: Wettkämpfe im Figurenschwimmen erfordern sofortige, präzise Bewertungen von mehreren Offiziellen gleichzeitig - doch ausgerechnet Schwimmbäder haben notorisch schlechtes WLAN. Gleichzeitig müssen Startnummern eindeutig vergeben, persönliche Daten der teilnehmenden Kinder geschützt und alle Bewertungen nachvollziehbar dokumentiert werden.

- **Die Lösung**: Aquarius kombiniert offline-fähige Mobile Apps für Kampfrichter mit einem cloud-synchronisierten Wettkampf-Management-System. Kampfrichter können auch ohne Netzverbindung bewerten, die Daten werden automatisch synchronisiert sobald Konnektivität besteht. Die Web-Anwendung ermöglicht Organisatoren die zentrale Verwaltung von Teilnehmern, Figuren-Katalogen und Ergebnissen.


- **Reale Komplexität**: Aquarius adressiert typische Herausforderungen verteilter und interaktiver Systeme: 
  - GDPR-Compliance für Kinder-Daten, 
  - atomare Startnummern-Vergabe unter Nebenläufigkeit, 
  - Historisierung trotz evolvierender Figuren-Kataloge, 
  - Split-Brain Problem bei Netzwerk-Partitionierung der Kampfrichter-Apps 
  - Benutzbarkeit auch für Laien, selbsterklärende Workflows, fehlertolerante Eingaben sind essentiell für den Einsatz in der Praxis.


- **Didaktischer Wert**: Aquarius dient als umfassende Fallstudie für Software-Architektur-Schulungen und demonstriert praxisnahe Herausforderungen moderner Systeme.
