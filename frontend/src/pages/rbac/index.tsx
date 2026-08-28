import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Lock, UserCheck, Key, Plus, EyeOff, CheckCircle } from 'lucide-react';

interface SecurityPolicyItem {
  id: string;
  role_name: string;
  dataset_name: string;
  row_level_filter: string;
  masked_columns: string[];
  pii_unmask_allowed: boolean;
}

const mockPolicies: SecurityPolicyItem[] = [
  { id: 'pol_analyst', role_name: 'Data Analyst', dataset_name: 'gold.fact_orders', row_level_filter: 'tenant_id = :current_user.tenant_id', masked_columns: ['credit_card_mask'], pii_unmask_allowed: false },
  { id: 'pol_crm_rep', role_name: 'CRM Support Specialist', dataset_name: 'silver.dim_customers', row_level_filter: 'assigned_region = :current_user.region', masked_columns: ['ssn_hash'], pii_unmask_allowed: false },
  { id: 'pol_dpo_admin', role_name: 'Data Protection Officer (DPO)', dataset_name: 'ALL_DATASETS', row_level_filter: 'NONE (Full Tenant Access)', masked_columns: [], pii_unmask_allowed: true },
];

export default function RBACIndexPage() {
  const columns: DataGridColumn<SecurityPolicyItem>[] = [
    {
      key: 'role_name',
      header: 'Assigned Role',
      render: (p) => (
        <div className="flex items-center gap-2">
          <Key className="w-4 h-4 text-cyan-400" />
          <strong className="text-white">{p.role_name}</strong>
        </div>
      ),
    },
    {
      key: 'dataset_name',
      header: 'Target Dataset',
      render: (p) => <span className="font-mono text-cyan-400 font-semibold">{p.dataset_name}</span>,
    },
    {
      key: 'row_level_filter',
      header: 'Row-Level Security (RLS) Predicate',
      render: (p) => <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300 text-xs">{p.row_level_filter}</span>,
    },
    {
      key: 'masked_columns',
      header: 'Column-Level Dynamic Masking',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.masked_columns.length > 0 ? (
            p.masked_columns.map((col) => (
              <span key={col} className="bg-red-950 text-red-400 border border-red-800 px-1.5 py-0.5 rounded font-mono text-[10px] flex items-center gap-1">
                <EyeOff className="w-3 h-3" /> {col}
              </span>
            ))
          ) : (
            <span className="text-emerald-400 font-semibold text-xs flex items-center gap-1">
              <CheckCircle className="w-3 h-3" /> Unmasked
            </span>
          )}
        </div>
      ),
    },
    {
      key: 'pii_unmask_allowed',
      header: 'PII Access',
      render: (p) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            p.pii_unmask_allowed
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {p.pii_unmask_allowed ? 'ALLOWED' : 'DENIED'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Fine-Grained Access Control & ABAC — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <ShieldCheck className="w-7 h-7 text-emerald-400" />
              Fine-Grained Security & Row-Level Masking Studio
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Configure dynamic row-level security (RLS) predicates, column-level redaction, and attribute-based access control (ABAC) policies.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Define Security Policy
          </button>
        </div>

        <DataGrid data={mockPolicies} columns={columns} title="Active Security & Masking Policies" />
      </div>
    </MainLayout>
  );
}
