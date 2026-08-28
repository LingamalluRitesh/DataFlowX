import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, Database, CheckCircle, Sparkles, Cloud, Server } from 'lucide-react';

interface CatalogIntegrationItem {
  id: string;
  name: string;
  type: 'AWS_GLUE' | 'HIVE_METASTORE' | 'ICEBERG_REST' | 'UNITY_CATALOG';
  endpoint: string;
  registered_tables_count: number;
  sync_cadence: string;
  status: 'SYNCHRONIZED' | 'SYNCING';
}

const mockCatalogs: CatalogIntegrationItem[] = [
  { id: 'cat_glue_prod', name: 'AWS Glue Data Catalog (us-east-1)', type: 'AWS_GLUE', endpoint: 'aws:glue:us-east-1:123456789012', registered_tables_count: 32, sync_cadence: 'Continuous (EventBridge)', status: 'SYNCHRONIZED' },
  { id: 'cat_hms_lake', name: 'Apache Hive Metastore Thrift', type: 'HIVE_METASTORE', endpoint: 'thrift://metastore.internal:9083', registered_tables_count: 24, sync_cadence: 'Hourly', status: 'SYNCHRONIZED' },
  { id: 'cat_iceberg_rest', name: 'Iceberg REST OpenAPI Catalog', type: 'ICEBERG_REST', endpoint: 'http://iceberg-catalog:8181/v1', registered_tables_count: 14, sync_cadence: 'Real-time commit hook', status: 'SYNCHRONIZED' },
  { id: 'cat_unity_dbx', name: 'Databricks Unity Catalog', type: 'UNITY_CATALOG', endpoint: 'https://company.databricks.com', registered_tables_count: 18, sync_cadence: 'Bi-directional', status: 'SYNCHRONIZED' },
];

export default function CatalogsIndexPage() {
  const columns: DataGridColumn<CatalogIntegrationItem>[] = [
    {
      key: 'name',
      header: 'Lakehouse Metastore Catalog',
      render: (c) => (
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          <strong className="text-white">{c.name}</strong>
        </div>
      ),
    },
    {
      key: 'type',
      header: 'Catalog Protocol',
      render: (c) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{c.type}</span>,
    },
    { key: 'endpoint', header: 'Remote Endpoint URI', render: (c) => <span className="font-mono text-slate-400 text-xs">{c.endpoint}</span> },
    { key: 'registered_tables_count', header: 'Synchronized Tables', render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.registered_tables_count} tables</span> },
    { key: 'sync_cadence', header: 'Sync Mode', render: (c) => <span className="text-slate-300 text-xs">{c.sync_cadence}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Open Lakehouse Catalogs — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Layers className="w-7 h-7 text-cyan-400" />
            Open Lakehouse Catalogs & Metastore Sync
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Bi-directional synchronization with AWS Glue Data Catalog, Apache Hive Metastore, Iceberg REST, and Databricks Unity Catalog.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Lakehouse Catalogs</div>
            <div className="text-2xl font-bold text-white mt-1">4 Catalogs</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Synchronized Tables</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">88 Tables</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Schema Metadata Drift</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0% (In Sync)</div>
          </div>
        </div>

        <DataGrid data={mockCatalogs} columns={columns} title="Connected Lakehouse Metastore Catalogs" />
      </div>
    </MainLayout>
  );
}
