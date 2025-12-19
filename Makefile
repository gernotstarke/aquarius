.PHONY: help docs docs-diagrams docs-html docs-pdf docs-watch docs-serve docs-build-image clean test

# Docker configuration
DOCKER_IMAGE := aquarius-docs:latest
DOCKER_RUN := docker run --rm -v $(CURDIR)/docs:/docs -w /docs $(DOCKER_IMAGE)

# Documentation paths
DOCS_SRC := docs/src
DOCS_BUILD := docs/build

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Docker Build

docs-build-image: ## Build the Docker image for documentation generation
	@echo "Building documentation Docker image..."
	@docker build -f Dockerfile.docs -t $(DOCKER_IMAGE) .
	@echo "✓ Docker image built: $(DOCKER_IMAGE)"

##@ Documentation

docs: docs-diagrams docs-html ## Generate all documentation (diagrams + HTML) - Docker-based
	@echo "✓ Documentation generated successfully"

docs-diagrams: ## Generate PNG diagrams from PlantUML sources (Docker-based)
	@echo "Generating diagrams from PlantUML..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		mkdir -p $(DOCS_BUILD)/images; \
		$(DOCKER_RUN) plantuml -tpng -o ../../../build/images src/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated in $(DOCS_BUILD)/images/"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		mkdir -p $(DOCS_BUILD)/images; \
		$(DOCKER_RUN) plantuml -tpng -o ../../../build/images src/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated in $(DOCS_BUILD)/images/"; \
	elif command -v plantuml >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local plantuml..."; \
		mkdir -p $(DOCS_BUILD)/images; \
		plantuml -tpng -o ../../../build/images $(DOCS_SRC)/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated (local mode)"; \
	else \
		echo "❌ Neither Docker nor local plantuml available."; \
		echo "  Install Docker or plantuml to generate diagrams."; \
		exit 1; \
	fi

docs-html: ## Generate HTML documentation from AsciiDoc (Docker-based)
	@echo "Generating HTML documentation..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		mkdir -p $(DOCS_BUILD); \
		$(DOCKER_RUN) asciidoctor src/architecture.adoc \
			-o build/architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ HTML documentation generated: $(DOCS_BUILD)/architecture.html"; \
		echo "  View with: make docs-serve"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		mkdir -p $(DOCS_BUILD); \
		$(DOCKER_RUN) asciidoctor src/architecture.adoc \
			-o build/architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ HTML documentation generated: $(DOCS_BUILD)/architecture.html"; \
	elif command -v asciidoctor >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local asciidoctor..."; \
		mkdir -p $(DOCS_BUILD); \
		asciidoctor $(DOCS_SRC)/architecture.adoc \
			-o $(DOCS_BUILD)/architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-a imagesdir=images \
			-r asciidoctor-diagram 2>/dev/null || \
		asciidoctor $(DOCS_SRC)/architecture.adoc \
			-o $(DOCS_BUILD)/architecture.html \
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
	@echo "Generating PDF documentation..."
	@if docker images -q $(DOCKER_IMAGE) 2>/dev/null | grep -q .; then \
		mkdir -p $(DOCS_BUILD); \
		$(DOCKER_RUN) asciidoctor-pdf src/architecture.adoc \
			-o build/architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ PDF documentation generated: $(DOCS_BUILD)/architecture.pdf"; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "⚠ Docker image not found. Building it now..."; \
		$(MAKE) docs-build-image; \
		mkdir -p $(DOCS_BUILD); \
		$(DOCKER_RUN) asciidoctor-pdf src/architecture.adoc \
			-o build/architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram; \
		echo "✓ PDF documentation generated: $(DOCS_BUILD)/architecture.pdf"; \
	elif command -v asciidoctor-pdf >/dev/null 2>&1; then \
		echo "⚠ Docker not available, using local asciidoctor-pdf..."; \
		mkdir -p $(DOCS_BUILD); \
		asciidoctor-pdf $(DOCS_SRC)/architecture.adoc \
			-o $(DOCS_BUILD)/architecture.pdf \
			-a sectnums \
			-a imagesdir=images \
			-r asciidoctor-diagram 2>/dev/null || \
		asciidoctor-pdf $(DOCS_SRC)/architecture.adoc \
			-o $(DOCS_BUILD)/architecture.pdf \
			-a sectnums \
			-a imagesdir=images; \
		echo "✓ PDF documentation generated (local mode)"; \
	else \
		echo "❌ Neither Docker nor local asciidoctor-pdf available."; \
		echo "  Install Docker or asciidoctor-pdf to generate PDF."; \
		exit 1; \
	fi

docs-watch: ## Watch documentation files for changes and rebuild (requires docker-compose)
	@echo "Watching documentation for changes..."
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose -f docker-compose.docs.yml run --rm docs-watch; \
	else \
		echo "❌ docker-compose not found. Install docker-compose for watch mode."; \
		exit 1; \
	fi

docs-serve: ## Serve documentation on http://localhost:8000
	@echo "Serving documentation on http://localhost:8000"
	@echo "Open http://localhost:8000/build/architecture.html in your browser"
	@echo "Press Ctrl+C to stop"
	@python3 -m http.server 8000 -d docs/

##@ Development

dev: ## Start development environment
	@echo "Starting development environment..."
	@echo "⚠ Development targets not yet implemented"

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
