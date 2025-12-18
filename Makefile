.PHONY: help docs docs-diagrams docs-html docs-pdf docs-watch docs-serve clean

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Documentation

docs: docs-diagrams docs-html ## Generate all documentation (diagrams + HTML)
	@echo "✓ Documentation generated successfully"

docs-diagrams: ## Generate PNG diagrams from PlantUML sources
	@echo "Generating diagrams from PlantUML..."
	@if command -v plantuml >/dev/null 2>&1; then \
		mkdir -p docs/architecture/images/generated; \
		plantuml -tpng -o ../generated docs/architecture/images/puml/*.puml; \
		echo "✓ Diagrams generated in docs/architecture/images/generated/"; \
	else \
		echo "⚠ plantuml not found. Install with:"; \
		echo "  • macOS: brew install plantuml"; \
		echo "  • Linux: apt install plantuml"; \
		echo "  • Or download from: https://plantuml.com/download"; \
	fi

docs-html: ## Generate HTML documentation from AsciiDoc
	@echo "Generating HTML documentation..."
	@if command -v asciidoctor >/dev/null 2>&1; then \
		asciidoctor docs/architecture.adoc \
			-o docs/architecture.html \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font \
			-r asciidoctor-diagram 2>/dev/null || \
			asciidoctor docs/architecture.adoc \
				-o docs/architecture.html \
				-a toc=left \
				-a toclevels=3 \
				-a sectnums \
				-a icons=font; \
		echo "✓ HTML documentation generated: docs/architecture.html"; \
		echo "  View with: make docs-serve"; \
	else \
		echo "⚠ asciidoctor not found. Install with: gem install asciidoctor"; \
		echo "  For diagram support: gem install asciidoctor-diagram"; \
	fi

docs-pdf: ## Generate PDF documentation (requires asciidoctor-pdf)
	@echo "Generating PDF documentation..."
	@if command -v asciidoctor-pdf >/dev/null 2>&1; then \
		asciidoctor-pdf docs/architecture.adoc \
			-o docs/architecture.pdf \
			-a sectnums \
			-r asciidoctor-diagram 2>/dev/null || \
			asciidoctor-pdf docs/architecture.adoc \
				-o docs/architecture.pdf \
				-a sectnums; \
		echo "✓ PDF documentation generated: docs/architecture.pdf"; \
	else \
		echo "⚠ asciidoctor-pdf not found. Install with: gem install asciidoctor-pdf"; \
		echo "  For diagram support: gem install asciidoctor-diagram"; \
	fi

docs-watch: ## Watch documentation files for changes and rebuild
	@echo "Watching documentation for changes..."
	@if command -v watchexec >/dev/null 2>&1; then \
		watchexec -w docs -e adoc,puml "make docs-html"; \
	else \
		echo "⚠ watchexec not found. Install with: brew install watchexec (macOS) or apt install watchexec (Linux)"; \
		echo "  Alternatively use: find docs -name '*.adoc' | entr make docs-html"; \
	fi

docs-serve: ## Serve documentation on http://localhost:8000
	@echo "Serving documentation on http://localhost:8000"
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

clean: ## Remove generated files
	@echo "Cleaning generated files..."
	@rm -f docs/architecture.html docs/architecture.pdf
	@rm -f docs/architecture/images/generated/*.png
	@echo "✓ Cleanup complete"
