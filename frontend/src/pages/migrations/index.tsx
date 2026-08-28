import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitPullRequest, Database, ArrowRight, CheckCircle, Code, Plus, Sparkles } from 'lucide-react';

interface MigrationItem {
  version: string;
  table_name: string;
  description: string;
  checksum: string;
  applied_at: string;
  status: 'APPLIED' | 'PENDING' | 'ROLLED_BACK';
}

const mockMigrations: MigrationItem[] = [
  { version: 'v20260828_01', table_name: 'gold.fact_orders', description: 'Add loyalty_points_earned and tax_rate_applied columns', checksum: 'a8f9c1b4...', applied_at: '10 mins ago', status: 'APPLIED' },
  { version: 'v20260828_02', table_name: 'silver.dim_customers', description: 'Widen email_hash VARCHAR to VARCHAR(128)', checksum: '3e7b89d2...', applied_at: '1 hour ago', status: 'APPLIED' },
  { version: 'v20260827_01', table_name: 'bronze.raw_transactions', description: 'Add metadata JSONB column for webhook event headers', checksum: 'd14a908f...', applied_at: '1 day ago', status: 'APPLIED' },
];

export default function MigrationsIndexPage() {
  const columns: DataGridColumn<MigrationItem>[] = [
    {
      key: 'version',
      header: 'Migration Version',
      render: (m) => (
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{m.version}</strong>
        </div>
      ),
    },
    { key: 'table_name', header: 'Target Table', render: (m) => <span className="font-mono text-cyan-300 font-semibold">{m.table_name}</span> },
    { key: 'description', header: 'Change Summary', sortable: false },
    { key: 'checksum', header: 'SHA-256 Checksum', render: (m) => <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-400 text-xs">{m.checksum}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {m.status}
        </span>
      ),
    },
    { key: 'applied_at', header: 'Timestamp' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Lakehouse DDL Migrations — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <GitPullRequest className="w-7 h-7 text-cyan-400" />
              Automated Lakehouse DDL Migrations & Schema Evolution
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Forward and rollback migration scripts with automated structural diffing, breaking change detection, and checksum verification.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Sparkles className="w-4 h-4" /> Compare & Generate Migration
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Applied Migrations</div>
            <div className="text-2xl font-bold text-white mt-1">24 Versions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Backward Compatibility</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Compatible</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pending Schema Diffs</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0 Pending</div>
          </div>
        </div>

        <DataGrid data={mockMigrations} columns={columns} title="Applied Schema Migrations" />
      </div>
    </MainLayout>
  );
}
