import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Sparkles, Database, Play, Download, CheckCircle, RefreshCw } from 'lucide-react';

interface BenchmarkDomainItem {
  id: string;
  name: string;
  category: string;
  sample_rows_generated: number;
  format: string;
  description: string;
}

const mockBenchmarks: BenchmarkDomainItem[] = [
  { id: 'bench_ecom', name: 'E-Commerce Transactions & Orders', category: 'Retail', sample_rows_generated: 1000000, format: 'PARQUET', description: 'Order IDs, customer tokens, basket items, tax, and order statuses' },
  { id: 'bench_ledger', name: 'Double-Entry General Financial Ledger', category: 'FinTech', sample_rows_generated: 500000, format: 'DELTA', description: 'Balanced debit/credit journal entries with chart of accounts' },
  { id: 'bench_ehr', name: 'Healthcare Clinical Encounters (EHR)', category: 'Health', sample_rows_generated: 250000, format: 'ICEBERG', description: 'ICD-10 diagnoses, CPT codes, systolic/diastolic blood pressure' },
  { id: 'bench_rtb', name: 'AdTech Real-Time Programmatic Bidding', category: 'AdTech', sample_rows_generated: 2000000, format: 'PARQUET', description: 'OpenRTB impressions, bids, clearing prices, and click rates' },
  { id: 'bench_logistics', name: 'Supply Chain & Warehouse Tracking', category: 'Logistics', sample_rows_generated: 750000, format: 'DELTA', description: 'SKU stock movements, carrier waybills, and dispatch timestamps' },
];

export default function SyntheticBenchmarkPage() {
  const columns: DataGridColumn<BenchmarkDomainItem>[] = [
    {
      key: 'name',
      header: 'Benchmark Domain Generator',
      render: (b) => (
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <strong className="text-white">{b.name}</strong>
        </div>
      ),
    },
    { key: 'category', header: 'Industry Sector' },
    { key: 'format', header: 'Target Format', render: (b) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{b.format}</span> },
    { key: 'sample_rows_generated', header: 'Capacity Benchmark', render: (b) => <span className="font-mono text-cyan-300 font-bold">{b.sample_rows_generated.toLocaleString()} rows</span> },
    {
      key: 'id',
      header: 'Action',
      render: (b) => (
        <button className="flex items-center gap-1 px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          <Play className="w-3 h-3 fill-white" /> Generate Data
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Synthetic Benchmark Generator — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sparkles className="w-7 h-7 text-cyan-400" />
            High-Throughput Synthetic Benchmark Generator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Generate massive multi-million row synthetic enterprise datasets across retail, FinTech, healthcare, AdTech, and supply chain domains.
          </p>
        </div>

        <DataGrid data={mockBenchmarks} columns={columns} title="Synthetic Enterprise Datasets" />
      </div>
    </MainLayout>
  );
}
