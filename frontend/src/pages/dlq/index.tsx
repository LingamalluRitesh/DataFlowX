import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { AlertOctagon, RotateCcw, Trash2, CheckCircle, ShieldAlert, FileText } from 'lucide-react';

interface DLQRecordItem {
  id: string;
  source_pipeline: string;
  quarantine_reason: string;
  payload_preview: string;
  quarantined_at: string;
  status: 'PENDING_REPLAY' | 'REPLAYED' | 'DISCARDED';
}

const mockDLQRecords: DLQRecordItem[] = [
  { id: 'dlq_rec_910', source_pipeline: 'etl_daily_gold_aggregator', quarantine_reason: 'NULL value in required column: customer_id', payload_preview: '{"order_id": 9012, "customer_id": null, "amount": 42.00}', quarantined_at: '10 mins ago', status: 'PENDING_REPLAY' },
  { id: 'dlq_rec_911', source_pipeline: 'stream_clickstream_events', quarantine_reason: 'Schema type mismatch: expected INT, got STRING "invalid"', payload_preview: '{"user_id": "invalid", "click_type": "nav"}', quarantined_at: '1 hour ago', status: 'PENDING_REPLAY' },
];

export default function DeadLetterQueuePage() {
  const columns: DataGridColumn<DLQRecordItem>[] = [
    { key: 'id', header: 'DLQ Record ID', render: (d) => <strong className="text-cyan-400 font-mono">{d.id}</strong> },
    { key: 'source_pipeline', header: 'Originating Pipeline', render: (d) => <span className="font-mono text-white text-xs">{d.source_pipeline}</span> },
    { key: 'quarantine_reason', header: 'Quarantine Reason', render: (d) => <span className="text-amber-400 font-medium text-xs">{d.quarantine_reason}</span> },
    { key: 'payload_preview', header: 'Payload JSON Snippet', render: (d) => <span className="font-mono text-slate-400 text-[11px] truncate max-w-xs">{d.payload_preview}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (d) => (
        <span className="px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800 text-[10px] font-bold">
          {d.status}
        </span>
      ),
    },
    {
      key: 'id',
      header: 'Actions',
      render: (d) => (
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-1 px-2.5 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-[11px] font-semibold transition">
            <RotateCcw className="w-3 h-3" /> Replay
          </button>
          <button className="p-1 rounded bg-slate-800 hover:bg-red-950 text-slate-400 hover:text-red-400 transition">
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Dead-Letter Queue (DLQ) Manager — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <AlertOctagon className="w-7 h-7 text-amber-400" />
              Dead-Letter Queue (DLQ) Partition Manager & Replay
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Inspect corrupted or non-conforming records quarantined to S3/Delta DLQ partitions and trigger automated replay jobs.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <RotateCcw className="w-4 h-4" /> Replay All Pending Records
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pending DLQ Quarantine Records</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">2 Records</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Successful Replays (30d)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">1,418 Records</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">DLQ Storage Location</div>
            <div className="text-sm font-mono text-cyan-300 mt-2">s3://lakehouse/quarantine/dlq/</div>
          </div>
        </div>

        <DataGrid data={mockDLQRecords} columns={columns} title="Quarantined Dead-Letter Queue Records" />
      </div>
    </MainLayout>
  );
}
