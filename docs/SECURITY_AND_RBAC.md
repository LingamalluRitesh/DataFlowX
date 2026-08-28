# DataFlowX Enterprise Security & RBAC Guide

## 1. Multi-Tenant Organization & Workspace Isolation
DataFlowX implements strict multi-tenancy:
- **Organizations**: Enterprise accounts with isolated billing, SSO, and global policies.
- **Workspaces**: Logical project boundaries within organizations with distinct datasets, pipelines, and secrets.
- **Foreign Key Scoping**: Every database entity (`Source`, `Dataset`, `Pipeline`, `Execution`) is strictly scoped by `workspace_id`.

## 2. Granular Role-Based Access Control (RBAC)
Pre-configured roles and custom role permission matrices:
- **`Super Admin`**: Full platform governance, user management, and system configuration.
- **`Org Admin`**: Organization workspace creation, billing, and team invitations.
- **`Data Engineer`**: Create and modify connectors, datasets, DAG pipelines, and quality suites.
- **`Data Analyst`**: View datasets, execute pipelines, inspect lineage graphs and quality reports.
- **`Viewer / Auditor`**: Read-only access to execution histories and immutable audit logs.

## 3. AES-256-GCM Credential Vault
All sensitive credentials (database passwords, API bearer tokens, TLS private keys) are encrypted using AES-256 authenticated encryption with associated data (AEAD) or Fernet key derivation prior to storage in PostgreSQL.
