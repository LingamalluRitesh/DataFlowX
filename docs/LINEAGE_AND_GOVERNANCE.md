# DataFlowX Lineage & Data Governance Guide

## 1. End-to-End Visual Provenance Tracking
DataFlowX captures comprehensive data lineage across every execution:
- Upstream data sources (External DBs, Kafka topics, REST APIs).
- Bronze raw immutable landing zones.
- Silver curated datasets with quality transformations.
- Gold business metrics and star-schema analytical marts.
- Final warehouse tables (PostgreSQL, DuckDB, Snowflake, BigQuery).

## 2. Impact Analysis & Column-Level Lineage
- **Upstream Tracing**: Trace root cause data quality failures back to the specific source connector and batch timestamp.
- **Downstream Impact**: Understand which downstream reports and dashboards will be affected before modifying an upstream schema.
- **Data Contracts**: Define schema conformance SLAs with strict compile-time and runtime guarantees.
