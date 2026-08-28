import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Fingerprint, CheckCircle, Activity, Sparkles, Database, Layers } from 'lucide-react';

interface DatasetFingerprintItem {
  dataset_name: string;
  total_rows: number;
  distinct_cardinality_est: number;
  null_percentage: number;
  p50_val: string;
  p99_val: string;
  hll_registers: number;
}

const mockFingerprints: DatasetFingerprintItem[] = [
  { dataset_name: 'gold.fact_orders', total_rows: 5000000, distinct_cardinality_est: 482100, null_percentage: 0.0, p50_val: '$84.50', p99_val: '$1,250.00', hll_registers: 16384 },
  { dataset_name: 'silver.dim_customers', total_rows: 250000, distinct_cardinality_est: 250000, null_percentage: 0.02, p50_val: '34.0 yrs', p99_val: '78.0 yrs', hll_registers: 16384 },
  { dataset_name: 'bronze.iot_telemetry', total_rows: 14200000, distinct_cardinality_est: 1200, null_percentage: 0.15, p50_val: '42.1°C', p99_val: '89.4°C', hll_registers: 16384 },
];

export default function FingerprintsHubPage() {
  const columns: DataGridColumn<DatasetFingerprintItem>[] = [
    { key: 'dataset_name', header: 'Dataset Identifier', render: (f) => <strong className="text-white font-mono">{f.dataset_name}</strong> },
    { key: 'total_rows', header: 'Total Records', render: (f) => <span className="font-mono text-slate-300">{f.total_rows.toLocaleString()}</span> },
    { key: 'distinct_cardinality_est', header: 'HLL Distinct Cardinality', render: (f) => <span className="font-mono text-cyan-400 font-bold">~{f.distinct_cardinality_est.toLocaleString()}</span> },
    { key: 'null_percentage', header: 'Null Rate', render: (f) => <span className="font-mono text-amber-400">{(f.null_percentage * 100).toFixed(1)}%</span> },
    { key: 'p50_val', header: 'T-Digest Median (P50)', render: (f) => <span className="font-mono text-emerald-400">{f.p50_val}</span> },
    { key: 'p99_val', header: 'T-Digest Tail (P99)', render: (f) => <span className="font-mono text-purple-400 font-bold">{f.p99_val}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Probabilistic Fingerprints & HyperLogLog — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Fingerprint className="w-7 h-7 text-cyan-400" />
            Statistical Dataset Fingerprinting & Probabilistic Sketching
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            HyperLogLog cardinality counters, T-Digest streaming quantile clusters, and Count-Min sketch heavy-hitter estimators.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Fingerprinted Datasets</div>
            <div className="text-2xl font-bold text-white mt-1">3 Datasets</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">HLL Standard Error</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0.81% Error Bound</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Fingerprint Memory Size</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">16 KB / dataset</div>
          </div>
        </div>

        <DataGrid data={mockFingerprints} columns={columns} title="Probabilistic Dataset Sketches" />
      </div>
    </MainLayout>
  );
}
