# DataFlowX — Intelligent Enterprise Data Pipeline & Orchestration Platform

<div align="center">

![DataFlowX Logo](https://img.shields.io/badge/DataFlowX-Enterprise%20Pipeline%20Platform-blue?style=for-the-badge&logo=apache-airflow)
![Python Version](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Next.js Version](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)
![TypeScript Version](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)

**Next-Generation Distributed Data Engineering, Medallion Lakehouse & Workflow Orchestration Platform**

</div>

---

## 🌟 Key Platform Highlights
- 🚀 **Heterogeneous Data Connectors**: Ingest seamlessly from PostgreSQL, MySQL, MongoDB, REST APIs, CSV, Excel, JSON/NDJSON, Apache Kafka, and AWS S3 / MinIO.
- 🥉🥈🥇 **Medallion Lakehouse Architecture**: Built-in Bronze (raw immutable), Silver (cleansed & deduplicated), and Gold (aggregated business marts) storage tiers with Snappy columnar Parquet compression.
- 🛡️ **Automated Data Quality & Quarantining**: 10+ validation rules (NotNull, Unique, Range, Regex, Email, CustomSql) with automatic row-level quarantining and quality SLA scoring.
- 🕸️ **Visual DAG Pipeline Builder**: Interactive React Flow canvas with real-time Kahn's algorithm cycle detection, layered topological parallelization, and live streaming execution terminal.
- 🔄 **Self-Healing Exponential Backoff**: Intelligent retry engine with randomized jitter and granular non-retryable exception classification.
- 🔒 **Enterprise Security & Governance**: AES-256-GCM Credential Vault, granular multi-tenant RBAC, end-to-end visual data lineage graph, and immutable audit logging.
- ⚡ **High-Throughput Vectorized Engine**: Vectorized C-speed transformations, in-memory DuckDB & SQLite SQL queries, and safe AST Python sandboxing benchmarked at over 1,000,000 records.

---

## 🏗️ Architectural Topology

```
+-----------------------------------------------------------------------------------------+
|                                    DATA SOURCES                                         |
|  PostgreSQL | MySQL | MongoDB | REST APIs | CSV/Excel | JSON/NDJSON | Kafka | S3/MinIO   |
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                DATAFLOWX INGESTION ENGINE                                |
|  - Watermark-based High-Water State        - Streaming Micro-batch Engine               |
|  - Schema Discovery & DDL Inference        - Snappy-compressed Columnar Parquet Buffering|
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                MEDALLION LAKEHOUSE STORAGE                              |
|   [ Bronze Layer ]     -->      [ Silver Layer ]       -->      [ Gold Data Marts ]     |
|   Raw Immutable Events          Cleaned & Validated             Aggregated Metrics      |
|   (Zero-loss ingest)            (Quarantine bad rows)           (Analytical Star Schemas)|
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                               TRANSFORMATION & QUALITY ENGINE                           |
|  - Vectorized C-Speed Pandas & PyArrow Ops - 10+ Quality Rule Evaluators (NotNull, Range)|
|  - DuckDB & SQLite In-Memory SQL Engines   - Automated Row Quarantining & SLA Scoring   |
|  - Safe AST Custom Python Sandbox          - Statistical Data Profiling & Null Tracking |
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                               ORCHESTRATION & DISTRIBUTED WORKERS                       |
|  - Kahn's Algorithm Cycle Detection        - Celery Distributed Worker Cluster          |
|  - Topological Layer Parallelization       - Distributed Redlock Mutex Daemon          |
|  - Exponential Backoff with Full Jitter    - Cron & Watermark Triggers                  |
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                             API, SECURITY & GOVERNANCE LAYER                            |
|  - FastAPI Async REST API (OpenAPI 3.1)    - End-to-End Visual Data Lineage Graph       |
|  - AES-256-GCM Credential Vault            - Immutable Security & Mutation Audit Logs   |
|  - Granular RBAC Permissions Matrix        - Prometheus Metrics & Real-time Alerts      |
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                 ENTERPRISE WEB CONSOLE                                  |
|  - Next.js 14 / React 18 / TypeScript      - Interactive React Flow DAG Builder         |
|  - Real-time Terminal Execution Stream     - 20+ Dedicated Mission Control Dashboards   |
+-----------------------------------------------------------------------------------------+
```

---

## ⚡ Quickstart

### 1. Run with Docker Compose
```bash
# Clone the repository
git clone https://github.com/LingamalluRitesh/DataFlowX.git
cd DataFlowX

# Launch all infrastructure and application services
docker compose up -d
```

### 2. Local Python & Frontend Development
```bash
# 1. Install backend requirements
pip install -r requirements.txt

# 2. Seed database & run verified Customer 360 demo pipeline
python scripts/seed_demo_data.py
python scripts/run_demo_pipeline.py

# 3. Start Backend Server
uvicorn backend.main:app --reload --port 8000

# 4. Start Frontend Console (in new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔑 Default Credentials

| Portal | URL | Default Username | Default Password |
| :--- | :--- | :--- | :--- |
| **DataFlowX Console** | `http://localhost:3000` | `admin@dataflowx.io` | `Admin@DataFlowX2026!` |
| **FastAPI Swagger Docs**| `http://localhost:8000/docs` | *(Bearer JWT)* | *(Use login endpoint)* |
| **MinIO S3 Console** | `http://localhost:9001` | `minioadmin` | `minioadmin2026!` |
| **Prometheus Metrics** | `http://localhost:9090` | *(Unauthenticated)* | *(Unauthenticated)* |

---

## 🧪 Comprehensive Test Suite & Benchmarks

Run the complete 21-test suite covering unit tests, integration tests, API endpoints, and 1,000,000-record performance benchmarks:
```bash
pytest tests/ -v
```

```
tests/integration/test_api_endpoints.py::test_health_and_root_endpoints PASSED
tests/integration/test_api_endpoints.py::test_auth_registration_and_login_flow PASSED
tests/integration/test_api_endpoints.py::test_sources_and_connectors_api PASSED
tests/integration/test_pipeline_medallion.py::test_full_medallion_pipeline_integration PASSED
tests/performance/test_performance_benchmarks.py::test_10k_records_benchmark PASSED
tests/performance/test_performance_benchmarks.py::test_100k_records_benchmark PASSED
tests/performance/test_performance_benchmarks.py::test_1m_records_throughput_benchmark PASSED
tests/unit/test_dag_cycle_detector.py::test_valid_dag_topological_sort_and_layers PASSED
tests/unit/test_dag_cycle_detector.py::test_cycle_detection_in_cyclic_dag PASSED
tests/unit/test_operators.py::test_select_and_rename_operators PASSED
tests/unit/test_operators.py::test_deduplicate_and_normalize_operators PASSED
tests/unit/test_operators.py::test_filter_and_calculated_column PASSED
tests/unit/test_operators.py::test_aggregate_operator PASSED
tests/unit/test_quality_engine.py::test_individual_quality_rules PASSED
tests/unit/test_quality_engine.py::test_quality_suite_evaluator_and_quarantine PASSED
tests/unit/test_retry_jitter.py::test_exponential_backoff_delay_calculation PASSED
tests/unit/test_retry_jitter.py::test_retry_jitter_bounds PASSED
tests/unit/test_retry_jitter.py::test_retryable_vs_non_retryable_classification PASSED
tests/unit/test_security_vault.py::test_password_hashing PASSED
tests/unit/test_security_vault.py::test_credential_vault_encryption_decryption PASSED
tests/unit/test_security_vault.py::test_jwt_token_issuance_and_decoding PASSED

============================= 21 passed in 12.71s =============================
```

---

## 📚 Complete Enterprise Documentation Library

Detailed documentation manuals are available in the [`docs/`](docs/) directory:
1. 📐 [**System Architecture**](docs/ARCHITECTURE.md)
2. 🔌 [**Connectors Framework Guide**](docs/CONNECTORS_GUIDE.md)
3. ⚙️ [**Data Engine & Vectorized Operators**](docs/DATA_ENGINE.md)
4. 🛡️ [**Data Quality & Row Quarantining**](docs/DATA_QUALITY.md)
5. 🥉🥈🥇 [**Medallion Lakehouse Guide**](docs/MEDALLION_ARCHITECTURE.md)
6. 🔄 [**Orchestration Engine & Redlock**](docs/ORCHESTRATION_ENGINE.md)
7. 🎨 [**Visual DAG Builder Manual**](docs/DAG_BUILDER_GUIDE.md)
8. 🔒 [**Enterprise Security & RBAC**](docs/SECURITY_AND_RBAC.md)
9. 🗺️ [**Data Lineage & Governance**](docs/LINEAGE_AND_GOVERNANCE.md)
10. 📊 [**Observability, Prometheus & Alerts**](docs/OBSERVABILITY_AND_ALERTS.md)
11. 🚀 [**Deployment & Operations (Docker & K8s)**](docs/DEPLOYMENT_GUIDE.md)
12. 📖 [**REST API Reference**](docs/API_REFERENCE.md)
13. 💻 [**Developer Manual & Contributions**](docs/DEVELOPER_MANUAL.md)

---

## 📄 License
DataFlowX is licensed under the Apache License, Version 2.0.
