---
title: "Aquarius Dashboard"
permalink: /app/dashboard/
layout: splash
classes: no-wave
header:
  overlay_image: /assets/images/splash/aquarius-dashboard-splash.webp
  caption: "System-Status und Statistiken"
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

<div class="dashboard-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">

  <div class="dashboard-card" style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #6f42c1;"><i class="fas fa-server"></i> App-Status</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li><strong>Umgebung:</strong> <span id="dash-environment">-</span></li>
      <li><strong>Region:</strong> <span id="dash-region">-</span></li>
      <li><strong>Backend-Version:</strong> <span id="dash-version">-</span></li>
      <li><strong>Benutzer:</strong> <span id="dash-user-count">-</span></li>
      <li><strong>Health:</strong> <span id="dash-health" style="color: #999;">prüfe...</span></li>
    </ul>
  </div>

  <div class="dashboard-card" style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #007bff;"><i class="fas fa-database"></i> Datenbank</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      <li><strong>Typ:</strong> <span id="dash-db-type">-</span></li>
      <li><strong>Tabellen:</strong> <span id="dash-table-count">-</span></li>
      <li><strong>Größe:</strong> <span id="dash-db-size">-</span></li>
      <li><strong>Ping:</strong> <span id="dash-db-health-latency">-</span></li>
      <li><strong>Schreiben:</strong> <span id="dash-db-write-latency">-</span></li>
      <li><strong>Lesen:</strong> <span id="dash-db-read-latency">-</span></li>
      <li><strong>Perf-Tests:</strong> <span id="dash-db-perf-rows">-</span></li>
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

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) return "-";
    const units = ["B", "KB", "MB", "GB", "TB"];
    let size = bytes;
    let unitIndex = 0;
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex += 1;
    }
    return `${size.toFixed(1)} ${units[unitIndex]}`;
  }

  function formatMs(value) {
    if (!Number.isFinite(value) || value < 0) return "-";
    return `${value.toFixed(1)} ms`;
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
        updateText("dash-db-size", formatBytes(Number(data?.database?.size_bytes)));
        updateText("dash-db-health-latency", formatMs(Number(data?.database?.health_latency_ms)));
        updateText("dash-db-write-latency", formatMs(Number(data?.database?.write_latency_ms)));
        updateText("dash-db-read-latency", formatMs(Number(data?.database?.read_latency_ms)));
        updateText("dash-db-perf-rows", String(data?.database?.performance_rows ?? "-"));
        updateText("dash-user-count", String(data?.counts?.users ?? "-"));
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
