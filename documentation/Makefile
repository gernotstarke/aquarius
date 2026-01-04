.PHONY: help docs html pdf serve clean build-image

# Docker configuration
DOCKER_IMAGE := aquarius-docs:latest
DOCKER_RUN := docker run --rm -v $(CURDIR):/docs -w /docs $(DOCKER_IMAGE)

# Paths (relative to documentation/)
BUILD_DIR := build
SRC_DIR := .

##@ Documentation

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

docs: html ## Generate all documentation
	@echo "✅ Documentation generated!"
	@echo "   📄 View: $(BUILD_DIR)/aquarius-architecture.html"

html: ## Generate HTML documentation from AsciiDoc
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📄 Generating HTML documentation..."
	@mkdir -p $(BUILD_DIR)
	@if command -v asciidoctor >/dev/null 2>&1; then \
		asciidoctor architecture/*.adoc \
			-D $(BUILD_DIR) \
			-a toc=left \
			-a toclevels=3 \
			-a sectnums \
			-a icons=font; \
		echo "✅ HTML generated (local asciidoctor)"; \
	else \
		echo "❌ asciidoctor not found"; \
		echo "   Install: brew install asciidoctor"; \
		echo "   Or use: make build-image && make html"; \
		exit 1; \
	fi

pdf: ## Generate PDF documentation
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📑 Generating PDF documentation..."
	@mkdir -p $(BUILD_DIR)
	@if command -v asciidoctor-pdf >/dev/null 2>&1; then \
		asciidoctor-pdf architecture/*.adoc \
			-D $(BUILD_DIR) \
			-a sectnums; \
		echo "✅ PDF generated (local asciidoctor-pdf)"; \
	else \
		echo "❌ asciidoctor-pdf not found"; \
		echo "   Install: gem install asciidoctor-pdf"; \
		exit 1; \
	fi

serve: ## Serve documentation locally
	@echo "🌐 Serving documentation at http://localhost:8000"
	@cd $(BUILD_DIR) && python3 -m http.server 8000

build-image: ## Build Docker image for documentation generation
	@echo "🐳 Building documentation Docker image..."
	@cd .. && docker build -f Dockerfile.docs -t $(DOCKER_IMAGE) .
	@echo "✅ Docker image built: $(DOCKER_IMAGE)"

clean: ## Clean build artifacts
	@echo "🧹 Cleaning documentation..."
	@rm -rf $(BUILD_DIR)
	@echo "✅ Cleanup complete!"
