---
permalink: /requirements/business-model-canvas/
title: "Business Model Canvas"
layout: splash
header:
  overlay_image: /assets/images/splash/aquarius-requirements-header-1500.webp
  overlay_filter: linear-gradient(rgba(0, 60, 120, 0.6), rgba(0, 60, 120, 0.6))
  actions:
    - label: "Anforderungen"
      url: "/requirements/"
    - label: "Architektur"
      url: "/architecture/"
    - label: "Anwendung"
      url: "/app/"
---

<div id="interactive-bmc-container"></div>

<style>
  #interactive-bmc-container {
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    border: 1px solid #eee;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-radius: 8px;
    overflow: hidden;
  }
  
  #interactive-bmc-container svg {
    width: 100%;
    height: auto;
    display: block;
    cursor: default;
  }

  /* Style for interactive zones */
  #interactive-bmc-container svg .interactive-zone {
    cursor: pointer;
    transition: fill 0.3s ease;
  }
</style>

<script src="/assets/js/interactive-canvas.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    if (window.initInteractiveCanvas) {
      window.initInteractiveCanvas({
        containerId: 'interactive-bmc-container',
        svgUrl: '/assets/images/requirements/aquarius-bmc.svg',
        originalViewBox: "0 0 1181 779",
        highlightColor: '#BBDEFB', // Blueish highlight for requirements
        originalColor: '#D2D2D2'
      });
    }
  });
</script>

## Mehr Informationen zum _Business Model Canvas_


* [Kompakte Einführung mit kleinen Beispielen](https://www.thepowermba.com/en/blog/business-model-canvas)

* [Beschreibung vom "Erfinder" selbst](https://www.strategyzer.com/business-models-the-toolkit-to-design-a-disruptive-company)
* [kurze Video-Einführung, auch von den Erfindern des BMC](https://youtu.be/QoAOzMTLP5s?si=Jva1Xf9iD40OGg24)




[← Zurück zu Requirements](/requirements/)