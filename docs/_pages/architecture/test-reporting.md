---
permalink: /architecture/test-reporting/
title: "Test Report"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
  caption: "Automatisierte Testberichte"
  actions:
    - label: "Architektur"
      url: "/architecture/"
    - label: "ADRs"
      url: "/architecture/adrs/"
---

Diese Seite zeigt die Ergebnisse der automatisierten Tests für Aquarius.

{% if site.data.test_stats %}
## Zusammenfassung

<div class="test-summary-cards">
  <div class="test-card test-card--passed">
    <span class="test-card-number">{{ site.data.test_stats.passed }}</span>
    <span class="test-card-label">Bestanden</span>
  </div>
  <div class="test-card test-card--failed">
    <span class="test-card-number">{{ site.data.test_stats.failed }}</span>
    <span class="test-card-label">Fehlgeschlagen</span>
  </div>
  <div class="test-card test-card--skipped">
    <span class="test-card-number">{{ site.data.test_stats.skipped }}</span>
    <span class="test-card-label">Übersprungen</span>
  </div>
  <div class="test-card test-card--total">
    <span class="test-card-number">{{ site.data.test_stats.percentage }}%</span>
    <span class="test-card-label">Erfolgsrate</span>
  </div>
</div>
{% else %}
<div class="notice--warning">
  <p><strong>Keine Testdaten verfügbar.</strong></p>
  <p>Führe <code>make test</code> aus, um Testberichte zu generieren.</p>
</div>
{% endif %}

## Testdetails

{% if site.data.test_results %}
<table class="test-results-table">
  <thead>
    <tr>
      <th>Status</th>
      <th>Test</th>
    </tr>
  </thead>
  <tbody>
    {% for test in site.data.test_results %}
    <tr class="test-row--{{ test.result }}">
      <td class="test-status">
        {% if test.result == 'passed' %}
          <span class="test-icon test-icon--passed">✓</span>
        {% elsif test.result == 'failed' %}
          <span class="test-icon test-icon--failed">✗</span>
        {% else %}
          <span class="test-icon test-icon--skipped">⊘</span>
        {% endif %}
      </td>
      <td>
        <span class="test-description">{{ test.description }}</span>
        <br><code class="test-technical-name">{{ test.technical_name }}</code>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
<p><em>Keine detaillierten Testergebnisse verfügbar.</em></p>
{% endif %}

<style>
.test-summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.test-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem 1rem;
  border-radius: 8px;
  text-align: center;
}

.test-card-number {
  font-size: 2.5rem;
  font-weight: bold;
  line-height: 1;
}

.test-card-label {
  font-size: 0.85rem;
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.test-card--passed {
  background-color: #d4edda;
  border: 1px solid #28a745;
  color: #155724;
}

.test-card--failed {
  background-color: #f8d7da;
  border: 1px solid #dc3545;
  color: #721c24;
}

.test-card--skipped {
  background-color: #e2e3e5;
  border: 1px solid #6c757d;
  color: #383d41;
}

.test-card--total {
  background-color: #cce5ff;
  border: 1px solid #007bff;
  color: #004085;
}

.test-results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}

.test-results-table th,
.test-results-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.test-results-table th {
  background-color: #f8f9fa;
}

.test-status {
  width: 50px;
  text-align: center;
}

.test-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.test-icon--passed { color: #28a745; }
.test-icon--failed { color: #dc3545; }
.test-icon--skipped { color: #6c757d; }

.test-description {
  font-weight: 500;
}

.test-technical-name {
  font-size: 0.75rem;
  color: #6c757d;
}

.test-row--failed {
  background-color: #fff5f5;
}

.test-row--skipped {
  background-color: #fafafa;
}
</style>
