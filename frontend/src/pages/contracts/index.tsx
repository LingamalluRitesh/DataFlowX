import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Plus, CheckCircle, AlertTriangle, FileText, ArrowRight } from 'lucide-react';

interface DataContractItem {
  id: string;
  dataset_name: string;
  version: string;
  producer: string;
  consumers_count: number;
  sla_freshness_hours: number;
  min_quality_score: number;
  status: 'ACTIVE' | 'DRAFT' | 'DEPRECATED';
  last_evaluated: string;
}

const mockContracts: DataContractItem[] = [
  { id: 'contract_01', dataset_name: 'fact_orders', version: 'v2.1.0', producer: 'Checkout Service Team', consumers_count: 5, sla_freshness_hours: 2, min_quality_score: 98.0, status: 'ACTIVE', last_evaluated: '10 mins ago' },
  { id: 'contract_02', dataset_name: 'dim_customers', version: 'v1.4.0', producer: 'Identity Core Team', consumers_count: 8, sla_freshness_hours: 24, min_quality_score: 95.0, status: 'ACTIVE', last_evaluated: '1 hour ago' },
  { id: 'contract_03', dataset_name: 'financial_ledger', version: 'v3.0.0', producer: 'Billing Microservice', consumers_count: 3, sla_freshness_hours: 1, min_quality_score: 100.0, status: 'ACTIVE', last_evaluated: '5 mins ago' },
];

export default function ContractsIndexPage() {
  const columns: DataGridColumn<DataContractItem>[] = [
    {
      key: 'dataset_name',
      header: 'Dataset Contract',
      render: (c) => (
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-white">{c.dataset_name}</span>
          <span className="bg-slate-800 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded">{c.version}</span>
        </div>
      ),
    },
    { key: 'producer', header: 'Producer' },
    {
      key: 'consumers_count',
      header: 'Consumers',
      render: (c) => <span className="font-mono text-slate-300">{c.consumers_count} downstream apps</span>,
    },
    {
      key: 'sla_freshness_hours',
      header: 'Freshness SLA',
      render: (c) => <span className="font-mono text-cyan-400">&le; {c.sla_freshness_hours}h max</span>,
    },
    {
      key: 'min_quality_score',
      header: 'Min Quality SLA',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">&ge; {c.min_quality_score}%</span>,
    },
    {
      key: 'status',
      header: 'Contract Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
    { key: 'last_evaluated', header: 'Last Evaluated' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Data Contracts & SLAs — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <ShieldCheck className="w-7 h-7 text-emerald-400" />
              Producer-Consumer Data Contracts
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Enforce schema specifications, prevent upstream breaking changes, and guarantee freshness SLAs.
            </p>
          </div>

          <Link
            href="/contracts/new"
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto"
          >
            <Plus className="w-4 h-4" /> Create Data Contract
          </Link>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Contracts</div>
            <div className="text-2xl font-bold text-white mt-1">14 Contracts</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">SLA Compliance Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">99.8% On-Time</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Breaking Changes Prevented</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">37 Blocked</div>
          </div>
        </div>

        {/* Contracts DataGrid */}
        <DataGrid data={mockContracts} columns={columns} title="Registered Data Contracts" />
      </div>
    </MainLayout>
  );
}
