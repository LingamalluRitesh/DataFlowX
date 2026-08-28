import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { AlertOctagon, HelpCircle, CheckCircle, Flame, Layers, ArrowRight, ShieldAlert } from 'lucide-react';

interface RootCauseAnalysisItem {
  incident_id: string;
  failed_pipeline: string;
  isolated_root_cause: string;
  error_category: 'OUT_OF_MEMORY' | 'NETWORK_TIMEOUT' | 'SCHEMA_MISMATCH';
  remediation_recommendation: string;
  blast_radius_tier: string;
  confidence_score: number;
}

const mockRCAs: RootCauseAnalysisItem[] = [
  {
    incident_id: 'inc_8912',
    failed_pipeline: 'etl_daily_gold_aggregator',
    isolated_root_cause: 'Task "VectorBatch_SIMD_Agg" exceeded container memory ceiling (16GB)',
    error_category: 'OUT_OF_MEMORY',
    remediation_recommendation: 'Increase worker RAM limit or enable bin-packing chunk slicing (128MB chunks).',
    blast_radius_tier: 'TIER_1_OUTAGE (Executive Revenue Board Affected)',
    confidence_score: 98.5,
  },
  {
    incident_id: 'inc_8913',
    failed_pipeline: 'cdc_wal_bronze_stream',
    isolated_root_cause: 'PostgreSQL upstream WAL socket read timed out after 30,000ms',
    error_category: 'NETWORK_TIMEOUT',
    remediation_recommendation: 'Increase keepalive probe frequency and check RDS replication slot lag.',
    blast_radius_tier: 'TIER_2_OUTAGE (Bronze Ingestion Delay)',
    confidence_score: 92.0,
  },
];

export default function RCADiagnosticsPage() {
  const columns: DataGridColumn<RootCauseAnalysisItem>[] = [
    {
      key: 'failed_pipeline',
      header: 'Failed DAG Pipeline',
      render: (r) => (
        <div>
          <strong className="text-white font-mono text-xs">{r.failed_pipeline}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{r.incident_id}</div>
        </div>
      ),
    },
    {
      key: 'error_category',
      header: 'Identified Failure Pattern',
      render: (r) => (
        <span className="bg-red-950 text-red-400 border border-red-800 font-mono text-[10px] px-2 py-0.5 rounded font-bold">
          {r.error_category}
        </span>
      ),
    },
    { key: 'isolated_root_cause', header: 'Isolated Root Cause Node', sortable: false },
    { key: 'remediation_recommendation', header: 'Remediation Advice', sortable: false },
    {
      key: 'confidence_score',
      header: 'AI Confidence',
      render: (r) => <span className="font-mono text-emerald-400 font-bold">{r.confidence_score}%</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Automated Root Cause Analysis (RCA) — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <AlertOctagon className="w-7 h-7 text-red-400" />
            Automated Root Cause Analysis (RCA) & Blast Radius Diagnostics
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Reverse DAG dependency traversal, NLP stack trace classification, and downstream consumer outage quantification.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Root Cause Isolation Time</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">120 Milliseconds</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Classification Accuracy</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">98.5% Confidence</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Actionable Remediation Provided</div>
            <div className="text-2xl font-bold text-white mt-1">100% of Failures</div>
          </div>
        </div>

        <DataGrid data={mockRCAs} columns={columns} title="Active Incident RCA Reports" />
      </div>
    </MainLayout>
  );
}
