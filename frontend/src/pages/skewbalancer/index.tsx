import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Scale, Activity, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface KeySkewItem {
  partition_key: string;
  source_stream: string;
  volume_percentage: number;
  skew_severity: 'HOTSPOT_CRITICAL' | 'MODERATE_SKEW' | 'BALANCED';
  salt_partitions_applied: number;
  post_balance_stddev: number;
}

const mockSkews: KeySkewItem[] = [
  { partition_key: 'merchant_id:AMZN_US', source_stream: 'events.orders.stream', volume_percentage: 28.4, skew_severity: 'HOTSPOT_CRITICAL', salt_partitions_applied: 8, post_balance_stddev: 1.2 },
  { partition_key: 'user_id:vip_corp_100', source_stream: 'events.orders.stream', volume_percentage: 18.2, skew_severity: 'MODERATE_SKEW', salt_partitions_applied: 4, post_balance_stddev: 0.8 },
  { partition_key: 'category_id:electronics', source_stream: 'events.catalog.stream', volume_percentage: 14.5, skew_severity: 'MODERATE_SKEW', salt_partitions_applied: 4, post_balance_stddev: 0.9 },
];

export default function SkewBalancerStudioPage() {
  const columns: DataGridColumn<KeySkewItem>[] = [
    {
      key: 'partition_key',
      header: 'Stream Partition Key',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Scale className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.partition_key}</strong>
        </div>
      ),
    },
    { key: 'source_stream', header: 'Stream Topic', render: (s) => <span className="font-mono text-slate-300 text-xs">{s.source_stream}</span> },
    {
      key: 'volume_percentage',
      header: 'Traffic Share',
      render: (s) => <span className="font-mono text-amber-400 font-bold">{s.volume_percentage}% of total</span>,
    },
    {
      key: 'salt_partitions_applied',
      header: 'Dynamic Salts',
      render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.salt_partitions_applied} Salts</span>,
    },
    {
      key: 'post_balance_stddev',
      header: 'Post-Balancing Variance',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">σ = {s.post_balance_stddev}</span>,
    },
    {
      key: 'skew_severity',
      header: 'Skew Status',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.skew_severity === 'HOTSPOT_CRITICAL'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {s.skew_severity}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Key-Skew & Hotspot Balancer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Scale className="w-7 h-7 text-cyan-400" />
            Key-Skew & Heavy Hotspot Partition Balancer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time key frequency counters detecting heavy partition keys and injecting dynamic deterministic salt prefixes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Salted Hotkeys</div>
            <div className="text-2xl font-bold text-white mt-1">3 Keyed Partitions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Worker Load Balance Variance</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">σ &lt; 1.0 (Evenly Distributed)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Auto-Mitigation Mode</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Dynamic Salting Active</div>
          </div>
        </div>

        <DataGrid data={mockSkews} columns={columns} title="Managed Key Skew Partitions" />
      </div>
    </MainLayout>
  );
}
