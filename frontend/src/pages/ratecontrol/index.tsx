import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Gauge, Zap, Activity, CheckCircle, ShieldAlert, Sliders } from 'lucide-react';

interface RateLimiterRuleItem {
  id: string;
  stream_endpoint: string;
  algorithm: 'TOKEN_BUCKET' | 'LEAKY_BUCKET';
  max_rate_rps: number;
  burst_capacity: number;
  backpressure_state: 'NORMAL' | 'THROTTLED';
  dropped_events_24h: number;
}

const mockLimiters: RateLimiterRuleItem[] = [
  { id: 'rate_01', stream_endpoint: '/api/v1/stream/ingest/clickstream', algorithm: 'TOKEN_BUCKET', max_rate_rps: 5000, burst_capacity: 10000, backpressure_state: 'NORMAL', dropped_events_24h: 0 },
  { id: 'rate_02', stream_endpoint: '/api/v1/stream/ingest/iot_telemetry', algorithm: 'TOKEN_BUCKET', max_rate_rps: 20000, burst_capacity: 40000, backpressure_state: 'NORMAL', dropped_events_24h: 0 },
  { id: 'rate_03', stream_endpoint: '/api/v1/webhooks/incoming/shopify', algorithm: 'LEAKY_BUCKET', max_rate_rps: 500, burst_capacity: 1000, backpressure_state: 'NORMAL', dropped_events_24h: 0 },
];

export default function RateControlPage() {
  const columns: DataGridColumn<RateLimiterRuleItem>[] = [
    {
      key: 'stream_endpoint',
      header: 'Stream Ingestion Endpoint',
      render: (r) => (
        <div className="flex items-center gap-2">
          <Gauge className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{r.stream_endpoint}</strong>
        </div>
      ),
    },
    {
      key: 'algorithm',
      header: 'Limiter Algorithm',
      render: (r) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{r.algorithm}</span>,
    },
    { key: 'max_rate_rps', header: 'Sustained Rate Limit', render: (r) => <span className="font-mono text-cyan-300 font-bold">{r.max_rate_rps.toLocaleString()} RPS</span> },
    { key: 'burst_capacity', header: 'Max Burst Headroom', render: (r) => <span className="font-mono text-slate-300">{r.burst_capacity.toLocaleString()} req</span> },
    {
      key: 'backpressure_state',
      header: 'Backpressure Status',
      render: (r) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            r.backpressure_state === 'NORMAL'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800 animate-pulse'
          }`}
        >
          {r.backpressure_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Rate Limiting & Backpressure — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Gauge className="w-7 h-7 text-cyan-400" />
            Streaming Rate Limiting & Backpressure Controller
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Token bucket rate limiters, burst protection, and adaptive buffer saturation backpressure throttling.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Ingestion Ingress (Current)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">25,500 RPS</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Worker Queue Saturation</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">34.2% (Healthy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Backpressure Throttle Rate</div>
            <div className="text-2xl font-bold text-white mt-1">0% Throttled</div>
          </div>
        </div>

        <DataGrid data={mockLimiters} columns={columns} title="Active Rate Limiters & Backpressure Monitors" />
      </div>
    </MainLayout>
  );
}
