---
layout: splash
permalink: /architecture/test-reporting/
title: "Test Report"
excerpt: "Übersicht über alle automatisierten Testfälle"
header:
  overlay_image: /assets/images/splash/aquarius-app-header-1500x400.webp
  overlay_filter: "0.4"
  caption: "Status der automatisierten Tests"
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

<style>
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
</style>

{% assign grouped_results = site.data.test_results | group_by: "entity" %}
<div class="test-report-container">
  <p>Diese Seite zeigt den aktuellen Status aller automatisierten Backend- und Frontend-Tests.</p>
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
  {% endfor %}
</div>
