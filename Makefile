.PHONY: help docs docs-html docs-pdf docs-watch docs-serve clean

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Documentation

docs: docs-html ## Generate all documentation formats (HTML only for now, PDF requires asciidoctor-pdf)
	@echo "✓ Documentation generated successfully"

docs-html: ## Generate HTML documentation from AsciiDoc
	@echo "Generating HTML documentation..."
	@if command -v asciidoctor >/dev/null 2>&1; then \
		asciidoctor docs/architecture.adoc -o docs/architecture.html -a toc=left -a toclevels=3; \
		echo "✓ HTML documentation generated: docs/architecture.html"; \
	else \
		echo "⚠ asciidoctor not found. Install with: gem install asciidoctor"; \
		echo "  Falling back to viewing AsciiDoc source..."; \
	fi

docs-pdf: ## Generate PDF documentation (requires asciidoctor-pdf)
	@echo "Generating PDF documentation..."
	@if command -v asciidoctor-pdf >/dev/null 2>&1; then \
		asciidoctor-pdf docs/architecture.adoc -o docs/architecture.pdf; \
		echo "✓ PDF documentation generated: docs/architecture.pdf"; \
	else \
		echo "⚠ asciidoctor-pdf not found. Install with: gem install asciidoctor-pdf"; \
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
	@echo "✓ Cleanup complete"
