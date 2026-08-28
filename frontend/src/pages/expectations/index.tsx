import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { CheckCircle2, ShieldCheck, AlertTriangle, Play, Sparkles, FileCheck } from 'lucide-react';

interface ExpectationSuiteItem {
  suite_name: string;
  dataset_target: string;
  total_expectations: number;
  passing_count: number;
  success_rate_pct: number;
  status: 'PASSED' | 'FAILED';
}

const mockSuites: ExpectationSuiteItem[] = [
  { suite_name: 'fact_orders_financial_integrity_suite', dataset_target: 'gold.fact_orders', total_expectations: 16, passing_count: 16, success_rate_pct: 100.0, status: 'PASSED' },
  { suite_name: 'dim_customers_identity_suite', dataset_target: 'silver.dim_customers', total_expectations: 12, passing_count: 12, success_rate_pct: 100.0, status: 'PASSED' },
  { suite_name: 'iot_telemetry_range_suite', dataset_target: 'bronze.iot_telemetry', total_expectations: 8, passing_count: 8, success_rate_pct: 100.0, status: 'PASSED' },
];

export default function GreatExpectationsPage() {
  const columns: DataGridColumn<ExpectationSuiteItem>[] = [
    {
      key: 'suite_name',
      header: 'Great Expectations Suite',
      render: (e) => (
        <div className="flex items-center gap-2">
          <FileCheck className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{e.suite_name}</strong>
        </div>
      ),
    },
    { key: 'dataset_target', header: 'Target Dataset', render: (e) => <span className="font-mono text-slate-300 text-xs">{e.dataset_target}</span> },
    { key: 'total_expectations', header: 'Total Assertions', render: (e) => <span className="font-mono text-slate-400">{e.total_expectations} assertions</span> },
    {
      key: 'success_rate_pct',
      header: 'Quality Score',
      render: (e) => <span className="font-mono text-emerald-400 font-bold">{e.success_rate_pct}% ({e.passing_count}/{e.total_expectations})</span>,
    },
    {
      key: 'status',
      header: 'Suite Result',
      render: (e) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {e.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Great Expectations Quality Suites — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <CheckCircle2 className="w-7 h-7 text-emerald-400" />
            Great Expectations Data Quality Assertion Suites
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Declarative data quality testing framework with column value bounds, uniqueness constraints, and schema conformance validation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Expectation Suites</div>
            <div className="text-2xl font-bold text-white mt-1">3 Suites</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Automated Assertions</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">36 Assertions Passed</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Standard Conformance</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Great Expectations v0.18</div>
          </div>
        </div>

        <DataGrid data={mockSuites} columns={columns} title="Configured Expectation Suites" />
      </div>
    </MainLayout>
  );
}
