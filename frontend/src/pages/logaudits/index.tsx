import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { AlertCircle, HardDrive, ShieldCheck, CheckCircle, Trash2, ArrowRight } from 'lucide-react';

interface StorageAuditItem {
  table_name: string;
  format_type: 'DELTA_LAKE' | 'APACHE_ICEBERG' | 'APACHE_HUDI';
  total_physical_files: number;
  active_committed_files: number;
  orphaned_files_count: number;
  wasted_storage_mb: number;
  integrity_status: 'CLEAN' | 'ORPHANS_DETECTED';
}

const mockAudits: StorageAuditItem[] = [
  { table_name: 'gold.fact_orders', format_type: 'DELTA_LAKE', total_physical_files: 132, active_committed_files: 128, orphaned_files_count: 4, wasted_storage_mb: 38.4, integrity_status: 'ORPHANS_DETECTED' },
  { table_name: 'silver.dim_customers', format_type: 'APACHE_ICEBERG', total_physical_files: 64, active_committed_files: 64, orphaned_files_count: 0, wasted_storage_mb: 0.0, integrity_status: 'CLEAN' },
  { table_name: 'bronze.iot_telemetry', format_type: 'APACHE_HUDI', total_physical_files: 240, active_committed_files: 240, orphaned_files_count: 0, wasted_storage_mb: 0.0, integrity_status: 'CLEAN' },
];

export default function LogAuditsScannerPage() {
  const columns: DataGridColumn<StorageAuditItem>[] = [
    { key: 'table_name', header: 'Lakehouse Table', render: (a) => <strong className="text-white font-mono text-xs">{a.table_name}</strong> },
    {
      key: 'format_type',
      header: 'Table Format',
      render: (a) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{a.format_type}</span>,
    },
    { key: 'total_physical_files', header: 'Object Store Files', render: (a) => <span className="font-mono text-slate-300">{a.total_physical_files} files</span> },
    { key: 'active_committed_files', header: 'Active Committed', render: (a) => <span className="font-mono text-cyan-300 font-bold">{a.active_committed_files} files</span> },
    {
      key: 'orphaned_files_count',
      header: 'Orphaned Dangling Files',
      render: (a) => (
        <span className={`font-mono font-bold ${a.orphaned_files_count > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
          {a.orphaned_files_count} orphans
        </span>
      ),
    },
    {
      key: 'wasted_storage_mb',
      header: 'Wasted Storage Space',
      render: (a) => <span className="font-mono text-slate-300">{a.wasted_storage_mb.toFixed(1)} MB</span>,
    },
    {
      key: 'integrity_status',
      header: 'Log Audit State',
      render: (a) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            a.integrity_status === 'CLEAN'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {a.integrity_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Transaction Log Audits & Orphan Scanner — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <HardDrive className="w-7 h-7 text-cyan-400" />
            Lakehouse Transaction Log Integrity & Orphan File Scanner
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated reconciliation between physical object store files and transaction log metadata to reclaim orphaned storage.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Audited Datasets</div>
            <div className="text-2xl font-bold text-white mt-1">3 Tables</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Orphaned Storage</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">38.4 MB (4 Files)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Log Consistency Score</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">98.8% Consistent</div>
          </div>
        </div>

        <DataGrid data={mockAudits} columns={columns} title="Lakehouse Storage Audit Results" />
      </div>
    </MainLayout>
  );
}
