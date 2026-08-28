import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Copy, Sparkles, CheckCircle, Activity, Filter, Radio } from 'lucide-react';

interface StreamDedupSessionItem {
  id: string;
  stream_topic: string;
  strategy: 'SLIDING_BLOOM_FILTER' | 'EXACT_REDIS_TTL' | 'ROCKSDB_KEY_VALUE';
  events_scanned_24h: number;
  duplicates_suppressed: number;
  duplicate_ratio_pct: number;
  status: 'ACTIVE' | 'WARMING';
}

const mockDedupSessions: StreamDedupSessionItem[] = [
  { id: 'dedup_01', stream_topic: 'events.clickstream_stream', strategy: 'SLIDING_BLOOM_FILTER', events_scanned_24h: 14200000, duplicates_suppressed: 84000, duplicate_ratio_pct: 0.59, status: 'ACTIVE' },
  { id: 'dedup_02', stream_topic: 'iot.sensor_telemetry', strategy: 'SLIDING_BLOOM_FILTER', events_scanned_24h: 38000000, duplicates_suppressed: 245000, duplicate_ratio_pct: 0.64, status: 'ACTIVE' },
  { id: 'dedup_03', stream_topic: 'financial.payment_events', strategy: 'EXACT_REDIS_TTL', events_scanned_24h: 1200000, duplicates_suppressed: 180, duplicate_ratio_pct: 0.015, status: 'ACTIVE' },
];

export default function StreamingDedupPage() {
  const columns: DataGridColumn<StreamDedupSessionItem>[] = [
    {
      key: 'stream_topic',
      header: 'Streaming Topic',
      render: (s) => (
        <div>
          <strong className="text-white font-mono text-xs">{s.stream_topic}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{s.id}</div>
        </div>
      ),
    },
    {
      key: 'strategy',
      header: 'Deduplication Engine',
      render: (s) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{s.strategy}</span>,
    },
    { key: 'events_scanned_24h', header: 'Events Scanned', render: (s) => <span className="font-mono text-slate-300">{s.events_scanned_24h.toLocaleString()}</span> },
    {
      key: 'duplicates_suppressed',
      header: 'Duplicate Events Suppressed',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.duplicates_suppressed.toLocaleString()} dropped</span>,
    },
    {
      key: 'duplicate_ratio_pct',
      header: 'Duplication Rate',
      render: (s) => <span className="font-mono text-amber-400">{s.duplicate_ratio_pct}%</span>,
    },
    {
      key: 'status',
      header: 'State',
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
        <title>Streaming Deduplication & Sliding Bloom Filters — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Filter className="w-7 h-7 text-cyan-400" />
            Streaming Deduplication & Multi-Window Sliding Bloom Filters
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Constant-memory sliding Bloom filters and exact state store key deduplication suppressing message duplicates in real time.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Duplicate Events Blocked</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">329,180 Duplicates</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Memory Footprint</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.2 MB / stream</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Processing Overhead</div>
            <div className="text-2xl font-bold text-white mt-1">&lt;0.05 ms / msg</div>
          </div>
        </div>

        <DataGrid data={mockDedupSessions} columns={columns} title="Active Deduplication Pipelines" />
      </div>
    </MainLayout>
  );
}
