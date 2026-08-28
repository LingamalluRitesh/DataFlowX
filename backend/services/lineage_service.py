"""
DataFlowX Data Lineage & Governance Service
Builds end-to-end data provenance graphs (Source -> Bronze -> Silver -> Gold -> Warehouse -> Analytics).
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import DataContract, EntityTag, LineageEdge, LineageNode, TagDefinition
from backend.schemas.lineage import DataContractCreate, LineageGraphOut, TagCreate


class LineageService:
    """End-to-end lineage tracking and graph construction."""

    @staticmethod
    async def get_lineage_graph(session: AsyncSession, workspace_id: Optional[str]) -> LineageGraphOut:
        nodes_stmt = select(LineageNode)
        edges_stmt = select(LineageEdge)

        if workspace_id:
            nodes_stmt = nodes_stmt.where(LineageNode.workspace_id == workspace_id)

        nodes = (await session.execute(nodes_stmt)).scalars().all()
        edges = (await session.execute(edges_stmt)).scalars().all()

        nodes_out = [
            {
                "id": n.id,
                "entity_type": n.entity_type,
                "entity_id": n.entity_id,
                "name": n.name,
                "layer": n.layer,
                "metadata": n.metadata_json or {}
            }
            for n in nodes
        ]

        edges_out = [
            {
                "id": e.id,
                "source_node_id": e.source_node_id,
                "target_node_id": e.target_node_id,
                "transformation_type": e.transformation_type,
                "pipeline_id": e.pipeline_id,
                "execution_id": e.execution_id,
                "column_mappings": e.column_mappings_json
            }
            for e in edges
        ]

        return LineageGraphOut(nodes=nodes_out, edges=edges_out)

    @staticmethod
    async def record_lineage_edge(
        session: AsyncSession,
        workspace_id: Optional[str],
        source_name: str,
        source_type: str,
        target_name: str,
        target_type: str,
        pipeline_id: Optional[str] = None,
        layer: Optional[str] = None
    ) -> LineageEdge:
        # Find or create source node
        src_node = (await session.execute(select(LineageNode).where(LineageNode.name == source_name))).scalar_one_or_none()
        if not src_node:
            src_node = LineageNode(
                workspace_id=workspace_id,
                name=source_name,
                entity_type=source_type,
                entity_id=source_name.lower().replace(" ", "_"),
                layer=layer
            )
            session.add(src_node)
            await session.flush()

        # Find or create target node
        tgt_node = (await session.execute(select(LineageNode).where(LineageNode.name == target_name))).scalar_one_or_none()
        if not tgt_node:
            tgt_node = LineageNode(
                workspace_id=workspace_id,
                name=target_name,
                entity_type=target_type,
                entity_id=target_name.lower().replace(" ", "_"),
                layer=layer
            )
            session.add(tgt_node)
            await session.flush()

        edge = LineageEdge(
            source_node_id=src_node.id,
            target_node_id=tgt_node.id,
            pipeline_id=pipeline_id,
            transformation_type="PIPELINE_FLOW"
        )
        session.add(edge)
        await session.commit()
        return edge

    @staticmethod
    async def create_data_contract(session: AsyncSession, workspace_id: Optional[str], payload: DataContractCreate) -> DataContract:
        contract = DataContract(
            workspace_id=workspace_id,
            name=payload.name,
            dataset_id=payload.dataset_id,
            schema_version_id=payload.schema_version_id,
            sla_freshness_hours=payload.sla_freshness_hours,
            min_quality_score=payload.min_quality_score,
            max_null_percentage=payload.max_null_percentage,
            owner_email=payload.owner_email,
            status="ACTIVE"
        )
        session.add(contract)
        await session.commit()
        await session.refresh(contract)
        return contract

    @staticmethod
    async def list_tags(session: AsyncSession, org_id: str) -> List[TagDefinition]:
        stmt = select(TagDefinition).where(TagDefinition.organization_id == org_id).order_by(TagDefinition.name)
        tags = (await session.execute(stmt)).scalars().all()
        return list(tags)

    @staticmethod
    async def create_tag(session: AsyncSession, org_id: str, payload: TagCreate) -> TagDefinition:
        tag = TagDefinition(
            organization_id=org_id,
            name=payload.name,
            color=payload.color,
            category=payload.category,
            description=payload.description
        )
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag
