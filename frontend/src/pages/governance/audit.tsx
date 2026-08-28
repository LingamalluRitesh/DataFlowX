import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileText, ShieldAlert, CheckCircle, User, Clock, Lock, Key } from 'lucide-react';

interface AuditLogEvent {
  id: string;
  actor_email: string;
  action_type: 'SCHEMA_ALTER' | 'PII_ACCESS' | 'CONTRACT_PUBLISH' | 'POLICY_UPDATE' | 'SECRET_ROTATION';
  resource: string;
  ip_address: string;
  timestamp: string;
  result: 'SUCCESS' | 'DENIED';
}

const mockAuditLogs: AuditLogEvent[] = [
  { id: 'aud_9012', actor_email: 'sec-admin@company.io', action_type: 'POLICY_UPDATE', resource: 'policy: rbac_analyst_orders', ip_address: '10.0.4.15', timestamp: '5 mins ago', result: 'SUCCESS' },
  { id: 'aud_9011', actor_email: 'unknown_analyst@company.io', action_type: 'PII_ACCESS', resource: 'column: dim_customers.ssn_hash', ip_address: '192.168.1.55', timestamp: '18 mins ago', result: 'DENIED' },
  { id: 'aud_9010', actor_email: 'lead-engineer@company.io', action_type: 'CONTRACT_PUBLISH', resource: 'contract: fact_orders_v2', ip_address: '10.0.2.88', timestamp: '1 hour ago', result: 'SUCCESS' },
  { id: 'aud_9009', actor_email: 'vault-automation@system.io', action_type: 'SECRET_ROTATION', resource: 'vault: database/snowflake_creds', ip_address: '10.0.1.1', timestamp: '3 hours ago', result: 'SUCCESS' },
];

export default function GovernanceAuditPage() {
  const columns: DataGridColumn<AuditLogEvent>[] = [
    {
      key: 'action_type',
      header: 'Audit Action Type',
      render: (a) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            a.action_type === 'PII_ACCESS'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : a.action_type === 'SECRET_ROTATION'
              ? 'bg-purple-950 text-purple-400 border border-purple-800'
              : 'bg-cyan-950 text-cyan-400 border border-cyan-800'
          }`}
        >
          {a.action_type}
        </span>
      ),
    },
    { key: 'actor_email', header: 'Actor / User Principal' },
    { key: 'resource', header: 'Target Resource', render: (a) => <span className="font-mono text-xs text-slate-300">{a.resource}</span> },
    { key: 'ip_address', header: 'Caller IP', render: (a) => <span className="font-mono text-slate-400">{a.ip_address}</span> },
    {
      key: 'result',
      header: 'Authorization Result',
      render: (a) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            a.result === 'SUCCESS'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-red-950 text-red-400 border border-red-800 animate-pulse'
          }`}
        >
          {a.result}
        </span>
      ),
    },
    { key: 'timestamp', header: 'Event Timestamp' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Compliance Audit Trail — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileText className="w-7 h-7 text-cyan-400" />
            Immutable Compliance & Security Audit Trail
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Tamper-evident access log records for SOX, HIPAA, and GDPR compliance tracking all schema alterations, access attempts, and policy changes.
          </p>
        </div>

        <DataGrid data={mockAuditLogs} columns={columns} title="Audit Event Log Stream" />
      </div>
    </MainLayout>
  );
}
