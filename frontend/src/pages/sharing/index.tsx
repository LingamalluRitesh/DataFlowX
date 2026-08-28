import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Share2, Lock, CheckCircle, Database, Layers, ArrowRight, Download } from 'lucide-react';

interface DeltaShareItem {
  share_name: string;
  schema_count: number;
  table_count: number;
  recipients_count: number;
  protocol_version: string;
  status: 'ACTIVE' | 'REVOKED';
}

const mockShares: DeltaShareItem[] = [
  { share_name: 'global_financial_share', schema_count: 2, table_count: 8, recipients_count: 14, protocol_version: 'v1.0 (Open Delta Sharing)', status: 'ACTIVE' },
  { share_name: 'marketing_analytics_share', schema_count: 1, table_count: 4, recipients_count: 6, protocol_version: 'v1.0 (Open Delta Sharing)', status: 'ACTIVE' },
  { share_name: 'b2b_partner_telemetry', schema_count: 1, table_count: 2, recipients_count: 22, protocol_version: 'v1.0 (Open Delta Sharing)', status: 'ACTIVE' },
];

export default function DeltaSharingPage() {
  const columns: DataGridColumn<DeltaShareItem>[] = [
    {
      key: 'share_name',
      header: 'Delta Share Identifier',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Share2 className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.share_name}</strong>
        </div>
      ),
    },
    { key: 'table_count', header: 'Shared Tables', render: (s) => <span className="font-mono text-slate-300">{s.table_count} tables</span> },
    { key: 'recipients_count', header: 'External Recipients', render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.recipients_count} partners</span> },
    { key: 'protocol_version', header: 'Protocol Standard', render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.protocol_version}</span> },
    {
      key: 'status',
      header: 'Status',
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
        <title>Delta Sharing & External Data Exchange — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Share2 className="w-7 h-7 text-cyan-400" />
            Delta Sharing & Multi-Party Data Exchange Portal
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Open Delta Sharing standard protocol server providing zero-copy direct Parquet streaming to external partners and business units.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Outbound Shares</div>
            <div className="text-2xl font-bold text-white mt-1">3 Shares</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">External Organizations Connected</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">42 Recipients</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Shared Lakehouse Data</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.4 TB Zero-Copy</div>
          </div>
        </div>

        <DataGrid data={mockShares} columns={columns} title="Active Delta Sharing Shares" />
      </div>
    </MainLayout>
  );
}
