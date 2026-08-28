import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Activity, GitCommit, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface OTelSpanItem {
  trace_id: string;
  span_name: string;
  service_name: string;
  duration_ms: number;
  span_kind: 'INTERNAL' | 'CLIENT' | 'SERVER' | 'PRODUCER';
  status_code: 'OK' | 'ERROR';
}

const mockSpans: OTelSpanItem[] = [
  { trace_id: '4bf92f3577b34da6a3ce929d0e0e4736', span_name: 'engine.vectorized_scan', service_name: 'query_execution_kernel', duration_ms: 1.45, span_kind: 'INTERNAL', status_code: 'OK' },
  { trace_id: '4bf92f3577b34da6a3ce929d0e0e4736', span_name: 'storage.s3_read_parquet_stripe', service_name: 'lakehouse_io_layer', duration_ms: 3.20, span_kind: 'CLIENT', status_code: 'OK' },
  { trace_id: '4bf92f3577b34da6a3ce929d0e0e4736', span_name: 'security.rls_filter_eval', service_name: 'governance_filter_proxy', duration_ms: 0.05, span_kind: 'INTERNAL', status_code: 'OK' },
];

export default function TelemetrySpansPage() {
  const columns: DataGridColumn<OTelSpanItem>[] = [
    {
      key: 'span_name',
      header: 'OpenTelemetry Span Name',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.span_name}</strong>
        </div>
      ),
    },
    { key: 'service_name', header: 'Service Component', render: (s) => <span className="text-slate-300 font-mono text-xs">{s.service_name}</span> },
    {
      key: 'span_kind',
      header: 'Span Kind',
      render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{s.span_kind}</span>,
    },
    {
      key: 'duration_ms',
      header: 'Execution Duration',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.duration_ms.toFixed(2)} ms</span>,
    },
    { key: 'trace_id', header: 'W3C Trace Context ID', render: (s) => <span className="font-mono text-slate-400 text-xs truncate max-w-xs">{s.trace_id}</span> },
    {
      key: 'status_code',
      header: 'Span State',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.status_code}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>OpenTelemetry Distributed Tracing & Spans — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            OpenTelemetry Distributed Tracing & W3C Span DAG Inspector
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            End-to-end W3C trace context propagation, microsecond span waterfall timelines, and distributed error root-cause diagnostics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Traces Captured (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">8.5M Traces</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Trace Propagation Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;0.02 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">OpenTelemetry Standard</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">OTLP v1.3.0</div>
          </div>
        </div>

        <DataGrid data={mockSpans} columns={columns} title="Distributed Execution Spans" />
      </div>
    </MainLayout>
  );
}
