import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitCompare, Code, AlertTriangle, CheckCircle, FileCode, ArrowRight } from 'lucide-react';

interface SchemaDiffItem {
  table_name: string;
  source_version: string;
  target_version: string;
  added_columns: string[];
  dropped_columns: string[];
  breaking_change: boolean;
  generated_migration_up: string;
}

const mockDiffs: SchemaDiffItem[] = [
  { table_name: 'gold.fact_orders', source_version: 'v2', target_version: 'v3', added_columns: ['tax_amount (DOUBLE)', 'discount_code (STRING)'], dropped_columns: [], breaking_change: false, generated_migration_up: 'ALTER TABLE gold.fact_orders ADD COLUMN tax_amount DOUBLE; ALTER TABLE gold.fact_orders ADD COLUMN discount_code STRING;' },
  { table_name: 'silver.dim_customers', source_version: 'v1', target_version: 'v2', added_columns: ['loyalty_tier (STRING)'], dropped_columns: [], breaking_change: false, generated_migration_up: 'ALTER TABLE silver.dim_customers ADD COLUMN loyalty_tier STRING;' },
];

export default function SchemaDiffStudioPage() {
  const columns: DataGridColumn<SchemaDiffItem>[] = [
    { key: 'table_name', header: 'Target Table', render: (d) => <strong className="text-white font-mono text-xs">{d.table_name}</strong> },
    {
      key: 'source_version',
      header: 'Version Transition',
      render: (d) => (
        <span className="font-mono text-xs">
          <span className="text-slate-400">{d.source_version}</span> → <span className="text-cyan-300 font-bold">{d.target_version}</span>
        </span>
      ),
    },
    {
      key: 'added_columns',
      header: 'Added Fields',
      render: (d) => (
        <div className="flex flex-wrap gap-1">
          {d.added_columns.map((c) => (
            <span key={c} className="bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono text-[9px] px-1.5 py-0.2 rounded">
              +{c}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'breaking_change',
      header: 'Breaking Impact',
      render: (d) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            d.breaking_change
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
          }`}
        >
          {d.breaking_change ? 'BREAKING' : 'NON-BREAKING'}
        </span>
      ),
    },
    { key: 'generated_migration_up', header: 'Generated SQL Migration (UP)', render: (d) => <span className="font-mono text-slate-300 text-xs truncate max-w-xs">{d.generated_migration_up}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Schema Version Diff & Migration DDL — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitCompare className="w-7 h-7 text-cyan-400" />
            Schema Version Diff & Idempotent Migration DDL Generator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Visual schema version comparison, backward/forward compatibility analysis, and auto-generated UP/DOWN DDL migration scripts.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pending Schema Diffs</div>
            <div className="text-2xl font-bold text-white mt-1">2 Diffs</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Breaking Changes Detected</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0 Breaking (Safe)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Migration Script Idempotency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Validated</div>
          </div>
        </div>

        <DataGrid data={mockDiffs} columns={columns} title="Lakehouse Schema Evolution Diffs" />
      </div>
    </MainLayout>
  );
}
