import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileText, Database, CheckCircle, Clock, Layers, ArrowRight } from 'lucide-react';

interface WALTransactionItem {
  xid: number;
  table_name: string;
  lsn_position: string;
  buffered_ops_count: number;
  transaction_duration_ms: number;
  status: 'COMMITTED' | 'IN_FLIGHT';
}

const mockWAL: WALTransactionItem[] = [
  { xid: 894120, table_name: 'postgres.public.orders', lsn_position: '0/16B2D80', buffered_ops_count: 14, transaction_duration_ms: 12.4, status: 'COMMITTED' },
  { xid: 894121, table_name: 'postgres.public.order_items', lsn_position: '0/16B3100', buffered_ops_count: 48, transaction_duration_ms: 24.1, status: 'COMMITTED' },
  { xid: 894122, table_name: 'mysql.inventory.stock_levels', lsn_position: 'binlog.000412:4892', buffered_ops_count: 6, transaction_duration_ms: 5.0, status: 'COMMITTED' },
];

export default function WALCDCBufferPage() {
  const columns: DataGridColumn<WALTransactionItem>[] = [
    {
      key: 'xid',
      header: 'Transaction ID (XID)',
      render: (w) => (
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">XID #{w.xid}</strong>
        </div>
      ),
    },
    { key: 'table_name', header: 'Source Table', render: (w) => <span className="text-slate-300 font-mono text-xs">{w.table_name}</span> },
    { key: 'lsn_position', header: 'WAL / Binlog LSN', render: (w) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{w.lsn_position}</span> },
    {
      key: 'buffered_ops_count',
      header: 'Operations in Batch',
      render: (w) => <span className="font-mono text-cyan-300 font-bold">{w.buffered_ops_count} ops</span>,
    },
    {
      key: 'transaction_duration_ms',
      header: 'Buffer Latency',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.transaction_duration_ms} ms</span>,
    },
    {
      key: 'status',
      header: 'Commit State',
      render: (w) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {w.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>WAL CDC Transaction Buffer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileText className="w-7 h-7 text-cyan-400" />
            Write-Ahead Log (WAL) & Binlog Transaction Buffer Monitor
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Buffers in-flight multi-statement CDC transactions until commit to ensure zero partial/torn transaction writes in Lakehouses.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Buffered Transactions</div>
            <div className="text-2xl font-bold text-white mt-1">0 In-Flight (Clean)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Committed CDC Batches (24h)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">1.4M Batches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Transaction Atomicity</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Strict ACID</div>
          </div>
        </div>

        <DataGrid data={mockWAL} columns={columns} title="Committed CDC Transaction Streams" />
      </div>
    </MainLayout>
  );
}
