import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Plane, Zap, Activity, CheckCircle, Flame, Server, ArrowRight } from 'lucide-react';

interface FlightStreamSessionItem {
  ticket_id: string;
  client_id: string;
  throughput_mb_s: number;
  records_streamed: number;
  protocol: 'ARROW_FLIGHT_SQL' | 'ARROW_FLIGHT_IPC';
  duration_ms: number;
  status: 'STREAMING' | 'COMPLETED';
}

const mockFlightStreams: FlightStreamSessionItem[] = [
  { ticket_id: 'flight_tkt_9012', client_id: 'bi_tableau_connector_01', throughput_mb_s: 420.5, records_streamed: 2500000, protocol: 'ARROW_FLIGHT_SQL', duration_ms: 120.4, status: 'COMPLETED' },
  { ticket_id: 'flight_tkt_9013', client_id: 'python_notebook_client', throughput_mb_s: 580.0, records_streamed: 5000000, protocol: 'ARROW_FLIGHT_IPC', duration_ms: 180.2, status: 'COMPLETED' },
  { ticket_id: 'flight_tkt_9014', client_id: 'ml_training_worker_04', throughput_mb_s: 640.2, records_streamed: 1400000, protocol: 'ARROW_FLIGHT_SQL', duration_ms: 45.0, status: 'STREAMING' },
];

export default function ArrowFlightPage() {
  const columns: DataGridColumn<FlightStreamSessionItem>[] = [
    { key: 'ticket_id', header: 'Flight Ticket / Query ID', render: (f) => <strong className="text-cyan-400 font-mono text-xs">{f.ticket_id}</strong> },
    { key: 'client_id', header: 'Connected Client', render: (f) => <span className="font-mono text-white text-xs">{f.client_id}</span> },
    {
      key: 'protocol',
      header: 'Protocol Standard',
      render: (f) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{f.protocol}</span>,
    },
    { key: 'throughput_mb_s', header: 'Throughput', render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.throughput_mb_s} MB/s</span> },
    { key: 'records_streamed', header: 'Streamed Rows', render: (f) => <span className="font-mono text-slate-300">{f.records_streamed.toLocaleString()} rows</span> },
    {
      key: 'status',
      header: 'Status',
      render: (f) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            f.status === 'COMPLETED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-cyan-950 text-cyan-400 border border-cyan-800 animate-pulse'
          }`}
        >
          {f.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Apache Arrow Flight SQL Server — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Plane className="w-7 h-7 text-cyan-400" />
            Apache Arrow Flight SQL & High-Speed Stream Server
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy columnar gRPC streaming for business intelligence tools, pandas, Polars, and machine learning runtimes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Flight Server Ingress / Egress</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">640.2 MB/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Flight gRPC Streams</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1 Active Stream</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Speedup vs Traditional JDBC/ODBC</div>
            <div className="text-2xl font-bold text-purple-400 mt-1">18.4x Faster</div>
          </div>
        </div>

        <DataGrid data={mockFlightStreams} columns={columns} title="Active Arrow Flight SQL Streams" />
      </div>
    </MainLayout>
  );
}
