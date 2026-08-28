import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Gauge, Cpu, Zap, CheckCircle, Flame, Layers } from 'lucide-react';

interface BenchmarkMetricItem {
  benchmark_name: string;
  dataset_size_records: string;
  engine_pipeline: string;
  throughput_rps: string;
  p99_latency_ms: number;
  memory_peak_mb: number;
  verdict: 'PASS' | 'OPTIMAL';
}

const mockBenchmarks: BenchmarkMetricItem[] = [
  { benchmark_name: 'TPC-H Q1 Vectorized Aggregation', dataset_size_records: '10,000,000 Rows', engine_pipeline: 'DataFlowX SIMD MPP Engine', throughput_rps: '4,250,000 rows/sec', p99_latency_ms: 28.4, memory_peak_mb: 340, verdict: 'OPTIMAL' },
  { benchmark_name: 'High-Velocity Hash Join (1M x 1M)', dataset_size_records: '2,000,000 Rows', engine_pipeline: 'Vectorized HashJoinExec', throughput_rps: '2,800,000 rows/sec', p99_latency_ms: 45.1, memory_peak_mb: 512, verdict: 'OPTIMAL' },
  { benchmark_name: 'Sliding Window DABA Aggregation', dataset_size_records: '5,000,000 Events', engine_pipeline: 'Two-Stacks Streaming CEP', throughput_rps: '6,100,000 events/sec', p99_latency_ms: 12.2, memory_peak_mb: 64, verdict: 'OPTIMAL' },
  { benchmark_name: 'Parquet Dictionary Decoding & Scan', dataset_size_records: '20,000,000 Rows', engine_pipeline: 'Pure Parquet Columnar Reader', throughput_rps: '8,400,000 rows/sec', p99_latency_ms: 62.0, memory_peak_mb: 420, verdict: 'OPTIMAL' },
];

export default function BenchmarkDashboardPage() {
  const columns: DataGridColumn<BenchmarkMetricItem>[] = [
    { key: 'benchmark_name', header: 'Benchmark Test Suite', render: (b) => <strong className="text-white font-mono text-xs">{b.benchmark_name}</strong> },
    { key: 'dataset_size_records', header: 'Dataset Volume', render: (b) => <span className="font-mono text-slate-300 text-xs">{b.dataset_size_records}</span> },
    { key: 'engine_pipeline', header: 'Execution Pipeline', render: (b) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{b.engine_pipeline}</span> },
    { key: 'throughput_rps', header: 'Processing Throughput', render: (b) => <span className="font-mono text-emerald-400 font-bold">{b.throughput_rps}</span> },
    { key: 'p99_latency_ms', header: 'P99 Latency', render: (b) => <span className="font-mono text-cyan-300 font-bold">{b.p99_latency_ms} ms</span> },
    { key: 'memory_peak_mb', header: 'Peak Memory', render: (b) => <span className="font-mono text-slate-300">{b.memory_peak_mb} MB</span> },
    {
      key: 'verdict',
      header: 'Benchmark Verdict',
      render: (b) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {b.verdict}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Performance Benchmarks & Profiling — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Gauge className="w-7 h-7 text-cyan-400" />
            Lakehouse MPP Engine Performance Benchmarks & Stress Profiling
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated TPC-H query execution benchmarks, SIMD batch throughput records, and memory saturation metrics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak SIMD Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">8.4M rows / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average P99 Execution Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">36.9 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Memory Efficiency</div>
            <div className="text-2xl font-bold text-white mt-1">100% Zero-Copy IPC</div>
          </div>
        </div>

        <DataGrid data={mockBenchmarks} columns={columns} title="Automated Performance Benchmark Matrix" />
      </div>
    </MainLayout>
  );
}
