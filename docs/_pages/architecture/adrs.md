---
permalink: /architecture/adrs/
title: "Architecture Decision Records"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
---

# Architecture Decision Records (ADRs)

ADRs dokumentieren wichtige Architekturentscheidungen mit ihrem Kontext, den betrachteten Alternativen und den Begründungen.

<table class="adr-list">
  <thead>
    <tr>
      <th>Nr.</th>
      <th>Status</th>
      <th>Titel</th>
    </tr>
  </thead>
  <tbody>
{% assign sorted_adrs = site.adrs | sort: "adr_number" %}
{% for adr in sorted_adrs %}
    <tr>
      <td><code>{{ adr.adr_number }}</code></td>
      <td>{% include adr-status-icon.html status=adr.adr_status %}</td>
      <td><a href="{{ adr.url }}">{{ adr.title }}</a></td>
    </tr>
{% endfor %}
  </tbody>
</table>

{% if site.adrs.size == 0 %}
<p><em>Keine ADRs gefunden. Bitte führen Sie <code>make website-dev</code> aus, um die ADRs zu kompilieren.</em></p>
{% endif %}

[← Zurück zur Architektur-Übersicht](/architecture/)
