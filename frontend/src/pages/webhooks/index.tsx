import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Webhook, ShieldCheck, Key, CheckCircle, Zap, ArrowRight, Plus } from 'lucide-react';

interface WebhookEndpointItem {
  webhook_id: string;
  target_pipeline_id: string;
  endpoint_path: string;
  auth_mode: 'HMAC_SHA256' | 'BEARER_TOKEN';
  invocations_24h: number;
  status: 'ACTIVE' | 'DISABLED';
}

const mockWebhooks: WebhookEndpointItem[] = [
  { webhook_id: 'wh_shopify_orders', target_pipeline_id: 'pipeline_shopify_ingest', endpoint_path: '/api/v1/webhooks/incoming/wh_shopify_orders', auth_mode: 'HMAC_SHA256', invocations_24h: 1420, status: 'ACTIVE' },
  { webhook_id: 'wh_stripe_charges', target_pipeline_id: 'pipeline_stripe_settlement', endpoint_path: '/api/v1/webhooks/incoming/wh_stripe_charges', auth_mode: 'HMAC_SHA256', invocations_24h: 890, status: 'ACTIVE' },
  { webhook_id: 'wh_github_releases', target_pipeline_id: 'pipeline_contract_sync', endpoint_path: '/api/v1/webhooks/incoming/wh_github_releases', auth_mode: 'HMAC_SHA256', invocations_24h: 12, status: 'ACTIVE' },
];

export default function WebhooksManagementPage() {
  const columns: DataGridColumn<WebhookEndpointItem>[] = [
    {
      key: 'webhook_id',
      header: 'Webhook Trigger ID',
      render: (w) => (
        <div className="flex items-center gap-2">
          <Webhook className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{w.webhook_id}</strong>
        </div>
      ),
    },
    { key: 'target_pipeline_id', header: 'Target Trigger Pipeline', render: (w) => <span className="font-mono text-purple-300 text-xs">{w.target_pipeline_id}</span> },
    { key: 'endpoint_path', header: 'Inbound Webhook URL', render: (w) => <span className="font-mono text-slate-400 text-xs">{w.endpoint_path}</span> },
    {
      key: 'auth_mode',
      header: 'Security Verification',
      render: (w) => <span className="bg-slate-800 text-emerald-400 font-mono text-[10px] px-2 py-0.5 rounded">{w.auth_mode}</span>,
    },
    { key: 'invocations_24h', header: 'Invocations (24h)', render: (w) => <span className="font-mono text-cyan-300 font-bold">{w.invocations_24h.toLocaleString()} calls</span> },
    {
      key: 'status',
      header: 'Status',
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
        <title>Webhook Inbound Triggers & Security — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Webhook className="w-7 h-7 text-cyan-400" />
              Inbound Webhook Triggers & HMAC Security Hub
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Event-driven pipeline triggers with HMAC-SHA256 signature verification and replay-attack protection.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Provision Inbound Webhook
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Webhook Endpoints</div>
            <div className="text-2xl font-bold text-white mt-1">3 Endpoints</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Triggered Runs (24h)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">2,322 Triggered</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Trigger Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.2 ms</div>
          </div>
        </div>

        <DataGrid data={mockWebhooks} columns={columns} title="Registered Webhook Endpoints" />
      </div>
    </MainLayout>
  );
}
