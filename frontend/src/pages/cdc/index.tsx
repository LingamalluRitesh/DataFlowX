import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { RefreshCw, Database, Activity, Zap, Play, Pause, Layers } from 'lucide-react';

interface CDCStreamItem {
  id: string;
  source_db: string;
  table_name: string;
  change_rate_per_min: number;
  last_lsn_offset: string;
  lag_ms: number;
  status: 'STREAMING' | 'SYNCING' | 'PAUSED';
}

const mockCdcStreams: CDCStreamItem[] = [
  { id: 'cdc_pg_orders', source_db: 'Postgres (Production OLTP)', table_name: 'public.orders', change_rate_per_min: 1450, last_lsn_offset: '0/16B2D40', lag_ms: 120, status: 'STREAMING' },
  { id: 'cdc_mysql_users', source_db: 'MySQL (Auth Cluster)', table_name: 'auth.users', change_rate_per_min: 320, last_lsn_offset: 'mysql-bin.000412:4592', lag_ms: 85, status: 'STREAMING' },
  { id: 'cdc_oracle_inventory', source_db: 'Oracle 19c (Warehouse ERP)', table_name: 'INVENTORY.STOCK', change_rate_per_min: 890, last_lsn_offset: 'SCN:94820194', lag_ms: 240, status: 'STREAMING' },
];

export default function CDCIndexPage() {
  const columns: DataGridColumn<CDCStreamItem>[] = [
    {
      key: 'table_name',
      header: 'CDC Replication Table',
      render: (c) => (
        <div>
          <strong className="text-white font-mono">{c.table_name}</strong>
          <div className="text-[10px] text-slate-500">{c.source_db}</div>
        </div>
      ),
    },
    {
      key: 'change_rate_per_min',
      header: 'Mutation Velocity',
      render: (c) => <span className="font-mono text-cyan-400 font-bold">{c.change_rate_per_min.toLocaleString()} ops/min</span>,
    },
    {
      key: 'last_lsn_offset',
      header: 'Last WAL / LSN Offset',
      render: (c) => <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300 text-xs">{c.last_lsn_offset}</span>,
    },
    {
      key: 'lag_ms',
      header: 'Replication Lag',
      render: (c) => (
        <span className={`font-mono font-semibold ${c.lag_ms < 200 ? 'text-emerald-400' : 'text-amber-400'}`}>
          {c.lag_ms} ms
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold animate-pulse">
          {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Change Data Capture (CDC) Streams — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <RefreshCw className="w-7 h-7 text-cyan-400 animate-spin" />
            Change Data Capture (CDC) Real-Time Streams
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Low-latency WAL / binlog streaming replication into Bronze Delta & Iceberg lakehouses powered by Debezium decoders.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active WAL Stream Connectors</div>
            <div className="text-2xl font-bold text-white mt-1">3 Connectors</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average End-to-End Lag</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">148 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Mutated Records (24h)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">3,830,400</div>
          </div>
        </div>

        <DataGrid data={mockCdcStreams} columns={columns} title="Active Change Data Capture Streams" />
      </div>
    </MainLayout>
  );
}
