import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cpu, Plus, Sparkles, Filter, Code, CheckCircle, Database } from 'lucide-react';

interface TransformOperatorItem {
  id: string;
  name: string;
  category: 'CLEANSING' | 'WINDOW' | 'CRYPTO' | 'NLP' | 'GEOSPATIAL' | 'RESHAPING' | 'SCD';
  description: string;
  vectorized: boolean;
  doc_url: string;
}

const mockOperators: TransformOperatorItem[] = [
  { id: 'op_window_lead_lag', name: 'LeadLagOperator', category: 'WINDOW', description: 'Calculates partition offsets and shifts for moving trend analysis', vectorized: true, doc_url: '/docs/transforms#window' },
  { id: 'op_crypto_salt_hash', name: 'SaltedHashTokenizeOperator', category: 'CRYPTO', description: 'Irreversible cryptographic SHA-256 / SHA-512 salting for GDPR compliance', vectorized: true, doc_url: '/docs/transforms#crypto' },
  { id: 'op_scd_type2', name: 'SCDType2Operator', category: 'SCD', description: 'Maintains historical versioning with effective_from / effective_to dates and is_current flag', vectorized: true, doc_url: '/docs/transforms#scd2' },
  { id: 'op_geo_haversine', name: 'HaversineDistanceOperator', category: 'GEOSPATIAL', description: 'Vectorized Great-Circle distance calculation in kilometers between coordinate pairs', vectorized: true, doc_url: '/docs/transforms#geospatial' },
  { id: 'op_fuzzy_jaro', name: 'FuzzyStringMatchOperator', category: 'CLEANSING', description: 'Computes Jaro-Winkler, Levenshtein, and Soundex phonetic string similarities', vectorized: true, doc_url: '/docs/transforms#fuzzy' },
  { id: 'op_json_flattener', name: 'DeepJSONFlattenerOperator', category: 'RESHAPING', description: 'Recursively flattens deeply nested JSON structures into tabular columns', vectorized: true, doc_url: '/docs/transforms#json' },
];

export default function TransformationsIndexPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const filtered = selectedCategory === 'ALL' ? mockOperators : mockOperators.filter((o) => o.category === selectedCategory);

  const columns: DataGridColumn<TransformOperatorItem>[] = [
    {
      key: 'name',
      header: 'Operator Class Name',
      render: (o) => (
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-purple-400" />
          <strong className="text-white font-mono">{o.name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Transformation Category',
      render: (o) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            o.category === 'WINDOW'
              ? 'bg-cyan-950 text-cyan-400 border border-cyan-800'
              : o.category === 'CRYPTO'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : o.category === 'SCD'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-purple-950 text-purple-400 border border-purple-800'
          }`}
        >
          {o.category}
        </span>
      ),
    },
    { key: 'description', header: 'Description', sortable: false },
    {
      key: 'vectorized',
      header: 'Engine Acceleration',
      render: (o) => (
        <span className="text-emerald-400 text-xs font-semibold flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5" /> Vectorized NumPy
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Transformation Operators & Rules — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Cpu className="w-7 h-7 text-purple-400" />
            Vectorized Transformation Operator Catalog
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Browse and configure over 30+ built-in high-performance data transformation operators and analytical window functions.
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {['ALL', 'WINDOW', 'CRYPTO', 'SCD', 'GEOSPATIAL', 'CLEANSING', 'RESHAPING'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                selectedCategory === cat
                  ? 'bg-purple-600 text-white font-semibold'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <DataGrid data={filtered} columns={columns} title="Transformation Operators" />
      </div>
    </MainLayout>
  );
}
