import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Radio, Plus, CheckCircle, Clock, Database, Globe, FileCheck, Layers } from 'lucide-react';

interface SensorItem {
  id: string;
  name: string;
  sensor_type: 'S3_KEY' | 'SQL_QUERY' | 'FILE' | 'WEBHOOK' | 'CROSS_PIPELINE';
  target: string;
  poke_interval_seconds: number;
  timeout_seconds: number;
  last_poke: string;
  state: 'WAITING' | 'SATISFIED' | 'TIMED_OUT';
}

const mockSensors: SensorItem[] = [
  { id: 'sensor_01', name: 's3_orders_landing_sensor', sensor_type: 'S3_KEY', target: 's3://bronze-landing/orders/2026/08/28/*.parquet', poke_interval_seconds: 60, timeout_seconds: 3600, last_poke: '30s ago', state: 'SATISFIED' },
  { id: 'sensor_02', name: 'sql_pos_sync_sensor', sensor_type: 'SQL_QUERY', target: 'SELECT count(*) > 1000 FROM staging_pos_logs', poke_interval_seconds: 120, timeout_seconds: 7200, last_poke: '1m ago', state: 'WAITING' },
  { id: 'sensor_03', name: 'stripe_charge_webhook_sensor', sensor_type: 'WEBHOOK', target: 'https://dataflowx.io/api/v1/webhooks/tokens/wh_sec_89f', poke_interval_seconds: 10, timeout_seconds: 14400, last_poke: '5s ago', state: 'WAITING' },
  { id: 'sensor_04', name: 'cross_pipe_dim_customer_sensor', sensor_type: 'CROSS_PIPELINE', target: 'pipeline: crm_scd2_sync (status=SUCCESS)', poke_interval_seconds: 30, timeout_seconds: 3600, last_poke: '15s ago', state: 'SATISFIED' },
];

export default function SensorsIndexPage() {
  const columns: DataGridColumn<SensorItem>[] = [
    {
      key: 'name',
      header: 'Sensor Name',
      render: (s) => (
        <div>
          <strong className="text-white">{s.name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{s.id}</div>
        </div>
      ),
    },
    {
      key: 'sensor_type',
      header: 'Type',
      render: (s) => (
        <span className="bg-slate-800 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded border border-slate-700">
          {s.sensor_type}
        </span>
      ),
    },
    {
      key: 'target',
      header: 'Target / Condition Spec',
      render: (s) => <span className="font-mono text-xs text-slate-300 truncate max-w-xs block">{s.target}</span>,
    },
    {
      key: 'poke_interval_seconds',
      header: 'Poke Interval',
      render: (s) => <span className="font-mono text-slate-400">{s.poke_interval_seconds}s</span>,
    },
    {
      key: 'state',
      header: 'State',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.state === 'SATISFIED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : s.state === 'WAITING'
              ? 'bg-amber-950 text-amber-400 border border-amber-800 animate-pulse'
              : 'bg-red-950 text-red-400 border border-red-800'
          }`}
        >
          {s.state}
        </span>
      ),
    },
    { key: 'last_poke', header: 'Last Poke' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Workflow Sensors & External State — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Radio className="w-7 h-7 text-cyan-400 animate-pulse" />
              Workflow Sensors & State Monitors
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Event-driven sensors polling S3 object landing, SQL boolean conditions, cross-pipeline dependencies, and webhook callbacks.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Add Sensor
          </button>
        </div>

        <DataGrid data={mockSensors} columns={columns} title="Configured External Sensors" />
      </div>
    </MainLayout>
  );
}
