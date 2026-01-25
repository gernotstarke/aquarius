.PHONY: help web mobile docs

##@ Aquarius Monorepo

help: ## Show all available targets
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🏊 Aquarius Monorepo - Available Targets"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Projects:"
	@echo "  web/           - Desktop/Web Application (Backend + Frontend)"
	@echo "  mobile/        - Mobile Application (iOS/Android)"
	@echo "  documentation/ - Architecture & Requirements Documentation"
	@echo "  docs/          - Jekyll Static Website (GitHub Pages)"
	@echo ""
	@echo "Quick Start:"
	@echo "  make web-dev        - Start web app development servers"
	@echo "  make test           - Run all tests and generate reports"
	@echo ""
	@echo "Website (Jekyll + Docker):"
	@echo "  make website-compile - Compile ADRs and other content for Jekyll"
	@echo "  make website-dev     - Compile, obfuscate, start Jekyll server"
	@echo "  make website-clean   - Stop server and clean generated files"
	@echo ""
	@echo "Password Protection (Architecture Section):"
	@echo "  make protect-obfuscate              - Obfuscate password-protect.js"
	@echo "  make protect-hash PASSWORD=xxx      - Generate SHA-256 hash for password"
	@echo "  make protect-setup                  - Full setup with instructions"
	@echo ""
	@echo "For project-specific help:"
	@echo "  cd web && make help"
	@echo "  cd mobile && make help"
	@echo "  cd documentation && make help"
	@echo ""

##@ Web App

web-logs: ## Show web app logs
	@cd web && make deploy-logs

web-clean: ## Clean web app build artifacts
	@cd web && make clean

web-backend-build: ## Build the backend Docker image
	@cd web && docker compose build backend

##@ Testing

test: test-report-json ## Run all tests (backend + frontend) and generate reports
	@echo "🔄 Recompiling website content with test results..."
	@$(MAKE) website-compile
	@echo ""
	@echo "✅ Tests complete! Run 'make website-dev' to see results on the site."

test-report-json: test-backend-json test-frontend-json ## Generate JSON reports for frontend and backend tests
	@echo "✅ All raw test reports generated in docs/build/test-results/"
	@echo "⚙️  Compiling test results for Jekyll..."
	@python3 scripts/compile-test-results.py

test-backend-json: web-backend-build
	@echo "🧪 Running backend tests and generating JSON report..."
	@mkdir -p docs/build/test-results
	@cd web && docker compose run --rm -v $(PWD)/docs/build/test-results:/app/test-results backend pytest --json-report --json-report-file=/app/test-results/backend.json

test-frontend-json:
	@echo "🧪 Running frontend tests and generating JSON report..."
	@mkdir -p docs/build/test-results
	@cd web/frontend && npm install && npm run test -- --reporter=json > ../../docs/build/test-results/frontend.json

##@ Mobile App

mobile-ios: ## Run iOS simulator
	@if [ -d "mobile" ]; then \
		cd mobile && make ios-simulator; \
	else \
		echo "⚠️  Mobile app not yet initialized"; \
		echo "   Run: cd mobile && npm install"; \
	fi

mobile-android: ## Run Android emulator
	@if [ -d "mobile" ]; then \
		cd mobile && make android-emulator; \
	else \
		echo "⚠️  Mobile app not yet initialized"; \
	fi

mobile-build-ios: ## Build iOS app
	@if [ -d "mobile" ]; then \
		cd mobile && make build-ios; \
	else \
		echo "⚠️  Mobile app not yet initialized"; \
	fi

mobile-test: ## Run mobile app tests
	@if [ -d "mobile" ]; then \
		cd mobile && make test; \
	else \
		echo "⚠️  Mobile app not yet initialized"; \
	fi

##@ Project Website (Jekyll)

website-compile: ## Compile content for Jekyll (ADRs, arc42, test stats)
	@echo "📄 Compiling ADRs for Jekyll..."
	@mkdir -p docs/_adrs
	@cd docs && docker compose run --rm compile-adrs
	@echo "📄 Compiling arc42 documentation for Jekyll..."
	@cd docs && docker compose run --rm compile-arc42
	@echo "📊 Compiling test statistics..."
	@mkdir -p docs/_data
	@if [ -f docs/build/test-results/backend.json ] || [ -f docs/build/test-results/frontend.json ]; then \
		python3 scripts/compile-test-results.py; \
	else \
		echo '{"passed": 0, "failed": 0, "skipped": 0, "total": 0, "percentage": 0}' > docs/_data/test_stats.json; \
		echo "   ⚠️  No test results found. Run 'make test' to generate test reports."; \
	fi

