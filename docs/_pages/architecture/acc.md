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

<script>
  (function() {
    const svgUrl = '/assets/images/architecture/Aquarius-ACC.svg';
    const containerId = 'interactive-acc-container';
    const originalViewBox = "0 0 1181 779";
    const highlightColor = '#C8E6C9'; // Very light green for hover
    const originalColor = '#D2D2D2';

    document.addEventListener('DOMContentLoaded', function() {
      const container = document.getElementById(containerId);
      if (!container) return;

      fetch(svgUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error(`SVG not found at ${svgUrl}`);
          }
          return response.text();
        })
        .then(svgText => {
          container.innerHTML = svgText;
          const svg = container.querySelector('svg');
          if (svg) {
            initInteractiveSVG(svg);
          }
        })
        .catch(error => {
          console.error('Error loading interactive ACC:', error);
          container.innerHTML = `<p>Error loading interactive canvas. Please ensure the file exists at ${svgUrl}</p>`;
        });
    });

    function initInteractiveSVG(svg) {
      let activeZoom = null;
      
      const zones = svg.querySelectorAll('rect[fill="#D2D2D2"]');

      zones.forEach(zone => {
        zone.classList.add('interactive-zone');
        
        zone.addEventListener('mouseover', () => {
          if (zone.getAttribute('fill') === originalColor) {
            zone.style.fill = highlightColor;
          }
        });

        zone.addEventListener('mouseout', () => {
          if (zone.style.fill) {
            zone.style.fill = ''; // Revert to original CSS/attribute value
          }
        });
      });

      svg.addEventListener('click', function(e) {
        const target = e.target;

        if (target.classList.contains('interactive-zone')) {
          handleZoneClick(target);
        } else {
          resetZoom();
        }
      });
      
      function handleZoneClick(zone) {
        if (activeZoom === zone) {
          resetZoom();
          return;
        }

        const bbox = zone.getBBox();
        zoomTo(bbox);
        activeZoom = zone;
      }

      function resetZoom() {
        if (!activeZoom) return;
        animateViewBox(originalViewBox);
        activeZoom = null;
      }

      function zoomTo(bbox) {
        const padding = 20;
        const x = Math.max(0, bbox.x - padding);
        const y = Math.max(0, bbox.y - padding);
        const w = bbox.width + (padding * 2);
        const h = bbox.height + (padding * 2);
        
        const newViewBox = `${x} ${y} ${w} ${h}`;
        animateViewBox(newViewBox);
      }
      
      let currentAnimation = null;

      function animateViewBox(targetViewBoxStr) {
        if (!svg.getAttribute('viewBox')) {
            svg.setAttribute('viewBox', originalViewBox);
        }
        const targetNums = targetViewBoxStr.split(' ').map(Number);
        const currentNums = (svg.getAttribute('viewBox') || originalViewBox).split(' ').map(Number);
        
        const startTime = performance.now();
        const duration = 500; // ms

        if (currentAnimation) cancelAnimationFrame(currentAnimation);

        function step(now) {
          const progress = Math.min((now - startTime) / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3); // Ease out cubic
          
          const nextNums = currentNums.map((start, i) => {
            return start + (targetNums[i] - start) * ease;
          });
          
          svg.setAttribute('viewBox', nextNums.join(' '));

          if (progress < 1) {
            currentAnimation = requestAnimationFrame(step);
          } else {
            currentAnimation = null;
          }
        }
        
        currentAnimation = requestAnimationFrame(step);
      }
    }
  })();
</script>

[← Zurück zur Architektur-Übersicht](/architecture/)
