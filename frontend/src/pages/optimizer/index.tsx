import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitFork, Activity, CheckCircle, Sparkles, Cpu, Layers } from 'lucide-react';

interface MemoGroupItem {
  group_id: number;
  equivalent_plans_count: number;
  best_operator: string;
  estimated_cpu_cost: number;
  estimated_io_cost: number;
  total_cost_score: number;
}

const mockGroups: MemoGroupItem[] = [
  { group_id: 0, equivalent_plans_count: 8, best_operator: 'HashJoin(customers, orders)', estimated_cpu_cost: 14.5, estimated_io_cost: 28.0, total_cost_score: 42.5 },
  { group_id: 1, equivalent_plans_count: 4, best_operator: 'ParquetVectorScan(orders)', estimated_cpu_cost: 4.2, estimated_io_cost: 18.5, total_cost_score: 22.7 },
  { group_id: 2, equivalent_plans_count: 2, best_operator: 'Filter(status = COMPLETED)', estimated_cpu_cost: 1.8, estimated_io_cost: 0.0, total_cost_score: 1.8 },
];

export default function CascadesOptimizerPage() {
  const columns: DataGridColumn<MemoGroupItem>[] = [
    {
      key: 'group_id',
      header: 'Memo Group ID',
      render: (g) => <span className="font-mono text-cyan-400 font-bold">Group {g.group_id}</span>,
    },
    { key: 'equivalent_plans_count', header: 'Equivalent Expressions Explored', render: (g) => <span className="font-mono text-slate-300">{g.equivalent_plans_count} plans</span> },
    { key: 'best_operator', header: 'Minimum Cost Physical Operator', render: (g) => <strong className="text-white font-mono">{g.best_operator}</strong> },
    { key: 'estimated_cpu_cost', header: 'CPU Cost', render: (g) => <span className="font-mono text-slate-400">{g.estimated_cpu_cost}</span> },
    { key: 'estimated_io_cost', header: 'Disk I/O Cost', render: (g) => <span className="font-mono text-slate-400">{g.estimated_io_cost}</span> },
    {
      key: 'total_cost_score',
      header: 'Estimated Total Cost',
      render: (g) => <span className="font-mono text-emerald-400 font-bold">{g.total_cost_score} units</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Cascades Query Optimizer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitFork className="w-7 h-7 text-cyan-400" />
            Cascades Top-Down Cost-Based Query Optimizer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Top-down memo structure exploration, algebraic equivalence transformations, and branch-and-bound plan pruning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Explored Memo Groups</div>
            <div className="text-2xl font-bold text-white mt-1">3 Groups</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Search Space Reduction</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">94.2% Pruned</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Best Plan Estimated Cost</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">42.50 Cost Units</div>
          </div>
        </div>

        <DataGrid data={mockGroups} columns={columns} title="Cascades Memo Groups & Physical Choices" />
      </div>
    </MainLayout>
  );
}