website-dev: website-compile ## Start project website locally (http://localhost:4000)
	@echo "🔐 Obfuscating protected JavaScript..."
	@cd docs && docker compose run --rm obfuscate
	@echo "🌐 Starting Jekyll website..."
	@cd docs && docker compose up jekyll

website-clean: ## Stop project website and clean up
	@cd docs && docker compose down
	@rm -rf docs/_site docs/_adrs docs/_pages/architecture/arc42.html
	@echo "✅ Removed docs/_site, docs/_adrs, and generated arc42 content"

##@ Documentation

docs-build: ## Generate all documentation (arc42, ADRs)
	@cd documentation && make docs

docs-serve: ## Serve documentation locally
	@cd documentation && make serve

docs-pdf: ## Generate PDF documentation
	@cd documentation && make pdf

docs-clean: ## Clean documentation build artifacts
	@cd documentation && make clean

##@ Jekyll Documentation Site

docs-jekyll: website-compile ## Start Jekyll documentation site (http://localhost:4000)
	@echo "🔐 Obfuscating protected JavaScript..."
	@cd docs && docker compose run --rm obfuscate
	@echo "🚀 Starting Jekyll documentation site..."
	@echo "📖 Visit: http://localhost:4000"
	@cd docs && docker compose up jekyll

docs-jekyll-bg: website-compile ## Start Jekyll in background
	@cd docs && docker compose run --rm obfuscate
	@cd docs && docker compose up -d jekyll
	@echo "✅ Jekyll running in background"
	@echo "📖 Visit: http://localhost:4000"

docs-jekyll-down: ## Stop Jekyll server
	@cd docs && docker compose down

docs-jekyll-logs: ## View Jekyll logs
	@cd docs && docker compose logs -f jekyll

##@ Installation & Setup

install: ## Install all dependencies (web + mobile + docs)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📦 Installing dependencies for all projects..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🌐 Web App..."
	@cd web/backend && pip install -r requirements.txt
	@cd web/frontend && npm install
	@echo ""
	@if [ -d "mobile" ]; then \
		echo "📱 Mobile App..."; \
		cd mobile && npm install; \
		echo ""; \
	fi
	@echo "📚 Documentation..."
	@cd documentation && make build-image
	@echo ""
	@echo "✅ All dependencies installed!"

clean: ## Clean all build artifacts
	@echo "🧹 Cleaning all projects..."
	@cd web && make clean
	@if [ -d "mobile" ]; then cd mobile && make clean; fi
	@cd documentation && make clean
	@echo "✅ Cleanup complete!"

##@ Password Protection

protect-obfuscate: ## Obfuscate the password protection JavaScript (runs in Docker)
	@cd docs && docker compose run --rm obfuscate

protect-hash: ## Generate SHA-256 hash for a password (usage: make protect-hash PASSWORD=mypassword)
	@if [ -z "$(PASSWORD)" ]; then \
		echo "Usage: make protect-hash PASSWORD=yourpassword"; \
		echo ""; \
		echo "Example:"; \
		echo "  make protect-hash PASSWORD=training2024"; \
		echo ""; \
		echo "The generated hash can be set in:"; \
		echo "  - docs/_config.yml as 'protected_password_hash'"; \
		echo "  - Page front matter as 'password_hash'"; \
	else \
		echo "🔑 Generating SHA-256 hash for password..."; \
		if command -v shasum >/dev/null 2>&1; then \
			HASH=$$(printf %s "$(PASSWORD)" | shasum -a 256 | awk '{print $$1}'); \
		elif command -v sha256sum >/dev/null 2>&1; then \
			HASH=$$(printf %s "$(PASSWORD)" | sha256sum | awk '{print $$1}'); \
		else \
			echo "Error: no SHA-256 tool found (need shasum or sha256sum)."; \
			exit 1; \
		fi; \
		echo ""; \
		echo "Password: $(PASSWORD)"; \
		echo "SHA-256:  $$HASH"; \
		echo ""; \
		echo "Add to docs/_config.yml:"; \
		echo "  protected_password_hash: \"$$HASH\""; \
	fi

protect-setup: protect-obfuscate ## Full setup: obfuscate JS and show instructions
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔐 Password Protection Setup Complete"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Next steps:"
	@echo "1. Generate a password hash:"
	@echo "   make protect-hash PASSWORD=your-secure-password"
	@echo ""
	@echo "2. Add the hash to docs/_config.yml:"
	@echo "   protected_password_hash: \"<hash>\""
	@echo ""
	@echo "3. Deploy the site"
	@echo ""
	@echo "Default password (CHANGE THIS!): training2024"
	@echo ""

##@ Git & Repository

status: ## Show git status and branch info
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Repository Status"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@git status
	@echo ""
	@echo "Branch: $$(git branch --show-current)"
	@echo "Last commit: $$(git log -1 --pretty=format:'%h - %s (%an, %ar)')"
