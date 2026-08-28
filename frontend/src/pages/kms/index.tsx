import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Key, Lock, ShieldCheck, CheckCircle, RefreshCw, Layers } from 'lucide-react';

interface KMSKeyItem {
  key_id: string;
  provider: 'AWS_KMS' | 'GCP_KMS' | 'AZURE_KEYVAULT';
  key_algorithm: string;
  key_usage: string;
  rotation_cadence: string;
  status: 'ENABLED' | 'ROTATING';
}

const mockKeys: KMSKeyItem[] = [
  { key_id: 'arn:aws:kms:us-east-1:123456789012:key/dataflowx-lake-master', provider: 'AWS_KMS', key_algorithm: 'AES_256_GCM (SYMMETRIC_DEFAULT)', key_usage: 'ENVELOPE_ENCRYPTION', rotation_cadence: 'Annual (AWS-managed)', status: 'ENABLED' },
  { key_id: 'projects/dfx-prod/locations/global/keyRings/lake/cryptoKeys/lakehouse', provider: 'GCP_KMS', key_algorithm: 'GOOGLE_SYMMETRIC_ENCRYPTION', key_usage: 'ENVELOPE_ENCRYPTION', rotation_cadence: '90 Days', status: 'ENABLED' },
  { key_id: 'https://dfx-vault.vault.azure.net/keys/lakehouse-cmk', provider: 'AZURE_KEYVAULT', key_algorithm: 'RSA-HSM 4096-bit', key_usage: 'KEY_ENCAPSULATION', rotation_cadence: '180 Days', status: 'ENABLED' },
];

export default function KMSManagementPage() {
  const columns: DataGridColumn<KMSKeyItem>[] = [
    {
      key: 'key_id',
      header: 'KMS Customer Managed Key (CMK)',
      render: (k) => (
        <div className="flex items-center gap-2">
          <Key className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs truncate max-w-sm">{k.key_id}</strong>
        </div>
      ),
    },
    {
      key: 'provider',
      header: 'KMS Provider',
      render: (k) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{k.provider}</span>,
    },
    { key: 'key_algorithm', header: 'Cipher Algorithm', render: (k) => <span className="font-mono text-slate-300 text-xs">{k.key_algorithm}</span> },
    { key: 'rotation_cadence', header: 'Key Rotation', render: (k) => <span className="text-slate-400 text-xs">{k.rotation_cadence}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (k) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {k.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>KMS Envelope Encryption & Security — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Lock className="w-7 h-7 text-cyan-400" />
            KMS Envelope Encryption & Multi-Cloud Key Management
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AES-256-GCM envelope encryption protecting sensitive Lakehouse Parquet partitions at rest with AWS KMS, Google Cloud KMS, and Azure Key Vault HSMs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Encryption Keys</div>
            <div className="text-2xl font-bold text-white mt-1">3 CMKs</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Hardware Security Level</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">FIPS 140-2 Level 3</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Encrypted Lakehouse Volume</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Encrypted at Rest</div>
          </div>
        </div>

        <DataGrid data={mockKeys} columns={columns} title="Managed Customer Encryption Keys (CMKs)" />
      </div>
    </MainLayout>
  );
}
