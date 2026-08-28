import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Search, Sparkles, Database, Layers, ArrowRight, BookOpen } from 'lucide-react';

interface SemanticSearchResultItem {
  asset_id: string;
  title: string;
  domain: string;
  combined_score: number;
  bm25_score: number;
  cosine_similarity: number;
  matched_excerpt: string;
}

const mockVectorResults: SemanticSearchResultItem[] = [
  { asset_id: 'gold.fact_orders', title: 'Daily Aggregated Order Invoices', domain: 'E-Commerce', combined_score: 0.0321, bm25_score: 8.42, cosine_similarity: 0.94, matched_excerpt: 'Aggregated revenue transactions, tax charges, and customer lifetime value metrics.' },
  { asset_id: 'silver.dim_customers', title: 'Canonical Customer 360 Dimension', domain: 'CRM', combined_score: 0.0289, bm25_score: 7.15, cosine_similarity: 0.91, matched_excerpt: 'Unified customer profiles with salted email hashes, loyalty tiers, and registration dates.' },
  { asset_id: 'gold.fact_payment_ledgers', title: 'Double-Entry General Ledger', domain: 'FinTech', combined_score: 0.0245, bm25_score: 6.80, cosine_similarity: 0.88, matched_excerpt: 'Balanced debits and credits across chart of accounts with currency conversions.' },
];

export default function VectorSearchStudioPage() {
  const [query, setQuery] = useState('find customer invoice and revenue transaction tables');

  const columns: DataGridColumn<SemanticSearchResultItem>[] = [
    {
      key: 'title',
      header: 'Catalog Asset Title',
      render: (r) => (
        <div>
          <strong className="text-white">{r.title}</strong>
          <div className="text-xs text-cyan-400 font-mono mt-0.5">{r.asset_id}</div>
        </div>
      ),
    },
    { key: 'domain', header: 'Domain' },
    {
      key: 'cosine_similarity',
      header: 'Semantic Similarity',
      render: (r) => (
        <span className="font-mono text-emerald-400 font-bold">
          {(r.cosine_similarity * 100).toFixed(1)}% match
        </span>
      ),
    },
    { key: 'bm25_score', header: 'BM25 Score', render: (r) => <span className="font-mono text-slate-300">{r.bm25_score.toFixed(2)}</span> },
    { key: 'matched_excerpt', header: 'Context Excerpt', sortable: false },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Semantic Vector & Schema Search — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sparkles className="w-7 h-7 text-purple-400" />
            AI Semantic Catalog & Vector Schema Search
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Search datasets, columns, and documentation using natural language queries powered by HNSW vector graphs and BM25 hybrid ranking.
          </p>
        </div>

        {/* Search Input Bar */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
          <div className="relative">
            <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about schemas, business terms, columns, or data assets..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-12 pr-28 py-3 text-sm text-white focus:outline-none focus:border-cyan-500 font-medium"
            />
            <button className="absolute right-2 top-2 px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
              Search
            </button>
          </div>
        </div>

        <DataGrid data={mockVectorResults} columns={columns} title="Hybrid Search Matches (HNSW + BM25 RRF)" />
      </div>
    </MainLayout>
  );
}
