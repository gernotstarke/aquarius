---
permalink: /architecture/adrs/
title: "Architecture Decision Records"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
---


Hier dokumentieren wir mit [ADRs](https://adr.github.io/) wichtige Architekturentscheidungen mit ihrem Kontext, den betrachteten Alternativen und den Begründungen.
Gepflegt (_maintained_) werden diese Entscheidungen im Aquarius GitHub Repository unter /documentation/adrs, in Markdown Format.


<div class="arch-search-container" data-scope="adr">
  <div class="arch-search-box">
    <i class="fas fa-search arch-search-icon"></i>
    <input type="text" id="arch-search-input" placeholder="ADRs durchsuchen..." autocomplete="off">
  </div>
  <div id="arch-search-results" class="arch-search-results"></div>
  <small class="arch-search-hint"><i class="fas fa-info-circle"></i> Suche ist auf ADRs beschränkt</small>
</div>

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
