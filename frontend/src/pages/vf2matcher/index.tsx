import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Network, ShieldAlert, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface VF2PatternMatchItem {
  match_id: string;
  pattern_name: string;
  mapped_nodes: string;
  subgraph_size_nodes: number;
  confidence_score: number;
  risk_category: 'HIGH_RISK_FRAUD_RING' | 'CYCLIC_TRANSFER' | 'ANOMALOUS_CLUSTER';
}

const mockVF2: VF2PatternMatchItem[] = [
  { match_id: 'vf2_match_01', pattern_name: 'Circular Money Laundering Ring (A->B->C->A)', mapped_nodes: '{A: usr_890, B: acc_112, C: mkt_441}', subgraph_size_nodes: 3, confidence_score: 0.985, risk_category: 'HIGH_RISK_FRAUD_RING' },
  { match_id: 'vf2_match_02', pattern_name: 'Bipartite User-Device Collusion Cluster', mapped_nodes: '{U1: usr_102, U2: usr_103, D1: dev_881}', subgraph_size_nodes: 3, confidence_score: 0.940, risk_category: 'ANOMALOUS_CLUSTER' },
  { match_id: 'vf2_match_03', pattern_name: 'High-Frequency Rapid Transfer Cascade', mapped_nodes: '{Src: usr_440, Rel: TRANSFERRED, Tgt: usr_991}', subgraph_size_nodes: 2, confidence_score: 0.912, risk_category: 'CYCLIC_TRANSFER' },
];

export default function VF2MatcherStudioPage() {
  const columns: DataGridColumn<VF2PatternMatchItem>[] = [
    {
      key: 'match_id',
      header: 'Pattern Match ID',
      render: (v) => (
        <div className="flex items-center gap-2">
          <Network className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{v.match_id}</strong>
        </div>
      ),
    },
    { key: 'pattern_name', header: 'Target Subgraph Pattern', render: (v) => <span className="text-slate-300 text-xs">{v.pattern_name}</span> },
    { key: 'mapped_nodes', header: 'Mapped Graph Entities', render: (v) => <span className="font-mono text-cyan-300 text-xs">{v.mapped_nodes}</span> },
    { key: 'subgraph_size_nodes', header: 'Subgraph Size', render: (v) => <span className="font-mono text-slate-300">{v.subgraph_size_nodes} nodes</span> },
    {
      key: 'confidence_score',
      header: 'Isomorphism Score',
      render: (v) => <span className="font-mono text-emerald-400 font-bold">{(v.confidence_score * 100).toFixed(1)}% Match</span>,
    },
    {
      key: 'risk_category',
      header: 'Risk Classification',
      render: (v) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            v.risk_category === 'HIGH_RISK_FRAUD_RING'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {v.risk_category}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>VF2 Subgraph Pattern Matching — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Network className="w-7 h-7 text-cyan-400" />
            VF2 Subgraph Pattern Matching & Fraud Ring Detection
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Exact and approximate subgraph isomorphism search identifying fraud rings, mule accounts, and collusion topologies.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Detected Fraud Topologies</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Matches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">VF2 Algorithm Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">1.8 ms / graph</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Isomorphism Precision</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Deterministic</div>
          </div>
        </div>

        <DataGrid data={mockVF2} columns={columns} title="Active Subgraph Isomorphism Patterns" />
      </div>
    </MainLayout>
  );
}
