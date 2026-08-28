import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitMerge, Sparkles, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface MatchedEntityItem {
  id: string;
  source_record: string;
  target_record: string;
  levenshtein_distance: number;
  similarity_score: number;
  soundex_match: boolean;
  match_verdict: 'EXACT_MATCH' | 'HIGH_CONFIDENCE_MATCH' | 'POTENTIAL_MATCH';
}

const mockMatches: MatchedEntityItem[] = [
  { id: 'match_01', source_record: 'Acme Corporation Inc', target_record: 'Acme Corp, Inc.', levenshtein_distance: 3, similarity_score: 0.850, soundex_match: true, match_verdict: 'HIGH_CONFIDENCE_MATCH' },
  { id: 'match_02', source_record: 'Robert C. Smith', target_record: 'Rob Smith', levenshtein_distance: 6, similarity_score: 0.600, soundex_match: true, match_verdict: 'HIGH_CONFIDENCE_MATCH' },
  { id: 'match_03', source_record: '123 Market St, San Francisco', target_record: '123 Market Street, SF', levenshtein_distance: 7, similarity_score: 0.750, soundex_match: false, match_verdict: 'HIGH_CONFIDENCE_MATCH' },
];

export default function StringSimilarityStudioPage() {
  const columns: DataGridColumn<MatchedEntityItem>[] = [
    {
      key: 'source_record',
      header: 'Source Record',
      render: (m) => (
        <div>
          <strong className="text-white text-xs">{m.source_record}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{m.id}</div>
        </div>
      ),
    },
    { key: 'target_record', header: 'Candidate Matched Record', render: (m) => <span className="text-cyan-300 font-mono text-xs">{m.target_record}</span> },
    { key: 'levenshtein_distance', header: 'Edit Distance', render: (m) => <span className="font-mono text-slate-300">{m.levenshtein_distance} edits</span> },
    {
      key: 'similarity_score',
      header: 'Fuzzy Similarity',
      render: (m) => <span className="font-mono text-emerald-400 font-bold">{(m.similarity_score * 100).toFixed(1)}% Match</span>,
    },
    {
      key: 'soundex_match',
      header: 'Phonetic Soundex',
      render: (m) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            m.soundex_match
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {m.soundex_match ? 'PHONETIC MATCH' : 'DIFF SOUNDEX'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Fuzzy String Similarity & Phonetics — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitMerge className="w-7 h-7 text-cyan-400" />
            Fuzzy String Similarity & Phonetic Record Linkage Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Levenshtein edit distances, Jaro-Winkler string similarity ratios, and Soundex phonetic hash encoding for deduplication.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Resolved Entity Clusters</div>
            <div className="text-2xl font-bold text-white mt-1">3 Clusters</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Entity Resolution Accuracy</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">99.4% Precision</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Linkage Execution Speed</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.8M pairs / sec</div>
          </div>
        </div>

        <DataGrid data={mockMatches} columns={columns} title="Active Entity Resolution Matches" />
      </div>
    </MainLayout>
  );
}
