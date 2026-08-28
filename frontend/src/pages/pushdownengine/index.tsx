import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ArrowDownRight, Layers, CheckCircle, Database, Sparkles, Filter } from 'lucide-react';

interface PushdownQueryItem {
  query_id: string;
  source_table: string;
  target_engine: string;
  pushed_predicates: string[];
  residual_predicates: string[];
  bytes_scanned_reduction_pct: number;
}

const mockPushdowns: PushdownQueryItem[] = [
  { query_id: 'push_01', source_table: 'enterprise.financials.snowflake_orders', target_engine: 'Snowflake', pushed_predicates: ["order_date >= '2026-01-01'", "status = 'COMPLETED'"], residual_predicates: ["REGEXP_LIKE(notes, 'urgent')"], bytes_scanned_reduction_pct: 92.4 },
  { query_id: 'push_02', source_table: 'enterprise.analytics.bigquery_events', target_engine: 'BigQuery', pushed_predicates: ["event_type = 'CHECKOUT'", "amount > 100"], residual_predicates: [], bytes_scanned_reduction_pct: 98.1 },
  { query_id: 'push_03', source_table: 'enterprise.lakehouse.s3_telemetry', target_engine: 'Iceberg (S3)', pushed_predicates: ["device_category = 'GATEWAY'"], residual_predicates: [], bytes_scanned_reduction_pct: 88.5 },
];

export default function PushdownEnginePage() {
  const columns: DataGridColumn<PushdownQueryItem>[] = [
    {
      key: 'source_table',
      header: 'Federated Target Table',
      render: (p) => (
        <div>
          <strong className="text-white font-mono text-xs">{p.source_table}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{p.query_id}</div>
        </div>
      ),
    },
    { key: 'target_engine', header: 'Remote Storage Engine', render: (p) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{p.target_engine}</span> },
    {
      key: 'pushed_predicates',
      header: 'Predicates Pushed Down (Remote Execution)',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.pushed_predicates.map((f) => (
            <span key={f} className="bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {f}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'residual_predicates',
      header: 'Residual Local Filters',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.residual_predicates.length > 0 ? (
            p.residual_predicates.map((r) => (
              <span key={r} className="bg-slate-800 text-slate-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
                {r}
              </span>
            ))
          ) : (
            <span className="text-slate-500 text-[10px] italic">None (100% Pushed)</span>
          )}
        </div>
      ),
    },
    {
      key: 'bytes_scanned_reduction_pct',
      header: 'I/O Bytes Pruned',
      render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.bytes_scanned_reduction_pct}% Pruned</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Predicate & Projection Pushdown — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ArrowDownRight className="w-7 h-7 text-cyan-400" />
            Query Predicate & Column Projection Pushdown Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AST filter analysis pushing WHERE predicates directly into remote Snowflake, BigQuery, and Iceberg storage layers to eliminate network I/O.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Network I/O Reduction</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">93.0% Network Bandwidth Saved</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pushdown Optimization Speed</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">&lt;0.1 ms / AST</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Remote Engine Pushdown Compliance</div>
            <div className="text-2xl font-bold text-white mt-1">100% ANSI Standard</div>
          </div>
        </div>

        <DataGrid data={mockPushdowns} columns={columns} title="Active Query Pushdown Execution Plans" />
      </div>
    </MainLayout>
  );
}
