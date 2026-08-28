import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Key, Lock, CheckCircle, Database, Layers, UserCheck } from 'lucide-react';

interface ABACPolicyItem {
  id: string;
  rule_name: string;
  target_table: string;
  required_clearance: string;
  allowed_departments: string[];
  encryption_standard: string;
  status: 'ENFORCED' | 'AUDIT_ONLY';
}

const mockABACPolicies: ABACPolicyItem[] = [
  { id: 'abac_01', rule_name: 'Financial Ledger ABAC Policy', target_table: 'gold.fact_orders', required_clearance: 'Clearance L3 (Confidential)', allowed_departments: ['Finance', 'Executive', 'Accounting'], encryption_standard: 'FPE-FF1 (Format Preserving)', status: 'ENFORCED' },
  { id: 'abac_02', rule_name: 'Customer PII Masking Policy', target_table: 'silver.dim_customers', required_clearance: 'Clearance L2 (Internal)', allowed_departments: ['Customer Support', 'Data Engineering', 'Marketing'], encryption_standard: 'AES-256-GCM + Salted SHA256', status: 'ENFORCED' },
  { id: 'abac_03', rule_name: 'IoT Telemetry Unrestricted Read', target_table: 'bronze.iot_telemetry', required_clearance: 'Clearance L1 (Public/Internal)', allowed_departments: ['All Departments'], encryption_standard: 'Plaintext (Unrestricted)', status: 'ENFORCED' },
];

export default function ABACGovernancePage() {
  const columns: DataGridColumn<ABACPolicyItem>[] = [
    {
      key: 'rule_name',
      header: 'ABAC Access Policy',
      render: (p) => (
        <div>
          <strong className="text-white font-mono text-xs">{p.rule_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{p.id}</div>
        </div>
      ),
    },
    { key: 'target_table', header: 'Target Table', render: (p) => <span className="font-mono text-purple-300 text-xs">{p.target_table}</span> },
    {
      key: 'required_clearance',
      header: 'Security Clearance Required',
      render: (p) => <span className="bg-slate-800 text-amber-300 font-mono text-[10px] px-2 py-0.5 rounded">{p.required_clearance}</span>,
    },
    {
      key: 'allowed_departments',
      header: 'Allowed Departments',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.allowed_departments.map((d) => (
            <span key={d} className="bg-slate-800 text-slate-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {d}
            </span>
          ))}
        </div>
      ),
    },
    { key: 'encryption_standard', header: 'Column Cipher Standard', render: (p) => <span className="font-mono text-cyan-300 text-xs">{p.encryption_standard}</span> },
    {
      key: 'status',
      header: 'Policy State',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>ABAC Zero-Trust Policy & Format-Preserving Encryption — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-7 h-7 text-cyan-400" />
            Attribute-Based Access Control (ABAC) & Format-Preserving Tokenization
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-trust fine-grained table, row, and column security policies evaluated against clearance levels and department attributes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active ABAC Policies</div>
            <div className="text-2xl font-bold text-white mt-1">3 Enforced Rules</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Evaluation Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;0.1 ms / query</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Zero-Trust Model</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">NIST SP 800-162 Compliant</div>
          </div>
        </div>

        <DataGrid data={mockABACPolicies} columns={columns} title="Managed ABAC Access Rules" />
      </div>
    </MainLayout>
  );
}
