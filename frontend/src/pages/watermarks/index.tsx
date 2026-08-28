import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Clock, Activity, CheckCircle, Droplet, Layers, AlertCircle } from 'lucide-react';

interface WatermarkStreamItem {
  stream_topic: string;
  current_watermark_time: string;
  allowed_lateness_ms: number;
  max_event_time_observed: string;
  late_events_dropped: number;
  lag_behind_wallclock_ms: number;
  status: 'EMITTING' | 'STALLED';
}

const mockWatermarks: WatermarkStreamItem[] = [
  { stream_topic: 'events.ecom_pageviews', current_watermark_time: '2026-08-29 00:24:45 UTC', allowed_lateness_ms: 5000, max_event_time_observed: '2026-08-29 00:24:50 UTC', late_events_dropped: 12, lag_behind_wallclock_ms: 124, status: 'EMITTING' },
  { stream_topic: 'iot.sensor_telemetry', current_watermark_time: '2026-08-29 00:24:52 UTC', allowed_lateness_ms: 2000, max_event_time_observed: '2026-08-29 00:24:54 UTC', late_events_dropped: 0, lag_behind_wallclock_ms: 68, status: 'EMITTING' },
  { stream_topic: 'financial.fx_trades', current_watermark_time: '2026-08-29 00:24:58 UTC', allowed_lateness_ms: 500, max_event_time_observed: '2026-08-29 00:24:58.5 UTC', late_events_dropped: 2, lag_behind_wallclock_ms: 18, status: 'EMITTING' },
];

export default function WatermarksStreamPage() {
  const columns: DataGridColumn<WatermarkStreamItem>[] = [
    { key: 'stream_topic', header: 'Streaming Topic', render: (w) => <strong className="text-white font-mono text-xs">{w.stream_topic}</strong> },
    { key: 'current_watermark_time', header: 'Monotonic Watermark Time', render: (w) => <span className="font-mono text-cyan-300 text-xs">{w.current_watermark_time}</span> },
    {
      key: 'allowed_lateness_ms',
      header: 'Allowed Lateness Bound',
      render: (w) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{w.allowed_lateness_ms} ms</span>,
    },
    { key: 'max_event_time_observed', header: 'Max Observed Event Time', render: (w) => <span className="font-mono text-slate-300 text-xs">{w.max_event_time_observed}</span> },
    {
      key: 'late_events_dropped',
      header: 'Dropped Late Events',
      render: (w) => <span className="font-mono text-amber-400 font-bold">{w.late_events_dropped} dropped</span>,
    },
    {
      key: 'lag_behind_wallclock_ms',
      header: 'Ingestion Latency',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.lag_behind_wallclock_ms} ms</span>,
    },
    {
      key: 'status',
      header: 'Watermark Status',
      render: (w) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {w.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Event-Time Watermarks — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Droplet className="w-7 h-7 text-cyan-400" />
            Bounded Out-of-Orderness Event-Time Watermark Monitor
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time streaming watermarks tracking monotonic progress, late-arriving event buffers, and window trigger checkpoints.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Watermark Generators</div>
            <div className="text-2xl font-bold text-white mt-1">3 Pipelines</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Streaming Lag</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">70 ms (Real-Time)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Watermark Monotonicity</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Strict</div>
          </div>
        </div>

        <DataGrid data={mockWatermarks} columns={columns} title="Managed Streaming Watermark Streams" />
      </div>
    </MainLayout>
  );
}
