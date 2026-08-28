import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Tag, GitBranch, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface RefItem {
  ref_name: string;
  table_name: string;
  ref_type: 'BRANCH' | 'TAG';
  target_snapshot_id: string;
  retention_policy: string;
  created_at: string;
}

const mockRefs: RefItem[] = [
  { ref_name: 'main', table_name: 'gold.fact_orders', ref_type: 'BRANCH', target_snapshot_id: '#89124912093812', retention_policy: 'Infinite (Primary Branch)', created_at: '2026-08-28 00:00 UTC' },
  { ref_name: 'q3_2026_financial_audit', table_name: 'gold.fact_orders', ref_type: 'TAG', target_snapshot_id: '#89124912093810', retention_policy: 'Immutable (Retain 7 Years)', created_at: '2026-08-28 23:55 UTC' },
  { ref_name: 'feature-ml-v4', table_name: 'gold.fact_orders', ref_type: 'BRANCH', target_snapshot_id: '#89124912093999', retention_policy: 'TTL 30 Days', created_at: '2026-08-29 00:20 UTC' },
];

export default function BranchTagsStudioPage() {
  const columns: DataGridColumn<RefItem>[] = [
    {
      key: 'ref_name',
      header: 'Reference Name',
      render: (r) => (
        <div className="flex items-center gap-2">
          {r.ref_type === 'BRANCH' ? <GitBranch className="w-4 h-4 text-purple-400" /> : <Tag className="w-4 h-4 text-cyan-400" />}
          <strong className="text-white font-mono text-xs">{r.ref_name}</strong>
        </div>
      ),
    },
    { key: 'table_name', header: 'Target Table', render: (r) => <span className="font-mono text-slate-300 text-xs">{r.table_name}</span> },
    {
      key: 'ref_type',
      header: 'Reference Type',
      render: (r) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            r.ref_type === 'BRANCH'
              ? 'bg-purple-950 text-purple-300 border border-purple-800'
              : 'bg-cyan-950 text-cyan-300 border border-cyan-800'
          }`}
        >
          {r.ref_type}
        </span>
      ),
    },
    { key: 'target_snapshot_id', header: 'Target Snapshot', render: (r) => <span className="font-mono text-cyan-300 text-xs">{r.target_snapshot_id}</span> },
    { key: 'retention_policy', header: 'Retention Policy', render: (r) => <span className="text-slate-300 text-xs">{r.retention_policy}</span> },
    { key: 'created_at', header: 'Creation Time', render: (r) => <span className="font-mono text-slate-400 text-xs">{r.created_at}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Named Branches & Audit Tags — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitBranch className="w-7 h-7 text-cyan-400" />
            Git-Style Lakehouse Named Branches & Immutable Audit Tags
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy branching for isolated pipeline experimentation (WAP pattern) and regulatory immutable snapshot tagging.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Table References</div>
            <div className="text-2xl font-bold text-white mt-1">3 References</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Branch Isolation Cost</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">$0.00 (Zero Storage Copy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Write-Audit-Publish (WAP)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Enabled</div>
          </div>
        </div>

        <DataGrid data={mockRefs} columns={columns} title="Managed Table Branches & Tags" />
      </div>
    </MainLayout>
  );
}
