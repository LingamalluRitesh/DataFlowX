.PHONY: help install-backend install-frontend dev-backend dev-frontend dev-worker dev-scheduler test lint seed-demo docker-up docker-down

help:
	@echo "DataFlowX - Enterprise Data Pipeline & Orchestration Platform"
	@echo ""
	@echo "Targets:"
	@echo "  install-backend   Install python backend dependencies"
	@echo "  install-frontend  Install Next.js frontend dependencies"
	@echo "  dev-backend       Start FastAPI backend development server"
	@echo "  dev-frontend      Start Next.js frontend development server"
	@echo "  dev-worker        Start Celery distributed task worker"
	@echo "  dev-scheduler     Start DAG pipeline scheduler daemon"
	@echo "  test              Run unit, integration, and performance tests"
	@echo "  lint              Run ruff and typescript lint checks"
	@echo "  seed-demo         Seed database with enterprise demo tenant & pipelines"
	@echo "  docker-up         Launch complete platform via Docker Compose"
	@echo "  docker-down       Stop all platform containers"

install-backend:
	pip install -r requirements.txt
	pip install -e .

install-frontend:
	cd frontend && npm install

dev-backend:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm run dev

dev-worker:
	celery -A orchestration_engine.workers.celery_app worker --loglevel=info -Q high_priority,default,low_priority

dev-scheduler:
	python -m orchestration_engine.scheduler.scheduler_daemon

test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-performance:
	pytest tests/performance/ -v

lint:
	ruff check .
	cd frontend && npm run lint

seed-demo:
	python scripts/seed_demo_data.py

run-demo-pipeline:
	python scripts/run_demo_pipeline.py

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
