import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileCheck, ShieldCheck, CheckCircle, Clock, AlertCircle, Layers } from 'lucide-react';

interface ODCSContractItem {
  contract_id: string;
  dataset_name: string;
  version: string;
  owner_team: string;
  rules_count: number;
  runtime_evaluation_ms: number;
  enforcement_action: 'QUARANTINE_BATCH' | 'ALERT_ONLY';
  compliance_state: 'VERIFIED' | 'BREACHED';
}

const mockContractsODCS: ODCSContractItem[] = [
  { contract_id: 'odcs_orders_v3', dataset_name: 'gold.fact_orders', version: 'v3.0.0', owner_team: 'Financial Engineering', rules_count: 18, runtime_evaluation_ms: 1.2, enforcement_action: 'QUARANTINE_BATCH', compliance_state: 'VERIFIED' },
  { contract_id: 'odcs_customers_v2', dataset_name: 'silver.dim_customers', version: 'v2.1.0', owner_team: 'Customer Master Data', rules_count: 12, runtime_evaluation_ms: 0.9, enforcement_action: 'QUARANTINE_BATCH', compliance_state: 'VERIFIED' },
  { contract_id: 'odcs_telemetry_v1', dataset_name: 'bronze.iot_telemetry', version: 'v1.4.0', owner_team: 'IoT Operations', rules_count: 8, runtime_evaluation_ms: 0.6, enforcement_action: 'ALERT_ONLY', compliance_state: 'VERIFIED' },
];

export default function ContractsEnginePage() {
  const columns: DataGridColumn<ODCSContractItem>[] = [
    {
      key: 'contract_id',
      header: 'ODCS Contract ID',
      render: (c) => (
        <div className="flex items-center gap-2">
          <FileCheck className="w-4 h-4 text-cyan-400" />
          <div>
            <strong className="text-white font-mono text-xs">{c.contract_id}</strong>
            <div className="text-[10px] text-cyan-400 font-mono">{c.version}</div>
          </div>
        </div>
      ),
    },
    { key: 'dataset_name', header: 'Target Dataset', render: (c) => <span className="font-mono text-purple-300 text-xs">{c.dataset_name}</span> },
    { key: 'owner_team', header: 'Owner Team', render: (c) => <span className="text-slate-300 text-xs">{c.owner_team}</span> },
    { key: 'rules_count', header: 'Contract Rules', render: (c) => <span className="font-mono text-slate-300">{c.rules_count} rules</span> },
    {
      key: 'runtime_evaluation_ms',
      header: 'Validation Latency',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.runtime_evaluation_ms} ms</span>,
    },
    {
      key: 'enforcement_action',
      header: 'Enforcement Policy',
      render: (c) => <span className="bg-slate-800 text-amber-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.enforcement_action}</span>,
    },
    {
      key: 'compliance_state',
      header: 'Compliance State',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.compliance_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>OpenDataContract Specification (ODCS v3.0) — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileCheck className="w-7 h-7 text-cyan-400" />
            OpenDataContract (ODCS v3.0) Specification & Runtime Enforcement
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Declarative data contracts defining schema expectations, business SLAs, and automated batch quarantine enforcement.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active ODCS Contracts</div>
            <div className="text-2xl font-bold text-white mt-1">3 Contracts</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Validation Pass Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Passing</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Enforcement Time</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0.9 ms / batch</div>
          </div>
        </div>

        <DataGrid data={mockContractsODCS} columns={columns} title="Managed ODCS Data Contracts" />
      </div>
    </MainLayout>
  );
}
