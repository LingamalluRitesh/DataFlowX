import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Plane, Zap, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface FlightEndpointItem {
  endpoint_uri: string;
  ticket_id: string;
  serialized_batch_format: string;
  stream_throughput_mb_s: number;
  active_client_connections: number;
  auth_type: string;
}

const mockFlightEndpoints: FlightEndpointItem[] = [
  { endpoint_uri: 'grpc+tls://flight.dataflowx.internal:32010', ticket_id: 'ticket_gold_orders_q3', serialized_batch_format: 'Arrow RecordBatch IPC (ZSTD)', stream_throughput_mb_s: 3450, active_client_connections: 18, auth_type: 'mTLS + JWT Bearer' },
  { endpoint_uri: 'grpc+tls://flight.dataflowx.internal:32010', ticket_id: 'ticket_dim_customers_all', serialized_batch_format: 'Arrow RecordBatch IPC (Uncompressed)', stream_throughput_mb_s: 4800, active_client_connections: 8, auth_type: 'mTLS + JWT Bearer' },
  { endpoint_uri: 'grpc+tls://flight.dataflowx.internal:32010', ticket_id: 'ticket_iot_telemetry_hot', serialized_batch_format: 'Arrow RecordBatch IPC (LZ4)', stream_throughput_mb_s: 2900, active_client_connections: 12, auth_type: 'mTLS + JWT Bearer' },
];

export default function FlightSQLServerPage() {
  const columns: DataGridColumn<FlightEndpointItem>[] = [
    {
      key: 'endpoint_uri',
      header: 'Flight SQL Server Endpoint',
      render: (f) => (
        <div className="flex items-center gap-2">
          <Plane className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{f.endpoint_uri}</strong>
        </div>
      ),
    },
    { key: 'ticket_id', header: 'Flight Ticket Descriptor', render: (f) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{f.ticket_id}</span> },
    { key: 'serialized_batch_format', header: 'IPC Wire Format', render: (f) => <span className="text-slate-300 text-xs">{f.serialized_batch_format}</span> },
    {
      key: 'stream_throughput_mb_s',
      header: 'Wire Throughput',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.stream_throughput_mb_s.toLocaleString()} MB/s</span>,
    },
    { key: 'active_client_connections', header: 'Client Streams', render: (f) => <span className="font-mono text-cyan-300">{f.active_client_connections} clients</span> },
    {
      key: 'auth_type',
      header: 'Security Clearance',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.auth_type}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Arrow Flight SQL Remote Streaming Server — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Plane className="w-7 h-7 text-cyan-400" />
            Apache Arrow Flight SQL High-Throughput Remote Server
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy binary columnar data streaming over gRPC HTTP/2 bypassing ODBC/JDBC serialization bottlenecks with 4+ GB/s throughput.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Flight SQL Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4.8 GB / sec (Zero-Copy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Columnar Streams</div>
            <div className="text-2xl font-bold text-white mt-1">38 Clients Connected</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Transport Wire Protocol</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">gRPC / Arrow IPC</div>
          </div>
        </div>

        <DataGrid data={mockFlightEndpoints} columns={columns} title="Active Arrow Flight Streaming Endpoints" />
      </div>
    </MainLayout>
  );
}
