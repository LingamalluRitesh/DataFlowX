"""
DataFlowX End-to-End Demo Pipeline Runner
Executes the live Customer 360 Medallion Pipeline through all stages:
Extraction -> Bronze Lake -> Quality Check & Quarantine -> Silver Normalization -> Gold Aggregation -> Warehouse Load -> Lineage & Profiling.
"""

import asyncio
from datetime import datetime, timezone
import json
import os
import sys
import time

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from backend.core.database import async_session_factory
from backend.database.models import Pipeline, PipelineVersion
from orchestration_engine.dag.models import DAGDefinition
from orchestration_engine.executor.dag_executor import DAGExecutor
from storage import ParquetManager, storage_engine

console = Console()


async def run_pipeline():
    console.print(Panel.fit("[bold cyan]DataFlowX — Customer 360 Enterprise Pipeline Runner[/bold cyan]"))

    async with async_session_factory() as session:
        # Find demo pipeline
        stmt = select(Pipeline).where(Pipeline.name == "Customer 360 Medallion Pipeline")
        pipeline = (await session.execute(stmt)).scalar_one_or_none()

        if not pipeline or not pipeline.active_version_id:
            console.print("[yellow]Demo pipeline not found in database. Running seed script first...[/yellow]")
            from scripts.seed_demo_data import seed_data
            await seed_data()
            pipeline = (await session.execute(stmt)).scalar_one()

        v_stmt = select(PipelineVersion).where(PipelineVersion.id == pipeline.active_version_id)
        p_ver = (await session.execute(v_stmt)).scalar_one()

    dag_data = p_ver.dag_definition_json
    dag_def = DAGDefinition(**dag_data)
    exec_id = f"exec_demo_{int(time.time())}"

    console.print(f"[bold]Triggering Execution ID:[/bold] [green]{exec_id}[/green]")
    console.print(f"[bold]Pipeline:[/bold] {pipeline.name} (Nodes: {len(dag_def.nodes)}, Edges: {len(dag_def.edges)})")

    executor = DAGExecutor(
        dag_definition=dag_def,
        pipeline_id=pipeline.id,
        execution_id=exec_id,
        max_workers=4
    )

    t0 = time.time()
    summary = executor.run()
    elapsed = time.time() - t0

    # Display Results Table
    table = Table(title=f"Execution Results — Status: [{ 'green' if summary.status == 'SUCCESS' else 'red' }]{summary.status}[/]")
    table.add_column("Node ID", style="cyan")
    table.add_column("Task Name", style="bold")
    table.add_column("Status", style="bold")
    table.add_column("Duration", justify="right")
    table.add_column("Records In", justify="right")
    table.add_column("Records Out", justify="right")
    table.add_column("Quality Score", justify="right")

    for nid, tres in summary.task_results.items():
        status_style = "green" if tres.status == "SUCCESS" else "red" if tres.status == "FAILED" else "yellow"
        q_score_str = f"{tres.quality_score:.1f}%" if tres.quality_score is not None else "-"
        table.add_row(
            nid,
            tres.name,
            f"[{status_style}]{tres.status}[/{status_style}]",
            f"{tres.duration_seconds}s",
            str(tres.records_in),
            str(tres.records_out),
            q_score_str
        )

    console.print(table)

    # Inspect Medallion Storage
    console.print("\n[bold]Medallion Lake Artifacts Generated:[/bold]")
    bronze_objs = storage_engine.list_objects("bronze/")
    silver_objs = storage_engine.list_objects("silver/")
    gold_objs = storage_engine.list_objects("gold/")
    quarantine_objs = storage_engine.list_objects("quarantine/")

    console.print(f"  [bold cyan]Bronze Lake:[/bold cyan] {len(bronze_objs)} parquet files")
    for b in bronze_objs[-2:]:
        console.print(f"    - {b}")

    console.print(f"  [bold silver]Silver Lake:[/bold silver] {len(silver_objs)} parquet files")
    for s in silver_objs[-2:]:
        console.print(f"    - {s}")

    console.print(f"  [bold yellow]Gold Mart Lake:[/bold yellow] {len(gold_objs)} parquet files")
    for g in gold_objs[-2:]:
        console.print(f"    - {g}")

    if quarantine_objs:
        console.print(f"  [bold red]Quarantine Storage:[/bold red] {len(quarantine_objs)} invalid record files")
        for q in quarantine_objs[-2:]:
            console.print(f"    - {q}")

    # Inspect Sample Warehouse Result
    console.print("\n[bold green]Previewing Gold Analytics Output:[/bold green]")
    final_output = summary.task_results.get("node_warehouse_load")
    if final_output and final_output.output_data:
        preview_tbl = Table(title="Gold Customer Spend Summary Table")
        cols = list(final_output.output_data[0].keys())
        for c in cols:
            preview_tbl.add_column(c, style="magenta")
        for row in final_output.output_data[:5]:
            preview_tbl.add_row(*[str(row.get(c, "")) for c in cols])
        console.print(preview_tbl)

    console.print(f"\n[bold green]Demo pipeline executed successfully in {elapsed:.2f} seconds![/bold green]\n")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
