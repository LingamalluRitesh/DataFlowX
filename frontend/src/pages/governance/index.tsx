import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Lock, BookMarked, Eye, AlertOctagon, CheckCircle, Plus } from 'lucide-react';

interface GlossaryItem {
  id: string;
  term: string;
  definition: string;
  domain: string;
  owner_email: string;
  tags: string[];
}

const mockGlossary: GlossaryItem[] = [
  { id: 'term_01', term: 'Active Customer', definition: 'A registered user who completed at least one transaction in the trailing 90 days.', domain: 'CRM', owner_email: 'growth@dataflowx.io', tags: ['kpi', 'customer'] },
  { id: 'term_02', term: 'Net Gross Revenue', definition: 'Total captured invoice volume minus refunds, payment gateway processing fees, and promotional discounts.', domain: 'Finance', owner_email: 'cfo-team@dataflowx.io', tags: ['finance', 'revenue'] },
  { id: 'term_03', term: 'Customer Churn', definition: 'The proportion of contractual subscribers who cancelled their plan within the calendar billing month.', domain: 'Subscription', owner_email: 'success@dataflowx.io', tags: ['retention'] },
];

export default function GovernanceIndexPage() {
  const columns: DataGridColumn<GlossaryItem>[] = [
    { key: 'term', header: 'Business Term', render: (g) => <strong className="text-cyan-400">{g.term}</strong> },
    { key: 'definition', header: 'Official Standard Definition', sortable: false },
    { key: 'domain', header: 'Domain' },
    { key: 'owner_email', header: 'Domain Steward' },
    {
      key: 'tags',
      header: 'Tags',
      render: (g) => (
        <div className="flex flex-wrap gap-1">
          {g.tags.map((t) => (
            <span key={t} className="bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded text-[10px]">
              #{t}
            </span>
          ))}
        </div>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Data Governance & GDPR Compliance — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <ShieldCheck className="w-7 h-7 text-emerald-400" />
              Data Governance & Compliance Center
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Enterprise business glossary stewardship, GDPR/CCPA privacy controls, PII scanning, and cryptographic token policies.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Add Glossary Term
          </button>
        </div>

        {/* Governance Health Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="text-xs text-slate-500 font-semibold uppercase">GDPR Compliance Posture</div>
              <CheckCircle className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2">100% Compliant</div>
            <div className="text-xs text-slate-400 mt-1">All 14 PII tables protected with SHA-256 salted tokens</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="text-xs text-slate-500 font-semibold uppercase">Business Glossary Terms</div>
              <BookMarked className="w-5 h-5 text-cyan-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2">48 Defined Terms</div>
            <div className="text-xs text-slate-400 mt-1">Mapped across 6 enterprise business domains</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="text-xs text-slate-500 font-semibold uppercase">Sensitive PII Columns</div>
              <Lock className="w-5 h-5 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2">12 Masked Fields</div>
            <div className="text-xs text-slate-400 mt-1">Credit cards, emails, SSNs, and phone numbers</div>
          </div>
        </div>

        {/* Glossary Table */}
        <DataGrid data={mockGlossary} columns={columns} title="Enterprise Business Glossary" />
      </div>
    </MainLayout>
  );
}
