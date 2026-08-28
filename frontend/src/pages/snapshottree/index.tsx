import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitFork, GitBranch, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface SnapshotNodeItem {
  snapshot_id: string;
  parent_snapshot_id: string;
  branch_tag: string;
  timestamp: string;
  summary_action: string;
  is_current_head: boolean;
}

const mockSnapshotTree: SnapshotNodeItem[] = [
  { snapshot_id: '#89124912093812', parent_snapshot_id: '#89124912093811', branch_tag: 'main', timestamp: '2026-08-29 00:23:50 UTC', summary_action: 'APPEND (4 files)', is_current_head: true },
  { snapshot_id: '#89124912093811', parent_snapshot_id: '#89124912093810', branch_tag: 'main', timestamp: '2026-08-29 00:18:12 UTC', summary_action: 'OVERWRITE (8 files)', is_current_head: false },
  { snapshot_id: '#89124912093810', parent_snapshot_id: 'None (Root)', branch_tag: 'main', timestamp: '2026-08-28 23:55:00 UTC', summary_action: 'CREATE TABLE (32 files)', is_current_head: false },
  { snapshot_id: '#89124912093999', parent_snapshot_id: '#89124912093811', branch_tag: 'feature-experiment-ml', timestamp: '2026-08-29 00:20:00 UTC', summary_action: 'APPEND (2 files)', is_current_head: false },
];

export default function SnapshotTreePage() {
  const columns: DataGridColumn<SnapshotNodeItem>[] = [
    {
      key: 'snapshot_id',
      header: 'Snapshot ID',
      render: (s) => (
        <div className="flex items-center gap-2">
          <GitFork className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.snapshot_id}</strong>
        </div>
      ),
    },
    { key: 'parent_snapshot_id', header: 'Parent Snapshot ID', render: (s) => <span className="font-mono text-slate-400 text-xs">{s.parent_snapshot_id}</span> },
    {
      key: 'branch_tag',
      header: 'Branch / Tag Name',
      render: (s) => (
        <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded flex items-center gap-1 w-fit font-bold">
          <GitBranch className="w-3 h-3 text-purple-400" /> {s.branch_tag}
        </span>
      ),
    },
    { key: 'timestamp', header: 'Snapshot Timestamp', render: (s) => <span className="font-mono text-slate-300 text-xs">{s.timestamp}</span> },
    { key: 'summary_action', header: 'Snapshot Action', render: (s) => <span className="text-slate-300 text-xs">{s.summary_action}</span> },
    {
      key: 'is_current_head',
      header: 'Branch Head',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.is_current_head
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {s.is_current_head ? 'CURRENT HEAD' : 'ANCESTOR'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Snapshot Ancestry & Branch DAG Explorer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitFork className="w-7 h-7 text-cyan-400" />
            Lakehouse Snapshot Ancestry & Branch Tree DAG Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Visual tree explorer tracking snapshot lineage, named branches (`main`, `experiment`), and historical time-travel tags.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Snapshot Nodes</div>
            <div className="text-2xl font-bold text-white mt-1">4 Snapshots</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Named Lakehouse Branches</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">2 Active Branches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Branch Isolation Guarantee</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Copy-On-Write Zero Overhead</div>
          </div>
        </div>

        <DataGrid data={mockSnapshotTree} columns={columns} title="Lakehouse Snapshot Ancestry DAG" />
      </div>
    </MainLayout>
  );
}
