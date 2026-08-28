# DataFlowX Architecture Blueprint

## 1. System Overview
**DataFlowX** is a next-generation, cloud-native enterprise data pipeline and workflow orchestration platform built for high-throughput batch and real-time streaming ETL/ELT workloads. It combines modern Medallion Lakehouse principles (Bronze, Silver, Gold layers) with a visual DAG execution engine, automated data quality scoring, immutable data lineage tracking, and multi-tenant enterprise governance.

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

## 2. Core Architectural Pillars
1. **Zero-Loss Medallion Guarantee**: Every raw byte received is preserved verbatim in Bronze Parquet storage before any transformations occur.
2. **Deterministic Isolation**: Failed data records are automatically quarantined into dedicated quarantine storage without halting or contaminating downstream business marts.
3. **Decoupled Compute & Storage**: The orchestration workers and query engines remain stateless, executing against local file systems, MinIO S3 object stores, or enterprise data warehouses.
4. **Resilience & Fault Tolerance**: Self-healing exponential backoff with full randomized jitter ensures external API rate limits or transient network failures do not result in pipeline outages.
