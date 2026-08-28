import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitBranch, GitMerge, Tag, CheckCircle, Plus, Layers } from 'lucide-react';

interface TableBranchItem {
  branch_name: string;
  table_name: string;
  base_snapshot_id: number;
  head_snapshot_id: number;
  commits_ahead: number;
  created_at: string;
  is_default: boolean;
}

const mockBranches: TableBranchItem[] = [
  { branch_name: 'main', table_name: 'gold.fact_orders', base_snapshot_id: 1, head_snapshot_id: 42, commits_ahead: 0, created_at: '30 days ago', is_default: true },
  { branch_name: 'feature/q4_tax_adjustments', table_name: 'gold.fact_orders', base_snapshot_id: 40, head_snapshot_id: 43, commits_ahead: 3, created_at: '2 hours ago', is_default: false },
  { branch_name: 'sandbox/ml_feature_backfill', table_name: 'gold.fact_orders', base_snapshot_id: 42, head_snapshot_id: 45, commits_ahead: 2, created_at: '1 day ago', is_default: false },
];

export default function TableBranchesPage() {
  const columns: DataGridColumn<TableBranchItem>[] = [
    {
      key: 'branch_name',
      header: 'Lakehouse Snapshot Branch',
      render: (b) => (
        <div className="flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{b.branch_name}</strong>
          {b.is_default && (
            <span className="bg-cyan-950 text-cyan-400 border border-cyan-800 text-[9px] font-bold px-1.5 py-0.2 rounded">
              DEFAULT
            </span>
          )}
        </div>
      ),
    },
    { key: 'table_name', header: 'Target Table', render: (b) => <span className="font-mono text-slate-300 text-xs">{b.table_name}</span> },
    { key: 'base_snapshot_id', header: 'Base Snapshot', render: (b) => <span className="font-mono text-slate-400">snap_{b.base_snapshot_id}</span> },
    { key: 'head_snapshot_id', header: 'Head Snapshot', render: (b) => <span className="font-mono text-purple-300 font-bold">snap_{b.head_snapshot_id}</span> },
    {
      key: 'commits_ahead',
      header: 'Commits Ahead',
      render: (b) => <span className="font-mono text-emerald-400 font-bold">+{b.commits_ahead} commits</span>,
    },
    { key: 'created_at', header: 'Created' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Lakehouse Snapshot Branching — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <GitBranch className="w-7 h-7 text-cyan-400" />
              Lakehouse Snapshot Branching & Git-like Data Isolation
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Zero-copy table branching for safe feature engineering, backfill experimentation, and audit tags.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Create Snapshot Branch
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Table Branches</div>
            <div className="text-2xl font-bold text-white mt-1">3 Branches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Isolation Storage Cost</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">$0.00 (Metadata Pointers)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Merge Safety Check</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Fast-Forward Ready</div>
          </div>
        </div>

        <DataGrid data={mockBranches} columns={columns} title="Lakehouse Branches & Isolated Heads" />
      </div>
    </MainLayout>
  );
}
