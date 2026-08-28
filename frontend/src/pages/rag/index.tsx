import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Search, Sparkles, Database, Layers, CheckCircle, Flame } from 'lucide-react';

interface RAGDocumentChunkItem {
  chunk_id: string;
  source_doc: string;
  text_snippet: string;
  dense_cosine_score: number;
  sparse_bm25_score: number;
  rrf_fused_score: number;
}

const mockRAGResults: RAGDocumentChunkItem[] = [
  { chunk_id: 'chk_01', source_doc: 'lakehouse_architecture_whitepaper.pdf', text_snippet: 'Delta Lake ACID transactions use optimistic concurrency control and JSON write-ahead logs...', dense_cosine_score: 0.892, sparse_bm25_score: 14.8, rrf_fused_score: 0.0327 },
  { chunk_id: 'chk_02', source_doc: 'orchestration_best_practices.md', text_snippet: 'SIMD-accelerated physical operators evaluate vectorized filters at over 40M rows per second...', dense_cosine_score: 0.841, sparse_bm25_score: 12.4, rrf_fused_score: 0.0294 },
  { chunk_id: 'chk_03', source_doc: 'differential_privacy_guidelines.docx', text_snippet: 'Laplace perturbation mechanism guarantees ε-differential privacy across aggregated queries...', dense_cosine_score: 0.795, sparse_bm25_score: 9.8, rrf_fused_score: 0.0241 },
];

export default function HybridRAGStudioPage() {
  const [searchQuery, setSearchQuery] = useState('ACID transactions and SIMD physical operators');

  const columns: DataGridColumn<RAGDocumentChunkItem>[] = [
    {
      key: 'source_doc',
      header: 'Source Document',
      render: (r) => (
        <div>
          <strong className="text-white font-mono text-xs">{r.source_doc}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{r.chunk_id}</div>
        </div>
      ),
    },
    { key: 'text_snippet', header: 'Chunk Text Content', sortable: false },
    { key: 'dense_cosine_score', header: 'Dense Vector Cosine', render: (r) => <span className="font-mono text-cyan-300 font-bold">{r.dense_cosine_score}</span> },
    { key: 'sparse_bm25_score', header: 'Sparse BM25', render: (r) => <span className="font-mono text-purple-300">{r.sparse_bm25_score}</span> },
    {
      key: 'rrf_fused_score',
      header: 'Hybrid RRF Score',
      render: (r) => <span className="font-mono text-emerald-400 font-bold">{r.rrf_fused_score}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Hybrid Dense + Sparse RAG Search — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Search className="w-7 h-7 text-cyan-400" />
            Hybrid Dense + Sparse RAG Retrieval & Vector Embeddings
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Reciprocal Rank Fusion (RRF) combining dense 1536-dim vector cosine similarity with Okapi BM25 sparse inverted indexes.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs font-semibold text-slate-400 uppercase mb-2">Hybrid Semantic Search Query</div>
          <div className="flex gap-3">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
            />
            <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow">
              <Sparkles className="w-3.5 h-3.5" /> Execute Hybrid Search
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Indexed Document Chunks</div>
            <div className="text-2xl font-bold text-white mt-1">45,000 Chunks</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Search Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">8.2 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Dense/Sparse Weighting</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">RRF (k=60)</div>
          </div>
        </div>

        <DataGrid data={mockRAGResults} columns={columns} title="Top Hybrid Search Results" />
      </div>
    </MainLayout>
  );
}
