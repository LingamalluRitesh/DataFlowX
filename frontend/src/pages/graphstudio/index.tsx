import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Share2, Activity, CheckCircle, Network, Layers, GitBranch } from 'lucide-react';

interface GraphQueryResult {
  source_entity: string;
  relationship: string;
  target_entity: string;
  shortest_path_hops: number;
  pagerank_influence: number;
  fraud_ring_detected: boolean;
}

const mockGraph: GraphQueryResult[] = [
  { source_entity: 'User:alice_901', relationship: 'TRANSFERRED_TO ($14,200)', target_entity: 'Merchant:crypto_exchange_us', shortest_path_hops: 1, pagerank_influence: 0.0425, fraud_ring_detected: false },
  { source_entity: 'Account:acc_8812', relationship: 'CO_SIGNER_OF', target_entity: 'Company:shell_holdings_llc', shortest_path_hops: 2, pagerank_influence: 0.0890, fraud_ring_detected: true },
  { source_entity: 'IP:192.168.1.100', relationship: 'ACCESSED_DEVICE', target_entity: 'Device:macbook_pro_m3', shortest_path_hops: 1, pagerank_influence: 0.0120, fraud_ring_detected: false },
];

export default function GraphStudioPage() {
  const columns: DataGridColumn<GraphQueryResult>[] = [
    { key: 'source_entity', header: 'Source Graph Node', render: (g) => <strong className="text-white font-mono text-xs">{g.source_entity}</strong> },
    {
      key: 'relationship',
      header: 'Directed Edge (Relationship)',
      render: (g) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{g.relationship}</span>,
    },
    { key: 'target_entity', header: 'Target Graph Node', render: (g) => <span className="font-mono text-cyan-300 text-xs">{g.target_entity}</span> },
    { key: 'shortest_path_hops', header: 'Dijkstra Hops', render: (g) => <span className="font-mono text-slate-300">{g.shortest_path_hops} hops</span> },
    {
      key: 'pagerank_influence',
      header: 'PageRank Score',
      render: (g) => <span className="font-mono text-emerald-400 font-bold">{g.pagerank_influence.toFixed(4)}</span>,
    },
    {
      key: 'fraud_ring_detected',
      header: 'VF2 Subgraph Match',
      render: (g) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            g.fraud_ring_detected
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
          }`}
        >
          {g.fraud_ring_detected ? 'FRAUD RING' : 'NORMAL'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Property Graph & Cypher Query Studio — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Share2 className="w-7 h-7 text-cyan-400" />
            Property Graph Database & Cypher Graph Pattern Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            In-memory property graph traversals, Cypher query parsing, PageRank centrality scores, and VF2 subgraph isomorphism matching.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Graph Nodes</div>
            <div className="text-2xl font-bold text-white mt-1">1.2M Nodes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Directed Edges</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">8.5M Edges</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">PageRank Convergence</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">12 Iterations</div>
          </div>
        </div>

        <DataGrid data={mockGraph} columns={columns} title="Cypher Graph Query Results" />
      </div>
    </MainLayout>
  );
}
