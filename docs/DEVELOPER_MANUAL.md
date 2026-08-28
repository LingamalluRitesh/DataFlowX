# DataFlowX Developer Manual & Contribution Guide

## 1. Local Development Setup
### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Docker & Docker Compose

### Step-by-Step Setup
```bash
# 1. Clone repo
git clone https://github.com/LingamalluRitesh/DataFlowX.git
cd DataFlowX

# 2. Setup Python environment
python -m venv .venv
# Activate venv:
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# 3. Setup Frontend
cd frontend
npm install
cd ..

# 4. Initialize database and seed demo data
python scripts/seed_demo_data.py
python scripts/run_demo_pipeline.py

# 5. Run tests
pytest tests/ -v
```

## 2. Project Layout
- `backend/`: FastAPI application, domain services, SQLAlchemy 2.0 models, Pydantic schemas, security vault.
- `connectors/`: Database, API, messaging, and file connectors.
- `data_engine/`: Vectorized operators, SQL query engine, quality rules, medallion storage, profiler.
- `orchestration_engine/`: Kahn's DAG cycle parser, task executor, retry engine, Redlock scheduler, Celery workers.
- `storage/`: Snappy Parquet manager, local & S3 storage engines.
- `frontend/`: Next.js 14, React 18, TailwindCSS, React Flow DAG canvas.
- `tests/`: Unit, integration, E2E, and 1M-record performance benchmarks.
- `infrastructure/`: Docker, Kubernetes, Helm, and Prometheus manifests.
- `docs/`: 13 enterprise documentation guides.
