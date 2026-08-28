import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Clock, Activity, CheckCircle, Droplet, Layers, AlertCircle } from 'lucide-react';

interface WatermarkLagItem {
  stream_id: string;
  watermark_timestamp: string;
  wallclock_timestamp: string;
  ingestion_lag_ms: number;
  max_allowed_lag_ms: number;
  is_monotonic: boolean;
  lag_state: 'OPTIMAL_REALTIME' | 'LAG_WARNING';
}

const mockLags: WatermarkLagItem[] = [
  { stream_id: 'stream.order_transactions', watermark_timestamp: '2026-08-29 00:24:58.120 UTC', wallclock_timestamp: '2026-08-29 00:24:58.185 UTC', ingestion_lag_ms: 65, max_allowed_lag_ms: 5000, is_monotonic: true, lag_state: 'OPTIMAL_REALTIME' },
  { stream_id: 'stream.iot_sensor_events', watermark_timestamp: '2026-08-29 00:24:57.800 UTC', wallclock_timestamp: '2026-08-29 00:24:58.185 UTC', ingestion_lag_ms: 385, max_allowed_lag_ms: 5000, is_monotonic: true, lag_state: 'OPTIMAL_REALTIME' },
  { stream_id: 'stream.user_clicks', watermark_timestamp: '2026-08-29 00:24:58.050 UTC', wallclock_timestamp: '2026-08-29 00:24:58.185 UTC', ingestion_lag_ms: 135, max_allowed_lag_ms: 5000, is_monotonic: true, lag_state: 'OPTIMAL_REALTIME' },
];

export default function WatermarkLagStudioPage() {
  const columns: DataGridColumn<WatermarkLagItem>[] = [
    {
      key: 'stream_id',
      header: 'Stream Channel',
      render: (w) => (
        <div className="flex items-center gap-2">
          <Droplet className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{w.stream_id}</strong>
        </div>
      ),
    },
    { key: 'watermark_timestamp', header: 'Current Watermark', render: (w) => <span className="font-mono text-cyan-300 text-xs">{w.watermark_timestamp}</span> },
    { key: 'wallclock_timestamp', header: 'System Wall-Clock', render: (w) => <span className="font-mono text-slate-400 text-xs">{w.wallclock_timestamp}</span> },
    {
      key: 'ingestion_lag_ms',
      header: 'Real-Time Ingestion Lag',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.ingestion_lag_ms} ms</span>,
    },
    {
      key: 'is_monotonic',
      header: 'Monotonicity',
      render: (w) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          STRICT MONOTONIC
        </span>
      ),
    },
    {
      key: 'lag_state',
      header: 'Stream Lag State',
      render: (w) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {w.lag_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Watermark Lag & Monotonicity — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Clock className="w-7 h-7 text-cyan-400" />
            Streaming Watermark Ingestion Lag & Monotonic Progress Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Millisecond-precision comparison between wall-clock time and streaming watermark advances to detect lagging pipeline operators.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Stream Lag</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">195 ms (Real-Time)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Watermark Monotonicity</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Monotonic</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Allowed Lateness Bound</div>
            <div className="text-2xl font-bold text-white mt-1">5,000 ms Max Buffer</div>
          </div>
        </div>

        <DataGrid data={mockLags} columns={columns} title="Managed Stream Watermark Status" />
      </div>
    </MainLayout>
  );
}
