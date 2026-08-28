import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Disc, Layers, CheckCircle, Database, Sparkles, ArrowRight } from 'lucide-react';

interface PQCodebookItem {
  codebook_id: string;
  dimension: number;
  subvectors_m: number;
  k_centroids_per_subspace: number;
  raw_vector_size_bytes: number;
  compressed_pq_bytes: number;
  compression_factor: string;
}

const mockCodebooks: PQCodebookItem[] = [
  { codebook_id: 'pq_1536_sub16', dimension: 1536, subvectors_m: 16, k_centroids_per_subspace: 256, raw_vector_size_bytes: 6144, compressed_pq_bytes: 16, compression_factor: '384x (99.7% reduction)' },
  { codebook_id: 'pq_768_sub8', dimension: 768, subvectors_m: 8, k_centroids_per_subspace: 256, raw_vector_size_bytes: 3072, compressed_pq_bytes: 8, compression_factor: '384x (99.7% reduction)' },
  { codebook_id: 'pq_256_sub8', dimension: 256, subvectors_m: 8, k_centroids_per_subspace: 256, raw_vector_size_bytes: 1024, compressed_pq_bytes: 8, compression_factor: '128x (99.2% reduction)' },
];

export default function PQCompressorPage() {
  const columns: DataGridColumn<PQCodebookItem>[] = [
    {
      key: 'codebook_id',
      header: 'PQ Codebook ID',
      render: (p) => (
        <div className="flex items-center gap-2">
          <Disc className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{p.codebook_id}</strong>
        </div>
      ),
    },
    { key: 'dimension', header: 'Embedding Dim', render: (p) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{p.dimension}-dim</span> },
    { key: 'subvectors_m', header: 'Subspaces (M)', render: (p) => <span className="font-mono text-slate-300">{p.subvectors_m} subspaces</span> },
    { key: 'k_centroids_per_subspace', header: 'Centroids / Subspace (K)', render: (p) => <span className="font-mono text-cyan-300">K={p.k_centroids_per_subspace} (8-bit)</span> },
    {
      key: 'compression_factor',
      header: 'Memory Compression Ratio',
      render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.compression_factor}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Product Quantization (PQ) Vector Compression — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Disc className="w-7 h-7 text-cyan-400" />
            Product Quantization (PQ) Vector Compression Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Splits high-dimensional vector embeddings into orthogonal subspaces with 8-bit centroid byte codes, reducing RAM usage by 384x.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average RAM Reduction</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">384x Memory Compression</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Asymmetric Distance Computation (ADC)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">SIMD Lookups Active</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Quantization Accuracy</div>
            <div className="text-2xl font-bold text-white mt-1">97.8% Top-10 Recall</div>
          </div>
        </div>

        <DataGrid data={mockCodebooks} columns={columns} title="Managed Product Quantization Codebooks" />
      </div>
    </MainLayout>
  );
}
