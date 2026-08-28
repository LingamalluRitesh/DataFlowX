import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cpu, Server, Activity, CheckCircle, Flame, Layers } from 'lucide-react';

interface ClusterNodeItem {
  node_id: string;
  driver_type: 'RAY_ACTOR_POOL' | 'KUBERNETES_WORKER' | 'CELERY_DISTRIBUTED';
  cpu_allocated: string;
  memory_allocated_gb: number;
  active_partition_tasks: number;
  uptime: string;
  health: 'HEALTHY' | 'DRAINING';
}

const mockNodes: ClusterNodeItem[] = [
  { node_id: 'ray-worker-node-us-east-1a-01', driver_type: 'RAY_ACTOR_POOL', cpu_allocated: '14 / 16 Cores (87.5%)', memory_allocated_gb: 54.2, active_partition_tasks: 8, uptime: '14d 6h', health: 'HEALTHY' },
  { node_id: 'k8s-pod-worker-default-78bf', driver_type: 'KUBERNETES_WORKER', cpu_allocated: '4 / 8 Cores (50.0%)', memory_allocated_gb: 16.0, active_partition_tasks: 4, uptime: '2d 18h', health: 'HEALTHY' },
  { node_id: 'celery-async-broker-queue-03', driver_type: 'CELERY_DISTRIBUTED', cpu_allocated: '2 / 4 Cores (50.0%)', memory_allocated_gb: 8.5, active_partition_tasks: 2, uptime: '30d 12h', health: 'HEALTHY' },
];

export default function DistributedClustersPage() {
  const columns: DataGridColumn<ClusterNodeItem>[] = [
    {
      key: 'node_id',
      header: 'Compute Node Identifier',
      render: (n) => (
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{n.node_id}</strong>
        </div>
      ),
    },
    {
      key: 'driver_type',
      header: 'Execution Driver',
      render: (n) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{n.driver_type}</span>,
    },
    { key: 'cpu_allocated', header: 'CPU Core Allocation', render: (n) => <span className="font-mono text-cyan-300 text-xs">{n.cpu_allocated}</span> },
    {
      key: 'memory_allocated_gb',
      header: 'Memory In-Use',
      render: (n) => <span className="font-mono text-emerald-400 font-bold">{n.memory_allocated_gb.toFixed(1)} GB</span>,
    },
    { key: 'active_partition_tasks', header: 'Active Tasks', render: (n) => <span className="font-mono text-slate-300">{n.active_partition_tasks} tasks</span> },
    {
      key: 'health',
      header: 'Node State',
      render: (n) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {n.health}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Distributed Ray & K8s Compute Clusters — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Cpu className="w-7 h-7 text-cyan-400" />
            Distributed Ray, Kubernetes & Celery Compute Worker Clusters
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Dynamic worker pod auto-scaling, plasma shared memory allocation, and distributed task admission governance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Compute Cores</div>
            <div className="text-2xl font-bold text-white mt-1">28 Cores Active</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Memory In-Use</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">78.7 GB / 128 GB</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cluster Autoscaler</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">HPA Enabled</div>
          </div>
        </div>

        <DataGrid data={mockNodes} columns={columns} title="Active Distributed Worker Pool" />
      </div>
    </MainLayout>
  );
}
