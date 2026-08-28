import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileCheck, ShieldCheck, CheckCircle, AlertTriangle, Play, Sparkles } from 'lucide-react';

interface ContractVerificationItem {
  contract_id: string;
  dataset_name: string;
  total_checks: number;
  passed_checks: number;
  conformance_pct: number;
  sla_freshness_status: 'MET' | 'BREACHED';
  status: 'CONFORMING' | 'NON_CONFORMING';
}

const mockVerifications: ContractVerificationItem[] = [
  { contract_id: 'contract_fact_orders_v2', dataset_name: 'gold.fact_orders', total_checks: 18, passed_checks: 18, conformance_pct: 100.0, sla_freshness_status: 'MET', status: 'CONFORMING' },
  { contract_id: 'contract_dim_customers_v1', dataset_name: 'silver.dim_customers', total_checks: 12, passed_checks: 12, conformance_pct: 100.0, sla_freshness_status: 'MET', status: 'CONFORMING' },
  { contract_id: 'contract_iot_stream_v1', dataset_name: 'bronze.iot_telemetry', total_checks: 14, passed_checks: 14, conformance_pct: 100.0, sla_freshness_status: 'MET', status: 'CONFORMING' },
];

export default function ContractVerificationPage() {
  const columns: DataGridColumn<ContractVerificationItem>[] = [
    {
      key: 'contract_id',
      header: 'Contract ID',
      render: (c) => (
        <div>
          <strong className="text-white font-mono">{c.contract_id}</strong>
          <div className="text-xs text-cyan-400 font-mono mt-0.5">{c.dataset_name}</div>
        </div>
      ),
    },
    {
      key: 'conformance_pct',
      header: 'Conformance Score',
      render: (c) => (
        <span className="font-mono text-emerald-400 font-bold">
          {c.conformance_pct}% ({c.passed_checks}/{c.total_checks} checks)
        </span>
      ),
    },
    {
      key: 'sla_freshness_status',
      header: 'Freshness SLA',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.sla_freshness_status}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
    {
      key: 'contract_id',
      header: 'Action',
      render: (c) => (
        <button className="flex items-center gap-1 px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          <Play className="w-3 h-3 fill-white" /> Re-Verify
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Contract Runtime Verifier — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <FileCheck className="w-7 h-7 text-cyan-400" />
              Data Contract Runtime Verification Test Harness
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Automated runtime test harness validating live Parquet and Delta Lake datasets against published OpenDataContract specifications.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Sparkles className="w-4 h-4" /> Run All Verifications
          </button>
        </div>

        <DataGrid data={mockVerifications} columns={columns} title="Live Data Contract Verification Test Suite" />
      </div>
    </MainLayout>
  );
}
