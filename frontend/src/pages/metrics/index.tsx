import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ThroughputAreaChart, LatencyBarChart } from '@/components/charts/MetricCharts';
import { Activity, Cpu, Server, HardDrive, CheckCircle, Flame, BarChart2 } from 'lucide-react';

interface MetricTimeSeriesItem {
  metric_name: string;
  metric_type: string;
  value: string;
  labels: string;
  help_text: string;
}

const mockMetrics: MetricTimeSeriesItem[] = [
  { metric_name: 'dataflowx_events_ingested_total', metric_type: 'counter', value: '142,850,210', labels: 'layer="bronze", format="parquet"', help_text: 'Total streaming events written to lakehouse' },
  { metric_name: 'dataflowx_pipeline_duration_seconds_p99', metric_type: 'gauge', value: '199.5 ms', labels: 'pipeline="etl_daily_gold"', help_text: '99th percentile end-to-end processing latency' },
  { metric_name: 'dataflowx_active_worker_pods', metric_type: 'gauge', value: '24', labels: 'namespace="dataflowx-jobs"', help_text: 'Current autoscaled Kubernetes worker pods' },
  { metric_name: 'dataflowx_memory_resident_bytes', metric_type: 'gauge', value: '215.8 MB', labels: 'process="coordinator"', help_text: 'Resident set memory footprint' },
];

const throughputData = [
  { timestamp: '00:00', rows_per_sec: 14000, bytes_kb: 1600 },
  { timestamp: '06:00', rows_per_sec: 22000, bytes_kb: 2500 },
  { timestamp: '12:00', rows_per_sec: 48000, bytes_kb: 5600 },
  { timestamp: '18:00', rows_per_sec: 34000, bytes_kb: 3900 },
  { timestamp: '23:59', rows_per_sec: 19000, bytes_kb: 2200 },
];

const latencyData = [
  { stage: 'Kafka Ingest', latency_ms: 4.5, p99_ms: 12.0 },
  { stage: 'Vector Transformation', latency_ms: 18.2, p99_ms: 38.4 },
  { stage: 'Quality Check', latency_ms: 8.1, p99_ms: 21.0 },
  { stage: 'Lakehouse MVCC Commit', latency_ms: 14.8, p99_ms: 31.5 },
];

export default function PlatformMetricsPage() {
  const columns: DataGridColumn<MetricTimeSeriesItem>[] = [
    { key: 'metric_name', header: 'Prometheus Metric Name', render: (m) => <strong className="text-white font-mono">{m.metric_name}</strong> },
    { key: 'metric_type', header: 'Type', render: (m) => <span className="bg-slate-800 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded">{m.metric_type}</span> },
    { key: 'value', header: 'Current Value', render: (m) => <span className="font-mono text-emerald-400 font-bold">{m.value}</span> },
    { key: 'labels', header: 'Prometheus Labels', render: (m) => <span className="font-mono text-slate-400 text-xs">{m.labels}</span> },
    { key: 'help_text', header: 'Description', sortable: false },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Prometheus & OpenTelemetry Metrics — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            Prometheus & OpenTelemetry Observability Metrics
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time telemetry counters, latency distributions, JVM/Python memory footprints, and cluster metrics exporter.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ThroughputAreaChart data={throughputData} height={280} />
          <LatencyBarChart data={latencyData} height={280} />
        </div>

        <DataGrid data={mockMetrics} columns={columns} title="Prometheus Metrics Exposition Feed" />
      </div>
    </MainLayout>
  );
}
