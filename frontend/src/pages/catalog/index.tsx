import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { BookOpen, Tag, Shield, Search, Database, Layers, CheckCircle } from 'lucide-react';

interface CatalogAssetItem {
  id: string;
  name: string;
  layer: 'BRONZE' | 'SILVER' | 'GOLD';
  domain: string;
  owner: string;
  quality_score: number;
  columns_count: number;
  pii_detected: boolean;
  tags: string[];
}

const mockAssets: CatalogAssetItem[] = [
  { id: 'asset_01', name: 'fact_orders_daily', layer: 'GOLD', domain: 'E-Commerce', owner: 'analytics@dataflowx.io', quality_score: 99.4, columns_count: 24, pii_detected: false, tags: ['core', 'revenue', 'gold'] },
  { id: 'asset_02', name: 'dim_customers_scd2', layer: 'SILVER', domain: 'CRM', owner: 'crm-team@dataflowx.io', quality_score: 98.2, columns_count: 18, pii_detected: true, tags: ['pii', 'gdpr', 'scd2'] },
  { id: 'asset_03', name: 'raw_kafka_telemetry', layer: 'BRONZE', domain: 'IoT Devices', owner: 'infra@dataflowx.io', quality_score: 94.8, columns_count: 12, pii_detected: false, tags: ['streaming', 'bronze'] },
  { id: 'asset_04', name: 'financial_ledger_gl', layer: 'GOLD', domain: 'Finance', owner: 'accounting@dataflowx.io', quality_score: 100.0, columns_count: 32, pii_detected: false, tags: ['audit', 'sox', 'finance'] },
  { id: 'asset_05', name: 'marketing_attribution_events', layer: 'SILVER', domain: 'Marketing', owner: 'growth@dataflowx.io', quality_score: 96.5, columns_count: 15, pii_detected: true, tags: ['utm', 'campaigns'] },
];

export default function CatalogIndexPage() {
  const [domainFilter, setDomainFilter] = useState<string>('ALL');

  const filtered = domainFilter === 'ALL' ? mockAssets : mockAssets.filter((a) => a.domain === domainFilter);

  const columns: DataGridColumn<CatalogAssetItem>[] = [
    {
      key: 'name',
      header: 'Asset Name',
      render: (a) => (
        <Link href={`/catalog/${a.id}`} className="font-semibold text-cyan-400 hover:underline flex items-center gap-2">
          <Database className="w-4 h-4 text-slate-400" />
          {a.name}
        </Link>
      ),
    },
    {
      key: 'layer',
      header: 'Medallion Layer',
      render: (a) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            a.layer === 'GOLD'
              ? 'bg-amber-950 text-amber-400 border border-amber-800'
              : a.layer === 'SILVER'
              ? 'bg-slate-800 text-slate-300 border border-slate-700'
              : 'bg-orange-950 text-orange-400 border border-orange-800'
          }`}
        >
          {a.layer}
        </span>
      ),
    },
    { key: 'domain', header: 'Business Domain' },
    { key: 'owner', header: 'Owner' },
    {
      key: 'quality_score',
      header: 'Quality Score',
      render: (a) => (
        <div className="flex items-center gap-2">
          <div className="w-16 bg-slate-800 h-2 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${a.quality_score}%` }} />
          </div>
          <span className="font-bold text-emerald-400">{a.quality_score}%</span>
        </div>
      ),
    },
    {
      key: 'pii_detected',
      header: 'PII Status',
      render: (a) =>
        a.pii_detected ? (
          <span className="px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 text-[10px] font-bold">
            PII DETECTED
          </span>
        ) : (
          <span className="text-slate-500 text-xs">Clean</span>
        ),
    },
    {
      key: 'tags',
      header: 'Tags',
      render: (a) => (
        <div className="flex flex-wrap gap-1">
          {a.tags.map((t) => (
            <span key={t} className="bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded text-[10px]">
              #{t}
            </span>
          ))}
        </div>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Enterprise Data Catalog — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <BookOpen className="w-7 h-7 text-cyan-400" />
              Enterprise Data Catalog
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Search, explore, and govern bronze, silver, and gold datasets across your organization.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/governance"
              className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
            >
              Business Glossary
            </Link>
            <Link
              href="/contracts"
              className="px-3.5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition"
            >
              Data Contracts
            </Link>
          </div>
        </div>

        {/* Domain Filter Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {['ALL', 'E-Commerce', 'CRM', 'Finance', 'IoT Devices', 'Marketing'].map((d) => (
            <button
              key={d}
              onClick={() => setDomainFilter(d)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                domainFilter === d
                  ? 'bg-cyan-500 text-slate-950 font-semibold'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {d}
            </button>
          ))}
        </div>

        {/* Catalog Table */}
        <DataGrid data={filtered} columns={columns} title="Indexed Catalog Assets" />
      </div>
    </MainLayout>
  );
}
