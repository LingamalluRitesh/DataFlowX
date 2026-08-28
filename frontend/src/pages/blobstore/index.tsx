import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cloud, HardDrive, Database, Server, CheckCircle, ArrowRight } from 'lucide-react';

interface BlobStoreBucketItem {
  uri: string;
  provider: 'AWS_S3' | 'GOOGLE_GCS' | 'AZURE_ADLS';
  region: string;
  total_objects: number;
  total_size_gb: number;
  encryption: string;
}

const mockBuckets: BlobStoreBucketItem[] = [
  { uri: 's3://lakehouse-prod-us-east-1/', provider: 'AWS_S3', region: 'us-east-1', total_objects: 4520, total_size_gb: 1240.5, encryption: 'SSE-KMS (aws/s3)' },
  { uri: 'gs://lakehouse-analytics-eu/', provider: 'GOOGLE_GCS', region: 'europe-west1', total_objects: 1890, total_size_gb: 620.0, encryption: 'Google-managed' },
  { uri: 'abfs://lakehouse@dataflowx.dfs.core.windows.net/', provider: 'AZURE_ADLS', region: 'eastus2', total_objects: 3100, total_size_gb: 890.2, encryption: 'Microsoft-managed' },
];

export default function BlobStoreExplorerPage() {
  const columns: DataGridColumn<BlobStoreBucketItem>[] = [
    {
      key: 'uri',
      header: 'Storage Bucket URI',
      render: (b) => (
        <div className="flex items-center gap-2">
          <Cloud className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{b.uri}</strong>
        </div>
      ),
    },
    {
      key: 'provider',
      header: 'Cloud Provider',
      render: (b) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{b.provider}</span>,
    },
    { key: 'region', header: 'Region', render: (b) => <span className="font-mono text-slate-300 text-xs">{b.region}</span> },
    { key: 'total_objects', header: 'Objects', render: (b) => <span className="font-mono text-emerald-400 font-bold">{b.total_objects.toLocaleString()}</span> },
    { key: 'total_size_gb', header: 'Data Stored', render: (b) => <span className="font-mono text-cyan-300 font-bold">{b.total_size_gb} GB</span> },
    { key: 'encryption', header: 'Encryption At Rest', render: (b) => <span className="text-slate-400 text-xs">{b.encryption}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Multi-Cloud Object Storage Explorer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Cloud className="w-7 h-7 text-cyan-400" />
            Multi-Cloud Object Storage Lake Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Unified abstraction layer connecting AWS S3, Google Cloud Storage (GCS), and Azure Data Lake Storage Gen2 (ADLS).
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Connected Lakes</div>
            <div className="text-2xl font-bold text-white mt-1">3 Cloud Lakes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Objects Tracked</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">9,510 Objects</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Aggregated Footprint</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">2.75 TB</div>
          </div>
        </div>

        <DataGrid data={mockBuckets} columns={columns} title="Multi-Cloud Object Storage Buckets" />
      </div>
    </MainLayout>
  );
}
