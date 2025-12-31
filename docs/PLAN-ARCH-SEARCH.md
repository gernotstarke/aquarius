# Plan: Simple Search for Architecture Documents

## Goal
Add client-side search functionality for the protected Architecture section, allowing users to quickly find ADRs and other architecture documentation.

## Approach: Lunr.js (Client-Side Search)

**Why Lunr.js?**
- No external services or accounts needed
- Works entirely in the browser
- Search index generated at Jekyll build time
- Lightweight (~8KB minified)
- Well-established for Jekyll sites

## How It Works

```
Build Time:                          Runtime:
┌─────────────┐                     ┌─────────────┐
│ Jekyll      │──generates──────────│ search.json │
│ builds site │                     │ (index)     │
└─────────────┘                     └──────┬──────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │ Lunr.js     │
                                    │ searches    │
                                    │ client-side │
                                    └─────────────┘
```

## Implementation

### 1. Search Index (`docs/search.json`)

Jekyll generates JSON index at build time:
```json
[
  {
    "title": "ADR-001: Vite als Build-Tool",
    "url": "/architecture/adrs/ADR-001/",
    "content": "Full text content...",
    "category": "adr",
    "status": "accepted"
  }
]
```

### 2. Search UI

Add search box to Architecture index page (`/architecture/`):
```html
<div class="arch-search">
  <input type="text" id="arch-search-input"
         placeholder="ADRs durchsuchen...">
  <div id="arch-search-results"></div>
</div>
```

### 3. Search Script (`docs/assets/js/arch-search.js`)

- Load search.json
- Initialize Lunr.js index
- Handle search input
- Display results with highlighting

### 4. Scope

Search covers **Architecture section only**:
- ADRs (from `_adrs` collection)
- Future: arc42, ACC, Tech-Stack Canvas

## Files to Create/Modify

| File | Action |
|------|--------|
| `docs/search.json` | Create - Liquid template for index |
| `docs/assets/js/arch-search.js` | Create - Search logic |
| `docs/_pages/architecture/index.md` | Modify - Add search box |
| `docs/assets/css/aquarius.css` | Modify - Search styling |
| `docs/_layouts/protected.html` | Modify - Include Lunr.js |

## Security Consideration

- Search index is **generated** and included in build
- Index is **only accessible after authentication** (on protected pages)
- No server-side component needed

## Questions

1. **Search scope**: Only ADRs, or all architecture pages?
2. **Placement**: Search box on main `/architecture/` page, or also on ADR index?
3. **Results display**: Inline dropdown, or separate results section?

## Alternative Considered

**Simple.Jekyll.Search**: Even lighter, but less powerful (no fuzzy matching, no relevance scoring). Lunr.js is still simple but more capable.
