import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileSpreadsheet, Database, CheckCircle, Clock, Layers, ArrowRight } from 'lucide-react';

interface ManifestListItem {
  manifest_path: string;
  snapshot_id: string;
  data_files_count: number;
  manifest_size_kb: number;
  partition_summary: string;
  file_format: string;
}

const mockManifests: ManifestListItem[] = [
  { manifest_path: 's3://lakehouse/metadata/snap-891249-m0.avro', snapshot_id: '#89124912093812', data_files_count: 32, manifest_size_kb: 4.8, partition_summary: 'region_id in (US_EAST, US_WEST)', file_format: 'AVRO_MANIFEST' },
  { manifest_path: 's3://lakehouse/metadata/snap-891249-m1.avro', snapshot_id: '#89124912093812', data_files_count: 24, manifest_size_kb: 3.6, partition_summary: 'region_id in (EU_CENTRAL, AP_SOUTH)', file_format: 'AVRO_MANIFEST' },
  { manifest_path: 's3://lakehouse/metadata/snap-891248-m0.avro', snapshot_id: '#89124912093811', data_files_count: 48, manifest_size_kb: 6.2, partition_summary: 'region_id in (GLOBAL_ALL)', file_format: 'AVRO_MANIFEST' },
];

export default function ManifestListsPage() {
  const columns: DataGridColumn<ManifestListItem>[] = [
    {
      key: 'manifest_path',
      header: 'Avro Manifest List URI',
      render: (m) => (
        <div className="flex items-center gap-2">
          <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs truncate max-w-xs">{m.manifest_path}</strong>
        </div>
      ),
    },
    { key: 'snapshot_id', header: 'Owner Snapshot', render: (m) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{m.snapshot_id}</span> },
    {
      key: 'data_files_count',
      header: 'Indexed Data Files',
      render: (m) => <span className="font-mono text-emerald-400 font-bold">{m.data_files_count} files</span>,
    },
    { key: 'manifest_size_kb', header: 'Manifest Size', render: (m) => <span className="font-mono text-slate-300">{m.manifest_size_kb.toFixed(1)} KB</span> },
    { key: 'partition_summary', header: 'Partition Key Bounds', render: (m) => <span className="font-mono text-cyan-300 text-xs">{m.partition_summary}</span> },
    {
      key: 'file_format',
      header: 'Format',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {m.file_format}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Avro Manifest Lists & Partition Bounds — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileSpreadsheet className="w-7 h-7 text-cyan-400" />
            Avro Manifest Lists & Partition Column Bounds Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy Avro manifest lists tracking added, existing, and deleted data file paths alongside lower/upper partition values for query pruning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Manifest Lists Indexed</div>
            <div className="text-2xl font-bold text-white mt-1">3 Manifest Lists</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Partition Pruning Efficiency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">94.2% Manifests Skipped</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Specification Standard</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Iceberg Format V2</div>
          </div>
        </div>

        <DataGrid data={mockManifests} columns={columns} title="Managed Avro Manifest Lists" />
      </div>
    </MainLayout>
  );
}
