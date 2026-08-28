# DataFlowX Deployment & Operations Manual

## 1. Quickstart with Docker Compose
Start the complete DataFlowX platform stack in seconds:
```bash
# 1. Clone repository
git clone https://github.com/LingamalluRitesh/DataFlowX.git
cd DataFlowX

# 2. Start all services
docker compose up -d

# 3. Seed demo data and execute Customer 360 pipeline
python scripts/seed_demo_data.py
python scripts/run_demo_pipeline.py
```

Access the interfaces:
- **Web Console**: `http://localhost:3000` (Login: `admin@dataflowx.io` / `Admin@DataFlowX2026!`)
- **FastAPI OpenAPI Swagger**: `http://localhost:8000/docs`
- **MinIO S3 Console**: `http://localhost:9001` (User: `minioadmin` / Pass: `minioadmin2026!`)
- **Prometheus Metrics**: `http://localhost:9090`

## 2. Production Kubernetes Deployment (Helm)
```bash
# Deploy using Helm
helm upgrade --install dataflowx ./infrastructure/helm/dataflowx \
  --namespace dataflowx \
  --create-namespace \
  --values ./infrastructure/helm/dataflowx/values.yaml
```
