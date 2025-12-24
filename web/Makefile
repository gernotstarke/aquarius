.PHONY: help dev dev-down test db-reset db-seed db-import-figures deploy deploy-status deploy-logs deploy-ssh deploy-rollback deploy-setup clean

##@ Web App Development

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

dev: ## Start development servers (backend + frontend)
	@echo "🚀 Starting web app development servers..."
	@docker compose up

dev-down: ## Stop development servers
	@docker compose down

test: ## Run tests
	@echo "🧪 Running tests..."
	@docker compose exec backend pytest

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning web app..."
	@find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find backend -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf frontend/dist frontend/node_modules/.vite
	@echo "✅ Cleanup complete!"

##@ Database

db-reset: ## Reset database (drop all tables and recreate)
	@echo "⚠️  This will DELETE all data!"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose exec backend python seed_db.py; \
	else \
		echo "❌ Cancelled"; \
	fi

db-seed: ## Seed database with sample data
	@echo "📊 Seeding database..."
	@docker compose exec backend python seed_db.py

db-import-figures: ## Import figures from JSON catalog (usage: make db-import-figures FILE=path/to/catalog.json)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE parameter is required"; \
		echo "Usage:"; \
		echo "  make db-import-figures FILE=backend/data/figuren/figuren-v1.0-saison-2024.json"; \
		exit 1; \
	fi
	@docker compose exec backend python import_figures.py "$(FILE)"

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
