import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Activity, Clock, Layers, Zap, CheckCircle, ArrowRight } from 'lucide-react';

interface TraceSpanItem {
  span_id: string;
  trace_id: string;
  operation_name: string;
  duration_ms: number;
  service_component: string;
  status: 'OK' | 'ERROR';
}

const mockSpans: TraceSpanItem[] = [
  { span_id: 'sp_89a0', trace_id: 'tr_4f8e9102cba76543', operation_name: 'VectorBatch.SIMD_Filter[amount > 100]', duration_ms: 1.45, service_component: 'mpp_engine', status: 'OK' },
  { span_id: 'sp_89a1', trace_id: 'tr_4f8e9102cba76543', operation_name: 'ParquetReader.ScanRowGroups[s3://lakehouse/orders]', duration_ms: 14.80, service_component: 'storage_io', status: 'OK' },
  { span_id: 'sp_89a2', trace_id: 'tr_4f8e9102cba76543', operation_name: 'DataQuality.CheckNulls[customer_id]', duration_ms: 0.85, service_component: 'quality_engine', status: 'OK' },
  { span_id: 'sp_89a3', trace_id: 'tr_4f8e9102cba76543', operation_name: 'DeltaLake.CommitSnapshot[v42]', duration_ms: 22.10, service_component: 'acid_manager', status: 'OK' },
];

export default function DistributedTracingPage() {
  const columns: DataGridColumn<TraceSpanItem>[] = [
    { key: 'operation_name', header: 'Span Operation', render: (s) => <strong className="text-white font-mono text-xs">{s.operation_name}</strong> },
    { key: 'service_component', header: 'Subsystem', render: (s) => <span className="bg-slate-800 text-cyan-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.service_component}</span> },
    {
      key: 'duration_ms',
      header: 'Execution Latency',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.duration_ms} ms</span>,
    },
    { key: 'span_id', header: 'Span ID', render: (s) => <span className="font-mono text-slate-400 text-xs">{s.span_id}</span> },
    { key: 'trace_id', header: 'W3C Trace ID', render: (s) => <span className="font-mono text-purple-300 text-xs">{s.trace_id}</span> },
    {
      key: 'status',
      header: 'Span Status',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>OpenTelemetry Distributed Tracing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            OpenTelemetry Distributed Tracing & Span Waterfall Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            W3C traceparent context propagation, microsecond span waterfall profiling, and Jaeger/Zipkin telemetry integration.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Traced Execution Time</div>
            <div className="text-2xl font-bold text-white mt-1">39.2 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Microsecond Spans Captured</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4 Spans</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Telemetry Exporter</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">OTel / Jaeger gRPC</div>
          </div>
        </div>

        <DataGrid data={mockSpans} columns={columns} title="Distributed Execution Spans (Trace #tr_4f8e9102cba76543)" />
      </div>
    </MainLayout>
  );
}
