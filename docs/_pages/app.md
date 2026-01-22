---
permalink: /app/
title: "Aquarius Anwendungen"
excerpt: "hier läuft's!"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-app-header-1500x400.webp
  overlay_filter: "0.4"
  caption: "Planung und Durchführung von Wettkämpfen"
  actions:
    - label: "Architektur"
      url: "/architecture/"
    - label: "Anforderungen"
      url: "/requirements/"
---



<div class="req-tile-grid">
  <a id="tile-control" href="http://localhost:5173" target="_blank" rel="noopener noreferrer" class="req-tile app-tile--violet-1">
    <span id="control-app-status" class="status-indicator" title="Checking status..."></span>
    <img src="/assets/images/applications/aquarius-control-logo-nobg-200.webp" alt="Aquarius Control" style="height: 5rem; margin-bottom: 1rem;">
    <h3>Aquarius Control</h3>
  </a>

  <a id="tile-splash" href="/app/mobile/" class="req-tile app-tile--violet-2">
    <img src="/assets/images/applications/aquarius-splash-logo-nobg-200.webp" alt="Aquarius Splash" style="height: 5rem; margin-bottom: 1rem;">
    <h3>Aquarius Splash</h3>
  </a>

  <a id="tile-score" href="http://localhost:5173/score" target="_blank" rel="noopener noreferrer" class="req-tile app-tile--violet-1">
    <span id="score-app-status" class="status-indicator" title="Checking status..."></span>
    <img src="/assets/images/applications/aquarius-score-logo-nobg-200.webp" alt="Aquarius Score" style="height: 5rem; margin-bottom: 1rem;">
    <h3>Aquarius Score</h3>
  </a>

  <a id="tile-pulse" href="http://localhost:5173/admin" target="_blank" rel="noopener noreferrer" class="req-tile app-tile--red-1">
    <span id="pulse-app-status" class="status-indicator" title="Checking status..."></span>
    <img src="/assets/images/applications/aquarius-pulse-logo-nobg-200.webp" alt="Aquarius Pulse" style="height: 5rem; margin-bottom: 1rem;">
    <h3>Aquarius Pulse</h3>
  </a>

  <a id="tile-dashboard" href="/app/dashboard/" class="req-tile app-tile--violet-2">
    <i class="fas fa-tachometer-alt" style="font-size: 4rem; margin-bottom: 1rem;"></i>
    <h3>Dashboard</h3>
  </a>
</div>

<p class="status-legend" style="margin-top: 1.5rem; font-size: 0.85rem; color: #666;">
  <strong>Status:</strong>
  <span style="display: inline-flex; align-items: center; margin-left: 1rem;">
    <span style="width: 10px; height: 10px; background: #28a745; border-radius: 50%; display: inline-block; margin-right: 0.3rem;"></span> Online
  </span>
  <span style="display: inline-flex; align-items: center; margin-left: 1rem;">
    <span style="width: 10px; height: 10px; background: #dc3545; border-radius: 50%; display: inline-block; margin-right: 0.3rem;"></span> Offline
  </span>
</p>

---

## Die Aquarius Apps

<div class="app-descriptions" style="margin: 2rem 0;">

<h3><img src="/assets/images/applications/aquarius-control-logo-nobg-200.webp" alt="" style="height: 2rem; vertical-align: middle; margin-right: 0.5rem;"> Aquarius Control</h3>
<p>Das zentrale Programm für Saison- und Wettkampfplanung sowie alle Grunddaten (Kinder, Schwimmbäder, Vereine, Verbände). Backoffice-Mitarbeitende planen hier die Saison, bearbeiten Anmeldungen und erfassen während des Wettkampfs die Bewertungen.</p>

<h3><img src="/assets/images/applications/aquarius-splash-logo-nobg-200.webp" alt="" style="height: 2rem; vertical-align: middle; margin-right: 0.5rem;"> Aquarius Splash</h3>
<p>Die App für Kinder und Eltern zur Anmeldung sowie zur Anzeige von Ranglisten und Ergebnissen. <em>"Splash: Dein Wettkampf. Deine Platzierung."</em> – Resultate zeitnah aktualisiert, stets am Puls des Geschehens.</p>

<h3><img src="/assets/images/applications/aquarius-score-logo-nobg-200.webp" alt="" style="height: 2rem; vertical-align: middle; margin-right: 0.5rem;"> Aquarius Score</h3>
<p>Eine App für Mobilgeräte zur Unterstützung der Punkt- und Kampfrichter. Offizielle bewerten hier Starts während der Wettkämpfe. Die Bewertung wird sofort übertragen oder bei fehlender Verbindung lokal gespeichert und später synchronisiert.</p>

<h3><img src="/assets/images/applications/aquarius-pulse-logo-nobg-200.webp" alt="" style="height: 2rem; vertical-align: middle; margin-right: 0.5rem;"> Aquarius Pulse</h3>
<p>Die Admin-App für User- und Rechteverwaltung, Monitoring, Datenbank-Pflege und Backup. Zugang nur mit 2-Faktor-Authentisierung für maximale Sicherheit der personenbezogenen Daten.</p>

</div>

---

## Hinweise

<div id="local-hinweise" hidden>
  <p>Um die Anwendungen lokal zu starten, führen Sie bitte <code>make dev</code> im Root-Verzeichnis aus.</p>
  <p>Dies startet:</p>
  <ul>
    <li>Backend API auf Port 8000</li>
    <li>Frontend Web-App auf Port 5173</li>
  </ul>
  <p>Die Mobile App erfordert einen separaten Start via Expo (siehe Mobile-Seite).</p>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function() {
    // Configuration
    const localAppUrl = "http://localhost:5173";
    const prodAppUrl = "https://aquarius.fly.dev";

    // Determine target URL based on where the docs are running
    const isLocalDocs = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
    const targetUrl = isLocalDocs ? localAppUrl : prodAppUrl;
    
    const localHinweise = document.getElementById("local-hinweise");
    if (localHinweise) {
      localHinweise.hidden = !isLocalDocs;
    }

    // Update link href if in production
    const controlTile = document.getElementById("tile-control");
    if (controlTile && !isLocalDocs) {
        controlTile.href = prodAppUrl;
    }
    const scoreTile = document.getElementById("tile-score");
    if (scoreTile && !isLocalDocs) {
        scoreTile.href = prodAppUrl + "/score";
    }
    const pulseTile = document.getElementById("tile-pulse");
    if (pulseTile && !isLocalDocs) {
        pulseTile.href = prodAppUrl + "/admin";
    }

    const indicatorControl = document.getElementById("control-app-status");
    const indicatorScore = document.getElementById("score-app-status");
    const indicatorPulse = document.getElementById("pulse-app-status");

    // Check function using fetch to health endpoint
    function checkStatus() {
      fetch(targetUrl + "/api/health", {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache'
      })
      .then(response => {
        if (response.ok) {
          [indicatorControl, indicatorScore, indicatorPulse].forEach(indicator => {
            if (indicator) {
              indicator.className = "status-indicator status-online";
              indicator.title = "App is running";
            }
          });
        } else {
          throw new Error('App returned error');
        }
      })
      .catch(error => {
        [indicatorControl, indicatorScore, indicatorPulse].forEach(indicator => {
          if (indicator) {
            indicator.className = "status-indicator status-offline";
            indicator.title = "App unreachable";
          }
        });
      });
    }

    // Initial check
    checkStatus();

    // Check every 10 seconds
    setInterval(checkStatus, 10000);
  });
</script>
