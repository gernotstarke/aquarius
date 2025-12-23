.PHONY: help docs docs-diagrams docs-adrs docs-html docs-pdf docs-watch docs-serve docs-build-image clean test dev dev-down db-reset db-seed db-import-figures

# Docker configuration
DOCKER_IMAGE := arqua42-docs:latest
DOCKER_RUN := docker run --rm -v $(CURDIR)/docs:/docs -w /docs $(DOCKER_IMAGE)

# Documentation paths
DOCS_SRC := docs/src
DOCS_BUILD := docs/build

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Docker Build

docs-build-image: ## Build the Docker image for documentation generation
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🐳 Building documentation Docker image..."
	@echo "   Image: $(DOCKER_IMAGE)"
	@echo "   Dockerfile: Dockerfile.docs"
	@docker build -f Dockerfile.docs -t $(DOCKER_IMAGE) .
	@echo "✓ Docker image built successfully: $(DOCKER_IMAGE)"

##@ Documentation

docs: docs-diagrams docs-adrs docs-html ## Generate all documentation (diagrams + HTML) - Docker-based
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✓ Documentation generated successfully"
	@echo "  📄 HTML: docs/build/arqua42-architecture.html"
  📋 ADRs: docs/build/adrs/
	@echo "  📊 Diagrams: docs/build/images/"
	@echo "  View with: make docs-serve"

docs-diagrams: ## Generate PNG diagrams from PlantUML sources (Docker-based)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Generating PlantUML diagrams..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD)/images; \
		echo "   Running: plantuml -tpng -o ../../../../build/images ..."; \
		$(DOCKER_RUN) plantuml -tpng -o ../../../../build/images src/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated in $(DOCS_BUILD)/images/ (via Docker)"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD)/images; \
		echo "   Running: plantuml -tpng -o ../../../../build/images ..."; \
		$(DOCKER_RUN) plantuml -tpng -o ../../../../build/images src/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated in $(DOCS_BUILD)/images/ (via Docker)"; \
	elif command -v plantuml >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local plantuml..."; \
		mkdir -p $(DOCS_BUILD)/images; \
		plantuml -tpng -o ../../../../build/images $(DOCS_SRC)/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated (local mode)"; \
	else \
		echo "❌ Neither Docker nor local plantuml available."; \
		echo "  Install Docker or plantuml to generate diagrams."; \
		exit 1; \
	fi

docs-html: ## Generate HTML documentation from AsciiDoc (Docker-based)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📄 Generating HTML documentation..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD); \
		echo "   Running: asciidoctor src/arqua42-architecture.adoc -o build/arqua42-architecture.html ..."; \
		$(DOCKER_RUN) asciidoctor src/arqua42-architecture.adoc \
			-o build/arqua42-architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ HTML documentation generated: $(DOCS_BUILD)/arqua42-architecture.html (via Docker)"; \
		echo "  View with: make docs-serve"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD); \
		echo "   Running: asciidoctor src/arqua42-architecture.adoc -o build/arqua42-architecture.html ..."; \
		$(DOCKER_RUN) asciidoctor src/arqua42-architecture.adoc \
			-o build/arqua42-architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ HTML documentation generated: $(DOCS_BUILD)/arqua42-architecture.html (via Docker)"; \
	elif command -v asciidoctor >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local asciidoctor..."; \
		mkdir -p $(DOCS_BUILD); \
		asciidoctor $(DOCS_SRC)/arqua42-architecture.adoc \
			-o $(DOCS_BUILD)/arqua42-architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram 2>/dev/null || \
		asciidoctor $(DOCS_SRC)/arqua42-architecture.adoc \
			-o $(DOCS_BUILD)/arqua42-architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images; \
		echo "✓ HTML documentation generated (local mode)"; \
	else \
		echo "❌ Neither Docker nor local asciidoctor available."; \
		echo "  Install Docker or asciidoctor to generate HTML."; \
		exit 1; \
	fi

