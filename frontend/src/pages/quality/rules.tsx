import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Plus, CheckCircle, AlertTriangle, Sparkles, Filter, Code } from 'lucide-react';

interface QualityRuleItem {
  id: string;
  name: string;
  rule_type: string;
  target_column: string;
  threshold_pct: number;
  last_pass_rate: number;
  status: 'PASSING' | 'FAILING';
}

const mockQualityRules: QualityRuleItem[] = [
  { id: 'rule_01', name: 'zscore_outlier_order_total', rule_type: 'STATISTICAL_ZSCORE', target_column: 'order_total', threshold_pct: 99.0, last_pass_rate: 99.8, status: 'PASSING' },
  { id: 'rule_02', name: 'luhn_check_credit_card', rule_type: 'LUHN_CHECKSUM', target_column: 'card_number', threshold_pct: 100.0, last_pass_rate: 100.0, status: 'PASSING' },
  { id: 'rule_03', name: 'iqr_outlier_latency', rule_type: 'IQR_ANOMALY', target_column: 'duration_ms', threshold_pct: 98.0, last_pass_rate: 98.4, status: 'PASSING' },
  { id: 'rule_04', name: 'uuid_format_session_id', rule_type: 'UUID_FORMAT', target_column: 'session_id', threshold_pct: 100.0, last_pass_rate: 100.0, status: 'PASSING' },
  { id: 'rule_05', name: 'monotonic_increasing_id', rule_type: 'MONOTONIC_INCREASING', target_column: 'sequence_num', threshold_pct: 100.0, last_pass_rate: 99.9, status: 'FAILING' },
];

export default function QualityRulesStudioPage() {
  const columns: DataGridColumn<QualityRuleItem>[] = [
    {
      key: 'name',
      header: 'Rule Definition Name',
      render: (r) => (
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{r.name}</strong>
        </div>
      ),
    },
    {
      key: 'rule_type',
      header: 'Rule Type',
      render: (r) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{r.rule_type}</span>,
    },
    {
      key: 'target_column',
      header: 'Target Column',
      render: (r) => <span className="font-mono text-cyan-300 font-semibold">{r.target_column}</span>,
    },
    {
      key: 'threshold_pct',
      header: 'Threshold SLA',
      render: (r) => <span className="font-mono text-slate-300">&ge; {r.threshold_pct}%</span>,
    },
    {
      key: 'last_pass_rate',
      header: 'Last Run Pass Rate',
      render: (r) => (
        <span className={`font-mono font-bold ${r.last_pass_rate >= r.threshold_pct ? 'text-emerald-400' : 'text-red-400'}`}>
          {r.last_pass_rate}%
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (r) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            r.status === 'PASSING'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-red-950 text-red-400 border border-red-800 animate-pulse'
          }`}
        >
          {r.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Data Quality Rules Suite — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <ShieldCheck className="w-7 h-7 text-cyan-400" />
              Advanced Quality Rules & Assertions Studio
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Configure statistical Z-Score tests, IQR anomaly bands, Luhn MOD-10 checksums, UUID format validation, and custom DSL assertions.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Create Assertion Rule
          </button>
        </div>

        <DataGrid data={mockQualityRules} columns={columns} title="Configured Quality Rules" />
      </div>
    </MainLayout>
  );
}
