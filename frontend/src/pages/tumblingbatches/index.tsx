import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, PackageCheck, CheckCircle, Database, Clock, ArrowRight } from 'lucide-react';

interface TumblingBatchItem {
  batch_id: number;
  stream_topic: string;
  elements_in_batch: number;
  flush_reason: 'COUNT_REACHED' | 'TIMEOUT_FLUSH' | 'MANUAL_BARRIER';
  accumulation_time_ms: number;
  emitted_record_size_kb: number;
  status: 'EMITTED' | 'BUFFERING';
}

const mockBatches: TumblingBatchItem[] = [
  { batch_id: 10420, stream_topic: 'events.orders.stream', elements_in_batch: 5000, flush_reason: 'COUNT_REACHED', accumulation_time_ms: 24.5, emitted_record_size_kb: 480.2, status: 'EMITTED' },
  { batch_id: 10419, stream_topic: 'events.orders.stream', elements_in_batch: 5000, flush_reason: 'COUNT_REACHED', accumulation_time_ms: 22.1, emitted_record_size_kb: 478.5, status: 'EMITTED' },
  { batch_id: 10418, stream_topic: 'iot.sensor.stream', elements_in_batch: 1200, flush_reason: 'TIMEOUT_FLUSH', accumulation_time_ms: 100.0, emitted_record_size_kb: 94.0, status: 'EMITTED' },
];

export default function TumblingBatchesStudioPage() {
  const columns: DataGridColumn<TumblingBatchItem>[] = [
    {
      key: 'batch_id',
      header: 'Batch ID',
      render: (b) => (
        <span className="font-mono text-cyan-300 font-bold flex items-center gap-1.5">
          <PackageCheck className="w-3.5 h-3.5" /> Batch #{b.batch_id}
        </span>
      ),
    },
    { key: 'stream_topic', header: 'Stream Channel', render: (b) => <strong className="text-white font-mono text-xs">{b.stream_topic}</strong> },
    {
      key: 'elements_in_batch',
      header: 'Accumulated Elements',
      render: (b) => <span className="font-mono text-emerald-400 font-bold">{b.elements_in_batch.toLocaleString()} items</span>,
    },
    {
      key: 'flush_reason',
      header: 'Trigger Condition',
      render: (b) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{b.flush_reason}</span>,
    },
    { key: 'accumulation_time_ms', header: 'Window Duration', render: (b) => <span className="font-mono text-slate-300">{b.accumulation_time_ms.toFixed(1)} ms</span> },
    { key: 'emitted_record_size_kb', header: 'Emitted Size', render: (b) => <span className="font-mono text-cyan-300">{b.emitted_record_size_kb.toFixed(1)} KB</span> },
    {
      key: 'status',
      header: 'State',
      render: (b) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {b.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Tumbling Count Micro-Batch Accumulator — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <PackageCheck className="w-7 h-7 text-cyan-400" />
            Tumbling Count Micro-Batch Stream Accumulator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            High-throughput event batching accumulating fixed count thresholds or early timeout barriers for vector reductions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Emitted Micro-Batches (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">4.2M Batches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Batch Accumulation Time</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">23.3 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Memory Zero-Copy Delivery</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Shared Memory</div>
          </div>
        </div>

        <DataGrid data={mockBatches} columns={columns} title="Emitted Tumbling Micro-Batches" />
      </div>
    </MainLayout>
  );
}