docs-pdf: ## Generate PDF documentation (Docker-based)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📑 Generating PDF documentation..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD); \
		echo "   Running: asciidoctor-pdf src/arqua42-architecture.adoc -o build/arqua42-architecture.pdf ..."; \
		$(DOCKER_RUN) asciidoctor-pdf src/arqua42-architecture.adoc \
			-o build/arqua42-architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ PDF documentation generated: $(DOCS_BUILD)/arqua42-architecture.pdf (via Docker)"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD); \
		echo "   Running: asciidoctor-pdf src/arqua42-architecture.adoc -o build/arqua42-architecture.pdf ..."; \
		$(DOCKER_RUN) asciidoctor-pdf src/arqua42-architecture.adoc \
			-o build/arqua42-architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ PDF documentation generated: $(DOCS_BUILD)/arqua42-architecture.pdf (via Docker)"; \
	elif command -v asciidoctor-pdf >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local asciidoctor-pdf..."; \
		mkdir -p $(DOCS_BUILD); \
		asciidoctor-pdf $(DOCS_SRC)/arqua42-architecture.adoc \
			-o $(DOCS_BUILD)/arqua42-architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram 2>/dev/null || \
		asciidoctor-pdf $(DOCS_SRC)/arqua42-architecture.adoc \
			-o $(DOCS_BUILD)/arqua42-architecture.pdf \
			-a sectnums \
			-a imagesdir=images; \
		echo "✓ PDF documentation generated (local mode)"; \
	else \
		echo "❌ Neither Docker nor local asciidoctor-pdf available."; \
		echo "  Install Docker or asciidoctor-pdf to generate PDF."; \
		exit 1; \
	fi

docs-watch: ## Watch documentation files for changes and rebuild (requires docker compose)
	@echo "Watching documentation for changes..."
	@if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then \
		docker compose -f docker-compose.docs.yml run --rm docs-watch; \
	else \
		echo "❌ docker compose not found. Install docker compose for watch mode."; \
		exit 1; \
	fi

docs-serve: ## Serve documentation on http://localhost:8000
	@echo "Serving documentation on http://localhost:8000"
	@echo "Open http://localhost:8000/build/arqua42-architecture.html in your browser"
	@echo "Press Ctrl+C to stop"
	@python3 -m http.server 8000 -d docs/

##@ Development

dev: ## Start development environment with Docker Compose
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Starting Arqua42 CRUD Prototype..."
	@echo "   Backend:  http://localhost:8000"
	@echo "   Frontend: http://localhost:5173"
	@echo "   API Docs: http://localhost:8000/docs"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@docker compose up --build

dev-down: ## Stop development environment
	@echo "Stopping development environment..."
	@docker compose down

db-reset: ## Reset database (drop all tables and recreate)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🗑️  Resetting database..."
	@docker compose exec backend python seed_db.py
	@echo "✓ Database reset complete"

db-seed: ## Seed database with sample data
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 Seeding database..."
	@docker compose exec backend python seed_db.py
	@echo "✓ Database seeded with sample data"

db-import-figures: ## Import figures from JSON catalog (usage: make db-import-figures FILE=path/to/catalog.json)
	@if [ -z "$(FILE)" ]; then \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "❌ Error: FILE parameter is required"; \
		echo ""; \
		echo "Usage:"; \
		echo "  make db-import-figures FILE=data/figuren-kataloge/figuren-v1.0-saison-2024.json"; \
		echo ""; \
		echo "Available catalogs:"; \
		docker compose exec backend find data/figuren-kataloge -name "*.json" -type f 2>/dev/null || true; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		exit 1; \
	fi
	@docker compose exec backend python import_figures.py "$(FILE)"

lint: ## Run linters
	@echo "Running linters..."
	@echo "⚠ Lint targets not yet implemented"

test: ## Run tests
	@echo "Running tests..."
	@echo "⚠ Test targets not yet implemented"

##@ Cleanup

clean: ## Remove generated files (safely removes entire build directory)
	@echo "Cleaning generated files..."
	@rm -rf $(DOCS_BUILD)
	@echo "✓ Cleanup complete (removed $(DOCS_BUILD)/)"

