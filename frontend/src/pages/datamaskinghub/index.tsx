import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Lock, EyeOff, CheckCircle, ShieldCheck, Layers, FileKey } from 'lucide-react';

interface MaskingRuleItem {
  column_name: string;
  table_name: string;
  masking_strategy: 'HASH_SHA256' | 'MASK_EMAIL' | 'LAST_4_DIGITS' | 'FPE_FF1' | 'NULLIFY';
  sample_masked_output: string;
  exempt_roles: string[];
  status: 'ENFORCED' | 'AUDIT_ONLY';
}

const mockMasks: MaskingRuleItem[] = [
  { column_name: 'credit_card_number', table_name: 'gold.fact_orders', masking_strategy: 'LAST_4_DIGITS', sample_masked_output: '****-****-****-9812', exempt_roles: ['security_admin', 'pci_compliance_auditor'], status: 'ENFORCED' },
  { column_name: 'customer_email', table_name: 'silver.dim_customers', masking_strategy: 'MASK_EMAIL', sample_masked_output: 'j***@example.com', exempt_roles: ['customer_support_lead'], status: 'ENFORCED' },
  { column_name: 'tax_identifier_ssn', table_name: 'silver.dim_customers', masking_strategy: 'HASH_SHA256', sample_masked_output: 'e3b0c44298fc1c149afbf4c8996fb924...', exempt_roles: ['security_admin'], status: 'ENFORCED' },
];

export default function DataMaskingHubPage() {
  const columns: DataGridColumn<MaskingRuleItem>[] = [
    {
      key: 'column_name',
      header: 'Sensitive Column',
      render: (m) => (
        <div>
          <strong className="text-white font-mono text-xs">{m.column_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{m.table_name}</div>
        </div>
      ),
    },
    {
      key: 'masking_strategy',
      header: 'Masking Strategy',
      render: (m) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{m.masking_strategy}</span>,
    },
    { key: 'sample_masked_output', header: 'Cipher / Redacted Preview', render: (m) => <span className="font-mono text-cyan-300 text-xs">{m.sample_masked_output}</span> },
    {
      key: 'exempt_roles',
      header: 'Exempt Unmasked Roles',
      render: (m) => (
        <div className="flex flex-wrap gap-1">
          {m.exempt_roles.map((r) => (
            <span key={r} className="bg-slate-800 text-slate-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {r}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'status',
      header: 'Enforcement State',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {m.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Dynamic Data Masking & Tokenization Hub — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <EyeOff className="w-7 h-7 text-cyan-400" />
            Dynamic Column Masking & Format-Preserving Tokenization Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Role-based column redaction, partial email masking, salted SHA-256 tokenization, and FPE encryption policies.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Column Masking Rules</div>
            <div className="text-2xl font-bold text-white mt-1">3 Protected Columns</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Masking Latency Overhead</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt;0.01 ms / record</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cryptographic Integrity</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">NIST Compliant</div>
          </div>
        </div>

        <DataGrid data={mockMasks} columns={columns} title="Managed Dynamic Masking Policies" />
      </div>
    </MainLayout>
  );
}
