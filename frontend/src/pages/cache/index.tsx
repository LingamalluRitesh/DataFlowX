import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { HardDrive, Activity, Zap, CheckCircle, Trash2, RefreshCw } from 'lucide-react';

interface CacheEntryItem {
  cache_key: string;
  query_snippet: string;
  segment: 'PROTECTED' | 'PROBATIONARY';
  hit_count: number;
  memory_kb: number;
  expires_in_seconds: number;
}

const mockCacheEntries: CacheEntryItem[] = [
  { cache_key: 'c9a8b7c6d5e4f3a2', query_snippet: 'SELECT * FROM dim_customers WHERE country = "US"', segment: 'PROTECTED', hit_count: 1420, memory_kb: 450, expires_in_seconds: 240 },
  { cache_key: 'b1c2d3e4f5a6b7c8', query_snippet: 'SELECT SUM(amount) FROM fact_orders GROUP BY date', segment: 'PROTECTED', hit_count: 890, memory_kb: 120, expires_in_seconds: 180 },
  { cache_key: 'f9e8d7c6b5a43210', query_snippet: 'SELECT * FROM iot_telemetry WHERE device_id = 99', segment: 'PROBATIONARY', hit_count: 3, memory_kb: 85, expires_in_seconds: 60 },
];

export default function DistributedCachePage() {
  const columns: DataGridColumn<CacheEntryItem>[] = [
    { key: 'cache_key', header: 'Cache Key Hash', render: (c) => <strong className="text-cyan-400 font-mono text-xs">{c.cache_key}</strong> },
    { key: 'query_snippet', header: 'Parameterized SQL Snippet', render: (c) => <span className="font-mono text-slate-300 text-xs">{c.query_snippet}</span> },
    {
      key: 'segment',
      header: 'SLRU Segment',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.segment === 'PROTECTED'
              ? 'bg-purple-950 text-purple-400 border border-purple-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {c.segment}
        </span>
      ),
    },
    { key: 'hit_count', header: 'Cache Hits', render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.hit_count.toLocaleString()} hits</span> },
    { key: 'memory_kb', header: 'Memory Size', render: (c) => <span className="font-mono text-slate-400">{c.memory_kb} KB</span> },
    { key: 'expires_in_seconds', header: 'TTL Remaining', render: (c) => <span className="font-mono text-amber-400">{c.expires_in_seconds}s</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Distributed Query Cache & Memory — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <HardDrive className="w-7 h-7 text-cyan-400" />
            Distributed Query Cache & Scan-Resistant SLRU Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            2-Segmented LRU in-memory query cache with tag-based Lakehouse snapshot invalidation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Overall Cache Hit Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">94.8% Hits</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Allocated Cache Memory</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">655 KB / 100 MB</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Latency Saved</div>
            <div className="text-2xl font-bold text-purple-400 mt-1">120 ms / query</div>
          </div>
        </div>

        <DataGrid data={mockCacheEntries} columns={columns} title="Active Query Result Cache Entries" />
      </div>
    </MainLayout>
  );
}
