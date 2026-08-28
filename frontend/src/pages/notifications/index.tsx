import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Bell, ShieldAlert, CheckCircle, Mail, MessageSquare, PhoneCall, AlertTriangle } from 'lucide-react';

interface NotificationChannelItem {
  channel_name: string;
  channel_type: 'PAGERDUTY' | 'SLACK' | 'EMAIL_SMTP' | 'WEBHOOK';
  target_endpoint: string;
  severity_filter: 'CRITICAL_ONLY' | 'ALL_SEVERITIES' | 'WARNING_AND_ABOVE';
  dispatched_alerts_30d: number;
  status: 'ACTIVE' | 'PAUSED';
}

const mockChannels: NotificationChannelItem[] = [
  { channel_name: 'On-Call SRE Escalation', channel_type: 'PAGERDUTY', target_endpoint: 'pd:service:P9A8B7C', severity_filter: 'CRITICAL_ONLY', dispatched_alerts_30d: 4, status: 'ACTIVE' },
  { channel_name: '#data-pipeline-alerts', channel_type: 'SLACK', target_endpoint: 'https://hooks.slack.com/services/...', severity_filter: 'WARNING_AND_ABOVE', dispatched_alerts_30d: 48, status: 'ACTIVE' },
  { channel_name: 'Data Engineering Team Digest', channel_type: 'EMAIL_SMTP', target_endpoint: 'data-team@company.com', severity_filter: 'ALL_SEVERITIES', dispatched_alerts_30d: 120, status: 'ACTIVE' },
];

export default function NotificationsHubPage() {
  const columns: DataGridColumn<NotificationChannelItem>[] = [
    {
      key: 'channel_name',
      header: 'Notification Channel',
      render: (c) => (
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-cyan-400" />
          <strong className="text-white">{c.channel_name}</strong>
        </div>
      ),
    },
    {
      key: 'channel_type',
      header: 'Protocol / Provider',
      render: (c) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{c.channel_type}</span>,
    },
    { key: 'target_endpoint', header: 'Target Destination', render: (c) => <span className="font-mono text-slate-400 text-xs">{c.target_endpoint}</span> },
    {
      key: 'severity_filter',
      header: 'Severity Routing Rule',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.severity_filter === 'CRITICAL_ONLY'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : c.severity_filter === 'WARNING_AND_ABOVE'
              ? 'bg-amber-950 text-amber-400 border border-amber-800'
              : 'bg-slate-800 text-slate-300'
          }`}
        >
          {c.severity_filter}
        </span>
      ),
    },
    { key: 'dispatched_alerts_30d', header: 'Dispatched (30d)', render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.dispatched_alerts_30d} alerts</span> },
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
        <title>Alert Routing & Incident Hub — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Bell className="w-7 h-7 text-cyan-400" />
            Alert Routing & Incident Management Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Intelligent multi-channel routing: PagerDuty on-call escalation, Slack rich Block Kit notifications, and SMTP digests.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Notification Channels</div>
            <div className="text-2xl font-bold text-white mt-1">3 Channels</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Dispatched Alerts (30d)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">172 Alerts</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Avg PagerDuty MTTA</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">2.4 Minutes</div>
          </div>
        </div>

        <DataGrid data={mockChannels} columns={columns} title="Configured Alert Notification Channels" />
      </div>
    </MainLayout>
  );
}
