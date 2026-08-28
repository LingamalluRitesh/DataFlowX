import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Lock, CheckCircle, Sparkles, Layers, Sliders } from 'lucide-react';

interface DPQueryItem {
  query_id: string;
  target_table: string;
  aggregation_type: 'COUNT' | 'SUM' | 'AVG';
  true_value: string;
  epsilon_budget: number;
  noise_mechanism: 'LAPLACE' | 'GAUSSIAN';
  dp_perturbed_result: string;
}

const mockDP: DPQueryItem[] = [
  { query_id: 'dp_q_01', target_table: 'gold.fact_orders', aggregation_type: 'COUNT', true_value: '1,450,200 orders', epsilon_budget: 0.5, noise_mechanism: 'LAPLACE', dp_perturbed_result: '1,450,203 orders (DP Verified)' },
  { query_id: 'dp_q_02', target_table: 'silver.dim_customers', aggregation_type: 'SUM', true_value: '$45,820,100.00', epsilon_budget: 1.0, noise_mechanism: 'LAPLACE', dp_perturbed_result: '$45,820,084.20 (DP Verified)' },
  { query_id: 'dp_q_03', target_table: 'bronze.telemetry_sessions', aggregation_type: 'AVG', true_value: '142.50 ms', epsilon_budget: 0.8, noise_mechanism: 'GAUSSIAN', dp_perturbed_result: '142.48 ms (DP Verified)' },
];

export default function DifferentialPrivacyStudioPage() {
  const columns: DataGridColumn<DPQueryItem>[] = [
    {
      key: 'query_id',
      header: 'DP Protected Query',
      render: (d) => (
        <div>
          <strong className="text-white font-mono text-xs">{d.query_id}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{d.target_table}</div>
        </div>
      ),
    },
    {
      key: 'aggregation_type',
      header: 'Aggregation Op',
      render: (d) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{d.aggregation_type}</span>,
    },
    { key: 'true_value', header: 'Internal True Metric', render: (d) => <span className="font-mono text-slate-400 text-xs">{d.true_value}</span> },
    {
      key: 'epsilon_budget',
      header: 'Privacy Budget (ε)',
      render: (d) => <span className="font-mono text-cyan-300 font-bold">ε = {d.epsilon_budget}</span>,
    },
    { key: 'noise_mechanism', header: 'Noise Mechanism', render: (d) => <span className="font-mono text-slate-300 text-xs">{d.noise_mechanism}</span> },
    {
      key: 'dp_perturbed_result',
      header: 'Differential Privacy Output',
      render: (d) => <span className="font-mono text-emerald-400 font-bold">{d.dp_perturbed_result}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Differential Privacy (DP) Noise Engine — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-7 h-7 text-emerald-400" />
            Differential Privacy (DP) Laplace & Gaussian Noise Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Mathematical privacy guarantees for public analytics and external data sharing preventing membership inference attacks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Privacy Budget (Epsilon)</div>
            <div className="text-2xl font-bold text-white mt-1">ε = 10.0 / day</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Remaining Privacy Budget</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">ε = 7.7 Remaining</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Privacy Guarantee</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">(ε, δ)-DP Mathematical</div>
          </div>
        </div>

        <DataGrid data={mockDP} columns={columns} title="Differential Privacy Aggregation Queries" />
      </div>
    </MainLayout>
  );
}
