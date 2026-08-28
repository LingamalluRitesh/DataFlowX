import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Hash, Sparkles, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface LSHBucketItem {
  table_id: number;
  hash_bucket_code: string;
  indexed_vector_count: number;
  candidate_recall_pct: number;
  query_latency_us: number;
  collision_quality: 'HIGH_SELECTIVITY' | 'BALANCED';
}

const mockLSH: LSHBucketItem[] = [
  { table_id: 1, hash_bucket_code: '0b1101001011001101', indexed_vector_count: 1420, candidate_recall_pct: 98.4, query_latency_us: 120, collision_quality: 'HIGH_SELECTIVITY' },
  { table_id: 2, hash_bucket_code: '0b0010110100110010', indexed_vector_count: 980, candidate_recall_pct: 97.9, query_latency_us: 95, collision_quality: 'HIGH_SELECTIVITY' },
  { table_id: 3, hash_bucket_code: '0b1111000010101111', indexed_vector_count: 2150, candidate_recall_pct: 99.1, query_latency_us: 160, collision_quality: 'BALANCED' },
];

export default function LSHStudioPage() {
  const columns: DataGridColumn<LSHBucketItem>[] = [
    {
      key: 'table_id',
      header: 'LSH Hash Table',
      render: (l) => (
        <div className="flex items-center gap-2">
          <Hash className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">Table #{l.table_id}</strong>
        </div>
      ),
    },
    { key: 'hash_bucket_code', header: 'Hyperplane Hash Code (16-bit)', render: (l) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{l.hash_bucket_code}</span> },
    { key: 'indexed_vector_count', header: 'Vectors in Bucket', render: (l) => <span className="font-mono text-slate-300">{l.indexed_vector_count.toLocaleString()} vectors</span> },
    {
      key: 'candidate_recall_pct',
      header: 'Candidate Set Recall',
      render: (l) => <span className="font-mono text-emerald-400 font-bold">{l.candidate_recall_pct}% Recall</span>,
    },
    {
      key: 'query_latency_us',
      header: 'Bucket Lookup Latency',
      render: (l) => <span className="font-mono text-cyan-300 font-bold">{l.query_latency_us} μs</span>,
    },
    {
      key: 'collision_quality',
      header: 'Partition Quality',
      render: (l) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {l.collision_quality}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Locality-Sensitive Hashing (LSH) — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Hash className="w-7 h-7 text-cyan-400" />
            Locality-Sensitive Hashing (LSH) Random Hyperplane Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Random hyperplane projection hashing for constant-time candidate filtering in billion-scale cosine similarity searches.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Hash Tables</div>
            <div className="text-2xl font-bold text-white mt-1">4 Tables (16-bit)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Candidate Filtering Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">115 μs / query</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Candidate Recall</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">98.5% Top-K Recall</div>
          </div>
        </div>

        <DataGrid data={mockLSH} columns={columns} title="Random Hyperplane Hash Buckets" />
      </div>
    </MainLayout>
  );
}
