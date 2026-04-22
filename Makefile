.PHONY: help install dev test lint format clean docker-up docker-down api web cli db-migrate health

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m
VENV_PYTHON := $(CURDIR)/.venv/bin/python
PYTHON := $(if $(wildcard $(VENV_PYTHON)),$(VENV_PYTHON),python3)

help: ## Show this help message
	@echo "$(BLUE)JARVIS - AI Cognitive Assistant$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -e .
	cd apps/web && npm install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	pip install -e ".[dev]"
	pre-commit install
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

setup: ## Complete local setup (first time)
	@echo "$(BLUE)Setting up JARVIS for local development...$(NC)"
	make install
	make install-dev
	cp .env.example .env
	mkdir -p runtime/{working,metrics,innovations,logs,state}
	mkdir -p runtime/working/execution_logs
	@echo "$(YELLOW)⚠ Please edit .env with your API keys$(NC)"
	@echo "$(GREEN)✓ Setup complete!$(NC)"

dev: ## Start all services for development
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker-compose up -d postgres redis
	@echo "$(GREEN)✓ Infrastructure started$(NC)"
	@echo "$(YELLOW)Run 'make api' and 'make web' in separate terminals$(NC)"

api: ## Start API server
	@echo "$(BLUE)Starting API server...$(NC)"
	$(PYTHON) -m uvicorn apps.api.jarvis_api.main:app --reload --host 0.0.0.0 --port 8000

web: ## Start web dashboard
	@echo "$(BLUE)Starting web dashboard...$(NC)"
	cd apps/web && npm run dev

cli: ## Run CLI (use: make cli ARGS="strategist plan")
	@echo "$(BLUE)Running JARVIS CLI...$(NC)"
	$(PYTHON) -m apps.cli.jarvis_cli.main $(ARGS)

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v --cov=packages/jarvis_core --cov-report=term-missing
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest tests/unit/ -v

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running E2E tests...$(NC)"
	pytest tests/e2e/ -v

lint: ## Run linters
	@echo "$(BLUE)Running linters...$(NC)"
	ruff check .
	black --check .
	mypy packages/jarvis_core
	@echo "$(GREEN)✓ Linting completed$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff check --fix .
	black .
	isort .
	@echo "$(GREEN)✓ Code formatted$(NC)"

type-check: ## Run type checker
	@echo "$(BLUE)Running type checker...$(NC)"
	mypy packages/jarvis_core

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	cd apps/api/jarvis_api && alembic -c alembic.ini upgrade head
	@echo "$(GREEN)✓ Migrations completed$(NC)"

db-rollback: ## Rollback last migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	cd apps/api/jarvis_api && alembic -c alembic.ini downgrade -1

db-reset: ## Reset database (WARNING: destroys data)
	@echo "$(RED)⚠ WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 3; \
		make db-migrate; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	fi

seed: ## Seed database with test data
	@echo "$(BLUE)Seeding database...$(NC)"
	$(PYTHON) scripts/database/seed.py
	@echo "$(GREEN)✓ Database seeded$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf dist/ build/ htmlcov/
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-runtime: ## Clean runtime directory (logs, cache, etc.)
	@echo "$(YELLOW)Cleaning runtime directory...$(NC)"
	rm -rf runtime/working/* runtime/logs/* runtime/metrics/* runtime/innovations/*
	@echo "$(GREEN)✓ Runtime cleaned$(NC)"

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Docker images built$(NC)"

docker-up: ## Start all Docker services
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Docker services started$(NC)"

docker-down: ## Stop all Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Docker services stopped$(NC)"

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-ps: ## Show running containers
	docker-compose ps

health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@echo "API: $$(curl -s http://localhost:8000/health 2>/dev/null | jq -r .status 2>/dev/null || echo 'DOWN')"
	@echo "Web: $$(curl -s http://localhost:3000 > /dev/null 2>&1 && echo 'UP' || echo 'DOWN')"
	@echo "PostgreSQL: $$(docker-compose exec -T postgres pg_isready -U jarvis 2>/dev/null | grep -q accepting && echo 'UP' || echo 'DOWN')"
	@echo "Redis: $$(docker-compose exec -T redis redis-cli ping 2>/dev/null || echo 'DOWN')"

logs: ## Show application logs
	@echo "$(BLUE)Application logs:$(NC)"
	tail -f runtime/logs/*.log 2>/dev/null || echo "No logs found"

version: ## Show version information
	@echo "$(BLUE)JARVIS Version Information$(NC)"
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Node: $$(node --version 2>&1)"
	@echo "Docker: $$(docker --version 2>&1)"
	@echo "Docker Compose: $$(docker-compose --version 2>&1)"

k8s-deploy: ## Deploy to Kubernetes
	@echo "$(BLUE)Deploying to Kubernetes...$(NC)"
	kubectl apply -f infrastructure/kubernetes/base/

k8s-delete: ## Delete from Kubernetes
	@echo "$(YELLOW)Deleting from Kubernetes...$(NC)"
	kubectl delete -f infrastructure/kubernetes/base/

k8s-status: ## Check Kubernetes deployment status
	kubectl get pods,services,ingress

deploy-staging: ## Deploy to staging
	@echo "$(BLUE)Deploying to staging...$(NC)"
	./scripts/deployment/deploy_staging.sh

deploy-production: ## Deploy to production (requires approval)
	@echo "$(RED)⚠ Deploying to PRODUCTION$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		./scripts/deployment/deploy_production.sh; \
	fi

.DEFAULT_GOAL := help
