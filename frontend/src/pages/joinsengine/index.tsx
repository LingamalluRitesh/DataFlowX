import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitMerge, Layers, Cpu, CheckCircle, Flame, ArrowRight } from 'lucide-react';

interface JoinStrategyItem {
  strategy_name: string;
  algorithm: 'BROADCAST_HASH_JOIN' | 'SORT_MERGE_JOIN' | 'SHUFFLE_HASH_JOIN' | 'ASOF_TIME_JOIN';
  left_table_size: string;
  right_table_size: string;
  join_throughput: string;
  spill_to_disk: boolean;
  recommended_workload: string;
}

const mockJoins: JoinStrategyItem[] = [
  { strategy_name: 'Fact Orders x Dim Customers', algorithm: 'BROADCAST_HASH_JOIN', left_table_size: '10,000,000 Rows (Fact)', right_table_size: '50,000 Rows (Dim)', join_throughput: '3,800,000 rows/sec', spill_to_disk: false, recommended_workload: 'Small Dimension Broadcast (<100MB)' },
  { strategy_name: 'Ad Impressions x Click Events', algorithm: 'SORT_MERGE_JOIN', left_table_size: '50,000,000 Rows', right_table_size: '40,000,000 Rows', join_throughput: '1,950,000 rows/sec', spill_to_disk: false, recommended_workload: 'Large-scale Out-of-Core Tables' },
  { strategy_name: 'Equity Trades x BBO Quotes', algorithm: 'ASOF_TIME_JOIN', left_table_size: '5,000,000 Trades', right_table_size: '20,000,000 Quotes', join_throughput: '4,200,000 rows/sec', spill_to_disk: false, recommended_workload: 'Time-Series Temporal Alignment' },
];

export default function JoinsEnginePage() {
  const columns: DataGridColumn<JoinStrategyItem>[] = [
    { key: 'strategy_name', header: 'Physical Join Plan', render: (j) => <strong className="text-white font-mono text-xs">{j.strategy_name}</strong> },
    {
      key: 'algorithm',
      header: 'Join Algorithm',
      render: (j) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{j.algorithm}</span>,
    },
    { key: 'left_table_size', header: 'Probe / Left Input', render: (j) => <span className="font-mono text-slate-300 text-xs">{j.left_table_size}</span> },
    { key: 'right_table_size', header: 'Build / Right Input', render: (j) => <span className="font-mono text-slate-300 text-xs">{j.right_table_size}</span> },
    {
      key: 'join_throughput',
      header: 'Join Throughput',
      render: (j) => <span className="font-mono text-emerald-400 font-bold">{j.join_throughput}</span>,
    },
    {
      key: 'spill_to_disk',
      header: 'Memory Spill',
      render: (j) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            j.spill_to_disk ? 'bg-amber-950 text-amber-400' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
          }`}
        >
          {j.spill_to_disk ? 'SPILL TO DISK' : 'PURE IN-MEMORY'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Join Engine & Cost Optimizer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitMerge className="w-7 h-7 text-cyan-400" />
            Vectorized Physical Join Engine & Memory Optimizers
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Broadcast hash joins, out-of-core sort-merge joins, and temporal as-of joins optimized for high-throughput Lakehouse pipelines.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Join Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4.2M rows / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Hash Collision Factor</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">&lt;0.01% Collisions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Dynamic Broadcast Threshold</div>
            <div className="text-2xl font-bold text-white mt-1">128 MB (Configurable)</div>
          </div>
        </div>

        <DataGrid data={mockJoins} columns={columns} title="Active Physical Join Execution Plans" />
      </div>
    </MainLayout>
  );
}
