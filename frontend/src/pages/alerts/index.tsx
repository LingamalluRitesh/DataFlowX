import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { AlertConfigModal } from '@/components/modals/AlertConfigModal';
import { Bell, Plus, ShieldAlert, CheckCircle, Slack, Mail, Zap } from 'lucide-react';

interface AlertChannelItem {
  id: string;
  name: string;
  type: 'SLACK' | 'PAGERDUTY' | 'EMAIL' | 'WEBHOOK';
  target: string;
  min_severity: 'CRITICAL' | 'HIGH' | 'WARNING';
  active_rules_count: number;
  status: 'ACTIVE' | 'PAUSED';
}

const mockAlertChannels: AlertChannelItem[] = [
  { id: 'chan_01', name: 'DataOps Slack #alerts-dataflowx', type: 'SLACK', target: 'https://hooks.slack.com/services/...', min_severity: 'WARNING', active_rules_count: 8, status: 'ACTIVE' },
  { id: 'chan_02', name: 'PagerDuty Production On-Call', type: 'PAGERDUTY', target: 'pd-service-key-90a1b2...', min_severity: 'CRITICAL', active_rules_count: 4, status: 'ACTIVE' },
  { id: 'chan_03', name: 'Security DPO Incident Email', type: 'EMAIL', target: 'dpo-team@company.io', min_severity: 'HIGH', active_rules_count: 2, status: 'ACTIVE' },
];

export default function AlertsIndexPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const columns: DataGridColumn<AlertChannelItem>[] = [
    {
      key: 'name',
      header: 'Alert Channel Name',
      render: (c) => (
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-amber-400" />
          <strong className="text-white">{c.name}</strong>
        </div>
      ),
    },
    {
      key: 'type',
      header: 'Channel Type',
      render: (c) => (
        <span className="bg-slate-800 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded">
          {c.type}
        </span>
      ),
    },
    { key: 'target', header: 'Destination Endpoint', render: (c) => <span className="font-mono text-xs text-slate-400 truncate max-w-[200px] block">{c.target}</span> },
    {
      key: 'min_severity',
      header: 'Min Trigger Severity',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.min_severity === 'CRITICAL'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {c.min_severity}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Alerts & Incident Escalation — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Bell className="w-7 h-7 text-amber-400" />
              Alert Channels & Escalation Policies
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Configure multi-channel notifications across Slack, PagerDuty, Webhooks, and Email with deduplication and storm prevention.
            </p>
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto"
          >
            <Plus className="w-4 h-4" /> Add Alert Channel
          </button>
        </div>

        <DataGrid data={mockAlertChannels} columns={columns} title="Configured Alert Channels" />

        <AlertConfigModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      </div>
    </MainLayout>
  );
}
