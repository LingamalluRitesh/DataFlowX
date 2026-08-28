import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Table, Database, CheckCircle, Clock, Layers, ArrowRight } from 'lucide-react';

interface TableRowChunkItem {
  chunk_index: number;
  source_table: string;
  serialized_prose: string;
  injected_headers: string[];
  embedding_ready: boolean;
}

const mockRowChunks: TableRowChunkItem[] = [
  { chunk_index: 0, source_table: 'gold.fact_orders', serialized_prose: 'order_id: 98124, customer_id: C_4412, order_total: $245.50, status: COMPLETED, created_at: 2026-08-29', injected_headers: ['order_id', 'customer_id', 'order_total', 'status'], embedding_ready: true },
  { chunk_index: 1, source_table: 'gold.fact_orders', serialized_prose: 'order_id: 98125, customer_id: C_9910, order_total: $1,420.00, status: COMPLETED, created_at: 2026-08-29', injected_headers: ['order_id', 'customer_id', 'order_total', 'status'], embedding_ready: true },
  { chunk_index: 2, source_table: 'silver.dim_customers', serialized_prose: 'customer_id: C_4412, name: Acme Logistics, country: US, tier: ENTERPRISE, lifetime_value: $84,200', injected_headers: ['customer_id', 'name', 'country', 'tier'], embedding_ready: true },
];

export default function TableChunkerStudioPage() {
  const columns: DataGridColumn<TableRowChunkItem>[] = [
    {
      key: 'chunk_index',
      header: 'Row Chunk ID',
      render: (t) => (
        <span className="font-mono text-cyan-300 font-bold flex items-center gap-1.5">
          <Table className="w-3.5 h-3.5" /> Chunk #{t.chunk_index}
        </span>
      ),
    },
    { key: 'source_table', header: 'Source Table', render: (t) => <strong className="text-white font-mono text-xs">{t.source_table}</strong> },
    { key: 'serialized_prose', header: 'Contextual Injected Prose', render: (t) => <span className="font-mono text-slate-300 text-xs truncate max-w-sm">{t.serialized_prose}</span> },
    {
      key: 'injected_headers',
      header: 'Preserved Schema Headers',
      render: (t) => (
        <div className="flex flex-wrap gap-1">
          {t.injected_headers.map((h) => (
            <span key={h} className="bg-slate-800 text-purple-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {h}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'embedding_ready',
      header: 'Vector Status',
      render: (t) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          READY FOR RAG
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Contextual Table Row Chunker — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Table className="w-7 h-7 text-cyan-400" />
            Contextual Header-Injected Tabular Data Chunker
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Converts structured tabular rows into schema-contextual natural language prose chunks for LLM RAG pipelines.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tabular Schema Retention</div>
            <div className="text-2xl font-bold text-white mt-1">100% Header Preserved</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Row Serialization Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4.2M rows / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">RAG Vector Compatibility</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">HNSW / IVF-PQ Ready</div>
          </div>
        </div>

        <DataGrid data={mockRowChunks} columns={columns} title="Contextual Tabular Prose Chunks" />
      </div>
    </MainLayout>
  );
}
