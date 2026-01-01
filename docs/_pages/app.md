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
    <span id="planungs-app-status" class="status-indicator" title="Checking status..."></span>
    <img src="/assets/images/aquarius-wave-logo-highres-freigestellt.webp" alt="Aquarius Wave" style="height: 5rem; margin-bottom: 1rem;">
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

<script>
  document.addEventListener("DOMContentLoaded", function() {
    // Configuration
    const localAppUrl = "http://localhost:5173";
    const prodAppUrl = "https://aquarius.arc42.org";
    
    // Determine target URL based on where the docs are running
    const isLocalDocs = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
    const targetUrl = isLocalDocs ? localAppUrl : prodAppUrl;
    
    // Update link href if in production (optional, if we want the tile to link to prod automatically)
    // Currently the HTML has localhost hardcoded. Let's fix that too via JS for better UX.
    const planungsTile = document.querySelector(".app-tile--violet-1");
    if (planungsTile && !isLocalDocs) {
        planungsTile.href = prodAppUrl;
    }
    const adminTile = document.querySelector(".app-tile--red-1");
    if (adminTile && !isLocalDocs) {
        adminTile.href = prodAppUrl + "/admin";
    }

    const indicator = document.getElementById("planungs-app-status");
    if (!indicator) return;

    // Check function using Image load (favicon hack)
    function checkStatus() {
      const img = new Image();
      img.onload = function() {
        indicator.className = "status-indicator status-online";
        indicator.title = "App is running";
      };
      img.onerror = function() {
        indicator.className = "status-indicator status-offline";
        indicator.title = "App unreachable";
      };
      // Use logo with cache buster (favicon.ico might not exist in dev)
      img.src = targetUrl + "/aquarius-logo.png?t=" + new Date().getTime();
    }

    // Initial check
    checkStatus();
    
    // Check every 30 seconds
    setInterval(checkStatus, 30000);
  });
</script>
