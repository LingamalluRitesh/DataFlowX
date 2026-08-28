import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Network, Database, Layers, ArrowRight, Play, CheckCircle, Sparkles } from 'lucide-react';

interface VirtualFederatedTable {
  virtual_name: string;
  source_type: string;
  physical_table: string;
  pushdown_enabled: boolean;
  cache_ttl_seconds: number;
}

const mockFederatedTables: VirtualFederatedTable[] = [
  { virtual_name: 'v_customer_invoices', source_type: 'POSTGRES', physical_table: 'production_db.public.orders', pushdown_enabled: true, cache_ttl_seconds: 300 },
  { virtual_name: 'v_enterprise_accounts', source_type: 'SNOWFLAKE', physical_table: 'ANALYTICS_DB.PUBLIC.DIM_ACCOUNTS', pushdown_enabled: true, cache_ttl_seconds: 1800 },
  { virtual_name: 'v_raw_telemetry', source_type: 'S3_DELTA', physical_table: 's3://lakehouse/bronze/iot_telemetry', pushdown_enabled: true, cache_ttl_seconds: 60 },
];

export default function FederationStudioPage() {
  const columns: DataGridColumn<VirtualFederatedTable>[] = [
    {
      key: 'virtual_name',
      header: 'Virtual Table Name',
      render: (t) => (
        <div className="flex items-center gap-2">
          <Network className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{t.virtual_name}</strong>
        </div>
      ),
    },
    {
      key: 'source_type',
      header: 'Underlying Connector',
      render: (t) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{t.source_type}</span>,
    },
    { key: 'physical_table', header: 'Physical Remote Path', render: (t) => <span className="font-mono text-slate-300 text-xs">{t.physical_table}</span> },
    {
      key: 'pushdown_enabled',
      header: 'Predicate Pushdown',
      render: (t) => (
        <span className="text-emerald-400 font-semibold text-xs flex items-center gap-1">
          <CheckCircle className="w-3.5 h-3.5" /> Filter & Agg Pushdown Active
        </span>
      ),
    },
    { key: 'cache_ttl_seconds', header: 'Cache TTL', render: (t) => <span className="font-mono text-slate-400">{t.cache_ttl_seconds}s</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Query Federation & Virtual Data Lake — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Network className="w-7 h-7 text-cyan-400" />
            Query Federation & Virtual Data Lake Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Execute distributed joins across PostgreSQL, Snowflake, BigQuery, and S3 Parquet/Delta Lake tables without moving raw data.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Virtual Federated Tables</div>
            <div className="text-2xl font-bold text-white mt-1">3 Tables</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pushdown Efficiency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">98.5% Pushdown</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Network Transfer Saved</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">4.2 TB (30d)</div>
          </div>
        </div>

        <DataGrid data={mockFederatedTables} columns={columns} title="Active Virtual Federated Mappings" />
      </div>
    </MainLayout>
  );
}
