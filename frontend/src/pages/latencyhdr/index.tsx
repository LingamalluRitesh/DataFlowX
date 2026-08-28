import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Activity, Clock, CheckCircle, BarChart3, Layers, Zap } from 'lucide-react';

interface LatencyMetricItem {
  stream_id: string;
  p50_latency_us: number;
  p90_latency_us: number;
  p99_latency_us: number;
  p99_9_latency_us: number;
  max_latency_us: number;
  total_events: string;
  sla_status: 'HEALTHY' | 'VIOLATED';
}

const mockLatencies: LatencyMetricItem[] = [
  { stream_id: 'pipeline.financial_trades', p50_latency_us: 120, p90_latency_us: 280, p99_latency_us: 650, p99_9_latency_us: 1200, max_latency_us: 2450, total_events: '14,200,000', sla_status: 'HEALTHY' },
  { stream_id: 'pipeline.iot_telemetry', p50_latency_us: 450, p90_latency_us: 980, p99_latency_us: 2100, p99_9_latency_us: 4500, max_latency_us: 8900, total_events: '52,000,000', sla_status: 'HEALTHY' },
  { stream_id: 'pipeline.clickstream', p50_latency_us: 320, p90_latency_us: 740, p99_latency_us: 1800, p99_9_latency_us: 3900, max_latency_us: 7200, total_events: '89,000,000', sla_status: 'HEALTHY' },
];

export default function LatencyHDRPage() {
  const columns: DataGridColumn<LatencyMetricItem>[] = [
    { key: 'stream_id', header: 'Streaming Pipeline', render: (l) => <strong className="text-white font-mono text-xs">{l.stream_id}</strong> },
    {
      key: 'p50_latency_us',
      header: 'P50 Median Latency',
      render: (l) => <span className="font-mono text-cyan-300 font-bold">{l.p50_latency_us} μs</span>,
    },
    { key: 'p90_latency_us', header: 'P90 Latency', render: (l) => <span className="font-mono text-slate-300">{l.p90_latency_us} μs</span> },
    {
      key: 'p99_latency_us',
      header: 'P99 Latency',
      render: (l) => <span className="font-mono text-emerald-400 font-bold">{l.p99_latency_us} μs</span>,
    },
    {
      key: 'p99_9_latency_us',
      header: 'P99.9 Tail Latency',
      render: (l) => <span className="font-mono text-purple-300 font-bold">{l.p99_9_latency_us} μs</span>,
    },
    { key: 'total_events', header: 'Samples Recorded', render: (l) => <span className="font-mono text-slate-400">{l.total_events}</span> },
    {
      key: 'sla_status',
      header: 'SLA State',
      render: (l) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {l.sla_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>High-Dynamic Range Latency Histograms — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <BarChart3 className="w-7 h-7 text-cyan-400" />
            High-Dynamic Range (HDR) Microsecond Streaming Latency Histograms
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-allocation High-Dynamic Range (HDR) latency recording measuring sub-microsecond percentiles up to 3600 seconds.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Overall Platform P99 Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">650 μs (Sub-Millisecond)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Recorded Stream Samples</div>
            <div className="text-2xl font-bold text-white mt-1">155M Samples</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Histogram Accuracy</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">99.9% Precision</div>
          </div>
        </div>

        <DataGrid data={mockLatencies} columns={columns} title="Managed Pipeline Latency Percentiles" />
      </div>
    </MainLayout>
  );
}
