import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Network, TrendingUp, CheckCircle, Share2, Layers, Award } from 'lucide-react';

interface PageRankEntityItem {
  rank: number;
  entity_id: string;
  entity_type: string;
  pagerank_score: number;
  in_degree_links: number;
  out_degree_links: number;
  centrality_tier: 'CORE_HUB' | 'INFLUENCER' | 'PERIPHERY';
}

const mockRanks: PageRankEntityItem[] = [
  { rank: 1, entity_id: 'Company:global_corp_master', entity_type: 'ORGANIZATION', pagerank_score: 0.1420, in_degree_links: 1420, out_degree_links: 85, centrality_tier: 'CORE_HUB' },
  { rank: 2, entity_id: 'User:admin_super_user', entity_type: 'USER', pagerank_score: 0.0890, in_degree_links: 890, out_degree_links: 120, centrality_tier: 'CORE_HUB' },
  { rank: 3, entity_id: 'Merchant:stripe_gateway_us', entity_type: 'FINANCIAL_GATEWAY', pagerank_score: 0.0650, in_degree_links: 650, out_degree_links: 400, centrality_tier: 'INFLUENCER' },
];

export default function PageRankStudioPage() {
  const columns: DataGridColumn<PageRankEntityItem>[] = [
    {
      key: 'rank',
      header: 'Rank',
      render: (p) => (
        <span className="w-6 h-6 rounded-full bg-slate-800 text-cyan-400 font-mono text-xs flex items-center justify-center font-bold">
          #{p.rank}
        </span>
      ),
    },
    { key: 'entity_id', header: 'Graph Entity', render: (p) => <strong className="text-white font-mono text-xs">{p.entity_id}</strong> },
    { key: 'entity_type', header: 'Entity Category', render: (p) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{p.entity_type}</span> },
    {
      key: 'pagerank_score',
      header: 'PageRank Centrality Score',
      render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.pagerank_score.toFixed(4)}</span>,
    },
    { key: 'in_degree_links', header: 'Inbound In-Degree', render: (p) => <span className="font-mono text-cyan-300">{p.in_degree_links.toLocaleString()} links</span> },
    {
      key: 'centrality_tier',
      header: 'Influence Tier',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.centrality_tier}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>PageRank & Network Centrality — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Network className="w-7 h-7 text-cyan-400" />
            PageRank Centrality & Network Influence Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Iterative PageRank computation, eigenvector centrality analysis, and community hub identification across enterprise knowledge graphs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Graph Nodes Evaluated</div>
            <div className="text-2xl font-bold text-white mt-1">1.2M Nodes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Damping Factor (Alpha)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0.85 Standard</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Convergence Residual</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">&lt; 1e-6 (Stable)</div>
          </div>
        </div>

        <DataGrid data={mockRanks} columns={columns} title="Top Influential Knowledge Graph Entities" />
      </div>
    </MainLayout>
  );
}
