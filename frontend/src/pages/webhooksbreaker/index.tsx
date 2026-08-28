import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Radio, ShieldAlert, CheckCircle, Database, Layers, RefreshCw } from 'lucide-react';

interface CircuitItem {
  endpoint_host: string;
  circuit_state: 'CLOSED' | 'OPEN' | 'HALF_OPEN';
  consecutive_failures: number;
  successful_deliveries: number;
  dlq_pending_count: number;
  p99_latency_ms: number;
}

const mockCircuits: CircuitItem[] = [
  { endpoint_host: 'https://api.partner-hub.com/webhook/orders', circuit_state: 'CLOSED', consecutive_failures: 0, successful_deliveries: 142500, dlq_pending_count: 0, p99_latency_ms: 124 },
  { endpoint_host: 'https://analytics.external-bi.io/events', circuit_state: 'CLOSED', consecutive_failures: 0, successful_deliveries: 890000, dlq_pending_count: 0, p99_latency_ms: 85 },
  { endpoint_host: 'https://crm-sync.legacy-gateway.net/v1/sync', circuit_state: 'HALF_OPEN', consecutive_failures: 4, successful_deliveries: 1200, dlq_pending_count: 3, p99_latency_ms: 850 },
];

export default function WebhooksBreakerPage() {
  const columns: DataGridColumn<CircuitItem>[] = [
    {
      key: 'endpoint_host',
      header: 'Webhook Destination Endpoint',
      render: (c) => (
        <div className="flex items-center gap-2">
          <Radio className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs truncate max-w-sm">{c.endpoint_host}</strong>
        </div>
      ),
    },
    {
      key: 'circuit_state',
      header: 'Circuit Breaker State',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.circuit_state === 'CLOSED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : c.circuit_state === 'HALF_OPEN'
              ? 'bg-amber-950 text-amber-400 border border-amber-800'
              : 'bg-red-950 text-red-400 border border-red-800'
          }`}
        >
          {c.circuit_state}
        </span>
      ),
    },
    { key: 'successful_deliveries', header: 'Delivered (24h)', render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.successful_deliveries.toLocaleString()} msgs</span> },
    {
      key: 'dlq_pending_count',
      header: 'Dead-Letter Queue (DLQ)',
      render: (c) => (
        <span className={`font-mono font-bold ${c.dlq_pending_count > 0 ? 'text-amber-400' : 'text-slate-400'}`}>
          {c.dlq_pending_count} in DLQ
        </span>
      ),
    },
    { key: 'p99_latency_ms', header: 'P99 Delivery Latency', render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.p99_latency_ms} ms</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Webhook Circuit Breaker & Dead-Letter Queue — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Radio className="w-7 h-7 text-cyan-400" />
            Webhook Circuit Breaker & Dead-Letter Queue (DLQ) Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Resilient event dispatching with half-open circuit breaker recovery, exponential backoff retries, and quarantine dead-letter queues.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Webhook Dispatches (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">1.03M Dispatches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Delivery Success Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">99.99% Delivered</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Circuit Recovery Timeout</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">60 Seconds</div>
          </div>
        </div>

        <DataGrid data={mockCircuits} columns={columns} title="Managed Webhook Circuit Endpoints" />
      </div>
    </MainLayout>
  );
}
