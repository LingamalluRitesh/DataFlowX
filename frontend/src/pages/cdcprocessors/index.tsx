import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { RefreshCw, Database, Activity, CheckCircle, Flame, Layers } from 'lucide-react';

interface CDCProcessorItem {
  id: string;
  source_engine: 'POSTGRESQL_WAL' | 'MYSQL_BINLOG' | 'MONGODB_OPLOG';
  table_stream: string;
  lsn_committed: number;
  ops_per_second: number;
  auto_ddl_evolutions_applied: number;
  status: 'STREAMING' | 'PAUSED';
}

const mockProcessors: CDCProcessorItem[] = [
  { id: 'cdc_pg_01', source_engine: 'POSTGRESQL_WAL', table_stream: 'public.customers', lsn_committed: 89410291, ops_per_second: 1850, auto_ddl_evolutions_applied: 2, status: 'STREAMING' },
  { id: 'cdc_my_02', source_engine: 'MYSQL_BINLOG', table_stream: 'ecommerce.orders', lsn_committed: 10485760, ops_per_second: 4200, auto_ddl_evolutions_applied: 0, status: 'STREAMING' },
  { id: 'cdc_mg_03', source_engine: 'MONGODB_OPLOG', table_stream: 'rs0.device_events', lsn_committed: 17248891, ops_per_second: 3100, auto_ddl_evolutions_applied: 4, status: 'STREAMING' },
];

export default function CDCProcessorsPage() {
  const columns: DataGridColumn<CDCProcessorItem>[] = [
    {
      key: 'table_stream',
      header: 'Source CDC Stream',
      render: (c) => (
        <div>
          <strong className="text-white font-mono text-xs">{c.table_stream}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{c.id}</div>
        </div>
      ),
    },
    {
      key: 'source_engine',
      header: 'CDC Engine',
      render: (c) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{c.source_engine}</span>,
    },
    { key: 'lsn_committed', header: 'Committed LSN / Pos', render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.lsn_committed.toLocaleString()}</span> },
    { key: 'ops_per_second', header: 'Ingestion Throughput', render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.ops_per_second.toLocaleString()} ops/s</span> },
    {
      key: 'auto_ddl_evolutions_applied',
      header: 'Auto Schema DDLs',
      render: (c) => (
        <span className="font-mono text-xs text-slate-300">
          +{c.auto_ddl_evolutions_applied} columns evolved
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Debezium CDC Stream Processors — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <RefreshCw className="w-7 h-7 text-cyan-400" />
            Debezium CDC Envelope Processors & Schema Evolution
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time change data capture extraction for PostgreSQL WAL, MySQL Binlog, and MongoDB Oplog streams with automated schema evolution.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Change Stream Ingress</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">9,150 ops/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active CDC Connectors</div>
            <div className="text-2xl font-bold text-white mt-1">3 Connectors</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Automatic DDL Evolutions</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">6 Alterations Synced</div>
          </div>
        </div>

        <DataGrid data={mockProcessors} columns={columns} title="Active Change Data Capture Stream Processors" />
      </div>
    </MainLayout>
  );
}
