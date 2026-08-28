import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitFork, MapPin, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface ShortestPathItem {
  path_id: string;
  source_node: string;
  destination_node: string;
  total_weight_latency_ms: number;
  hop_count: number;
  traversed_path: string;
  path_health: 'OPTIMAL_ROUTE' | 'BACKUP_ROUTE';
}

const mockPaths: ShortestPathItem[] = [
  { path_id: 'path_us_eu_01', source_node: 'Node:us-east-dc-01', destination_node: 'Node:eu-central-dc-02', total_weight_latency_ms: 74.2, hop_count: 3, traversed_path: 'us-east-dc-01 -> transit-hub-ny -> transit-hub-london -> eu-central-dc-02', path_health: 'OPTIMAL_ROUTE' },
  { path_id: 'path_us_ap_02', source_node: 'Node:us-west-dc-03', destination_node: 'Node:ap-tokyo-dc-01', total_weight_latency_ms: 112.5, hop_count: 2, traversed_path: 'us-west-dc-03 -> transpacific-cable -> ap-tokyo-dc-01', path_health: 'OPTIMAL_ROUTE' },
  { path_id: 'path_data_lineage_03', source_node: 'Table:raw_transactions', destination_node: 'Model:gold_revenue_forecast', total_weight_latency_ms: 3.5, hop_count: 4, traversed_path: 'raw_transactions -> bronze_cdc -> silver_clean -> gold_fact -> model_forecast', path_health: 'OPTIMAL_ROUTE' },
];

export default function DijkstraRoutingPage() {
  const columns: DataGridColumn<ShortestPathItem>[] = [
    {
      key: 'path_id',
      header: 'Route Route ID',
      render: (p) => (
        <div className="flex items-center gap-2">
          <GitFork className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{p.path_id}</strong>
        </div>
      ),
    },
    { key: 'source_node', header: 'Origin Node', render: (p) => <span className="font-mono text-slate-300 text-xs">{p.source_node}</span> },
    { key: 'destination_node', header: 'Destination Node', render: (p) => <span className="font-mono text-cyan-300 text-xs">{p.destination_node}</span> },
    {
      key: 'total_weight_latency_ms',
      header: 'Total Cost / Latency',
      render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.total_weight_latency_ms} ms</span>,
    },
    { key: 'hop_count', header: 'Hops', render: (p) => <span className="font-mono text-slate-300">{p.hop_count} hops</span> },
    { key: 'traversed_path', header: 'Traversed Path Sequence', render: (p) => <span className="font-mono text-slate-400 text-xs">{p.traversed_path}</span> },
    {
      key: 'path_health',
      header: 'Route Status',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.path_health}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Dijkstra Shortest Path & Lineage Tracer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitFork className="w-7 h-7 text-cyan-400" />
            Dijkstra Weighted Shortest Path & Data Route Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Priority queue Dijkstra shortest path computations resolving minimum-cost routing paths across network nodes and pipeline lineage graphs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Shortest Paths</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Routes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Path Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">63.4 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Algorithmic Optimality</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Proven Optimal</div>
          </div>
        </div>

        <DataGrid data={mockPaths} columns={columns} title="Calculated Shortest Lineage & Routing Paths" />
      </div>
    </MainLayout>
  );
}
