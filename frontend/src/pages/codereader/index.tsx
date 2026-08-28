import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Code, FileCode, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface CodeASTChunkItem {
  chunk_index: number;
  symbol_name: string;
  symbol_type: 'CLASS' | 'FUNCTION' | 'METHOD';
  line_range: string;
  code_snippet_preview: string;
  token_count: number;
}

const mockCodeChunks: CodeASTChunkItem[] = [
  { chunk_index: 0, symbol_name: 'class HNSWIndex', symbol_type: 'CLASS', line_range: 'L12 - L84 (72 lines)', code_snippet_preview: 'class HNSWIndex:\n  def __init__(self, dim=128, m=16, ef=64):\n    self.dim = dim...', token_count: 340 },
  { chunk_index: 1, symbol_name: 'def search_knn', symbol_type: 'METHOD', line_range: 'L86 - L124 (38 lines)', code_snippet_preview: 'def search_knn(self, query_vec, k=10):\n  # Priority queue beam search...', token_count: 185 },
  { chunk_index: 2, symbol_name: 'class BroadcastHashJoin', symbol_type: 'CLASS', line_range: 'L10 - L55 (45 lines)', code_snippet_preview: 'class BroadcastHashJoin:\n  @classmethod\n  def execute_join(...):...', token_count: 220 },
];

export default function CodeReaderStudioPage() {
  const columns: DataGridColumn<CodeASTChunkItem>[] = [
    {
      key: 'symbol_name',
      header: 'AST Symbol Identifier',
      render: (c) => (
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{c.symbol_name}</strong>
        </div>
      ),
    },
    {
      key: 'symbol_type',
      header: 'AST Symbol Type',
      render: (c) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{c.symbol_type}</span>,
    },
    { key: 'line_range', header: 'Source Line Span', render: (c) => <span className="font-mono text-cyan-300 text-xs">{c.line_range}</span> },
    { key: 'code_snippet_preview', header: 'AST Code Preview', render: (c) => <span className="font-mono text-slate-300 text-[11px] truncate max-w-sm">{c.code_snippet_preview}</span> },
    {
      key: 'token_count',
      header: 'Token Count',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.token_count} tokens</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Syntax-Aware AST Code Chunker — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Code className="w-7 h-7 text-cyan-400" />
            Syntax-Aware Abstract Syntax Tree (AST) Source Code Chunker
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Grammar-accurate code decomposition splitting files at semantic class and function boundaries for codebase intelligence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Supported AST Grammars</div>
            <div className="text-2xl font-bold text-white mt-1">Python, TypeScript, SQL</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Symbol Extraction Accuracy</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Tree-sitter Accurate</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Chunking Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">&lt;0.5 ms / file</div>
          </div>
        </div>

        <DataGrid data={mockCodeChunks} columns={columns} title="Parsed AST Code Definition Chunks" />
      </div>
    </MainLayout>
  );
}
