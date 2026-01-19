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
    - label: "Zur Architektur"
      url: "/architecture/"
      btn_class: "btn btn--green"
    - label: "Zu den Anforderungen"
      url: "/requirements/"
      btn_class: "btn btn--blue"
---



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
    <span id="admin-app-status" class="status-indicator" title="Checking status..."></span>
    <i class="fas fa-skull-crossbones"></i>
    <h3>Admin UI</h3>
  </a>
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

<div id="app-dashboard">
  <p id="dashboard-status">Lade System-Status...</p>
  <ul>
    <li><strong>App-Umgebung:</strong> <span id="dashboard-location">-</span></li>
    <li><strong>Datenbank:</strong> <span id="dashboard-db-type">-</span></li>
    <li><strong>Tabellen:</strong> <span id="dashboard-table-count">-</span></li>
    <li><strong>Kind-Einträge:</strong> <span id="dashboard-kind-count">-</span></li>
    <li><strong>Anmeldungen:</strong> <span id="dashboard-anmeldung-count">-</span></li>
    <li><strong>Wettkämpfe:</strong> <span id="dashboard-wettkampf-count">-</span></li>
    <li><strong>Backend-Version:</strong> <span id="dashboard-backend-version">-</span></li>
  </ul>
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
    const planungsTile = document.querySelector(".app-tile--violet-1");
    if (planungsTile && !isLocalDocs) {
        planungsTile.href = prodAppUrl;
    }
    const adminTile = document.querySelector(".app-tile--red-1");
    if (adminTile && !isLocalDocs) {
        adminTile.href = prodAppUrl + "/admin";
    }

    const indicatorPlanung = document.getElementById("planungs-app-status");
    const indicatorAdmin = document.getElementById("admin-app-status");

    // Check function using fetch to health endpoint
    function checkStatus() {
      fetch(targetUrl + "/api/health", {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache'
      })
      .then(response => {
        if (response.ok) {
          if (indicatorPlanung) {
            indicatorPlanung.className = "status-indicator status-online";
            indicatorPlanung.title = "App is running";
          }
          if (indicatorAdmin) {
            indicatorAdmin.className = "status-indicator status-online";
            indicatorAdmin.title = "App is running";
          }
        } else {
          throw new Error('App returned error');
        }
      })
      .catch(error => {
        if (indicatorPlanung) {
          indicatorPlanung.className = "status-indicator status-offline";
          indicatorPlanung.title = "App unreachable";
        }
        if (indicatorAdmin) {
          indicatorAdmin.className = "status-indicator status-offline";
          indicatorAdmin.title = "App unreachable";
        }
      });
    }

    // Initial check
    checkStatus();
    
    // Check every 10 seconds
    setInterval(checkStatus, 10000);

    const dashboardStatus = document.getElementById("dashboard-status");
    const dashboardLocation = document.getElementById("dashboard-location");
    const dashboardDbType = document.getElementById("dashboard-db-type");
    const dashboardTableCount = document.getElementById("dashboard-table-count");
    const dashboardKindCount = document.getElementById("dashboard-kind-count");
    const dashboardAnmeldungCount = document.getElementById("dashboard-anmeldung-count");
    const dashboardWettkampfCount = document.getElementById("dashboard-wettkampf-count");
    const dashboardBackendVersion = document.getElementById("dashboard-backend-version");

    function updateText(node, value) {
      if (node) {
        node.textContent = value;
      }
    }

    fetch(targetUrl + "/api/status", {
      method: 'GET',
      mode: 'cors',
      cache: 'no-cache'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Status endpoint returned error');
      }
      return response.json();
    })
    .then(data => {
      if (dashboardStatus) {
        dashboardStatus.textContent = "System-Status verfügbar";
      }
      const environment = data?.app?.environment || "unbekannt";
      const region = data?.app?.region || "";
      const locationLabel = environment === "fly" ? `fly.io (${region || "unbekannt"})` : "lokal";
      updateText(dashboardLocation, locationLabel);
      updateText(dashboardDbType, data?.database?.type || "unbekannt");
      updateText(dashboardTableCount, String(data?.database?.table_count ?? "-"));
      updateText(dashboardKindCount, String(data?.counts?.kind ?? "-"));
      updateText(dashboardAnmeldungCount, String(data?.counts?.anmeldung ?? "-"));
      updateText(dashboardWettkampfCount, String(data?.counts?.wettkampf ?? "-"));
      updateText(dashboardBackendVersion, data?.version || "-");
    })
    .catch(() => {
      if (dashboardStatus) {
        dashboardStatus.textContent = "System-Status nicht erreichbar";
      }
    });
  });
</script>
