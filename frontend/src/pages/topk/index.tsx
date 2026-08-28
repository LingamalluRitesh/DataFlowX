import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Award, Flame, CheckCircle, Activity, Layers, Zap } from 'lucide-react';

interface HeavyHitterItem {
  rank: number;
  item_key: string;
  stream_name: string;
  estimated_count: number;
  max_error_bound: number;
  traffic_share_pct: number;
}

const mockTopK: HeavyHitterItem[] = [
  { rank: 1, item_key: 'product_id:98124 (MacBook Pro M3)', stream_name: 'events.ecom_pageviews', estimated_count: 142000, max_error_bound: 120, traffic_share_pct: 18.4 },
  { rank: 2, item_key: 'product_id:88129 (Sony WH-1000XM5)', stream_name: 'events.ecom_pageviews', estimated_count: 98000, max_error_bound: 120, traffic_share_pct: 12.7 },
  { rank: 3, item_key: 'endpoint:/api/v1/checkout', stream_name: 'ingress.api_gateway_logs', estimated_count: 85000, max_error_bound: 120, traffic_share_pct: 11.0 },
  { rank: 4, item_key: 'user_agent:iPhone16,1', stream_name: 'events.mobile_telemetry', estimated_count: 64000, max_error_bound: 120, traffic_share_pct: 8.3 },
];

export default function HeavyHittersPage() {
  const columns: DataGridColumn<HeavyHitterItem>[] = [
    {
      key: 'rank',
      header: 'Rank',
      render: (t) => (
        <span className="w-6 h-6 rounded-full bg-slate-800 text-cyan-400 font-mono text-xs flex items-center justify-center font-bold">
          #{t.rank}
        </span>
      ),
    },
    { key: 'item_key', header: 'Heavy-Hitter Entity Key', render: (t) => <strong className="text-white font-mono text-xs">{t.item_key}</strong> },
    { key: 'stream_name', header: 'Streaming Topic', render: (t) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{t.stream_name}</span> },
    { key: 'estimated_count', header: 'Estimated Frequency', render: (t) => <span className="font-mono text-emerald-400 font-bold">{t.estimated_count.toLocaleString()} occurrences</span> },
    { key: 'max_error_bound', header: 'Max Bound Error (ε)', render: (t) => <span className="font-mono text-slate-400">±{t.max_error_bound}</span> },
    {
      key: 'traffic_share_pct',
      header: 'Stream Dominance',
      render: (t) => <span className="font-mono text-cyan-300 font-bold">{t.traffic_share_pct}%</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Top-K Heavy Hitters — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Award className="w-7 h-7 text-cyan-400" />
            Streaming Top-K & Space-Saving Heavy-Hitters Console
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Metwally Space-Saving and Misra-Gries streaming algorithms tracking the top frequent items with deterministic error bounds.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tracked Heavy Hitters</div>
            <div className="text-2xl font-bold text-white mt-1">Top-100 Items</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Overestimation Error Bound</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;0.08% Error (ε)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">State Memory Size</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">64 KB per stream</div>
          </div>
        </div>

        <DataGrid data={mockTopK} columns={columns} title="Real-Time Heavy-Hitter Frequencies" />
      </div>
    </MainLayout>
  );
}
