.PHONY: help install dev test lint format clean docker-up docker-down k8s-deploy

help:
	@echo "JARVIS Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install         - Install all dependencies"
	@echo "  make install-dev     - Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev             - Start development environment"
	@echo "  make dev-api         - Start API server only"
	@echo "  make dev-web         - Start web dashboard only"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run all tests"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make test-integration- Run integration tests only"
	@echo "  make test-e2e        - Run end-to-end tests"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run linters"
	@echo "  make format          - Format code"
	@echo "  make type-check      - Run type checking"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-up       - Start Docker services"
	@echo "  make docker-down     - Stop Docker services"
	@echo "  make docker-logs     - View Docker logs"
	@echo ""
	@echo "Kubernetes:"
	@echo "  make k8s-deploy      - Deploy to Kubernetes"
	@echo "  make k8s-delete      - Delete from Kubernetes"
	@echo "  make k8s-status      - Check deployment status"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           - Clean generated files"
	@echo "  make db-migrate      - Run database migrations"
	@echo "  make db-seed         - Seed database with test data"

# Installation
install:
	pip install -r requirements.txt
	cd apps/web/dashboard && npm install

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-asyncio black ruff mypy isort bandit
	cd apps/web/dashboard && npm install
	pre-commit install

# Development
dev:
	docker-compose up -d postgres redis
	@echo "Starting services..."
	@sleep 3
	python -m apps.api.jarvis_api.main &
	cd apps/web/dashboard && npm run dev

dev-api:
	docker-compose up -d postgres redis
	python -m apps.api.jarvis_api.main

dev-web:
	cd apps/web/dashboard && npm run dev

# Testing
test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-e2e:
	pytest tests/e2e/ -v

test-coverage:
	pytest tests/ -v --cov=packages/jarvis_core --cov=apps/api --cov-report=html --cov-report=term

# Code Quality
lint:
	ruff check .
	black --check .
	isort --check-only .

format:
	ruff check --fix .
	black .
	isort .

type-check:
	mypy packages/jarvis_core apps/api --ignore-missing-imports

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Kubernetes
k8s-deploy:
	kubectl apply -f infrastructure/kubernetes/base/

k8s-delete:
	kubectl delete -f infrastructure/kubernetes/base/

k8s-status:
	kubectl get pods,services,ingress

# Maintenance
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	rm -rf htmlcov/ .coverage

db-migrate:
	cd apps/api/jarvis_api && alembic upgrade head

db-seed:
	python scripts/database/seed.py
