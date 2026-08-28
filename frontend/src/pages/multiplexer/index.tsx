import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Share2, Route, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface CDCRouteItem {
  route_id: string;
  source_stream: string;
  sink_type: 'ICEBERG_BRONZE' | 'ELASTICSEARCH_SEARCH' | 'KAFKA_TOPIC' | 'WEBHOOK_TARGET';
  destination_endpoint: string;
  fanout_multiplier: number;
  delivery_latency_ms: number;
  status: 'ROUTING' | 'PAUSED';
}

const mockRoutes: CDCRouteItem[] = [
  { route_id: 'route_cdc_01', source_stream: 'postgres.public.orders', sink_type: 'ICEBERG_BRONZE', destination_endpoint: 's3://lakehouse/bronze/orders_cdc/', fanout_multiplier: 3, delivery_latency_ms: 14.5, status: 'ROUTING' },
  { route_id: 'route_cdc_02', source_stream: 'postgres.public.orders', sink_type: 'ELASTICSEARCH_SEARCH', destination_endpoint: 'https://es-cluster:9200/orders_search', fanout_multiplier: 3, delivery_latency_ms: 8.2, status: 'ROUTING' },
  { route_id: 'route_cdc_03', source_stream: 'postgres.public.orders', sink_type: 'KAFKA_TOPIC', destination_endpoint: 'kafka://broker:9092/events.orders.fanout', fanout_multiplier: 3, delivery_latency_ms: 4.0, status: 'ROUTING' },
];

export default function CDCMultiplexerPage() {
  const columns: DataGridColumn<CDCRouteItem>[] = [
    {
      key: 'route_id',
      header: 'Fan-Out Route ID',
      render: (r) => (
        <div className="flex items-center gap-2">
          <Route className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{r.route_id}</strong>
        </div>
      ),
    },
    { key: 'source_stream', header: 'Source CDC Stream', render: (r) => <span className="font-mono text-slate-300 text-xs">{r.source_stream}</span> },
    {
      key: 'sink_type',
      header: 'Target Sink Destination',
      render: (r) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{r.sink_type}</span>,
    },
    { key: 'destination_endpoint', header: 'Sink URI', render: (r) => <span className="font-mono text-cyan-300 text-xs truncate max-w-xs">{r.destination_endpoint}</span> },
    {
      key: 'delivery_latency_ms',
      header: 'Fan-Out Latency',
      render: (r) => <span className="font-mono text-emerald-400 font-bold">{r.delivery_latency_ms} ms</span>,
    },
    {
      key: 'status',
      header: 'Route State',
      render: (r) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {r.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>CDC Sink Multiplexer & Fan-Out — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Share2 className="w-7 h-7 text-cyan-400" />
            CDC Change Event Sink Multiplexer & Fan-Out Route Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Simultaneous multi-destination CDC stream broadcasting to Lakehouse bronze tables, search indexes, and event broker topics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Fan-Out Routes</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Routes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Fan-Out Delivery Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Guaranteed Delivery</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average End-to-End Lag</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">8.9 ms (Sub-Second)</div>
          </div>
        </div>

        <DataGrid data={mockRoutes} columns={columns} title="Managed CDC Multiplexer Routes" />
      </div>
    </MainLayout>
  );
}
