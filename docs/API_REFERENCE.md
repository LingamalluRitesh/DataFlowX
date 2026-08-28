# DataFlowX REST API Reference

The DataFlowX REST API complies with OpenAPI 3.1 specifications. All authenticated endpoints require a `Bearer <access_token>` in the `Authorization` header.

## 1. Authentication & Users
- `POST /api/v1/auth/register`: Create user account & receive JWT token pair.
- `POST /api/v1/auth/login`: Authenticate with email/username and password.
- `POST /api/v1/auth/refresh`: Refresh expired access token with valid refresh token.
- `GET /api/v1/auth/me`: Retrieve current user profile, organization, and permissions.
- `GET /api/v1/users`: List organization members.
- `GET /api/v1/users/roles`: List system and custom RBAC roles.

## 2. Connectors & Data Sources
- `GET /api/v1/sources`: List configured data connectors.
- `POST /api/v1/sources`: Register new data connector with encrypted credentials.
- `GET /api/v1/sources/{id}`: Fetch connector details and health status.
- `POST /api/v1/sources/{id}/test`: Execute live connection health check.
- `GET /api/v1/sources/{id}/schema`: Discover remote database/file schema.
- `GET /api/v1/sources/{id}/preview`: Sample top N records from source.

## 3. Pipelines & Executions
- `GET /api/v1/pipelines`: List DAG workflows.
- `POST /api/v1/pipelines`: Create DAG pipeline definition.
- `GET /api/v1/pipelines/{id}`: Fetch pipeline details & visual DAG graph.
- `POST /api/v1/pipelines/{id}/run`: Trigger asynchronous pipeline execution.
- `GET /api/v1/executions`: List recent pipeline runs with status filters.
- `GET /api/v1/executions/{id}`: Fetch execution summary and task-level logs.
- `GET /api/v1/executions/{id}/logs`: Stream real-time terminal logs for execution.

## 4. Data Quality & Lineage
- `GET /api/v1/quality/rules`: List available quality rules.
- `GET /api/v1/quality/suites`: List configured test suites.
- `GET /api/v1/lineage/graph`: Retrieve end-to-end provenance graph.
- `GET /api/v1/audit/logs`: Search immutable audit logs.
- `GET /api/v1/monitoring/overview`: Platform-wide KPI overview and worker health.
