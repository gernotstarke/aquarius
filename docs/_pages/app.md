---
permalink: /app/
title: "Aquarius Anwendung"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-app-header-1500x400.webp
  overlay_filter: "0.4"
  caption: "Planung und Durchführung von Wettkämpfen"

app_actions:
  - title: "Planungs-App"
    excerpt: "![web-app](/assets/images/aquarius-application-logo.jpeg)<br>
    Startet die Web-Anwendung für Saisonplanung, Anmeldung und Verwaltung.<br>
    <small>(Entwicklungsserver muss laufen)</small>"
    url: "http://localhost:5173"
    btn_label: "App starten 🚀"
    btn_class: "btn btn--info"
    link_attributes:
      target: "_blank"
      rel: "noopener noreferrer"

  - title: "Mobile App"
    excerpt: "![mobile-app](/assets/images/aquarius-wave-logo-highres-freigestellt.webp)<br>
    Informationen zur mobilen App für Kampfrichter und Simulator-Start."
    url: "/app/mobile/"
    btn_label: "Simulator Info 📱"
    btn_class: "btn btn--success"

  - title: "Admin UI"
    excerpt: "![admin-ui](/assets/images/aquarius-architecture-logo.jpeg)<br>
    Verwaltung von Benutzern, Rechten und Systemkonfiguration.<br>
    <small>(Nur für Administratoren)</small>"
    url: "http://localhost:5173/admin"
    btn_label: "Admin Console ☠️"
    btn_class: "btn btn--danger"
    icon: "fas fa-skull"
    link_attributes:
      target: "_blank"
      rel: "noopener noreferrer"
---

# Aquarius Anwendungen

Wählen Sie den gewünschten Anwendungsbereich.

{% include feature_row id="app_actions" %}

---

## Entwicklungshinweise

Um die Anwendungen lokal zu starten, führen Sie bitte `make dev` im Root-Verzeichnis aus.
Dies startet:
* Backend API auf Port 8000
* Frontend Web-App auf Port 5173

Die Mobile App erfordert einen separaten Start via Expo (siehe Mobile-Seite).
