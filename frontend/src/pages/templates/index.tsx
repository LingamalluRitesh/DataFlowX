import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Copy, FileCode, CheckCircle, Sparkles, Layers, ArrowRight } from 'lucide-react';

interface PipelineTemplateItem {
  id: string;
  name: string;
  category: 'SCD_TYPE_2' | 'CDC_UPSERT' | 'DAILY_SNAPSHOT' | 'OLAP_ROLLUP';
  description: string;
  target_engine: string;
}

const mockTemplates: PipelineTemplateItem[] = [
  { id: 'tmpl_scd2', name: 'Slowly Changing Dimension Type 2 (SCD2)', category: 'SCD_TYPE_2', description: 'Tracks historical dimension record revisions with effective/end dates and current row flag.', target_engine: 'Delta Lake / Iceberg' },
  { id: 'tmpl_cdc_merge', name: 'Idempotent Debezium CDC Log Merge', category: 'CDC_UPSERT', description: 'Handles high-frequency WAL inserts, updates, and hard deletes with partition deduplication.', target_engine: 'Snowflake / BigQuery' },
  { id: 'tmpl_snapshot', name: 'Partitioned Periodic Table Snapshot', category: 'DAILY_SNAPSHOT', description: 'Generates point-in-time daily historical snapshots with atomic partition overwrites.', target_engine: 'Parquet S3 / GCS' },
  { id: 'tmpl_rollup', name: 'Multi-Tier OLAP Rollup & Aggregation Cube', category: 'OLAP_ROLLUP', description: 'Generates daily, monthly, and yearly OLAP summary rollups with GROUPING SETS.', target_engine: 'DuckDB / ClickHouse' },
];

export default function PipelineTemplatesPage() {
  const columns: DataGridColumn<PipelineTemplateItem>[] = [
    {
      key: 'name',
      header: 'Pipeline Recipe Name',
      render: (t) => (
        <div className="flex items-center gap-2">
          <FileCode className="w-4 h-4 text-cyan-400" />
          <strong className="text-white">{t.name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Pattern Category',
      render: (t) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{t.category}</span>,
    },
    { key: 'target_engine', header: 'Supported Lakehouse Engines', render: (t) => <span className="font-mono text-cyan-300 text-xs">{t.target_engine}</span> },
    { key: 'description', header: 'Pattern Overview', sortable: false },
    {
      key: 'id',
      header: 'Action',
      render: (t) => (
        <button className="flex items-center gap-1 px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          <Copy className="w-3 h-3" /> Instantiate
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Enterprise Pipeline Templates & Recipes — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileCode className="w-7 h-7 text-cyan-400" />
            Enterprise Pipeline Templates & Recipe Generators
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Production-grade pipeline recipes: SCD Type 2 dimension tracking, idempotent CDC merges, periodic snapshots, and OLAP rollups.
          </p>
        </div>

        <DataGrid data={mockTemplates} columns={columns} title="Standard Enterprise Pipeline Templates" />
      </div>
    </MainLayout>
  );
}
