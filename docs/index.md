---
layout: splash
title: "Arqua42"
excerpt: "Ein umfassendes Bewertungssystem für Kunstschwimmen, das Desktop-, Web- und mobile Anwendungen mit synchronisierter Datenverwaltung und Echtzeit-Bewertung verbindet."
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

<style>
/* Custom Button Styles - Injected directly into page */
.btn {
  display: inline-block !important;
  margin-top: 10px !important;
  padding: 10px 20px !important;
  border: 1px solid transparent !important;
  border-radius: 4px !important;
  text-decoration: none !important;
  cursor: pointer !important;
  font-weight: bold !important;
  text-align: center !important;
}

.btn--blue {
  background-color: #007bff !important;
  color: #fff !important;
  border-color: #007bff !important;
}
.btn--blue:hover { background-color: #0069d9 !important; text-decoration: none !important; }

.btn--green {
  background-color: #28a745 !important;
  color: #fff !important;
  border-color: #28a745 !important;
}
.btn--green:hover { background-color: #218838 !important; text-decoration: none !important; }

.btn--violet {
  background-color: #6f42c1 !important;
  color: #fff !important;
  border-color: #6f42c1 !important;
}
.btn--violet:hover { background-color: #5a32a3 !important; text-decoration: none !important; }

/* Footer Badges */
.footer-badges {
  display: inline-flex;
  gap: 10px;
  vertical-align: middle;
  margin-left: 10px;
}
.footer-badges img {
  height: 20px;
}
</style>

# Willkommen bei Arqua42

Arqua42 ist ein modernes Bewertungssystem für Kunstschwimm-Wettkämpfe (Synchron-Schwimmen).
Das System unterstützt Desktop-/Web-Anwendungen für Organisatoren und Administratoren sowie mobile Apps für Wertungsrichter
und bietet Echtzeit-Bewertung und synchronisierte Datenverwaltung.

{% include feature_row id="aquarius_sections" %}

---

## Über diese Dokumentation

Diese Dokumentation ist in drei Hauptbereiche unterteilt:

- **Anforderungen**: Verstehen, was das System tut und warum
- **Architektur**: Wie das System aufgebaut und strukturiert ist
- **Anwendung**: Wie man das System deployt, konfiguriert und nutzt

Navigieren Sie über die oben stehenden Bereiche oder nutzen Sie das Menü.