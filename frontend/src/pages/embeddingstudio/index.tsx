import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Sparkles, Compass, CheckCircle, Database, Layers, ArrowRight, Play } from 'lucide-react';

interface SemanticSearchItem {
  rank: number;
  document_snippet: string;
  source_dataset: string;
  cosine_similarity: number;
  embedding_norm: number;
}

const mockEmbeddings: SemanticSearchItem[] = [
  { rank: 1, document_snippet: 'Apache Iceberg ACID catalog specifications and hidden partition transforms.', source_dataset: 'docs.lakehouse_architecture', cosine_similarity: 0.942, embedding_norm: 1.0 },
  { rank: 2, document_snippet: 'Delta Lake transaction log replay and vacuum compaction cleanup procedures.', source_dataset: 'docs.storage_internals', cosine_similarity: 0.885, embedding_norm: 1.0 },
  { rank: 3, document_snippet: 'Hierarchical Navigable Small World (HNSW) vector search beam width algorithms.', source_dataset: 'docs.vector_rag_engine', cosine_similarity: 0.812, embedding_norm: 1.0 },
];

export default function EmbeddingStudioPage() {
  const [queryText, setQueryText] = useState("Explain how Apache Iceberg hidden partitioning works");

  const columns: DataGridColumn<SemanticSearchItem>[] = [
    {
      key: 'rank',
      header: 'Rank',
      render: (s) => (
        <span className="w-6 h-6 rounded-full bg-slate-800 text-cyan-400 font-mono text-xs flex items-center justify-center font-bold">
          #{s.rank}
        </span>
      ),
    },
    { key: 'document_snippet', header: 'Retrieved Document Chunks', render: (s) => <strong className="text-white text-xs">{s.document_snippet}</strong> },
    { key: 'source_dataset', header: 'Knowledge Source', render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.source_dataset}</span> },
    {
      key: 'cosine_similarity',
      header: 'Cosine Similarity Score',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{(s.cosine_similarity * 100).toFixed(1)}% Match</span>,
    },
    { key: 'embedding_norm', header: 'L2 Norm', render: (s) => <span className="font-mono text-slate-400 text-xs">L2={s.embedding_norm.toFixed(1)}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vector Embeddings & Semantic Search — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sparkles className="w-7 h-7 text-cyan-400" />
            Vector Embedding Inference & Semantic Search Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time neural text embedding generation, micro-batching inference queues, and cosine similarity vector retrieval.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Embedding Dimensions</div>
            <div className="text-2xl font-bold text-white mt-1">128-dim Float32</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Inference Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;1.2 ms / batch</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Normalization Status</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Unit L2-Normalized</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex gap-3 items-center">
          <input
            type="text"
            value={queryText}
            onChange={(e) => setQueryText(e.target.value)}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white text-xs focus:outline-none focus:border-cyan-500 font-mono"
            placeholder="Type query to test semantic similarity embedding..."
          />
          <button className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5">
            <Play className="w-3.5 h-3.5" /> Vectorize & Search
          </button>
        </div>

        <DataGrid data={mockEmbeddings} columns={columns} title="Top-K Semantic Similarity Matches" />
      </div>
    </MainLayout>
  );
}
