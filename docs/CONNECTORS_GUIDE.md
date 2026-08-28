# DataFlowX Connectors Framework Guide

## 1. Supported Heterogeneous Connectors
DataFlowX provides a pluggable, high-performance connector ecosystem with built-in connection pooling, credential encryption, and schema introspection.

| Connector Type | Protocol | Auth Methods | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | `asyncpg` / `psycopg2` | User/Pass, SSL/TLS, Vault | Schema inspection, incremental watermark queries, bulk copy |
| **MySQL** | `pymysql` / `aiomysql` | User/Pass, SSL/TLS | Table introspection, change tracking |
| **MongoDB** | `pymongo` / `motor` | SCRAM, X.509, Atlas URI | Document flattening, projection queries, collection discovery |
| **REST API** | `httpx` / HTTP/1.1 & HTTP/2 | Bearer JWT, API Key, Basic, OAuth2 | Pagination (Page, Offset, Cursor, Link Header), rate limit backoff |
| **CSV / TSV** | PyArrow / Pandas | Local, S3, FTP | Chunked streaming, auto-delimiter detection, gzip/snappy support |
| **Excel** | `openpyxl` | Local, S3 | Multi-sheet discovery, typed cell parsing, header detection |
| **JSON / NDJSON** | `orjson` / `json` | Local, S3 | JSONPath nested extraction, streaming line-delimited ingestion |
| **Kafka** | `confluent-kafka` | SASL_SSL, PLAIN, SCRAM | Offset tracking, consumer groups, partition rebalancing |
| **S3 / MinIO** | `boto3` / REST | IAM Role, Access Key/Secret | Prefix glob scanning, multipart upload, multi-bucket routing |

## 2. Connector Lifecycle Architecture
Every connector implements the abstract lifecycle defined in `connectors/base.py`:
1. `connect()`: Establishes network socket and verifies credentials.
2. `test_connection()`: Validates latency and health probe.
3. `discover_schema(target)`: Infers column names, physical types, and nullability.
4. `preview_data(target, limit)`: Samples the top N rows for visual DAG preview.
5. `extract_data(target, **kwargs)`: Streams records with watermark tracking.
6. `disconnect()`: Closes connection pool cleanly.
