---
title: "Test Report"
layout: splash
permalink: /architecture/test-reporting/
classes: no-wave
header:
  overlay_image: /assets/images/splash/test-results-header.webp
  caption: "Status der automatisierten Tests"
  actions:
    - label: "Anforderungen"
      url: "/requirements/"
    - label: "Architektur"
      url: "/architecture/"
    - label: "Anwendungen"
      url: "/app/"      
    - label: "Dashboard"
      url: "/app/dashboard/"  
---

<style>
  /* Improve contrast for header text on light background */
  .page__hero--overlay .page__title,
  .page__hero--overlay .page__lead,
  .page__hero--overlay .page__hero-caption {
    color: #1b5e20 !important;
    text-shadow: none !important;
  }

  .test-report-stats {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
    border: 1px solid #e9ecef;
  }

  .test-report-stats h3 {
    margin-top: 0;
    font-size: 1.2rem;
  }

  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    text-align: center;
  }

  .stat-item {
    padding: 0.5rem;
    background: white;
    border-radius: 0.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  .stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: bold;
    color: #2c3e50;
  }

  .stat-label {
    font-size: 0.85rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .test-report-toc {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }

  .test-report-toc h2 {
    margin-top: 0;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
  }

  .test-report-toc ul {
    columns: 2;
    -webkit-columns: 2;
    -moz-columns: 2;
    list-style-type: none;
    padding-left: 0;
    margin: 0;
  }

  .test-report-toc li {
    break-inside: avoid;
    margin-bottom: 0.5rem;
    padding-left: 1.2em;
    position: relative;
  }

  .test-report-toc li::before {
    content: "•";
    color: #0056b3;
    font-weight: bold;
    display: inline-block;
    width: 1em;
    margin-left: -1em;
  }

  .test-report-toc a {
    text-decoration: none;
    color: #0056b3;
  }

  .test-report-toc a:hover {
    text-decoration: underline;
  }

  .test-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    font-size: 0.9em;
  }
  .test-table th, .test-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  .test-table th {
    background-color: #f2f2f2;
  }
  .status-passed {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
    padding: .25em .4em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: .25rem;
  }
  .status-failed {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
    padding: .25em .4em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: .25rem;
  }
  .status-skipped {
    color: #856404;
    background-color: #fff3cd;
    border-color: #ffeeba;
    padding: .25em .4em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: .25rem;
  }
  .status-unknown {
    color: #004085;
    background-color: #cce5ff;
    border-color: #b8daff;
    padding: .25em .4em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: .25rem;
  }
  .top-link {
    text-align: right;
    font-size: 0.85em;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
  }
  .top-link a {
    color: #6c757d;
    text-decoration: none;
  }
  .top-link a:hover {
    color: #0056b3;
    text-decoration: underline;
  }
</style>

{% include test-stats.html %}

{% assign grouped_results = site.data.test_results | group_by: "entity" %}
<div class="test-report-container">
  <div class="test-report-stats">
    <h3>Zusammenfassung</h3>
    <div class="stat-grid">
      <div class="stat-item">
        <span class="stat-value" style="color: #2c3e50;">{{ test_stats_total }}</span>
        <span class="stat-label">Gesamt</span>
      </div>
      <div class="stat-item">
        <span class="stat-value" style="color: #28a745;">{{ test_stats_passed }}</span>
        <span class="stat-label">Bestanden</span>
      </div>
      <div class="stat-item">
        <span class="stat-value" style="color: #dc3545;">{{ test_stats_failed }}</span>
        <span class="stat-label">Fehlgeschlagen</span>
      </div>
      <div class="stat-item">
        <span class="stat-value" style="color: #ffc107;">{{ test_stats_skipped }}</span>
        <span class="stat-label">Übersprungen</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ test_stats_percentage }}%</span>
        <span class="stat-label">Erfolgsquote</span>
      </div>
    </div>
  </div>

  <div class="test-report-toc">
    <h2>Inhalt</h2>
    <ul>
      {% for group in grouped_results %}
        <li><a href="#{{ group.name | slugify }}">{{ group.name }}</a> ({{ group.items | size }})</li>
      {% endfor %}
    </ul>
  </div>

  {% for group in grouped_results %}
    <h2 id="{{ group.name | slugify }}">{{ group.name }}</h2>
    <table class="test-table">
      <thead>
        <tr>
          <th>Business-Erklärung (Slug)</th>
          <th>Technischer Name</th>
          <th>Ergebnis</th>
        </tr>
      </thead>
      <tbody>
        {% for test in group.items %}
          <tr>
            <td>
              <div class="business-explanation">{{ test.business_explanation }}</div>
              <div class="business-slug"><code>{{ test.business_slug }}</code></div>
            </td>
            <td><code>{{ test.technical_name }}</code></td>
            <td>
              {% assign status_class = "status-unknown" %}
              {% if test.result == "passed" %}
                {% assign status_class = "status-passed" %}
              {% elsif test.result == "failed" %}
                {% assign status_class = "status-failed" %}
              {% elsif test.result == "skipped" %}
                {% assign status_class = "status-skipped" %}
              {% endif %}
              <span class="{{ status_class }}">{{ test.result | capitalize }}</span>
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
    <p class="top-link"><a href="#">↑ Seitenanfang</a></p>
  {% endfor %}
</div>
