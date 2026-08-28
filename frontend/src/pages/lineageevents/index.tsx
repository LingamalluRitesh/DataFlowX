import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Share2, Activity, CheckCircle, Database, Layers, ArrowRight, ShieldCheck } from 'lucide-react';

interface OpenLineageEventItem {
  event_id: string;
  job_name: string;
  event_type: 'START' | 'RUNNING' | 'COMPLETE' | 'FAIL';
  input_dataset: string;
  output_dataset: string;
  event_time: string;
  facets_included: string[];
}

const mockLineageEvents: OpenLineageEventItem[] = [
  { event_id: 'evt_ol_901', job_name: 'etl_daily_gold_aggregator', event_type: 'COMPLETE', input_dataset: 'silver.raw_orders', output_dataset: 'gold.fact_orders', event_time: '2 mins ago', facets_included: ['schema', 'datasource', 'outputStatistics'] },
  { event_id: 'evt_ol_902', job_name: 'stream_clickstream_events', event_type: 'RUNNING', input_dataset: 'kafka://cluster/clickstream', output_dataset: 'bronze.raw_clickstream', event_time: '5 mins ago', facets_included: ['schema', 'datasource'] },
  { event_id: 'evt_ol_903', job_name: 'cdc_wal_bronze_stream', event_type: 'START', input_dataset: 'postgres://db/customers', output_dataset: 'silver.dim_customers', event_time: '10 mins ago', facets_included: ['schema', 'columnLineage'] },
];

export default function OpenLineageEventsPage() {
  const columns: DataGridColumn<OpenLineageEventItem>[] = [
    { key: 'event_id', header: 'Event ID', render: (e) => <strong className="text-cyan-400 font-mono text-xs">{e.event_id}</strong> },
    { key: 'job_name', header: 'OpenLineage Job', render: (e) => <span className="font-mono text-white text-xs">{e.job_name}</span> },
    {
      key: 'event_type',
      header: 'Event Type',
      render: (e) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            e.event_type === 'COMPLETE'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : e.event_type === 'RUNNING'
              ? 'bg-cyan-950 text-cyan-400 border border-cyan-800'
              : 'bg-purple-950 text-purple-400 border border-purple-800'
          }`}
        >
          {e.event_type}
        </span>
      ),
    },
    {
      key: 'input_dataset',
      header: 'Lineage Graph (Input → Output)',
      render: (e) => (
        <span className="font-mono text-xs">
          <span className="text-slate-300">{e.input_dataset}</span> → <span className="text-emerald-400 font-bold">{e.output_dataset}</span>
        </span>
      ),
    },
    {
      key: 'facets_included',
      header: 'Standard JSON Facets',
      render: (e) => (
        <div className="flex flex-wrap gap-1">
          {e.facets_included.map((f) => (
            <span key={f} className="bg-slate-800 text-cyan-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {f}
            </span>
          ))}
        </div>
      ),
    },
    { key: 'event_time', header: 'Event Timestamp' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>OpenLineage Event Stream & Facets — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Share2 className="w-7 h-7 text-cyan-400" />
            OpenLineage Standard Event Stream & Facets
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time OpenLineage 1.0 JSON event emitter streaming dataset facets to Marquez, OpenMetadata, and Collibra.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">OpenLineage Events Emitted (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">1,240 Events</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">OpenMetadata Sync Health</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Stream Delivery</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Standard Version</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">OpenLineage v1.0.5</div>
          </div>
        </div>

        <DataGrid data={mockLineageEvents} columns={columns} title="OpenLineage RunEvent Telemetry Feed" />
      </div>
    </MainLayout>
  );
}
