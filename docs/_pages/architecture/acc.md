---
permalink: /architecture/acc/
title: "Architecture Communication Canvas"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
---


<div id="interactive-acc-container"></div>

<style>
  #interactive-acc-container {
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    border: 1px solid #eee;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-radius: 8px;
    overflow: hidden;
  }
  
  #interactive-acc-container svg {
    width: 100%;
    height: auto;
    display: block;
    cursor: default; /* Default cursor elsewhere */
  }

  /* Style for interactive zones */
  #interactive-acc-container svg .interactive-zone {
    cursor: pointer;
    transition: fill 0.3s ease;
  }
</style>

<script src="/assets/js/interactive-canvas.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    if (window.initInteractiveCanvas) {
      window.initInteractiveCanvas({
        containerId: 'interactive-acc-container',
        svgUrl: '/assets/images/architecture/Aquarius-ACC.svg',
        originalViewBox: "0 0 1181 779",
        highlightColor: '#C8E6C9', // Very light green for hover
        originalColor: '#D2D2D2'
      });
    }
  });
</script>

[← Zurück zur Architektur-Übersicht](/architecture/)
