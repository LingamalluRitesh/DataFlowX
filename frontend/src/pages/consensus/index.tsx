import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Server, ShieldCheck, Activity, Cpu, CheckCircle, RefreshCw, Zap } from 'lucide-react';

interface ClusterNodeItem {
  node_id: string;
  role: 'LEADER' | 'FOLLOWER' | 'CANDIDATE';
  current_term: number;
  commit_index: number;
  ip_address: string;
  heartbeat_lag_ms: number;
  status: 'HEALTHY' | 'DEGRADED';
}

const mockNodes: ClusterNodeItem[] = [
  { node_id: 'coordinator-node-01', role: 'LEADER', current_term: 4, commit_index: 48920, ip_address: '10.0.1.10', heartbeat_lag_ms: 1, status: 'HEALTHY' },
  { node_id: 'coordinator-node-02', role: 'FOLLOWER', current_term: 4, commit_index: 48920, ip_address: '10.0.1.11', heartbeat_lag_ms: 12, status: 'HEALTHY' },
  { node_id: 'coordinator-node-03', role: 'FOLLOWER', current_term: 4, commit_index: 48920, ip_address: '10.0.1.12', heartbeat_lag_ms: 14, status: 'HEALTHY' },
];

export default function ConsensusIndexPage() {
  const columns: DataGridColumn<ClusterNodeItem>[] = [
    {
      key: 'node_id',
      header: 'Coordinator Node ID',
      render: (n) => (
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{n.node_id}</strong>
        </div>
      ),
    },
    {
      key: 'role',
      header: 'Raft Consensus Role',
      render: (n) => (
        <span
          className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
            n.role === 'LEADER'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-300'
          }`}
        >
          {n.role}
        </span>
      ),
    },
    { key: 'current_term', header: 'Raft Term', render: (n) => <span className="font-mono text-cyan-300">Term {n.current_term}</span> },
    { key: 'commit_index', header: 'Replicated Log Index', render: (n) => <span className="font-mono text-slate-300">{n.commit_index.toLocaleString()}</span> },
    { key: 'ip_address', header: 'Host IP', render: (n) => <span className="font-mono text-slate-400">{n.ip_address}</span> },
    { key: 'heartbeat_lag_ms', header: 'Heartbeat Lag', render: (n) => <span className="font-mono text-emerald-400">{n.heartbeat_lag_ms} ms</span> },
    {
      key: 'status',
      header: 'Health',
      render: (n) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold flex items-center gap-1 w-max">
          <CheckCircle className="w-3 h-3" /> {n.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Distributed Raft Consensus — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Server className="w-7 h-7 text-cyan-400" />
            Distributed Raft Consensus & Cluster Topology
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            High-availability cluster coordinator status, leader election heartbeats, distributed lease locks, and replicated state logs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cluster Quorum</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">3/3 Nodes (Healthy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Distributed Locks</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">14 Lease Locks</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Log Replication Latency</div>
            <div className="text-2xl font-bold text-purple-400 mt-1">&lt; 2 ms</div>
          </div>
        </div>

        <DataGrid data={mockNodes} columns={columns} title="Coordinator Node Topology" />
      </div>
    </MainLayout>
  );
}
