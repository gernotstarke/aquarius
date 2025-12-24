# Documentation - Aquarius Architecture & Requirements

arc42-basierte Architektur-Dokumentation und ADRs für alle Aquarius-Projekte.

## 📁 Structure

```
documentation/
├── adr/              # Architecture Decision Records (shared!)
├── architecture/     # arc42 AsciiDoc files
├── requirements/     # User Stories, Requirements
├── guides/           # How-To Guides
└── build/            # Generated HTML/PDF (gitignored)
```

## 🚀 Quick Start

```bash
# Generate HTML documentation
make docs

# Generate PDF
make pdf

# Serve locally
make serve
# → http://localhost:8000
```

## 📖 Architecture Decision Records (ADRs)

ADRs are **shared across all projects** (web, mobile).

### Naming Convention

- `ADR-001-web-*` - Web app specific
- `ADR-002-mobile-*` - Mobile app specific
- `ADR-003-shared-*` - Affects multiple projects

### Creating a new ADR

1. Copy `adr/template.md`
2. Name it: `ADR-XXX-[project]-title.md`
3. Fill in: Context, Decision, Consequences
4. Commit with descriptive message

## 🏗️ arc42 Architecture Documentation

Located in `architecture/`:

- `01-einfuehrung-ziele.adoc` - Introduction & Goals
- `02-randbedingungen.adoc` - Constraints
- `03-kontextabgrenzung.adoc` - Context & Scope
- `04-loesungsstrategie.adoc` - Solution Strategy
- `05-bausteinsicht.adoc` - Building Blocks
- `08-querschnittliche-konzepte.adoc` - Cross-cutting Concepts
- `08-4-cloud-deployment.adoc` - Cloud Deployment Architecture
- `09-architekturentscheidungen.adoc` - Architecture Decisions

## 🛠️ Tools

**Required:**
- asciidoctor (HTML generation)
- asciidoctor-pdf (PDF generation)

**Installation:**
```bash
# macOS
brew install asciidoctor

# Ruby gems
gem install asciidoctor asciidoctor-pdf
```

## 📋 Available Commands

```bash
make help       # Show all commands
make docs       # Generate all documentation
make html       # Generate HTML only
make pdf        # Generate PDF only
make serve      # Serve locally on port 8000
make clean      # Remove build artifacts
```
