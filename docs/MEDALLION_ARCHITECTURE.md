# DataFlowX Medallion Architecture Guide

## 1. Multi-Hop Lakehouse Architecture
DataFlowX implements the enterprise Medallion Lakehouse paradigm with three distinct storage tiers:

```
[ Raw Ingestion Sources ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│  🥉 BRONZE TIER — Raw Ingestion Lake                    │
│  • Storage: storage/bronze/{pipeline}/{date}/{id}.parquet│
│  • Format: Append-only Snappy-compressed Parquet       │
│  • Schema: Ingested verbatim with audit metadata       │
│  • SLA: Immutable historical record of truth           │
└─────────────────────────┬──────────────────────────────┘
                          │ (Quality & Cleaning Engine)
                          ▼
┌────────────────────────────────────────────────────────┐
│  🥈 SILVER TIER — Curated & Cleansed Lake               │
│  • Storage: storage/silver/{dataset}/v1/{id}.parquet   │
│  • Transformations: Deduplication, casing, type-casts   │
│  • Quarantining: Bad rows isolated to Quarantine store  │
│  • Schema: Conformed, strongly-typed enterprise schema │
└─────────────────────────┬──────────────────────────────┘
                          │ (Aggregation & Rollup Engine)
                          ▼
┌────────────────────────────────────────────────────────┐
│  🥇 GOLD TIER — Analytical Data Marts                   │
│  • Storage: storage/gold/{mart_name}/v1/{id}.parquet   │
│  • Models: Star schemas, customer 360, daily metrics   │
│  • Destinations: DuckDB / SQLite / PostgreSQL DW tables│
│  • SLA: Production BI, ML feature stores, reporting    │
└────────────────────────────────────────────────────────┘
```

## 2. Storage Partitioning & Retention
- **Date Partitioning**: Storage directories are partitioned by execution date (`YYYY-MM-DD`).
- **Snappy Compression**: All intermediate and final tables utilize Snappy columnar Parquet compression, reducing storage footprint by up to 85% compared to raw JSON/CSV.
- **Audit Metadata Columns**: Ingested records automatically receive `_dfx_ingested_at` and `_dfx_execution_id` lineage tracking columns.