docs-adrs: ## Convert ADRs from Markdown to HTML (Docker-based)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 Converting ADRs to HTML..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		echo "🐳 Using Docker image: $(DOCKER_IMAGE)"; \
		mkdir -p $(DOCS_BUILD)/adrs; \
		for adr in $(DOCS_SRC)/adrs/ADR-*.md; do \
			filename=$$(basename "$$adr" .md); \
			echo "   - $$filename.md → $$filename.html"; \
			$(DOCKER_RUN) pandoc "src/adrs/$$filename.md" \
				-o "build/adrs/$$filename.html" \
				--standalone \
				--toc \
				--toc-depth=2 \
				--metadata title="$$filename" \
				--css=../../style.css; \
		done; \
		echo "✓ ADRs converted to HTML in $(DOCS_BUILD)/adrs/ (via Docker)"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		mkdir -p $(DOCS_BUILD)/adrs; \
		for adr in $(DOCS_SRC)/adrs/ADR-*.md; do \
			filename=$$(basename "$$adr" .md); \
			echo "   - $$filename.md → $$filename.html"; \
			$(DOCKER_RUN) pandoc "src/adrs/$$filename.md" \
				-o "build/adrs/$$filename.html" \
				--standalone \
				--toc \
				--toc-depth=2 \
				--metadata title="$$filename"; \
		done; \
		echo "✓ ADRs converted to HTML (via Docker)"; \
	elif command -v pandoc >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local pandoc..."; \
		mkdir -p $(DOCS_BUILD)/adrs; \
		for adr in $(DOCS_SRC)/adrs/ADR-*.md; do \
			filename=$$(basename "$$adr" .md); \
			echo "   - $$filename"; \
			pandoc "$$adr" -o "$(DOCS_BUILD)/adrs/$$filename.html" \
				--standalone --toc --toc-depth=2 \
				--metadata title="$$filename"; \
		done; \
		echo "✓ ADRs converted (local mode)"; \
	else \
		echo "❌ Neither Docker nor pandoc available."; \
		echo "  Copying markdown files as fallback..."; \
		mkdir -p $(DOCS_BUILD)/adrs; \
		cp $(DOCS_SRC)/adrs/ADR-*.md $(DOCS_BUILD)/adrs/; \
		echo "⚠ ADRs copied as .md files (install Docker or pandoc for HTML conversion)"; \
	fi

##@ Cloud Deployment (fly.io)

deploy: ## Deploy to fly.io production
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Deploying to fly.io (aquarius.arc42.org)"
	@echo ""
	@echo "Prerequisites:"
	@echo "  ✓ flyctl installed (brew install flyctl)"
	@echo "  ✓ Logged in (flyctl auth login)"
	@echo "  ✓ Database created (turso db create aquarius)"
	@echo "  ✓ Secrets configured (flyctl secrets list)"
	@echo ""
	@read -p "Continue with deployment? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		flyctl deploy --remote-only; \
		echo ""; \
		echo "✅ Deployment complete!"; \
		echo "🔗 URL: https://aquarius.arc42.org"; \
	else \
		echo "❌ Deployment cancelled"; \
		exit 1; \
	fi

deploy-status: ## Show deployment status and logs
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Deployment Status"
	@echo ""
	@flyctl status
	@echo ""
	@echo "📝 Recent Logs (last 20 lines):"
	@echo ""
	@flyctl logs --lines 20

deploy-logs: ## Stream live logs from fly.io
	@flyctl logs

deploy-ssh: ## SSH into fly.io container
	@flyctl ssh console

deploy-rollback: ## Rollback to previous version
	@echo "⚠️  ROLLBACK TO PREVIOUS VERSION"
	@echo ""
	@flyctl releases
	@echo ""
	@read -p "Rollback to previous version? [yes/NO] " -r; \
	if [[ $$REPLY == "yes" ]]; then \
		flyctl releases rollback; \
	else \
		echo "❌ Rollback cancelled"; \
		exit 1; \
	fi

deploy-setup: ## Initial setup for fly.io deployment
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔧 fly.io Setup Wizard"
	@echo ""
	@echo "Step 1: Create fly.io app"
	@echo "  flyctl launch --no-deploy"
	@echo ""
	@echo "Step 2: Create Turso database"
	@echo "  turso db create aquarius --location fra"
	@echo "  turso db tokens create aquarius --expiration none"
	@echo ""
	@echo "Step 3: Set secrets"
	@echo "  flyctl secrets set DATABASE_URL='libsql://aquarius-xyz.turso.io?authToken=...'"
	@echo ""
	@echo "Step 4: Create SSL certificate"
	@echo "  flyctl certs create aquarius.arc42.org"
	@echo ""
	@echo "Step 5: Deploy"
	@echo "  make deploy"
	@echo ""
	@read -p "Start setup now? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "Creating fly.io app..."; \
		flyctl launch --no-deploy; \
	else \
		echo "Setup cancelled. Run commands manually."; \
	fi
