import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Code, CheckCircle, Database, Layers, Play, Sparkles } from 'lucide-react';

interface GraphQLTypeDefinitionItem {
  type_name: string;
  underlying_table: string;
  fields_count: number;
  dataloader_enabled: boolean;
  queries_count_24h: number;
}

const mockGraphQLTypes: GraphQLTypeDefinitionItem[] = [
  { type_name: 'FactOrder', underlying_table: 'gold.fact_orders', fields_count: 14, dataloader_enabled: true, queries_count_24h: 12500 },
  { type_name: 'DimCustomer', underlying_table: 'silver.dim_customers', fields_count: 8, dataloader_enabled: true, queries_count_24h: 8900 },
  { type_name: 'IoTTelemetry', underlying_table: 'bronze.iot_telemetry', fields_count: 12, dataloader_enabled: false, queries_count_24h: 4200 },
];

export default function GraphQLGatewayPage() {
  const [sampleQuery, setSampleQuery] = useState(`query GetCustomerOrders {
  dimcustomers(limit: 5) {
    id
    customer_name
    orders {
      order_id
      total_usd
    }
  }
}`);

  const columns: DataGridColumn<GraphQLTypeDefinitionItem>[] = [
    {
      key: 'type_name',
      header: 'GraphQL Type',
      render: (g) => (
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{g.type_name}</strong>
        </div>
      ),
    },
    { key: 'underlying_table', header: 'Mapped Lakehouse Table', render: (g) => <span className="font-mono text-slate-300 text-xs">{g.underlying_table}</span> },
    { key: 'fields_count', header: 'Exposed Fields', render: (g) => <span className="font-mono text-slate-400">{g.fields_count} fields</span> },
    {
      key: 'dataloader_enabled',
      header: 'Batched DataLoader',
      render: (g) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            g.dataloader_enabled
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {g.dataloader_enabled ? 'BATCHED (N+1 SAFE)' : 'DIRECT'}
        </span>
      ),
    },
    { key: 'queries_count_24h', header: 'Query Volume (24h)', render: (g) => <span className="font-mono text-emerald-400 font-bold">{g.queries_count_24h.toLocaleString()} req</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Universal GraphQL Data Gateway — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Code className="w-7 h-7 text-cyan-400" />
            Universal GraphQL Data Gateway & Schema Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Dynamic GraphQL SDL generation from Lakehouse tables with batched DataLoaders preventing N+1 query execution.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs font-semibold text-slate-300 uppercase mb-2">Interactive GraphQL Query Explorer</div>
          <div className="flex gap-4">
            <textarea
              value={sampleQuery}
              onChange={(e) => setSampleQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-cyan-300 font-mono focus:outline-none focus:border-cyan-500 h-36 resize-none"
            />
          </div>
          <div className="flex justify-end mt-2">
            <button className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow">
              <Play className="w-3 h-3 fill-white" /> Execute GraphQL Query
            </button>
          </div>
        </div>

        <DataGrid data={mockGraphQLTypes} columns={columns} title="Exposed Lakehouse GraphQL Entities" />
      </div>
    </MainLayout>
  );
}
