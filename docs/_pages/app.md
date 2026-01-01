---
permalink: /app/
title: "Aquarius Anwendung"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-app-header-1500x400.webp
  overlay_filter: "0.4"
  caption: "Planung und Durchführung von Wettkämpfen"
---

# Aquarius Anwendungen

Wählen Sie den gewünschten Anwendungsbereich.

<div class="req-tile-grid">
  <a href="http://localhost:5173" target="_blank" rel="noopener noreferrer" class="req-tile app-tile--violet-1">
    <i class="fas fa-laptop-code"></i>
    <h3>Planungs-App</h3>
  </a>

  <a href="/app/mobile/" class="req-tile app-tile--violet-2">
    <i class="fas fa-mobile-alt"></i>
    <h3>Mobile App</h3>
  </a>

  <a href="http://localhost:5173/admin" target="_blank" rel="noopener noreferrer" class="req-tile app-tile--red-1">
    <i class="fas fa-skull"></i>
    <h3>Admin UI</h3>
  </a>
</div>

---

## Entwicklungshinweise

Um die Anwendungen lokal zu starten, führen Sie bitte `make dev` im Root-Verzeichnis aus.
Dies startet:
* Backend API auf Port 8000
* Frontend Web-App auf Port 5173

Die Mobile App erfordert einen separaten Start via Expo (siehe Mobile-Seite).