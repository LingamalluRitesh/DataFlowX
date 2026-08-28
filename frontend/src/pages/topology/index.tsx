import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataMeshTopology } from '@/components/charts/DataMeshTopology';
import { Network, Server, Cloud, ShieldCheck, Cpu, HardDrive } from 'lucide-react';

export default function TopologyMapPage() {
  return (
    <MainLayout>
      <Head>
        <title>Global Cluster & Cloud Topology — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Network className="w-7 h-7 text-cyan-400" />
            Global Infrastructure & Cloud Topology
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time topology view across multi-region Kubernetes clusters, object storage lakes, Raft coordinators, and analytical warehouse nodes.
          </p>
        </div>

        {/* Global Cluster Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase flex items-center gap-1.5">
              <Server className="w-3.5 h-3.5 text-cyan-400" /> Worker Pods Active
            </div>
            <div className="text-3xl font-extrabold text-white mt-2">24 Pods</div>
            <div className="text-xs text-slate-400 mt-1">4 regions (us-east, us-west, eu-west, apac)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-purple-400" /> Total Allocated VCPUs
            </div>
            <div className="text-3xl font-extrabold text-purple-400 mt-2">96 Cores</div>
            <div className="text-xs text-slate-400 mt-1">Avg cluster load: 42.8%</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase flex items-center gap-1.5">
              <HardDrive className="w-3.5 h-3.5 text-emerald-400" /> Lakehouse Storage
            </div>
            <div className="text-3xl font-extrabold text-emerald-400 mt-2">12.4 TB</div>
            <div className="text-xs text-slate-400 mt-1">Delta & Iceberg Parquet partitions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase flex items-center gap-1.5">
              <Cloud className="w-3.5 h-3.5 text-amber-400" /> Multi-Cloud Connectors
            </div>
            <div className="text-3xl font-extrabold text-amber-400 mt-2">28 Connectors</div>
            <div className="text-xs text-slate-400 mt-1">AWS, GCP, Azure, Snowflake, Databricks</div>
          </div>
        </div>

        <DataMeshTopology />
      </div>
    </MainLayout>
  );
}
