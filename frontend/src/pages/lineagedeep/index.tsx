import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitCommit, Network, AlertOctagon, CheckCircle, Search, Layers } from 'lucide-react';

interface ColumnLineageEntry {
  source_col: string;
  target_col: string;
  transformation: string;
  blast_radius_score: number;
}

const mockColumnLineage: ColumnLineageEntry[] = [
  { source_col: 'bronze.raw_orders.cust_id', target_col: 'gold.fact_orders.customer_id', transformation: 'DIRECT (Identity)', blast_radius_score: 4.5 },
  { source_col: 'bronze.raw_orders.subtotal_cents', target_col: 'gold.fact_orders.total_usd', transformation: 'EXPRESSION (/ 100.0)', blast_radius_score: 8.0 },
  { source_col: 'bronze.raw_orders.order_date', target_col: 'gold.fact_orders.order_quarter', transformation: 'TEMPORAL (Quarter)', blast_radius_score: 3.2 },
];

export default function DeepColumnLineagePage() {
  const columns: DataGridColumn<ColumnLineageEntry>[] = [
    { key: 'source_col', header: 'Source Origin Column', render: (c) => <span className="font-mono text-cyan-400 font-semibold">{c.source_col}</span> },
    { key: 'target_col', header: 'Target Downstream Column', render: (c) => <strong className="text-white font-mono">{c.target_col}</strong> },
    { key: 'transformation', header: 'Transformation Function', render: (c) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.transformation}</span> },
    {
      key: 'blast_radius_score',
      header: 'Blast Radius Risk',
      render: (c) => (
        <span className="font-mono text-amber-400 font-bold">
          Score: {c.blast_radius_score}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Deep Column-Level Lineage — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitCommit className="w-7 h-7 text-cyan-400" />
            Deep Column-Level Lineage & SQL CTE Parser
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Fine-grained column transformation mappings, blast radius impact scoring, and root-cause tracing across SQL queries.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tracked Column Edges</div>
            <div className="text-2xl font-bold text-white mt-1">142 Edges</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Blast Radius</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">5.2 Impact Units</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">OpenLineage Standard</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Conforming</div>
          </div>
        </div>

        <DataGrid data={mockColumnLineage} columns={columns} title="Column-Level Dependency Graph" />
      </div>
    </MainLayout>
  );
}
