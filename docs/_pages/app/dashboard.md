---
permalink: /app/dashboard/
title: "Aquarius Dashboard"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-app-header-1500x400.webp
  overlay_filter: "0.4"
  caption: "System-Status und Statistiken"
  actions:
    - label: "Anwendungen"
      url: "/app/"
      btn_class: "btn btn--violet"
    - label: "Architektur"
      url: "/architecture/"
      btn_class: "btn btn--green"
---

<div class="dashboard-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">

  <div class="dashboard-card" style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #6f42c1;"><i class="fas fa-server"></i> App-Status</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li><strong>Umgebung:</strong> <span id="dash-environment">-</span></li>
      <li><strong>Region:</strong> <span id="dash-region">-</span></li>
      <li><strong>Backend-Version:</strong> <span id="dash-version">-</span></li>
      <li><strong>Health:</strong> <span id="dash-health" style="color: #999;">prüfe...</span></li>
    </ul>
  </div>

  <div class="dashboard-card" style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #007bff;"><i class="fas fa-database"></i> Datenbank</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li><strong>Typ:</strong> <span id="dash-db-type">-</span></li>
      <li><strong>Tabellen:</strong> <span id="dash-table-count">-</span></li>
    </ul>
  </div>

  <div class="dashboard-card" style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #28a745;"><i class="fas fa-chart-bar"></i> Statistiken</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li><strong>Kinder:</strong> <span id="dash-kind-count">-</span></li>
      <li><strong>Anmeldungen:</strong> <span id="dash-anmeldung-count">-</span></li>
      <li><strong>Wettkämpfe:</strong> <span id="dash-wettkampf-count">-</span></li>
    </ul>
  </div>

</div>

<p id="dash-error" style="color: #dc3545; display: none;"></p>
<p style="font-size: 0.85rem; color: #666; margin-top: 2rem;">
  <i class="fas fa-sync-alt"></i> Daten werden alle 30 Sekunden aktualisiert.
  Letzte Aktualisierung: <span id="dash-last-update">-</span>
</p>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const localAppUrl = "http://localhost:5173";
  const prodAppUrl = "https://aquarius.fly.dev";
  const isLocalDocs = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
  const targetUrl = isLocalDocs ? localAppUrl : prodAppUrl;

  function updateText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function formatTime(date) {
    return date.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  function fetchDashboardData() {
    // Health check
    fetch(targetUrl + "/api/health", { method: 'GET', mode: 'cors', cache: 'no-cache' })
      .then(response => {
        const healthEl = document.getElementById("dash-health");
        if (healthEl) {
          if (response.ok) {
            healthEl.textContent = "Online";
            healthEl.style.color = "#28a745";
          } else {
            healthEl.textContent = "Fehler";
            healthEl.style.color = "#dc3545";
          }
        }
      })
      .catch(() => {
        const healthEl = document.getElementById("dash-health");
        if (healthEl) {
          healthEl.textContent = "Offline";
          healthEl.style.color = "#dc3545";
        }
      });

    // Status data
    fetch(targetUrl + "/api/status", { method: 'GET', mode: 'cors', cache: 'no-cache' })
      .then(response => {
        if (!response.ok) throw new Error('Status error');
        return response.json();
      })
      .then(data => {
        document.getElementById("dash-error").style.display = "none";

        const env = data?.app?.environment || "unbekannt";
        updateText("dash-environment", env === "fly" ? "fly.io" : "lokal");
        updateText("dash-region", data?.app?.region || "-");
        updateText("dash-version", data?.version || "-");
        updateText("dash-db-type", data?.database?.type || "-");
        updateText("dash-table-count", String(data?.database?.table_count ?? "-"));
        updateText("dash-kind-count", String(data?.counts?.kind ?? "-"));
        updateText("dash-anmeldung-count", String(data?.counts?.anmeldung ?? "-"));
        updateText("dash-wettkampf-count", String(data?.counts?.wettkampf ?? "-"));
        updateText("dash-last-update", formatTime(new Date()));
      })
      .catch(err => {
        const errorEl = document.getElementById("dash-error");
        if (errorEl) {
          errorEl.textContent = "Status-Daten nicht verfügbar. Backend erreichbar?";
          errorEl.style.display = "block";
        }
        updateText("dash-last-update", formatTime(new Date()) + " (Fehler)");
      });
  }

  // Initial fetch
  fetchDashboardData();

  // Refresh every 30 seconds
  setInterval(fetchDashboardData, 30000);
});
</script>
