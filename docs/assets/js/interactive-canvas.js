/**
 * Interactive Canvas Logic
 * Handles SVG fetching, interactive zones (hover), and zoom-to-zone functionality.
 */

window.initInteractiveCanvas = function(config) {
  const {
    containerId,
    svgUrl,
    originalViewBox = "0 0 1181 779",
    highlightColor = '#C8E6C9', // Default highlight
    originalColor = '#D2D2D2',  // Color to look for
    zoneSelector = 'rect[fill="#D2D2D2"]' // Selector for interactive elements
  } = config;

  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Container with ID ${containerId} not found.`);
    return;
  }

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
        setupSVGInteraction(svg);
      }
    })
    .catch(error => {
      console.error('Error loading interactive canvas:', error);
      container.innerHTML = `<p>Error loading interactive canvas. Please ensure the file exists at ${svgUrl}</p>`;
    });

  function setupSVGInteraction(svg) {
    // Ensure viewBox is set
    if (!svg.getAttribute('viewBox')) {
      svg.setAttribute('viewBox', originalViewBox);
    }

    let activeZoom = null;
    let currentAnimation = null;

    // 1. Identify Zones
    // If a custom selector wasn't strictly provided, we use the default or the one passed in
    const zones = svg.querySelectorAll(zoneSelector);

    zones.forEach(zone => {
      zone.classList.add('interactive-zone');
      // Store original fill if needed, though we rely on attributes/styles mostly
      
      // Hover Effects
      zone.addEventListener('mouseenter', () => {
        // Only highlight if it currently has the "original" color (ignoring if it was already changed by something else, though simpler is better)
        // We simply force the highlight color on hover
        zone.style.fill = highlightColor;
      });

      zone.addEventListener('mouseleave', () => {
        // Revert to inline style removal (falls back to attribute)
        zone.style.fill = ''; 
      });
    });

    // 2. Click Handling (Delegation)
    svg.addEventListener('click', function(e) {
      const target = e.target;
      // Check if target or parent is a zone (in case of grouped elements, though rects are usually leaves)
      if (target.classList.contains('interactive-zone')) {
        handleZoneClick(target);
      } else {
        // Clicked outside a zone -> Reset
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

    function animateViewBox(targetViewBoxStr) {
      const targetNums = targetViewBoxStr.split(' ').map(Number);
      const currentAttr = svg.getAttribute('viewBox') || originalViewBox;
      const currentNums = currentAttr.split(' ').map(Number);
      
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
};
