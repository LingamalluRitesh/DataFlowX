"""
DataFlowX Enterprise Demo Seeder
Bootstraps initial super admin, demo organization, workspaces, sample connectors, quality rules, datasets, and pipeline definitions.
"""

import asyncio
from datetime import datetime, timezone
import json
import os
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from backend.core.config import settings
from backend.core.database import async_session_factory, Base, engine
from backend.core.encryption import vault
from backend.core.security import get_password_hash
from backend.database.models import (
    DataSource,
    Dataset,
    DatasetVersion,
    Organization,
    Pipeline,
    PipelineNode,
    PipelineSchedule,
    PipelineVersion,
    QualityCheck,
    QualityRuleDefinition,
    QualitySuite,
    Role,
    SourceCredential,
    User,
    UserRole,
    Workspace,
    WorkspaceMember,
)


async def seed_data():
    print("Initializing DataFlowX enterprise seed data...")

    # Create tables if not present
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # 1. Super Admin User
        admin_stmt = select(User).where(User.email == settings.INITIAL_ADMIN_EMAIL)
        admin_user = (await session.execute(admin_stmt)).scalar_one_or_none()

        if not admin_user:
            admin_user = User(
                email=settings.INITIAL_ADMIN_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.INITIAL_ADMIN_PASSWORD),
                full_name=settings.INITIAL_ADMIN_FULL_NAME,
                is_active=True,
                is_superuser=True,
                is_verified=True,
            )
            session.add(admin_user)
            await session.flush()
            print(f"Created Super Admin: {admin_user.email}")

        # 2. Demo Organization & Workspace
        org_stmt = select(Organization).where(Organization.name == settings.INITIAL_ORG_NAME)
        org = (await session.execute(org_stmt)).scalar_one_or_none()

        if not org:
            org = Organization(
                name=settings.INITIAL_ORG_NAME,
                slug="global-enterprise-corp",
                plan="enterprise"
            )
            session.add(org)
            await session.flush()

            ws = Workspace(
                organization_id=org.id,
                name=settings.INITIAL_WORKSPACE_NAME,
                slug="production-analytics",
                is_default=True
            )
            session.add(ws)
            await session.flush()

            # Add admin to workspace
            member = WorkspaceMember(
                workspace_id=ws.id,
                user_id=admin_user.id,
                role_name="admin",
                status="active"
            )
            session.add(member)
            print(f"Created Organization '{org.name}' and Workspace '{ws.name}'")
        else:
            ws = (await session.execute(select(Workspace).where(Workspace.organization_id == org.id))).scalar_one()

        # 3. Built-in Quality Rule Definitions
        builtin_rules = [
            ("NotNullCheck", "NOT_NULL", "Asserts that field contains no nulls", {}),
            ("UniqueKeyCheck", "UNIQUE", "Asserts uniqueness of key columns", {}),
            ("ValidEmailCheck", "EMAIL", "Asserts compliant RFC 5322 email addresses", {}),
            ("PositiveValueCheck", "RANGE", "Asserts values >= 0", {"min": 0}),
            ("ValidAgeCheck", "RANGE", "Asserts ages between 18 and 120", {"min": 18, "max": 120}),
            ("RegexFormatCheck", "REGEX", "Validates regex pattern", {"pattern": "^[A-Za-z0-9_-]+$"}),
        ]

        for rname, rtype, rdesc, rparams in builtin_rules:
            existing_r = (await session.execute(select(QualityRuleDefinition).where(QualityRuleDefinition.name == rname))).scalar_one_or_none()
            if not existing_r:
                r_def = QualityRuleDefinition(
                    workspace_id=ws.id,
                    name=rname,
                    rule_type=rtype,
                    description=rdesc,
                    parameters_schema_json=rparams,
                    is_builtin=True
                )
                session.add(r_def)

        # 4. Demo Data Source (Sample Customer CRM CSV)
        sample_csv_path = os.path.abspath("./storage/temp/raw_customers_demo.csv")
        os.makedirs(os.path.dirname(sample_csv_path), exist_ok=True)

        # Write sample raw CSV dataset if not exists
        if not os.path.exists(sample_csv_path):
            with open(sample_csv_path, "w", encoding="utf-8") as f:
                f.write("customer_id,full_name,email,age,country,total_spend,signup_date\n")
                f.write("CUST-001,  alice smith  ,alice@example.com,29,USA,1450.50,2025-01-15\n")
                f.write("CUST-002,BOB JONES,bob.jones@corporate.org,42,UK,890.00,2025-02-01\n")
                f.write("CUST-003,carol white,carol@invalid-email,17,Canada,-50.00,2025-02-10\n")  # Corrupted row
                f.write("CUST-004,david brown,david.brown@tech.io,35,USA,3200.75,2025-03-05\n")
                f.write("CUST-001,alice smith,alice@example.com,29,USA,1450.50,2025-01-15\n")  # Duplicate row
                f.write("CUST-005,  eva green  ,eva.green@domain.com,24,Germany,620.20,2025-03-20\n")
                f.write("CUST-006,frank miller,frank@miller.com,51,USA,4500.00,2025-04-12\n")

        src_stmt = select(DataSource).where(DataSource.name == "Customer CRM File Source")
        demo_src = (await session.execute(src_stmt)).scalar_one_or_none()
        if not demo_src:
            demo_src = DataSource(
                workspace_id=ws.id,
                name="Customer CRM File Source",
                slug="customer-crm-file-source",
                connector_type="csv",
                description="Raw customer account details and transaction history export",
                config={"file_path": sample_csv_path, "delimiter": ","},
                status="active",
                health_status="healthy"
            )
            session.add(demo_src)
            await session.flush()
            print(f"Created Demo Data Source: {demo_src.name}")

        # 5. Demo Pipeline Definition: Customer 360 Pipeline
        pipe_stmt = select(Pipeline).where(Pipeline.name == "Customer 360 Medallion Pipeline")
        demo_pipe = (await session.execute(pipe_stmt)).scalar_one_or_none()

        if not demo_pipe:
            demo_pipe = Pipeline(
                workspace_id=ws.id,
                name="Customer 360 Medallion Pipeline",
                slug="customer-360-medallion-pipeline",
                description="End-to-end extraction from CRM, Bronze ingestion, Data Quality validation, Silver normalization, and Gold warehouse aggregation.",
                pipeline_type="batch",
                environment="production",
                tags=["customer360", "finance", "production", "medallion"],
                status="active",
                is_active=True
            )
            session.add(demo_pipe)
            await session.flush()

            # Construct DAG Graph JSON
            dag_data = {
                "nodes": [
                    {
                        "id": "node_extract",
                        "type": "extract",
                        "name": "Extract Customer CRM",
                        "config": {
                            "connector_type": "csv",
                            "file_path": sample_csv_path,
                            "connector_config": {"file_path": sample_csv_path, "delimiter": ","}
                        },
                        "position": {"x": 50, "y": 100}
                    },
                    {
                        "id": "node_quality",
                        "type": "quality",
                        "name": "Validate & Quality Filter",
                        "config": {
                            "failure_action": "QUARANTINE_RECORDS",
                            "rules": [
                                {"rule_type": "NOT_NULL", "target_column": "customer_id", "rule_name": "Check Customer ID Not Null", "threshold_percentage": 100.0},
                                {"rule_type": "EMAIL", "target_column": "email", "rule_name": "Check Valid Email", "threshold_percentage": 90.0},
                                {"rule_type": "RANGE", "target_column": "total_spend", "rule_name": "Check Positive Spend", "threshold_percentage": 90.0, "condition_params": {"min": 0}}
                            ]
                        },
                        "position": {"x": 300, "y": 100}
                    },
                    {
                        "id": "node_silver_transform",
                        "type": "transform",
                        "name": "Clean & Deduplicate Silver",
                        "config": {
                            "steps": [
                                {"type": "deduplicate", "config": {"subset": ["customer_id"], "keep": "first"}},
                                {"type": "normalize", "config": {"columns": ["full_name"], "case_mode": "title", "strip_whitespace": True}},
                                {"type": "normalize", "config": {"columns": ["email"], "case_mode": "lower", "strip_whitespace": True}},
                                {"type": "calculated_column", "config": {"name": "customer_tier", "expression": "CASE WHEN total_spend > 2000 THEN 'VIP' WHEN total_spend > 1000 THEN 'Gold' ELSE 'Standard' END"}}
                            ]
                        },
                        "position": {"x": 550, "y": 100}
                    },
                    {
                        "id": "node_gold_aggregate",
                        "type": "aggregate",
                        "name": "Aggregate Gold Customer Mart",
                        "config": {
                            "group_by": ["country", "customer_tier"],
                            "aggregations": {"total_spend": "sum", "customer_id": "count"}
                        },
                        "position": {"x": 800, "y": 100}
                    },
                    {
                        "id": "node_warehouse_load",
                        "type": "warehouse_load",
                        "name": "Load Analytics Warehouse",
                        "config": {
                            "table_name": "mart_customer_spend_by_country",
                            "mode": "overwrite",
                            "primary_keys": ["country", "customer_tier"]
                        },
                        "position": {"x": 1050, "y": 100}
                    }
                ],
                "edges": [
                    {"source": "node_extract", "target": "node_quality"},
                    {"source": "node_quality", "target": "node_silver_transform"},
                    {"source": "node_silver_transform", "target": "node_gold_aggregate"},
                    {"source": "node_gold_aggregate", "target": "node_warehouse_load"}
                ],
                "globals": {}
            }

            p_ver = PipelineVersion(
                pipeline_id=demo_pipe.id,
                version_number=1,
                dag_definition_json=dag_data,
                node_count=len(dag_data["nodes"]),
                edge_count=len(dag_data["edges"]),
                checksum="initial_demo_hash_v1",
                commit_message="Initial Customer 360 Medallion DAG release"
            )
            session.add(p_ver)
            await session.flush()
            demo_pipe.active_version_id = p_ver.id

            # Add Schedule: Daily at 2 AM
            sched = PipelineSchedule(
                pipeline_id=demo_pipe.id,
                cron_expression="0 2 * * *",
                timezone="UTC",
                is_enabled=True
            )
            session.add(sched)
            print(f"Created Demo Pipeline: '{demo_pipe.name}' with DAG Version 1")

        await session.commit()
        print("\nSeed data bootstrap complete! Super Admin credentials:")
        print(f"  Email: {settings.INITIAL_ADMIN_EMAIL}")
        print(f"  Password: {settings.INITIAL_ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed_data())
