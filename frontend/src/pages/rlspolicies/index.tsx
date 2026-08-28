import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Shield, Filter, CheckCircle, Database, Layers, Lock } from 'lucide-react';

interface RLSPolicyItem {
  policy_id: string;
  table_name: string;
  tenant_isolation_col: string;
  department_filter: string;
  country_filter: string;
  enforcement_mode: 'STRICT_ROW_FILTER' | 'DYNAMIC_MASK';
  status: 'ACTIVE' | 'AUDIT_ONLY';
}

const mockRLS: RLSPolicyItem[] = [
  { policy_id: 'rls_fin_01', table_name: 'gold.fact_orders', tenant_isolation_col: 'tenant_id', department_filter: 'Finance, Executive', country_filter: 'US, EU', enforcement_mode: 'STRICT_ROW_FILTER', status: 'ACTIVE' },
  { policy_id: 'rls_crm_02', table_name: 'silver.dim_customers', tenant_isolation_col: 'tenant_id', department_filter: 'Support, Sales', country_filter: 'All Countries', enforcement_mode: 'DYNAMIC_MASK', status: 'ACTIVE' },
  { policy_id: 'rls_iot_03', table_name: 'bronze.iot_telemetry', tenant_isolation_col: 'tenant_id', department_filter: 'Engineering', country_filter: 'All Countries', enforcement_mode: 'STRICT_ROW_FILTER', status: 'ACTIVE' },
];

export default function RLSPoliciesPage() {
  const columns: DataGridColumn<RLSPolicyItem>[] = [
    {
      key: 'table_name',
      header: 'Target Lakehouse Table',
      render: (r) => (
        <div>
          <strong className="text-white font-mono text-xs">{r.table_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{r.policy_id}</div>
        </div>
      ),
    },
    { key: 'tenant_isolation_col', header: 'Tenant Isolation Key', render: (r) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{r.tenant_isolation_col}</span> },
    { key: 'department_filter', header: 'Allowed Departments', render: (r) => <span className="text-slate-300 text-xs">{r.department_filter}</span> },
    { key: 'country_filter', header: 'Geographic Region Clearance', render: (r) => <span className="font-mono text-cyan-300 text-xs">{r.country_filter}</span> },
    {
      key: 'enforcement_mode',
      header: 'Enforcement Mechanism',
      render: (r) => <span className="font-mono text-emerald-400 font-bold text-xs">{r.enforcement_mode}</span>,
    },
    {
      key: 'status',
      header: 'Policy State',
      render: (r) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {r.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Row-Level Security (RLS) & Column Masking — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Shield className="w-7 h-7 text-cyan-400" />
            Row-Level Security (RLS) & Dynamic Masking Policies
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-trust multi-tenant predicate injection, user department clearance, and dynamic column masking for Lakehouse queries.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active RLS Policies</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Rules</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Query Injection Overhead</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;0.05 ms / query</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tenant Isolation Grade</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Strict Cryptographic</div>
          </div>
        </div>

        <DataGrid data={mockRLS} columns={columns} title="Managed Row-Level Security Policies" />
      </div>
    </MainLayout>
  );
}
