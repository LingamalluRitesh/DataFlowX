import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ArrowRightLeft, CheckCircle, Copy, Sparkles, Terminal, Database } from 'lucide-react';

interface MigrationJobItem {
  id: string;
  source_dialect: 'TERADATA' | 'ORACLE_PLSQL' | 'SQL_SERVER_TSQL' | 'AMAZON_REDSHIFT';
  target_dialect: 'SNOWFLAKE' | 'POSTGRESQL' | 'PYSPARK' | 'GOOGLE_BIGQUERY';
  statements_transpiled: number;
  syntax_accuracy_pct: number;
  status: 'COMPLETED' | 'VALIDATING';
}

const mockMigrations: MigrationJobItem[] = [
  { id: 'mig_01', source_dialect: 'TERADATA', target_dialect: 'SNOWFLAKE', statements_transpiled: 1420, syntax_accuracy_pct: 99.8, status: 'COMPLETED' },
  { id: 'mig_02', source_dialect: 'ORACLE_PLSQL', target_dialect: 'POSTGRESQL', statements_transpiled: 850, syntax_accuracy_pct: 99.5, status: 'COMPLETED' },
  { id: 'mig_03', source_dialect: 'SQL_SERVER_TSQL', target_dialect: 'PYSPARK', statements_transpiled: 620, syntax_accuracy_pct: 100.0, status: 'COMPLETED' },
  { id: 'mig_04', source_dialect: 'AMAZON_REDSHIFT', target_dialect: 'GOOGLE_BIGQUERY', statements_transpiled: 410, syntax_accuracy_pct: 100.0, status: 'COMPLETED' },
];

export default function TranspilerStudioPage() {
  const [sourceSQL, setSourceSQL] = useState(`SEL customer_id, ZEROIFNULL(order_total) AS total,
CSUM(order_total, order_date) AS running_total
FROM orders_legacy;`);

  const [outputSQL, setOutputSQL] = useState(`SELECT customer_id, COALESCE(order_total, 0) AS total,
SUM(order_total) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS running_total
FROM orders_legacy;`);

  const columns: DataGridColumn<MigrationJobItem>[] = [
    {
      key: 'source_dialect',
      header: 'Source Legacy Dialect',
      render: (m) => <span className="bg-slate-800 text-amber-400 font-mono text-xs px-2 py-0.5 rounded">{m.source_dialect}</span>,
    },
    {
      key: 'target_dialect',
      header: 'Target Modern Dialect',
      render: (m) => <span className="bg-slate-800 text-cyan-400 font-mono text-xs px-2 py-0.5 rounded">{m.target_dialect}</span>,
    },
    { key: 'statements_transpiled', header: 'Statements Migrated', render: (m) => <span className="font-mono text-slate-300">{m.statements_transpiled.toLocaleString()} queries</span> },
    {
      key: 'syntax_accuracy_pct',
      header: 'Transpilation Accuracy',
      render: (m) => <span className="font-mono text-emerald-400 font-bold">{m.syntax_accuracy_pct}% Conformance</span>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {m.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>SQL Transpiler & Warehouse Migration — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ArrowRightLeft className="w-7 h-7 text-cyan-400" />
            Enterprise SQL Transpiler & Warehouse Migration Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated AST-level SQL translation: Teradata, Oracle PL/SQL, SQL Server T-SQL, and Redshift to Snowflake, BigQuery, and DuckDB.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
            <div className="text-xs font-semibold text-slate-400 uppercase">Input Legacy Dialect (Teradata / Oracle / T-SQL)</div>
            <textarea
              value={sourceSQL}
              onChange={(e) => setSourceSQL(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-amber-300 font-mono focus:outline-none focus:border-cyan-500 h-32 resize-none"
            />
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
            <div className="text-xs font-semibold text-slate-400 uppercase">Transpiled Target Dialect (Snowflake / DuckDB)</div>
            <textarea
              value={outputSQL}
              readOnly
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-cyan-300 font-mono focus:outline-none h-32 resize-none"
            />
          </div>
        </div>

        <DataGrid data={mockMigrations} columns={columns} title="Automated Warehouse Migration Suites" />
      </div>
    </MainLayout>
  );
}
