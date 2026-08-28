import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Minimize2, FileCode, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface FlattenerItem {
  table_name: string;
  struct_column: string;
  expanded_columns_count: number;
  sample_flattened_schema: string;
  throughput_rows_per_sec: string;
  status: 'OPTIMIZED' | 'ACTIVE';
}

const mockFlattener: FlattenerItem[] = [
  { table_name: 'events.web_sessions', struct_column: 'geo_metadata', expanded_columns_count: 8, sample_flattened_schema: 'geo_metadata.country, geo_metadata.city, geo_metadata.lat, geo_metadata.lng', throughput_rows_per_sec: '4.8M rows/s', status: 'OPTIMIZED' },
  { table_name: 'events.ecom_orders', struct_column: 'billing_address', expanded_columns_count: 6, sample_flattened_schema: 'billing_address.street, billing_address.zip, billing_address.state', throughput_rows_per_sec: '5.2M rows/s', status: 'OPTIMIZED' },
  { table_name: 'iot.telemetry_stream', struct_column: 'sensor_readings', expanded_columns_count: 14, sample_flattened_schema: 'sensor_readings.temperature, sensor_readings.vibration_x, sensor_readings.psi', throughput_rows_per_sec: '6.1M rows/s', status: 'OPTIMIZED' },
];

export default function NestedFlattenerPage() {
  const columns: DataGridColumn<FlattenerItem>[] = [
    { key: 'table_name', header: 'Target Lakehouse Table', render: (f) => <strong className="text-white font-mono text-xs">{f.table_name}</strong> },
    {
      key: 'struct_column',
      header: 'Nested Struct / JSON Column',
      render: (f) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{f.struct_column}</span>,
    },
    {
      key: 'expanded_columns_count',
      header: 'Flattened Columns',
      render: (f) => <span className="font-mono text-cyan-300 font-bold">+{f.expanded_columns_count} columns</span>,
    },
    { key: 'sample_flattened_schema', header: 'Dot-Notated Column Paths', render: (f) => <span className="font-mono text-slate-300 text-xs truncate max-w-sm">{f.sample_flattened_schema}</span> },
    {
      key: 'throughput_rows_per_sec',
      header: 'Flattening Throughput',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.throughput_rows_per_sec}</span>,
    },
    {
      key: 'status',
      header: 'State',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Nested Struct & JSON Flattener — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Minimize2 className="w-7 h-7 text-cyan-400" />
            Vectorized Nested Struct & JSON Record Flattener Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy recursive unnesting of deeply nested JSON documents, maps, and structs into flat columnar dot-notated Lakehouse schemas.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Flattened Schema Paths</div>
            <div className="text-2xl font-bold text-white mt-1">28 Columns</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average SIMD Unnest Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">5.4M rows / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">JSON Schema Discovery</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Dynamic Infer Active</div>
          </div>
        </div>

        <DataGrid data={mockFlattener} columns={columns} title="Managed Struct Flattener Operations" />
      </div>
    </MainLayout>
  );
}
