---
permalink: /architecture/acc/
title: "Architecture Communication Canvas"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  overlay_color: "#000"
  overlay_filter: "0.3"
---

# Architecture Communication Canvas

<div id="acc-container">
  <!-- Reconstructed SVG based on description (original file missing) -->
  <svg version="1.1" id="acc-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
     viewBox="0 0 1181 779" xml:space="preserve">
    <rect x="0" y="0" fill="#FFFFFF" width="1181" height="779"/>
    
    <!-- Row 1 -->
    <g class="acc-zone">
      <rect x="50" y="50" width="320" height="200" fill="#D2D2D2" />
      <text x="210" y="150" text-anchor="middle" dominant-baseline="middle">Context</text>
    </g>
    
    <g class="acc-zone">
      <rect x="430" y="50" width="320" height="200" fill="#D2D2D2" />
      <text x="590" y="150" text-anchor="middle" dominant-baseline="middle">Functional Overview</text>
    </g>
    
    <g class="acc-zone">
      <rect x="810" y="50" width="320" height="200" fill="#D2D2D2" />
      <text x="970" y="150" text-anchor="middle" dominant-baseline="middle">Quality Goals</text>
    </g>

    <!-- Row 2 -->
    <g class="acc-zone">
      <rect x="50" y="290" width="320" height="200" fill="#D2D2D2" />
      <text x="210" y="390" text-anchor="middle" dominant-baseline="middle">Constraints</text>
    </g>
    
    <g class="acc-zone">
      <rect x="430" y="290" width="320" height="200" fill="#D2D2D2" />
      <text x="590" y="390" text-anchor="middle" dominant-baseline="middle">Solution Strategy</text>
    </g>
    
    <g class="acc-zone">
      <rect x="810" y="290" width="320" height="200" fill="#D2D2D2" />
      <text x="970" y="390" text-anchor="middle" dominant-baseline="middle">Key Decisions</text>
    </g>

    <!-- Row 3 -->
    <g class="acc-zone">
      <rect x="50" y="530" width="320" height="200" fill="#D2D2D2" />
      <text x="210" y="630" text-anchor="middle" dominant-baseline="middle">Risks</text>
    </g>
    
    <g class="acc-zone">
      <rect x="430" y="530" width="320" height="200" fill="#D2D2D2" />
      <text x="590" y="630" text-anchor="middle" dominant-baseline="middle">Glossary</text>
    </g>
    
    <g class="acc-zone">
      <rect x="810" y="530" width="320" height="200" fill="#D2D2D2" />
      <text x="970" y="630" text-anchor="middle" dominant-baseline="middle">Interfaces</text>
    </g>
  </svg>
</div>

<style>
  #acc-container {
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    border: 1px solid #eee;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-radius: 8px;
    overflow: hidden;
  }
  
  #acc-svg {
    width: 100%;
    height: auto;
    display: block;
    cursor: default; /* Default cursor elsewhere */
  }

  .acc-zone {
    cursor: pointer;
    transition: opacity 0.3s;
  }

  .acc-zone rect {
    transition: fill 0.3s ease;
  }

  .acc-zone:hover rect {
    fill: #B0B0B0; /* Darker grey on hover */
  }
  
  .acc-zone text {
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 24px;
    fill: #333;
    pointer-events: none; /* Let clicks pass to the rect/group */
  }
</style>

<script>
  (function() {
    // Wait for DOM
    document.addEventListener('DOMContentLoaded', initAcc);

    function initAcc() {
      const svg = document.getElementById('acc-svg');
      if (!svg) return;

      const originalViewBox = "0 0 1181 779";
      let activeZoom = null;

      // Add transition to SVG itself for smooth zooming
      svg.style.transition = 'transform 0.5s ease'; 
      // Note: SMIL animate or CSS transition on viewBox is not universally supported smoothly
      // but modifying the attribute often works reasonably well, or we use CSS transform.
      // However, viewBox is better for responsive SVG scaling.
      // Let's implement a manual animation frame loop for smooth viewBox transition if needed,
      // or just rely on the browser's handling of attribute updates if wrapped in CSS transition (Chrome/FF support).
      // Actually, standard CSS transition does NOT animate viewBox.
      // We will use a simple requestAnimationFrame interpolation for smooth zoom.

      svg.addEventListener('click', function(e) {
        // Find closest group with class 'acc-zone'
        const zone = e.target.closest('.acc-zone');

        if (zone) {
          handleZoneClick(zone);
          e.stopPropagation();
        } else {
          // Clicked whitespace
          resetZoom();
        }
      });
      
      // Also reset if clicking outside the zones but on the SVG background
      // (Handled by the else block above mostly, assuming rects cover the zones)

      function handleZoneClick(zone) {
        const rect = zone.querySelector('rect');
        if (!rect) return;
        
        // Identify if we are already zoomed in on THIS zone
        if (activeZoom === zone) {
          resetZoom();
          return;
        }

        const bbox = rect.getBBox();
        zoomTo(bbox);
        activeZoom = zone;
      }

      function resetZoom() {
        if (!activeZoom) return;
        animateViewBox(originalViewBox);
        activeZoom = null;
      }

      function zoomTo(bbox) {
        // Add padding
        const padding = 20;
        const x = Math.max(0, bbox.x - padding);
        const y = Math.max(0, bbox.y - padding);
        const w = bbox.width + (padding * 2);
        const h = bbox.height + (padding * 2);
        
        // Ensure we don't go out of bounds (simplified)
        const newViewBox = `${x} ${y} ${w} ${h}`;
        animateViewBox(newViewBox);
      }
      
      let currentAnimation = null;

      function animateViewBox(targetViewBoxStr) {
        const targetNums = targetViewBoxStr.split(' ').map(Number);
        const currentNums = (svg.getAttribute('viewBox') || originalViewBox).split(' ').map(Number);
        
        const startTime = performance.now();
        const duration = 500; // ms

        if (currentAnimation) cancelAnimationFrame(currentAnimation);

        function step(now) {
          const progress = Math.min((now - startTime) / duration, 1);
          // Ease out cubic
          const ease = 1 - Math.pow(1 - progress, 3);
          
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