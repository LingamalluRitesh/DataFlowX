import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileSpreadsheet, Layers, Database, CheckCircle, ArrowRight } from 'lucide-react';

interface ManifestItem {
  manifest_path: string;
  format_type: 'ICEBERG_AVRO' | 'DELTA_SYMLINK' | 'HUDI_TIMELINE';
  snapshot_id: number;
  data_files_count: number;
  total_records: number;
  generated_at: string;
}

const mockManifests: ManifestItem[] = [
  { manifest_path: 's3://lakehouse/metadata/snap-108291.avro', format_type: 'ICEBERG_AVRO', snapshot_id: 108291, data_files_count: 16, total_records: 800000, generated_at: '2 mins ago' },
  { manifest_path: 's3://lakehouse/gold/fact_orders/_symlink_format_manifest/manifest', format_type: 'DELTA_SYMLINK', snapshot_id: 42, data_files_count: 8, total_records: 400000, generated_at: '15 mins ago' },
  { manifest_path: 's3://lakehouse/bronze/.hoodie/20260828235000.commit', format_type: 'HUDI_TIMELINE', snapshot_id: 20260828, data_files_count: 4, total_records: 125000, generated_at: '1 hour ago' },
];

export default function ManifestsIndexPage() {
  const columns: DataGridColumn<ManifestItem>[] = [
    {
      key: 'manifest_path',
      header: 'Manifest Location URI',
      render: (m) => (
        <div className="flex items-center gap-2">
          <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{m.manifest_path}</strong>
        </div>
      ),
    },
    {
      key: 'format_type',
      header: 'Manifest Specification',
      render: (m) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{m.format_type}</span>,
    },
    { key: 'snapshot_id', header: 'Snapshot ID', render: (m) => <span className="font-mono text-cyan-300 font-bold">{m.snapshot_id}</span> },
    { key: 'data_files_count', header: 'Referenced Files', render: (m) => <span className="font-mono text-slate-300">{m.data_files_count} files</span> },
    { key: 'total_records', header: 'Aggregated Records', render: (m) => <span className="font-mono text-emerald-400 font-bold">{m.total_records.toLocaleString()} rows</span> },
    { key: 'generated_at', header: 'Generated At' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Lakehouse Manifests Manager — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileSpreadsheet className="w-7 h-7 text-cyan-400" />
            Lakehouse Manifests & Symlink Generator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated generation and sync of Iceberg manifest lists, Delta symlink manifests for Athena/Presto, and Hudi timeline instants.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Lakehouse Manifests</div>
            <div className="text-2xl font-bold text-white mt-1">3 Manifests</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Athena / Presto Symlink Status</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Synchronized</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Tracked Parquet Files</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">28 Files</div>
          </div>
        </div>

        <DataGrid data={mockManifests} columns={columns} title="Lakehouse Manifest File Registry" />
      </div>
    </MainLayout>
  );
}
