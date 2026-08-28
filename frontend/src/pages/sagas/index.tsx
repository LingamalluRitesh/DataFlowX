import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Undo2, RotateCcw, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

interface SagaExecutionItem {
  saga_id: string;
  pipeline_name: string;
  total_steps: number;
  completed_steps: number;
  compensation_triggered: boolean;
  status: 'COMPLETED' | 'COMPENSATED' | 'EXECUTING';
}

const mockSagas: SagaExecutionItem[] = [
  { saga_id: 'saga_9182', pipeline_name: 'multi_region_lakehouse_sync', total_steps: 4, completed_steps: 4, compensation_triggered: false, status: 'COMPLETED' },
  { saga_id: 'saga_9183', pipeline_name: 'financial_ledger_settlement', total_steps: 5, completed_steps: 3, compensation_triggered: true, status: 'COMPENSATED' },
  { saga_id: 'saga_9184', pipeline_name: 'customer_data_deletion_gdpr', total_steps: 3, completed_steps: 3, compensation_triggered: false, status: 'COMPLETED' },
];

export default function SagaCoordinatorPage() {
  const columns: DataGridColumn<SagaExecutionItem>[] = [
    { key: 'saga_id', header: 'Saga Instance ID', render: (s) => <strong className="text-cyan-400 font-mono">{s.saga_id}</strong> },
    { key: 'pipeline_name', header: 'Orchestrated Pipeline', render: (s) => <span className="font-mono text-white text-xs">{s.pipeline_name}</span> },
    {
      key: 'completed_steps',
      header: 'Step Progress',
      render: (s) => (
        <span className="font-mono text-slate-300">
          <span className="text-emerald-400 font-bold">{s.completed_steps}</span> / {s.total_steps} steps
        </span>
      ),
    },
    {
      key: 'compensation_triggered',
      header: 'Compensating Rollback',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.compensation_triggered
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
          }`}
        >
          {s.compensation_triggered ? 'ROLLBACK EXECUTED' : 'NO ROLLBACK'}
        </span>
      ),
    },
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
        <title>Distributed Saga Coordinator — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Undo2 className="w-7 h-7 text-cyan-400" />
            Distributed Saga & Compensating Transaction Manager
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Guarantees multi-step eventual consistency across distributed storage tiers with automated compensating rollback workflows.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Executed Sagas (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">124 Sagas</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compensation Success Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100.0% Clean Rollbacks</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Consistency Guarantee</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Eventual Consistency</div>
          </div>
        </div>

        <DataGrid data={mockSagas} columns={columns} title="Distributed Saga Execution Journal" />
      </div>
    </MainLayout>
  );
}
