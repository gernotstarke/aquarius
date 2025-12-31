# Plan: ADRs on Jekyll Website

## Goal
Display ADRs from `/documentation/adr/` on the Jekyll website under `/architecture/adrs/`, maintaining the source files as the "single source of truth".

## Current State
- 18 ADRs exist in `/documentation/adr/ADR-XXX-*.md`
- ADR format: Standard markdown with YAML-like header (Status, Datum, Entscheider)
- Architecture section uses `protected` layout (password protection)

## Proposed Solution

### 1. Compile Script (`docs/scripts/compile-adrs.sh`)

A shell script that:
- Reads all ADR files from `/documentation/adr/`
- Converts each to Jekyll format by adding YAML front matter
- Generates an index page listing all ADRs
- Outputs to `docs/_pages/architecture/adrs/`

**Conversion logic:**
```
Input:  /documentation/adr/ADR-001-vite-build-tool.md
Output: /docs/_pages/architecture/adrs/001-vite-build-tool.md
```

**Front matter to add:**
```yaml
---
permalink: /architecture/adrs/001/
title: "ADR-001: Vite als Build-Tool"
layout: protected
---
```

### 2. Generated Files Structure

```
docs/_pages/architecture/adrs/
├── index.md          (generated - list of all ADRs)
├── 001-vite-build-tool.md
├── 002-react-router.md
├── ...
└── 018-domain-driven-design.md
```

### 3. Index Page Format

```markdown
# Architecture Decision Records

| Nr. | Titel | Status | Datum |
|-----|-------|--------|-------|
| [ADR-001](/architecture/adrs/001/) | Vite als Build-Tool | Akzeptiert | 2025-12-17 |
| [ADR-002](/architecture/adrs/002/) | React Router | Akzeptiert | 2025-12-17 |
...
```

### 4. Integration Points

#### Development (`make website-dev`)
```makefile
website-dev:
    @cd docs && docker compose run --rm compile-adrs  # NEW
    @cd docs && docker compose run --rm obfuscate
    @cd docs && docker compose up jekyll
```

#### Production (GitHub Actions)
Add step before Jekyll build:
```yaml
- name: Compile ADRs for Jekyll
  run: |
    chmod +x docs/scripts/compile-adrs.sh
    ./docs/scripts/compile-adrs.sh
```

### 5. Docker Compose Addition

New service for ADR compilation:
```yaml
compile-adrs:
  image: alpine:latest
  volumes:
    - ../documentation/adr:/source:ro
    - ./_pages/architecture/adrs:/output
    - ./scripts:/scripts:ro
  command: sh /scripts/compile-adrs.sh
```

### 6. Security Consideration

- All generated ADR pages use `layout: protected`
- Index page (`adrs/index.md`) also uses `protected` layout
- No bypass possible via direct URL

### 7. .gitignore Update

Add generated ADR files to `.gitignore`:
```
docs/_pages/architecture/adrs/*.md
!docs/_pages/architecture/adrs/.gitkeep
```

This ensures:
- Generated files not committed
- Source remains in `/documentation/adr/`
- Fresh compilation on each build

## Alternative Considered

**Jekyll Collections**: Could use Jekyll's collection feature to auto-generate pages from markdown. Rejected because:
- Requires copying files anyway
- Less control over URL structure
- More complex configuration

## Implementation Steps

1. Create `docs/scripts/compile-adrs.sh`
2. Update `docs/docker-compose.yml` with compile-adrs service
3. Update Makefile targets
4. Update GitHub Actions workflow
5. Update `.gitignore`
6. Remove static `adrs.md` placeholder
7. Test locally and in CI

## Questions for Review

1. Should ADR URLs be `/architecture/adrs/001/` or `/architecture/adrs/ADR-001/`?
2. Should we include the full ADR content or just summaries on the index page?
3. Any preference for the table format vs. tile/card format for the index?
