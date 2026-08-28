import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Trash2, ShieldCheck, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface VacuumPurgeItem {
  table_name: string;
  retention_threshold_hours: number;
  uncommitted_files_deleted: number;
  reclaimed_storage_gb: number;
  last_vacuum_time: string;
  next_scheduled_vacuum: string;
}

const mockVacuums: VacuumPurgeItem[] = [
  { table_name: 'gold.fact_orders', retention_threshold_hours: 168, uncommitted_files_deleted: 142, reclaimed_storage_gb: 45.2, last_vacuum_time: '2026-08-28 22:00 UTC', next_scheduled_vacuum: '2026-08-29 22:00 UTC' },
  { table_name: 'silver.dim_customers', retention_threshold_hours: 168, uncommitted_files_deleted: 64, reclaimed_storage_gb: 18.0, last_vacuum_time: '2026-08-28 22:00 UTC', next_scheduled_vacuum: '2026-08-29 22:00 UTC' },
  { table_name: 'bronze.iot_telemetry', retention_threshold_hours: 72, uncommitted_files_deleted: 520, reclaimed_storage_gb: 180.5, last_vacuum_time: '2026-08-28 18:00 UTC', next_scheduled_vacuum: '2026-08-29 18:00 UTC' },
];

export default function VacuumPurgePage() {
  const columns: DataGridColumn<VacuumPurgeItem>[] = [
    { key: 'table_name', header: 'Lakehouse Target Table', render: (v) => <strong className="text-white font-mono text-xs">{v.table_name}</strong> },
    {
      key: 'retention_threshold_hours',
      header: 'Retention Grace Period',
      render: (v) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{v.retention_threshold_hours}h (7 Days)</span>,
    },
    {
      key: 'uncommitted_files_deleted',
      header: 'Orphan Files Purged',
      render: (v) => <span className="font-mono text-amber-400 font-bold">{v.uncommitted_files_deleted} files</span>,
    },
    {
      key: 'reclaimed_storage_gb',
      header: 'Reclaimed Disk Storage',
      render: (v) => <span className="font-mono text-emerald-400 font-bold text-sm">{v.reclaimed_storage_gb.toFixed(1)} GB Freed</span>,
    },
    { key: 'last_vacuum_time', header: 'Last Execution', render: (v) => <span className="font-mono text-slate-300 text-xs">{v.last_vacuum_time}</span> },
    { key: 'next_scheduled_vacuum', header: 'Next Automated Run', render: (v) => <span className="font-mono text-cyan-300 text-xs">{v.next_scheduled_vacuum}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vacuum & Storage Garbage Collection — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Trash2 className="w-7 h-7 text-cyan-400" />
            Lakehouse Vacuum & Storage Garbage Collection Purger
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Reclaims object storage by safely deleting unreferenced and soft-deleted snapshot files exceeding configured retention grace periods.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Storage Reclaimed (30d)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">243.7 GB Freed</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Safety Lock Grace Period</div>
            <div className="text-2xl font-bold text-white mt-1">168 Hours Standard</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Storage Cost Reduction</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">$1,850.00 / year</div>
          </div>
        </div>

        <DataGrid data={mockVacuums} columns={columns} title="Automated Vacuum Operations" />
      </div>
    </MainLayout>
  );
}
