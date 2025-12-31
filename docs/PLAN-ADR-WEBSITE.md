# Plan: ADRs on Jekyll Website (Revised)

## Goal
Display ADRs from `/documentation/adr/` on the Jekyll website under `/architecture/adrs/`, using Jekyll Collections for simplified handling.

## Current State
- 18 ADRs in `/documentation/adr/ADR-XXX-*.md`
- All currently have status "Accepted" or "Akzeptiert"
- Architecture section uses `protected` layout

## Revised Approach: Jekyll Collections

### 1. Jekyll Collection Configuration

Add to `docs/_config.yml`:
```yaml
collections:
  adrs:
    output: true
    permalink: /architecture/adrs/:name/

defaults:
  - scope:
      path: ""
      type: adrs
    values:
      layout: protected
```

### 2. ADR Status Convention

Standardize status in ADR source files (first few lines):
```markdown
# ADR-001: Title Here

**Status:** Accepted | Deprecated | Rejected | Proposed | Superseded
**Datum:** 2025-12-17
```

**Status Icon Mapping:**

| Status | Icon | Color | FA Class |
|--------|------|-------|----------|
| Accepted / Akzeptiert | ✓ | Green | `fa-check-circle` + `text-success` |
| Proposed / Vorgeschlagen | ? | Blue | `fa-question-circle` + `text-info` |
| Deprecated / Veraltet | ⚠ | Orange | `fa-exclamation-triangle` + `text-warning` |
| Superseded / Ersetzt | → | Gray | `fa-arrow-right` + `text-muted` |
| Rejected / Abgelehnt | ✗ | Red | `fa-times-circle` + `text-danger` |

### 3. Compile Script (`docs/scripts/compile-adrs.sh`)

Simplified script that:
1. Reads each ADR from `/documentation/adr/`
2. Extracts title and status from content
3. Generates YAML front matter
4. Copies to `docs/_adrs/` (collection folder)

**Input:** `/documentation/adr/ADR-001-vite-build-tool.md`
**Output:** `/docs/_adrs/ADR-001-vite-build-tool.md`

**Generated front matter:**
```yaml
---
title: "ADR-001: Vite als Build-Tool für Frontend"
adr_number: "001"
adr_status: "accepted"
adr_date: "2025-12-17"
permalink: /architecture/adrs/ADR-001/
---
```

### 4. Directory Structure

```
docs/
├── _adrs/                          # Jekyll collection (generated, gitignored)
│   ├── ADR-001-vite-build-tool.md
│   ├── ADR-002-react-router.md
│   └── ...
├── _pages/architecture/adrs/
│   └── index.md                    # Hand-crafted index with Liquid loop
└── scripts/
    └── compile-adrs.sh
```

### 5. Index Page (`docs/_pages/architecture/adrs/index.md`)

```markdown
---
permalink: /architecture/adrs/
title: "Architecture Decision Records"
layout: protected
---

# Architecture Decision Records (ADRs)

<table class="adr-list">
  <thead>
    <tr><th>Nr.</th><th>Status</th><th>Titel</th></tr>
  </thead>
  <tbody>
{% assign sorted_adrs = site.adrs | sort: "adr_number" %}
{% for adr in sorted_adrs %}
  <tr>
    <td>{{ adr.adr_number }}</td>
    <td>{% include adr-status-icon.html status=adr.adr_status %}</td>
    <td><a href="{{ adr.url }}">{{ adr.title }}</a></td>
  </tr>
{% endfor %}
  </tbody>
</table>
```

### 6. Status Icon Include (`docs/_includes/adr-status-icon.html`)

```liquid
{% case include.status %}
  {% when "accepted" or "akzeptiert" %}
    <i class="fas fa-check-circle text-success" title="Accepted"></i>
  {% when "proposed" or "vorgeschlagen" %}
    <i class="fas fa-question-circle text-info" title="Proposed"></i>
  {% when "deprecated" or "veraltet" %}
    <i class="fas fa-exclamation-triangle text-warning" title="Deprecated"></i>
  {% when "superseded" or "ersetzt" %}
    <i class="fas fa-arrow-right text-muted" title="Superseded"></i>
  {% when "rejected" or "abgelehnt" %}
    <i class="fas fa-times-circle text-danger" title="Rejected"></i>
  {% else %}
    <i class="fas fa-circle text-muted" title="{{ include.status }}"></i>
{% endcase %}
```

### 7. Integration

#### Docker Compose (`docs/docker-compose.yml`)
```yaml
compile-adrs:
  image: alpine:latest
  volumes:
    - ../documentation/adr:/source:ro
    - ./_adrs:/output
    - ./scripts:/scripts:ro
  command: sh /scripts/compile-adrs.sh
```

#### Makefile
```makefile
website-dev:
    @echo "📄 Compiling ADRs..."
    @cd docs && docker compose run --rm compile-adrs
    @echo "🔐 Obfuscating JS..."
    @cd docs && docker compose run --rm obfuscate
    @echo "🌐 Starting Jekyll..."
    @cd docs && docker compose up jekyll
```

#### GitHub Actions
```yaml
- name: Compile ADRs for Jekyll
  run: |
    mkdir -p docs/_adrs
    chmod +x docs/scripts/compile-adrs.sh
    ./docs/scripts/compile-adrs.sh
```

### 8. Files to .gitignore

```
docs/_adrs/
```

### 9. CSS Addition (`docs/assets/css/aquarius.css`)

```css
/* ADR Status Colors */
.text-success { color: #28a745 !important; }
.text-info { color: #17a2b8 !important; }
.text-warning { color: #ffc107 !important; }
.text-danger { color: #dc3545 !important; }
.text-muted { color: #6c757d !important; }

.adr-list { width: 100%; }
.adr-list td, .adr-list th { padding: 0.5rem; }
.adr-list i { font-size: 1.1rem; }
```

## Implementation Steps

1. Update `_config.yml` with collection
2. Create `docs/scripts/compile-adrs.sh`
3. Create `docs/_includes/adr-status-icon.html`
4. Update `docs/_pages/architecture/adrs/index.md`
5. Add CSS for status colors
6. Update `docker-compose.yml`
7. Update Makefile
8. Update GitHub Actions workflow
9. Update `.gitignore`
10. Test locally

## Benefits of Collections Approach

- Jekyll handles URL generation automatically
- Liquid templates for iteration
- Front matter enables sorting/filtering
- Less custom code needed
- Standard Jekyll pattern
