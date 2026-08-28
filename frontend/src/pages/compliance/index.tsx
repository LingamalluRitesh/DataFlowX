import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileText, ShieldAlert, CheckCircle, Lock, Award, FileCheck } from 'lucide-react';

interface RoPAItem {
  activity_name: string;
  purpose: string;
  data_categories: string[];
  retention_period_days: number;
  security_measures: string;
  gdpr_article_status: 'COMPLIANT' | 'NEEDS_REVIEW';
}

const mockRoPA: RoPAItem[] = [
  { activity_name: 'Customer Transaction & Order Processing', purpose: 'Revenue auditing and financial reporting', data_categories: ['Customer Identifiers', 'Credit Card Last-4', 'Order Line Items'], retention_period_days: 730, security_measures: 'Envelope Encryption (AWS KMS) + SHA256 Salted Hashes', gdpr_article_status: 'COMPLIANT' },
  { activity_name: 'Website Telemetry & Behavioral Analytics', purpose: 'Product analytics and user experience', data_categories: ['Hashed Session IDs', 'IP Address (Truncated /24)', 'Pageview Events'], retention_period_days: 90, security_measures: 'Differential Privacy (ε=1.0) + Automated Inactivity TTL', gdpr_article_status: 'COMPLIANT' },
  { activity_name: 'Support Ticket Ingestion & NLP Routing', purpose: 'Customer support satisfaction', data_categories: ['Support Transcripts', 'Contact Email', 'Account Tier'], retention_period_days: 180, security_measures: 'Dynamic Regex PII Redaction + RBAC Filtering', gdpr_article_status: 'COMPLIANT' },
];

export default function RegulatoryCompliancePage() {
  const columns: DataGridColumn<RoPAItem>[] = [
    {
      key: 'activity_name',
      header: 'Processing Activity (RoPA Article 30)',
      render: (r) => <strong className="text-white font-mono text-xs">{r.activity_name}</strong>,
    },
    { key: 'purpose', header: 'Processing Legal Purpose', render: (r) => <span className="text-slate-300 text-xs">{r.purpose}</span> },
    {
      key: 'data_categories',
      header: 'Data Categories',
      render: (r) => (
        <div className="flex flex-wrap gap-1">
          {r.data_categories.map((c) => (
            <span key={c} className="bg-slate-800 text-purple-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {c}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'retention_period_days',
      header: 'Retention Period',
      render: (r) => <span className="font-mono text-cyan-300 font-bold">{r.retention_period_days} Days</span>,
    },
    { key: 'security_measures', header: 'Technical Safeguards', render: (r) => <span className="font-mono text-emerald-400 text-xs">{r.security_measures}</span> },
    {
      key: 'gdpr_article_status',
      header: 'Audit Status',
      render: (r) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {r.gdpr_article_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Regulatory Compliance & RoPA Dossier — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileText className="w-7 h-7 text-cyan-400" />
            GDPR, CCPA & HIPAA Regulatory Compliance & RoPA Dossier Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated Article 30 Records of Processing Activities (RoPA), Data Subject Request (DSR) tracking, and data retention policies.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Overall Compliance Score</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Compliant</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">PII Encryption Coverage</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% AES-256-GCM</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active RoPA Activities</div>
            <div className="text-2xl font-bold text-white mt-1">3 Activities</div>
          </div>
        </div>

        <DataGrid data={mockRoPA} columns={columns} title="Article 30 Record of Processing Activities" />
      </div>
    </MainLayout>
  );
}
