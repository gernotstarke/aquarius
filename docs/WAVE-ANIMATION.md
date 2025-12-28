# Wave-Animated Header Documentation

## Overview

The Aquarius splash header features a sophisticated multi-layer water-flowing animation effect using SVG turbulence filters, CSS masks, and layered pseudo-elements.

## Technical Architecture

### Three-Layer System

```
┌─────────────────────────────────────────┐
│  Layer 1 (::before)  - Top 33%         │  Gentle turbulence
│  Mask: fade from 60% → 0%              │  12s animation
├─────────────────────────────────────────┤
│  Layer 2 (::after)   - Middle 33%      │  Medium turbulence
│  Mask: fade in/out at 35% and 65%     │  15s animation (-4s delay)
├─────────────────────────────────────────┤
│  Layer 3 (wrapper)   - Bottom 33%      │  Strong turbulence
│  Mask: fade from 0% → 60%              │  18s animation (-8s delay)
└─────────────────────────────────────────┘
```

### SVG Turbulence Filters

Three distinct filters create the flowing water effect:

#### 1. turbulence-gentle (Top Layer)
- **baseFrequency**: 0.008-0.016 (animated)
- **numOctaves**: 3
- **displacement**: 15-20px
- **Effect**: Subtle wave motion

#### 2. turbulence-medium (Middle Layer)
- **baseFrequency**: 0.01-0.02 (animated)
- **numOctaves**: 4
- **displacement**: 25-35px
- **Effect**: Moderate distortion + seed animation

#### 3. turbulence-strong (Bottom Layer)
- **baseFrequency**: 0.015-0.025 (animated)
- **numOctaves**: 5
- **displacement**: 35-50px
- **Effect**: Strong wave motion + color shift (blue tint)

### CSS Masks (Horizontal Zones)

Each layer is limited to a specific vertical zone using CSS linear gradients:

```css
/* Top third */
mask: linear-gradient(to bottom,
  rgba(0,0,0,0.6) 0%,     /* Start visible */
  rgba(0,0,0,0.4) 33%,    /* Fade middle */
  rgba(0,0,0,0) 35%       /* Invisible at bottom */
);

/* Middle third */
mask: linear-gradient(to bottom,
  rgba(0,0,0,0) 30%,      /* Invisible at top */
  rgba(0,0,0,0.5) 35%,    /* Fade in */
  rgba(0,0,0,0.5) 65%,    /* Stay visible */
  rgba(0,0,0,0) 70%       /* Fade out */
);

/* Bottom third */
mask: linear-gradient(to bottom,
  rgba(0,0,0,0) 65%,      /* Invisible at top */
  rgba(0,0,0,0.4) 70%,    /* Fade in */
  rgba(0,0,0,0.6) 100%    /* Fully visible */
);
```

## Animation Timings

Different animation speeds create organic, non-repetitive motion:

| Layer | Duration | Delay | Transform | Effect |
|---|---|---|---|
| Layer 1 | 12s | 0s | translateX(±20px), scale(1.05-1.08) | Gentle horizontal sway |
| Layer 2 | 15s | -4s | translateX(±15px), translateY(±10px), scale(1.06-1.08) | Diagonal wave |
| Layer 3 | 18s | -8s | translateX(±25px), scale(1.07-1.10) | Strong horizontal flow |

**LCM (Least Common Multiple)**: 180s = Full cycle before repeat

## Performance Optimizations

```css
/* GPU acceleration */
will-change: transform, filter;
backface-visibility: hidden;
perspective: 1000px;

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  animation: none;
  transform: none;
}
```

## File Structure

```
docs/
├── assets/css/
│   └── wave-animation.scss          # Main CSS (compiled by Jekyll)
├── _includes/
│   ├── wave-filters.html            # SVG filter definitions
│   ├── head/custom.html             # Inject CSS in <head>
│   └── footer/custom.html           # Inject SVG before </body>
└── index.md                         # Uses .page__hero--overlay
```

## How It Works

1. **Jekyll builds** `wave-animation.scss` → `wave-animation.css`
2. **Head include** loads the CSS stylesheet
3. **Footer include** injects SVG filters into DOM
4. **Pseudo-elements** (::before, ::after) duplicate background image
5. **SVG filters** distort each layer differently
6. **CSS masks** limit each layer to horizontal zone
7. **Animations** create flowing motion with different speeds

## Browser Support

- ✅ Chrome/Edge 88+
- ✅ Firefox 90+
- ✅ Safari 14.1+
- ⚠️ iOS Safari (some SVG filter performance issues on older devices)

**Fallback**: Without SVG filter support, layers still animate with transforms (graceful degradation)

## Customization

### Adjust Animation Speed
Edit animation durations in `wave-animation.scss`:
```scss
animation: wave-flow-1 12s ease-in-out infinite;  // Make slower: 20s
```

### Change Turbulence Intensity
Edit SVG filters in `wave-filters.html`:
```html
<feDisplacementMap in="SourceGraphic" scale="15">  <!-- Increase for more distortion -->
```

### Modify Layer Zones
Change mask gradients in `wave-animation.scss`:
```scss
mask: linear-gradient(to bottom,
  rgba(0,0,0,0.6) 0%,
  rgba(0,0,0,0.4) 50%,   /* Change split point */
  rgba(0,0,0,0) 55%
);
```

## Testing Locally

```bash
cd docs
docker compose up
# Visit http://localhost:4000
# Watch header for flowing water animation
```

## Known Issues

- **Mobile Safari**: SVG filter animations may stutter on iPhone 11 and older
- **Firefox**: Slight performance drop with all three layers on weak GPUs
- **Edge**: Occasional mask rendering glitch (refresh fixes it)

## Credits

Technique inspired by:
- SVG Turbulence: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTurbulence)
- CSS Masks: [CSS-Tricks](https://css-tricks.com/almanac/properties/m/mask/)
- Shader-like effects: WebGL distortion shaders adapted to SVG

---

*Created for Aquarius swimming competition documentation site*
