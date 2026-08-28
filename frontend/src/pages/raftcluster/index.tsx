import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Server, Key, CheckCircle, Activity, Radio, Cpu } from 'lucide-react';

interface RaftNodeStatusItem {
  node_id: string;
  ip_address: string;
  role: 'LEADER' | 'FOLLOWER' | 'CANDIDATE';
  current_term: number;
  commit_index: number;
  last_heartbeat_ms_ago: number;
  fencing_token: number;
}

const mockRaftNodes: RaftNodeStatusItem[] = [
  { node_id: 'raft-coordinator-0', ip_address: '10.244.1.14:9000', role: 'LEADER', current_term: 42, commit_index: 89124, last_heartbeat_ms_ago: 12, fencing_token: 1045 },
  { node_id: 'raft-coordinator-1', ip_address: '10.244.2.18:9000', role: 'FOLLOWER', current_term: 42, commit_index: 89124, last_heartbeat_ms_ago: 45, fencing_token: 1045 },
  { node_id: 'raft-coordinator-2', ip_address: '10.244.3.22:9000', role: 'FOLLOWER', current_term: 42, commit_index: 89124, last_heartbeat_ms_ago: 50, fencing_token: 1045 },
];

export default function RaftClusterConsolePage() {
  const columns: DataGridColumn<RaftNodeStatusItem>[] = [
    {
      key: 'node_id',
      header: 'Raft Node ID',
      render: (n) => (
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{n.node_id}</strong>
        </div>
      ),
    },
    { key: 'ip_address', header: 'Node Endpoint', render: (n) => <span className="font-mono text-slate-400 text-xs">{n.ip_address}</span> },
    {
      key: 'role',
      header: 'Consensus Role',
      render: (n) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            n.role === 'LEADER'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-300'
          }`}
        >
          {n.role}
        </span>
      ),
    },
    { key: 'current_term', header: 'Consensus Term', render: (n) => <span className="font-mono text-purple-300 font-bold">Term {n.current_term}</span> },
    { key: 'commit_index', header: 'Committed LSN', render: (n) => <span className="font-mono text-emerald-400 font-bold">{n.commit_index.toLocaleString()}</span> },
    { key: 'fencing_token', header: 'Fencing Token', render: (n) => <span className="font-mono text-cyan-300">tok_{n.fencing_token}</span> },
    { key: 'last_heartbeat_ms_ago', header: 'Heartbeat Lag', render: (n) => <span className="font-mono text-slate-300">{n.last_heartbeat_ms_ago} ms</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Raft Consensus & Multi-Cluster Nodes — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-7 h-7 text-emerald-400" />
            Raft Consensus Cluster & Fencing Token Console
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            High-availability leader election, AppendEntries replication heartbeats, and optimistic leader leases with monotonic fencing tokens.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cluster Quorum Health</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">3/3 Nodes (Quorum OK)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Current Leader Node</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">raft-coordinator-0</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Consensus Replication Lag</div>
            <div className="text-2xl font-bold text-white mt-1">0 Entries Lag</div>
          </div>
        </div>

        <DataGrid data={mockRaftNodes} columns={columns} title="Raft Cluster Nodes Membership" />
      </div>
    </MainLayout>
  );
}
