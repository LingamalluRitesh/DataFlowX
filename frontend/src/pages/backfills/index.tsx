import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { History, Play, CheckCircle, Clock, Plus, Layers, AlertCircle } from 'lucide-react';

interface BackfillPartitionInfo {
  partition_id: string;
  start_date: string;
  end_date: string;
  status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED';
  records_processed: number;
}

interface BackfillJobSummary {
  id: string;
  pipeline_name: string;
  date_range: string;
  chunk_interval: string;
  total_partitions: number;
  completed_partitions: number;
  status: 'RUNNING' | 'COMPLETED' | 'FAILED';
  created_at: string;
  partitions: BackfillPartitionInfo[];
}

const mockBackfills: BackfillJobSummary[] = [
  {
    id: 'bf_2026_q1',
    pipeline_name: 'ecom_daily_etl_pipeline',
    date_range: '2026-01-01 to 2026-03-31',
    chunk_interval: '1d',
    total_partitions: 90,
    completed_partitions: 90,
    status: 'COMPLETED',
    created_at: '2026-08-28 10:15:00',
    partitions: [
      { partition_id: 'bf_2026_q1_p1', start_date: '2026-01-01', end_date: '2026-01-02', status: 'SUCCESS', records_processed: 45200 },
      { partition_id: 'bf_2026_q1_p2', start_date: '2026-01-02', end_date: '2026-01-03', status: 'SUCCESS', records_processed: 48900 },
    ],
  },
  {
    id: 'bf_crm_history',
    pipeline_name: 'crm_scd2_sync',
    date_range: '2025-06-01 to 2025-12-31',
    chunk_interval: '7d',
    total_partitions: 28,
    completed_partitions: 22,
    status: 'RUNNING',
    created_at: '2026-08-28 13:40:00',
    partitions: [
      { partition_id: 'bf_crm_p21', start_date: '2025-11-01', end_date: '2025-11-08', status: 'SUCCESS', records_processed: 120500 },
      { partition_id: 'bf_crm_p22', start_date: '2025-11-08', end_date: '2025-11-15', status: 'RUNNING', records_processed: 64000 },
      { partition_id: 'bf_crm_p23', start_date: '2025-11-15', end_date: '2025-11-22', status: 'PENDING', records_processed: 0 },
    ],
  },
];

export default function BackfillsIndexPage() {
  const [selectedJob, setSelectedJob] = useState<BackfillJobSummary>(mockBackfills[1]);

  const columns: DataGridColumn<BackfillJobSummary>[] = [
    {
      key: 'pipeline_name',
      header: 'Target Pipeline',
      render: (b) => (
        <div>
          <strong className="text-white">{b.pipeline_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{b.id}</div>
        </div>
      ),
    },
    { key: 'date_range', header: 'Historical Date Range' },
    {
      key: 'chunk_interval',
      header: 'Chunk Interval',
      render: (b) => <span className="bg-slate-800 px-2 py-0.5 rounded text-cyan-400 font-mono text-xs">{b.chunk_interval}</span>,
    },
    {
      key: 'completed_partitions',
      header: 'Progress',
      render: (b) => (
        <div className="flex items-center gap-2">
          <div className="w-20 bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-cyan-500 h-full rounded-full"
              style={{ width: `${(b.completed_partitions / b.total_partitions) * 100}%` }}
            />
          </div>
          <span className="font-mono text-slate-300 text-xs">
            {b.completed_partitions}/{b.total_partitions}
          </span>
        </div>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (b) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            b.status === 'COMPLETED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : b.status === 'RUNNING'
              ? 'bg-cyan-950 text-cyan-400 border border-cyan-800 animate-pulse'
              : 'bg-red-950 text-red-400 border border-red-800'
          }`}
        >
          {b.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Historical Backfill Manager — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <History className="w-7 h-7 text-cyan-400" />
              Historical Backfill Manager
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Trigger date-partitioned replay jobs, manage parallel sub-range backfills, and audit idempotent execution states.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Trigger New Backfill
          </button>
        </div>

        {/* Backfills Table */}
        <DataGrid data={mockBackfills} columns={columns} title="Backfill Jobs" />

        {/* Partition Execution Visualizer */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white">Active Partition Execution Matrix</h3>
              <p className="text-xs text-slate-400">Job: <span className="font-mono text-cyan-400">{selectedJob.id}</span> ({selectedJob.pipeline_name})</p>
            </div>
            <span className="text-xs bg-slate-800 px-2.5 py-1 rounded text-slate-300 font-mono">
              Max Concurrency: 4 Partitions
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {selectedJob.partitions.map((p) => (
              <div key={p.partition_id} className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                <div>
                  <div className="font-mono font-bold text-xs text-slate-200">{p.partition_id}</div>
                  <div className="text-[10px] text-slate-400 mt-0.5">{p.start_date} &rarr; {p.end_date}</div>
                  <div className="text-[10px] text-slate-500 mt-1 font-mono">{p.records_processed.toLocaleString()} records</div>
                </div>

                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    p.status === 'SUCCESS'
                      ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                      : p.status === 'RUNNING'
                      ? 'bg-cyan-950 text-cyan-400 border border-cyan-800 animate-pulse'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {p.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
