import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Scissors, FileText, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface TextChunkItem {
  chunk_index: number;
  document_name: string;
  chunk_text_preview: string;
  token_count: number;
  char_range: string;
  overlap_tokens: number;
}

const mockTextChunks: TextChunkItem[] = [
  { chunk_index: 0, document_name: 'architecture_specification_v2.md', chunk_text_preview: 'The DataFlowX Lakehouse platform unifies streaming and batch execution via Apache Arrow...', token_count: 210, char_range: '0 - 890', overlap_tokens: 25 },
  { chunk_index: 1, document_name: 'architecture_specification_v2.md', chunk_text_preview: 'Apache Iceberg snapshot metadata structures provide ACID linear serializable isolation...', token_count: 240, char_range: '810 - 1750', overlap_tokens: 25 },
  { chunk_index: 2, document_name: 'architecture_specification_v2.md', chunk_text_preview: 'Vector indexing uses Hierarchical Navigable Small World graphs for sub-millisecond retrieval...', token_count: 195, char_range: '1680 - 2490', overlap_tokens: 25 },
];

export default function ChunkerStudioPage() {
  const columns: DataGridColumn<TextChunkItem>[] = [
    {
      key: 'chunk_index',
      header: 'Chunk Sequence',
      render: (c) => (
        <span className="font-mono text-cyan-300 font-bold flex items-center gap-1.5">
          <Scissors className="w-3.5 h-3.5" /> Chunk #{c.chunk_index}
        </span>
      ),
    },
    { key: 'document_name', header: 'Source Document', render: (c) => <strong className="text-white font-mono text-xs">{c.document_name}</strong> },
    { key: 'chunk_text_preview', header: 'Chunk Text Content', render: (c) => <span className="text-slate-300 text-xs truncate max-w-sm">{c.chunk_text_preview}</span> },
    {
      key: 'token_count',
      header: 'Token Length',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.token_count} tokens</span>,
    },
    { key: 'char_range', header: 'Character Span', render: (c) => <span className="font-mono text-slate-400 text-xs">{c.char_range}</span> },
    {
      key: 'overlap_tokens',
      header: 'Sliding Overlap',
      render: (c) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.overlap_tokens} tokens</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Semantic Sentence & Paragraph Chunker — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Scissors className="w-7 h-7 text-cyan-400" />
            Semantic Sentence & Paragraph Document Chunker Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Recursive sentence boundary chunking preserving natural semantic prose context and sliding overlap for RAG vector pipelines.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Chunking Window Target</div>
            <div className="text-2xl font-bold text-white mt-1">256 Tokens (Sliding)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Overlap Boundary</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">25 Tokens Overlap</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Sentence Boundary Precision</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Boundary Clean</div>
          </div>
        </div>

        <DataGrid data={mockTextChunks} columns={columns} title="Extracted Semantic Document Chunks" />
      </div>
    </MainLayout>
  );
}
