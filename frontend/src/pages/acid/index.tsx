import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { History, ShieldCheck, Database, Layers, CheckCircle, Clock, Trash2 } from 'lucide-react';

interface MVCCCommitItem {
  version: number;
  txn_id: string;
  table_name: string;
  operation: 'MERGE' | 'APPEND' | 'OVERWRITE' | 'VACUUM';
  files_written: number;
  files_deleted: number;
  committed_at: string;
  status: 'COMMITTED' | 'ABORTED';
}

const mockCommits: MVCCCommitItem[] = [
  { version: 42, txn_id: 'txn_9a8b7c', table_name: 'gold.fact_orders', operation: 'MERGE', files_written: 4, files_deleted: 2, committed_at: '5 mins ago', status: 'COMMITTED' },
  { version: 41, txn_id: 'txn_6d5e4f', table_name: 'gold.fact_orders', operation: 'APPEND', files_written: 2, files_deleted: 0, committed_at: '1 hour ago', status: 'COMMITTED' },
  { version: 40, txn_id: 'txn_3c2b1a', table_name: 'gold.fact_orders', operation: 'VACUUM', files_written: 0, files_deleted: 14, committed_at: '1 day ago', status: 'COMMITTED' },
];

export default function LakehouseAcidPage() {
  const columns: DataGridColumn<MVCCCommitItem>[] = [
    {
      key: 'version',
      header: 'Snapshot Version',
      render: (c) => <strong className="text-cyan-400 font-mono">v{c.version}</strong>,
    },
    {
      key: 'txn_id',
      header: 'Transaction ID',
      render: (c) => <span className="font-mono text-slate-300 text-xs">{c.txn_id}</span>,
    },
    { key: 'table_name', header: 'Target Lakehouse Table', render: (c) => <span className="font-mono text-white">{c.table_name}</span> },
    {
      key: 'operation',
      header: 'ACID Operation',
      render: (c) => (
        <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">
          {c.operation}
        </span>
      ),
    },
    {
      key: 'files_written',
      header: 'Files Delta',
      render: (c) => (
        <span className="font-mono text-xs">
          <span className="text-emerald-400 font-bold">+{c.files_written}</span> /{' '}
          <span className="text-red-400 font-bold">-{c.files_deleted}</span>
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
    { key: 'committed_at', header: 'Timestamp' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Lakehouse ACID Transactions & Time Travel — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <History className="w-7 h-7 text-cyan-400" />
            Lakehouse ACID Transactions & Time Travel
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Audit commit logs, inspect point-in-time table states AS OF VERSION, and trigger garbage collection VACUUM jobs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Committed Versions</div>
            <div className="text-2xl font-bold text-white mt-1">42 Versions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Isolation Level</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">Snapshot Isolation (SI)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tombstone Retention</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">7 Days (168h)</div>
          </div>
        </div>

        <DataGrid data={mockCommits} columns={columns} title="Lakehouse Commit History Log" />
      </div>
    </MainLayout>
  );
}
