import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { ThroughputAreaChart, LatencyBarChart } from '@/components/charts/MetricCharts';
import { BarChart, TrendingUp, DollarSign, Activity, Zap, CheckCircle } from 'lucide-react';

const mockThroughput = [
  { timestamp: '00:00', rows_per_sec: 12000, bytes_kb: 1400 },
  { timestamp: '04:00', rows_per_sec: 14500, bytes_kb: 1680 },
  { timestamp: '08:00', rows_per_sec: 28000, bytes_kb: 3200 },
  { timestamp: '12:00', rows_per_sec: 42000, bytes_kb: 4900 },
  { timestamp: '16:00', rows_per_sec: 38000, bytes_kb: 4300 },
  { timestamp: '20:00', rows_per_sec: 24000, bytes_kb: 2800 },
  { timestamp: '23:59', rows_per_sec: 18000, bytes_kb: 2100 },
];

const mockLatency = [
  { stage: 'Data Ingestion', latency_ms: 12.4, p99_ms: 34.0 },
  { stage: 'Transformation', latency_ms: 28.5, p99_ms: 68.2 },
  { stage: 'Quality Check', latency_ms: 15.2, p99_ms: 41.5 },
  { stage: 'Lakehouse Write', latency_ms: 22.0, p99_ms: 55.8 },
];

export default function AnalyticsExecutiveDashboard() {
  return (
    <MainLayout>
      <Head>
        <title>Executive Analytics & Platform Telemetry — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <TrendingUp className="w-7 h-7 text-cyan-400" />
            Executive Analytics & Platform Health Telemetry
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Enterprise-wide telemetry overview covering daily event processing volumes, cluster compute efficiency, SLA adherence, and data throughput.
          </p>
        </div>

        {/* Metric Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">24h Event Volume</div>
            <div className="text-3xl font-extrabold text-cyan-400 mt-2">142.8M</div>
            <div className="text-xs text-emerald-400 mt-1 font-semibold">&uarr; 18.2% vs yesterday</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Global SLA Compliance</div>
            <div className="text-3xl font-extrabold text-emerald-400 mt-2">99.94%</div>
            <div className="text-xs text-slate-400 mt-1">3 SLA breaches in trailing 30d</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Avg Pipeline Latency</div>
            <div className="text-3xl font-extrabold text-purple-400 mt-2">78.1 ms</div>
            <div className="text-xs text-slate-400 mt-1">P99 tail latency: 199.5 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Lakehouse Datasets</div>
            <div className="text-3xl font-extrabold text-amber-400 mt-2">32 Tables</div>
            <div className="text-xs text-slate-400 mt-1">Bronze (12), Silver (14), Gold (6)</div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ThroughputAreaChart data={mockThroughput} height={320} />
          <LatencyBarChart data={mockLatency} height={320} />
        </div>
      </div>
    </MainLayout>
  );
}
