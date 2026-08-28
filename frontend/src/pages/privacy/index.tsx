import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Lock, ShieldCheck, EyeOff, CheckCircle, Sparkles, UserCheck } from 'lucide-react';

interface PrivacyDatasetItem {
  dataset_name: string;
  quasi_identifiers: string[];
  k_anonymity_val: number;
  l_diversity_val: number;
  t_closeness_emd: number;
  differential_privacy_eps: number;
  status: 'COMPLIANT' | 'RE-IDENTIFICATION_RISK';
}

const mockPrivacyDatasets: PrivacyDatasetItem[] = [
  { dataset_name: 'silver.dim_customers', quasi_identifiers: ['age_bracket', 'gender', 'zip3'], k_anonymity_val: 12, l_diversity_val: 4, t_closeness_emd: 0.08, differential_privacy_eps: 0.5, status: 'COMPLIANT' },
  { dataset_name: 'gold.patient_clinical_encounters', quasi_identifiers: ['birth_year', 'postal_code', 'ethnicity'], k_anonymity_val: 8, l_diversity_val: 5, t_closeness_emd: 0.11, differential_privacy_eps: 1.0, status: 'COMPLIANT' },
  { dataset_name: 'silver.user_browsing_telemetry', quasi_identifiers: ['device_family', 'country_code'], k_anonymity_val: 45, l_diversity_val: 8, t_closeness_emd: 0.04, differential_privacy_eps: 0.2, status: 'COMPLIANT' },
];

export default function PrivacyCompliancePage() {
  const columns: DataGridColumn<PrivacyDatasetItem>[] = [
    { key: 'dataset_name', header: 'Dataset Target', render: (p) => <strong className="text-white font-mono">{p.dataset_name}</strong> },
    {
      key: 'quasi_identifiers',
      header: 'Quasi-Identifiers',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.quasi_identifiers.map((qi) => (
            <span key={qi} className="bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-mono text-[10px]">
              {qi}
            </span>
          ))}
        </div>
      ),
    },
    { key: 'k_anonymity_val', header: 'k-Anonymity', render: (p) => <span className="font-mono text-cyan-400 font-bold">k={p.k_anonymity_val}</span> },
    { key: 'l_diversity_val', header: 'l-Diversity', render: (p) => <span className="font-mono text-purple-400 font-bold">l={p.l_diversity_val}</span> },
    { key: 't_closeness_emd', header: 't-Closeness (EMD)', render: (p) => <span className="font-mono text-emerald-400 font-bold">t={p.t_closeness_emd}</span> },
    { key: 'differential_privacy_eps', header: 'Diff Privacy (ε)', render: (p) => <span className="font-mono text-amber-400">ε={p.differential_privacy_eps}</span> },
    {
      key: 'status',
      header: 'Privacy Health',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Differential Privacy & Anonymity Center — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Lock className="w-7 h-7 text-emerald-400" />
            Differential Privacy & K-Anonymity Compliance Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Mathematical privacy guarantees: ε-Differential Privacy Laplace noise, k-Anonymity equivalence classes, and Earth Mover's Distance t-Closeness.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Protected Datasets</div>
            <div className="text-2xl font-bold text-white mt-1">3 Datasets</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Re-Identification Risk</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">&lt; 0.01% (Extremely Low)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Privacy Budget Spent (24h)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">ε = 1.7 / 10.0</div>
          </div>
        </div>

        <DataGrid data={mockPrivacyDatasets} columns={columns} title="Anonymized & Differentially Private Datasets" />
      </div>
    </MainLayout>
  );
}
