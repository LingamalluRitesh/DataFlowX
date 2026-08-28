import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Compass, Cpu, CheckCircle, Database, Layers, Sparkles } from 'lucide-react';

interface HNSWIndexItem {
  index_name: string;
  dimension: number;
  total_vectors: string;
  m_neighbors: number;
  ef_construction: number;
  recall_rate_pct: number;
  query_latency_ms: number;
}

const mockHNSW: HNSWIndexItem[] = [
  { index_name: 'product_multimodal_embeddings_v3', dimension: 1536, total_vectors: '10,000,000 Vectors', m_neighbors: 16, ef_construction: 64, recall_rate_pct: 99.2, query_latency_ms: 1.45 },
  { index_name: 'customer_support_transcripts_rag', dimension: 768, total_vectors: '2,500,000 Vectors', m_neighbors: 32, ef_construction: 128, recall_rate_pct: 99.8, query_latency_ms: 0.85 },
  { index_name: 'financial_fraud_entity_clusters', dimension: 256, total_vectors: '50,000,000 Vectors', m_neighbors: 16, ef_construction: 64, recall_rate_pct: 98.6, query_latency_ms: 2.10 },
];

export default function HNSWVectorIndexPage() {
  const columns: DataGridColumn<HNSWIndexItem>[] = [
    { key: 'index_name', header: 'Vector Index Table', render: (h) => <strong className="text-white font-mono text-xs">{h.index_name}</strong> },
    { key: 'dimension', header: 'Embedding Dimension', render: (h) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{h.dimension}-dim</span> },
    { key: 'total_vectors', header: 'Total Vectors', render: (h) => <span className="font-mono text-slate-300">{h.total_vectors}</span> },
    {
      key: 'm_neighbors',
      header: 'HNSW Graph Params (M / ef)',
      render: (h) => <span className="font-mono text-cyan-300 text-xs">M={h.m_neighbors}, ef={h.ef_construction}</span>,
    },
    {
      key: 'recall_rate_pct',
      header: 'ANN Top-10 Recall',
      render: (h) => <span className="font-mono text-emerald-400 font-bold">{h.recall_rate_pct}% Recall</span>,
    },
    {
      key: 'query_latency_ms',
      header: 'Search Latency',
      render: (h) => <span className="font-mono text-cyan-300 font-bold">{h.query_latency_ms} ms</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>HNSW Vector Graph Index & ANN Search — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Compass className="w-7 h-7 text-cyan-400" />
            HNSW, LSH & IVF-PQ Vector Database & ANN Indexing
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Hierarchical Navigable Small World graphs, Locality-Sensitive Hashing, and product quantization for billion-scale similarity search.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Indexed Vectors</div>
            <div className="text-2xl font-bold text-white mt-1">62.5M Vectors</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average ANN Recall</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">99.2% Accuracy</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Query Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.46 ms</div>
          </div>
        </div>

        <DataGrid data={mockHNSW} columns={columns} title="Managed Vector Graph Indexes" />
      </div>
    </MainLayout>
  );
}
