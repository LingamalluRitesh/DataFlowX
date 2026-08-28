import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, Database, CheckCircle, Clock, FileText, ArrowRight } from 'lucide-react';

interface IcebergSnapshotItem {
  snapshot_id: string;
  parent_id: string;
  timestamp: string;
  operation: string;
  manifest_list_path: string;
  total_records: string;
  added_files: number;
}

const mockIceberg: IcebergSnapshotItem[] = [
  { snapshot_id: '89124912093812', parent_id: '89124912093811', timestamp: '2026-08-29 00:23:50 UTC', operation: 'APPEND', manifest_list_path: 's3://lakehouse/metadata/snap-891249.avro', total_records: '14,250,000', added_files: 4 },
  { snapshot_id: '89124912093811', parent_id: '89124912093810', timestamp: '2026-08-29 00:18:12 UTC', operation: 'OVERWRITE', manifest_list_path: 's3://lakehouse/metadata/snap-891248.avro', total_records: '14,200,000', added_files: 8 },
  { snapshot_id: '89124912093810', parent_id: 'None (Root)', timestamp: '2026-08-28 23:55:00 UTC', operation: 'CREATE_TABLE', manifest_list_path: 's3://lakehouse/metadata/snap-891247.avro', total_records: '10,000,000', added_files: 32 },
];

export default function IcebergMetaPage() {
  const columns: DataGridColumn<IcebergSnapshotItem>[] = [
    {
      key: 'snapshot_id',
      header: 'Iceberg Snapshot ID',
      render: (i) => (
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{i.snapshot_id}</strong>
        </div>
      ),
    },
    { key: 'parent_id', header: 'Parent Snapshot ID', render: (i) => <span className="font-mono text-slate-400 text-xs">{i.parent_id}</span> },
    { key: 'timestamp', header: 'Snapshot Timestamp', render: (i) => <span className="font-mono text-slate-300 text-xs">{i.timestamp}</span> },
    {
      key: 'operation',
      header: 'Operation Type',
      render: (i) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{i.operation}</span>,
    },
    { key: 'total_records', header: 'Total Table Records', render: (i) => <span className="font-mono text-emerald-400 font-bold">{i.total_records}</span> },
    { key: 'added_files', header: 'Added Data Files', render: (i) => <span className="font-mono text-cyan-300">+{i.added_files} files</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Apache Iceberg Table Metadata & Snapshots — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Layers className="w-7 h-7 text-cyan-400" />
            Apache Iceberg Table Metadata Spec & Snapshot Tree Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Inspection of `v2.metadata.json` metadata manifests, linear snapshot history trees, and hidden partition specs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Current Iceberg Snapshot</div>
            <div className="text-2xl font-bold text-white mt-1">#89124912093812</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Table Format Version</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">Iceberg Format V2</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Snapshot Retention Policy</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">30 Days (720h)</div>
          </div>
        </div>

        <DataGrid data={mockIceberg} columns={columns} title="Iceberg Table Snapshot Lineage" />
      </div>
    </MainLayout>
  );
}
