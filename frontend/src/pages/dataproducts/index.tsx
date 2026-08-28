import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Box, Layers, ShieldCheck, Share2, Award, ArrowRight, ExternalLink } from 'lucide-react';

interface DataProductItem {
  product_id: string;
  name: string;
  domain: string;
  owner_team: string;
  output_protocol: 'DELTA_SHARING' | 'ARROW_FLIGHT_SQL' | 'ICEBERG_CATALOG' | 'REST_API';
  sla_freshness_minutes: number;
  quality_grade: 'AAA' | 'AA' | 'A';
  status: 'PUBLISHED' | 'STAGING';
}

const mockDataProducts: DataProductItem[] = [
  { product_id: 'dp_fin_01', name: 'Global Revenue & Ledger Mesh', domain: 'Finance', owner_team: 'Financial Engineering', output_protocol: 'DELTA_SHARING', sla_freshness_minutes: 15, quality_grade: 'AAA', status: 'PUBLISHED' },
  { product_id: 'dp_mkt_02', name: 'Omnichannel Customer 360', domain: 'Marketing', owner_team: 'Growth Analytics', output_protocol: 'ARROW_FLIGHT_SQL', sla_freshness_minutes: 60, quality_grade: 'AAA', status: 'PUBLISHED' },
  { product_id: 'dp_scm_03', name: 'Real-time Supply Chain Fleet', domain: 'Logistics', owner_team: 'Operations Intelligence', output_protocol: 'ICEBERG_CATALOG', sla_freshness_minutes: 5, quality_grade: 'AA', status: 'PUBLISHED' },
];

export default function DataProductsMeshPage() {
  const columns: DataGridColumn<DataProductItem>[] = [
    {
      key: 'name',
      header: 'Data Product Name',
      render: (p) => (
        <div className="flex items-center gap-2.5">
          <Box className="w-4 h-4 text-cyan-400" />
          <div>
            <strong className="text-white text-xs">{p.name}</strong>
            <div className="text-[10px] text-slate-500 font-mono">{p.product_id}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'domain',
      header: 'Mesh Domain',
      render: (p) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{p.domain}</span>,
    },
    { key: 'owner_team', header: 'Domain Owner', render: (p) => <span className="text-slate-300 text-xs">{p.owner_team}</span> },
    {
      key: 'output_protocol',
      header: 'Output Port Protocol',
      render: (p) => (
        <span className="font-mono text-cyan-300 text-xs flex items-center gap-1">
          <Share2 className="w-3 h-3" /> {p.output_protocol}
        </span>
      ),
    },
    {
      key: 'sla_freshness_minutes',
      header: 'Freshness SLA',
      render: (p) => <span className="font-mono text-emerald-400 font-bold">&lt; {p.sla_freshness_minutes} mins</span>,
    },
    {
      key: 'quality_grade',
      header: 'Quality Badge',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          GRADE {p.quality_grade}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Data Mesh & Data Products — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Box className="w-7 h-7 text-cyan-400" />
            Data Mesh Data Products & Domain Ports Console
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Decentralized domain ownership, discoverable output ports, and automated SLA data contracts for enterprise mesh architectures.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Published Data Products</div>
            <div className="text-2xl font-bold text-white mt-1">3 Products</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Autonomous Domains</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">3 Domains</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">SLA Compliance Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% On-Track</div>
          </div>
        </div>

        <DataGrid data={mockDataProducts} columns={columns} title="Enterprise Data Product Catalog" />
      </div>
    </MainLayout>
  );
}
