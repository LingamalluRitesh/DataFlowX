import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, Compass, CheckCircle, Database, Sparkles, ArrowRight } from 'lucide-react';

interface IVFPQIndexItem {
  index_name: string;
  n_clusters_k: number;
  n_probe_clusters: number;
  total_vectors_indexed: string;
  candidate_pruning_ratio: string;
  query_latency_ms: number;
  recall_rate: string;
}

const mockIVFPQ: IVFPQIndexItem[] = [
  { index_name: 'ivf_pq_ecom_products_v2', n_clusters_k: 1024, n_probe_clusters: 16, total_vectors_indexed: '10,000,000 Vectors', candidate_pruning_ratio: '98.4% Vectors Pruned', query_latency_ms: 0.95, recall_rate: '98.2% Top-10' },
  { index_name: 'ivf_pq_support_tickets_v1', n_clusters_k: 256, n_probe_clusters: 8, total_vectors_indexed: '2,500,000 Vectors', candidate_pruning_ratio: '96.8% Vectors Pruned', query_latency_ms: 0.65, recall_rate: '98.9% Top-10' },
  { index_name: 'ivf_pq_fraud_signatures_v3', n_clusters_k: 4096, n_probe_clusters: 32, total_vectors_indexed: '50,000,000 Vectors', candidate_pruning_ratio: '99.2% Vectors Pruned', query_latency_ms: 1.45, recall_rate: '97.5% Top-10' },
];

export default function IVFPQStudioPage() {
  const columns: DataGridColumn<IVFPQIndexItem>[] = [
    {
      key: 'index_name',
      header: 'IVF-PQ Index Table',
      render: (i) => (
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{i.index_name}</strong>
        </div>
      ),
    },
    { key: 'n_clusters_k', header: 'Voronoi Coarse Clusters (K)', render: (i) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">K={i.n_clusters_k}</span> },
    { key: 'n_probe_clusters', header: 'Probe Centroids (nprobe)', render: (i) => <span className="font-mono text-cyan-300">nprobe={i.n_probe_clusters}</span> },
    { key: 'total_vectors_indexed', header: 'Indexed Vectors', render: (i) => <span className="font-mono text-slate-300">{i.total_vectors_indexed}</span> },
    {
      key: 'candidate_pruning_ratio',
      header: 'Candidate Pruning',
      render: (i) => <span className="font-mono text-emerald-400 font-bold">{i.candidate_pruning_ratio}</span>,
    },
    {
      key: 'query_latency_ms',
      header: 'Search Latency',
      render: (i) => <span className="font-mono text-cyan-300 font-bold">{i.query_latency_ms} ms</span>,
    },
    {
      key: 'recall_rate',
      header: 'Recall Accuracy',
      render: (i) => <span className="font-mono text-emerald-400 font-bold">{i.recall_rate}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>IVF-PQ Inverted File Vector Index — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Compass className="w-7 h-7 text-cyan-400" />
            Inverted File with Product Quantization (IVF-PQ) Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Two-stage vector search: coarse Voronoi cell routing followed by sub-vector product quantization distance lookups.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Indexed Vectors</div>
            <div className="text-2xl font-bold text-white mt-1">62.5M Vectors</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Search Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0.95 ms (Sub-Millisecond)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Vector Pruning Efficiency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">98.4% Skipped</div>
          </div>
        </div>

        <DataGrid data={mockIVFPQ} columns={columns} title="Managed IVF-PQ Indexes" />
      </div>
    </MainLayout>
  );
}
