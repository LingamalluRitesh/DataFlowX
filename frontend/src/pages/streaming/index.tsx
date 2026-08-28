import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ThroughputAreaChart, LatencyBarChart } from '@/components/charts/MetricCharts';
import { Zap, Radio, Activity, Play, Pause, RefreshCw, Database } from 'lucide-react';

interface StreamingPipelineItem {
  stream_id: string;
  source_type: 'KAFKA' | 'REDIS_STREAM' | 'GRPC';
  target_layer: 'BRONZE' | 'SILVER';
  window_type: string;
  window_size_seconds: number;
  status: 'RUNNING' | 'PAUSED' | 'STOPPED';
  total_messages_ingested: number;
  throughput_eps: number;
}

const mockStreams: StreamingPipelineItem[] = [
  { stream_id: 'stream_clickstream_events', source_type: 'KAFKA', target_layer: 'BRONZE', window_type: 'TUMBLING', window_size_seconds: 60, status: 'RUNNING', total_messages_ingested: 3450000, throughput_eps: 4500.0 },
  { stream_id: 'stream_iot_telemetry_sensors', source_type: 'REDIS_STREAM', target_layer: 'SILVER', window_type: 'SLIDING', window_size_seconds: 300, status: 'RUNNING', total_messages_ingested: 1250000, throughput_eps: 1850.0 },
  { stream_id: 'stream_grpc_edge_gateway', source_type: 'GRPC', target_layer: 'BRONZE', window_type: 'TUMBLING', window_size_seconds: 30, status: 'RUNNING', total_messages_ingested: 890000, throughput_eps: 1200.0 },
];

const mockThroughputData = [
  { timestamp: '14:00', rows_per_sec: 3200, bytes_kb: 450 },
  { timestamp: '14:05', rows_per_sec: 4100, bytes_kb: 580 },
  { timestamp: '14:10', rows_per_sec: 4800, bytes_kb: 640 },
  { timestamp: '14:15', rows_per_sec: 5200, bytes_kb: 710 },
  { timestamp: '14:20', rows_per_sec: 4900, bytes_kb: 680 },
  { timestamp: '14:25', rows_per_sec: 5600, bytes_kb: 790 },
  { timestamp: '14:30', rows_per_sec: 6100, bytes_kb: 840 },
];

const mockLatencyData = [
  { stage: 'Kafka Ingest', latency_ms: 4.2, p99_ms: 12.5 },
  { stage: 'Schema Parse', latency_ms: 6.8, p99_ms: 18.2 },
  { stage: 'Crypto Masking', latency_ms: 8.5, p99_ms: 22.0 },
  { stage: 'Parquet Append', latency_ms: 14.1, p99_ms: 35.4 },
];

export default function StreamingIndexPage() {
  const columns: DataGridColumn<StreamingPipelineItem>[] = [
    {
      key: 'stream_id',
      header: 'Stream Pipeline ID',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <strong className="text-white">{s.stream_id}</strong>
        </div>
      ),
    },
    {
      key: 'source_type',
      header: 'Source Engine',
      render: (s) => <span className="bg-slate-800 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded">{s.source_type}</span>,
    },
    {
      key: 'target_layer',
      header: 'Target Layer',
      render: (s) => (
        <span className="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">
          {s.target_layer}
        </span>
      ),
    },
    {
      key: 'window_type',
      header: 'Window Spec',
      render: (s) => (
        <span className="font-mono text-slate-400 text-xs">
          {s.window_type} ({s.window_size_seconds}s)
        </span>
      ),
    },
    {
      key: 'throughput_eps',
      header: 'Throughput (EPS)',
      render: (s) => <span className="font-mono text-cyan-400 font-bold">{s.throughput_eps.toLocaleString()} eps</span>,
    },
    {
      key: 'total_messages_ingested',
      header: 'Total Events Ingested',
      render: (s) => <span className="font-mono text-slate-300">{s.total_messages_ingested.toLocaleString()}</span>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold animate-pulse">
          {s.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Real-Time Streaming Engine — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Radio className="w-7 h-7 text-amber-400 animate-pulse" />
            Real-Time Streaming & Micro-Batch Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Continuous event streaming pipelines with sliding window aggregations, late data watermarking, and ACID micro-batch checkpoints.
          </p>
        </div>

        {/* Streaming Real-Time Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <ThroughputAreaChart data={mockThroughputData} />
          <LatencyBarChart data={mockLatencyData} />
        </div>

        {/* Active Streams Table */}
        <DataGrid data={mockStreams} columns={columns} title="Active Real-Time Stream Pipelines" />
      </div>
    </MainLayout>
  );
}
