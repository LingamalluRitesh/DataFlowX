import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Globe, Database, CheckCircle, Sparkles, Layers, ArrowRight } from 'lucide-react';

interface FederatedTableItem {
  virtual_table: string;
  underlying_engine: string;
  native_location: string;
  column_count: number;
  pushdown_supported: boolean;
  cache_status: 'HOT' | 'WARM' | 'DIRECT';
}

const mockFedTables: FederatedTableItem[] = [
  { virtual_table: 'enterprise.financials.snowflake_orders', underlying_engine: 'Snowflake Data Cloud', native_location: 'SNOWFLAKE.PROD_DB.PUBLIC.ORDERS', column_count: 24, pushdown_supported: true, cache_status: 'HOT' },
  { virtual_table: 'enterprise.analytics.bigquery_events', underlying_engine: 'Google BigQuery', native_location: 'gcp-project.analytics.raw_events', column_count: 42, pushdown_supported: true, cache_status: 'HOT' },
  { virtual_table: 'enterprise.core.postgres_users', underlying_engine: 'Amazon RDS PostgreSQL', native_location: 'postgres.production.users', column_count: 18, pushdown_supported: true, cache_status: 'WARM' },
  { virtual_table: 'enterprise.lakehouse.s3_telemetry', underlying_engine: 'Apache Iceberg (S3)', native_location: 's3://lakehouse/bronze/telemetry/', column_count: 36, pushdown_supported: true, cache_status: 'HOT' },
];

export default function VirtualLakehousePage() {
  const columns: DataGridColumn<FederatedTableItem>[] = [
    { key: 'virtual_table', header: 'Virtual Lakehouse Namespace', render: (v) => <strong className="text-white font-mono text-xs">{v.virtual_table}</strong> },
    {
      key: 'underlying_engine',
      header: 'Backing Database Source',
      render: (v) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{v.underlying_engine}</span>,
    },
    { key: 'native_location', header: 'Remote Physical Target', render: (v) => <span className="font-mono text-slate-300 text-xs">{v.native_location}</span> },
    { key: 'column_count', header: 'Columns', render: (v) => <span className="font-mono text-slate-300">{v.column_count} cols</span> },
    {
      key: 'pushdown_supported',
      header: 'Predicate Pushdown',
      render: (v) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          FULL PUSHDOWN
        </span>
      ),
    },
    {
      key: 'cache_status',
      header: 'SLRU Query Cache',
      render: (v) => <span className="font-mono text-cyan-300 font-bold">{v.cache_status}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Virtual Lakehouse Query Federation — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Globe className="w-7 h-7 text-cyan-400" />
            Virtual Lakehouse & Multi-Source Query Federation
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy virtual data federation executing ANSI SQL queries seamlessly across Snowflake, BigQuery, PostgreSQL, and Iceberg.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Federated Data Sources</div>
            <div className="text-2xl font-bold text-white mt-1">4 Cloud Engines</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Virtual Catalog Tables</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4 Virtual Tables</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pushdown Optimization Ratio</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">94.2% Filters Pushed</div>
          </div>
        </div>

        <DataGrid data={mockFedTables} columns={columns} title="Unified Virtual Catalog Namespace" />
      </div>
    </MainLayout>
  );
}
