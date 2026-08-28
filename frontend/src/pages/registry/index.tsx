import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileCode, CheckCircle, ShieldCheck, Layers, GitCommit, Copy } from 'lucide-react';

interface SchemaSubjectItem {
  id: number;
  subject: string;
  version: number;
  schema_type: 'AVRO' | 'PROTOBUF' | 'JSON_SCHEMA';
  compatibility_mode: 'BACKWARD' | 'FORWARD' | 'FULL';
  fingerprint_md5: string;
  status: 'ACTIVE' | 'DEPRECATED';
}

const mockSubjects: SchemaSubjectItem[] = [
  { id: 1, subject: 'events.user_purchases-value', version: 3, schema_type: 'AVRO', compatibility_mode: 'BACKWARD', fingerprint_md5: 'a8b7c6d5e4f3a2b1', status: 'ACTIVE' },
  { id: 2, subject: 'telemetry.device_metrics-value', version: 2, schema_type: 'PROTOBUF', compatibility_mode: 'FULL', fingerprint_md5: 'f1e2d3c4b5a69788', status: 'ACTIVE' },
  { id: 3, subject: 'cdc.customers_cdc-value', version: 1, schema_type: 'AVRO', compatibility_mode: 'BACKWARD', fingerprint_md5: '3c4b5a69788f1e2d', status: 'ACTIVE' },
];

export default function SchemaRegistryPage() {
  const columns: DataGridColumn<SchemaSubjectItem>[] = [
    {
      key: 'subject',
      header: 'Subject Name',
      render: (s) => (
        <div className="flex items-center gap-2">
          <FileCode className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.subject}</strong>
        </div>
      ),
    },
    { key: 'version', header: 'Version', render: (s) => <span className="font-mono text-cyan-300 font-bold">v{s.version}</span> },
    {
      key: 'schema_type',
      header: 'Schema Format',
      render: (s) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{s.schema_type}</span>,
    },
    {
      key: 'compatibility_mode',
      header: 'Compatibility Policy',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.compatibility_mode}
        </span>
      ),
    },
    { key: 'fingerprint_md5', header: 'Fingerprint MD5', render: (s) => <span className="font-mono text-slate-400 text-xs">{s.fingerprint_md5}</span> },
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
        <title>Schema Registry & Evolution — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileCode className="w-7 h-7 text-cyan-400" />
            Schema Registry & Evolution Governance
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Confluent-compatible schema registry managing Avro and Protocol Buffer versions, fingerprint hashes, and compatibility verification.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Registered Subjects</div>
            <div className="text-2xl font-bold text-white mt-1">3 Subjects</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compatibility Conformance</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Validated</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Default Compatibility Mode</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">BACKWARD</div>
          </div>
        </div>

        <DataGrid data={mockSubjects} columns={columns} title="Registered Schema Subjects & Versions" />
      </div>
    </MainLayout>
  );
}
