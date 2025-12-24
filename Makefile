.PHONY: help web mobile docs

##@ Aquarius Monorepo

help: ## Show all available targets
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🏊 Aquarius Monorepo - Available Targets"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Projects:"
	@echo "  web/         - Desktop/Web Application (Backend + Frontend)"
	@echo "  mobile/      - Mobile Application (iOS/Android)"
	@echo "  documentation/ - Architecture & Requirements Documentation"
	@echo "  docs/        - Jekyll Static Website (GitHub Pages)"
	@echo ""
	@echo "Quick Start:"
	@echo "  make web-dev        - Start web app development servers"
	@echo "  make mobile-ios     - Run iOS simulator"
	@echo "  make docs-build     - Generate documentation"
	@echo ""
	@echo "For project-specific help:"
	@echo "  cd web && make help"
	@echo "  cd mobile && make help"
	@echo "  cd documentation && make help"
	@echo ""

##@ Web App

web-dev: ## Start web app development servers (backend + frontend)
	@cd web && make dev

web-test: ## Run web app tests
	@cd web && make test

web-db-reset: ## Reset web app database
	@cd web && make db-reset

web-db-seed: ## Seed web app database with test data
	@cd web && make db-seed

web-deploy: ## Deploy web app to fly.io
	@cd web && make deploy

web-deploy-status: ## Check web app deployment status
	@cd web && make deploy-status

web-logs: ## Show web app logs
	@cd web && make deploy-logs

web-clean: ## Clean web app build artifacts
	@cd web && make clean

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

##@ Documentation

docs-build: ## Generate all documentation (arc42, ADRs)
	@cd documentation && make docs

docs-serve: ## Serve documentation locally
	@cd documentation && make serve

docs-pdf: ## Generate PDF documentation
	@cd documentation && make pdf

docs-clean: ## Clean documentation build artifacts
	@cd documentation && make clean

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

##@ Git & Repository

status: ## Show git status and branch info
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Repository Status"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@git status
	@echo ""
	@echo "Branch: $$(git branch --show-current)"
	@echo "Last commit: $$(git log -1 --pretty=format:'%h - %s (%an, %ar)')"
