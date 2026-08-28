import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Lock, EyeOff, CheckCircle, Database, Layers } from 'lucide-react';

interface SanitizationRuleItem {
  id: string;
  table_name: string;
  column_name: string;
  policy_action: 'PII_REGEX_SCRUB' | 'SALTED_SHA256' | 'FULL_MASK' | 'PARTIAL_EMAIL';
  detected_pii_type: string;
  records_scrubbed_24h: number;
  status: 'ENFORCING' | 'AUDIT_ONLY';
}

const mockRules: SanitizationRuleItem[] = [
  { id: 'san_01', table_name: 'silver.dim_customers', column_name: 'ssn', policy_action: 'FULL_MASK', detected_pii_type: 'US_SSN', records_scrubbed_24h: 24500, status: 'ENFORCING' },
  { id: 'san_02', table_name: 'silver.dim_customers', column_name: 'email', policy_action: 'PARTIAL_EMAIL', detected_pii_type: 'EMAIL_ADDRESS', records_scrubbed_24h: 24500, status: 'ENFORCING' },
  { id: 'san_03', table_name: 'bronze.raw_clickstream', column_name: 'ip_address', policy_action: 'SALTED_SHA256', detected_pii_type: 'IPV4_ADDRESS', records_scrubbed_24h: 890000, status: 'ENFORCING' },
];

export default function SanitizationGovernancePage() {
  const columns: DataGridColumn<SanitizationRuleItem>[] = [
    {
      key: 'table_name',
      header: 'Target Field',
      render: (s) => (
        <div>
          <strong className="text-white font-mono text-xs">{s.table_name}.{s.column_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{s.id}</div>
        </div>
      ),
    },
    {
      key: 'detected_pii_type',
      header: 'Detected PII Entity',
      render: (s) => <span className="bg-slate-800 text-amber-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.detected_pii_type}</span>,
    },
    {
      key: 'policy_action',
      header: 'Sanitization Action',
      render: (s) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{s.policy_action}</span>,
    },
    { key: 'records_scrubbed_24h', header: 'Scrubbed (24h)', render: (s) => <span className="font-mono text-cyan-300 font-bold">{s.records_scrubbed_24h.toLocaleString()} records</span> },
    {
      key: 'status',
      header: 'Enforcement State',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>PII Scrubbing & Salted Pseudonymization — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <EyeOff className="w-7 h-7 text-cyan-400" />
            PII Scrubbing, Dynamic Redaction & Salted Pseudonymization
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated compliance scanning, salted SHA-256 pseudonymization, and column-level masking for GDPR, HIPAA, and CCPA.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Redaction Policies</div>
            <div className="text-2xl font-bold text-white mt-1">3 Policies</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Scrubbed PII Records (24h)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">939,000 Scrubbed</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compliance Level</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">GDPR / HIPAA Validated</div>
          </div>
        </div>

        <DataGrid data={mockRules} columns={columns} title="Active PII Sanitization Policies" />
      </div>
    </MainLayout>
  );
}
