import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Activity, Clock, Layers, CheckCircle, Zap, TrendingUp } from 'lucide-react';

interface DABAWindowItem {
  window_name: string;
  aggregation_func: 'SUM' | 'MAX' | 'MIN' | 'COUNT' | 'AVERAGE';
  window_capacity: number;
  amortized_complexity: string;
  current_window_aggregate: string;
  throughput_events_per_sec: string;
}

const mockDABA: DABAWindowItem[] = [
  { window_name: 'fact_order_stream.10k_sliding_sum', aggregation_func: 'SUM', window_capacity: 10000, amortized_complexity: 'O(1) Push/Pop', current_window_aggregate: '$1,420,500.00', throughput_events_per_sec: '6,100,000 ev/s' },
  { window_name: 'iot_vibration.5k_max_peak', aggregation_func: 'MAX', window_capacity: 5000, amortized_complexity: 'O(1) Push/Pop', current_window_aggregate: '94.2 dB Peak', throughput_events_per_sec: '7,800,000 ev/s' },
  { window_name: 'api_gateway_latency.1m_moving_avg', aggregation_func: 'AVERAGE', window_capacity: 60000, amortized_complexity: 'O(1) Push/Pop', current_window_aggregate: '14.5 ms Avg', throughput_events_per_sec: '5,400,000 ev/s' },
];

export default function DABASlidingWindowsPage() {
  const columns: DataGridColumn<DABAWindowItem>[] = [
    { key: 'window_name', header: 'Streaming Sliding Window', render: (w) => <strong className="text-white font-mono text-xs">{w.window_name}</strong> },
    {
      key: 'aggregation_func',
      header: 'Aggregation Function',
      render: (w) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{w.aggregation_func}</span>,
    },
    { key: 'window_capacity', header: 'Window Capacity (FIFO)', render: (w) => <span className="font-mono text-slate-300">{w.window_capacity.toLocaleString()} events</span> },
    {
      key: 'amortized_complexity',
      header: 'Algorithmic Complexity',
      render: (w) => <span className="font-mono text-cyan-300 font-bold">{w.amortized_complexity}</span>,
    },
    {
      key: 'current_window_aggregate',
      header: 'Instant Window Aggregate',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.current_window_aggregate}</span>,
    },
    {
      key: 'throughput_events_per_sec',
      header: 'Sliding Throughput',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.throughput_events_per_sec}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Two-Stacks O(1) Sliding Window Aggregators — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            Two-Stacks (DABA) O(1) Sliding Window Stream Aggregators
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Pure functional two-stacks queue sliding window aggregations executing MIN, MAX, SUM, and AVG in amortized O(1) time without recomputation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Sliding Stream Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">7.8M events / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Amortized Step Complexity</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">O(1) Step Time</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Memory Footprint per Window</div>
            <div className="text-2xl font-bold text-white mt-1">&lt;128 KB</div>
          </div>
        </div>

        <DataGrid data={mockDABA} columns={columns} title="Active O(1) Sliding Window Aggregators" />
      </div>
    </MainLayout>
  );
}
