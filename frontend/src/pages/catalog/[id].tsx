import React from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Database, ShieldAlert, ArrowLeft, CheckCircle, Tag, Clock, User, Layers } from 'lucide-react';

interface ColumnDetail {
  name: string;
  type: string;
  nullable: boolean;
  is_pii: boolean;
  pii_category?: string;
  description: string;
}

const mockColumns: ColumnDetail[] = [
  { name: 'customer_id', type: 'VARCHAR(64)', nullable: false, is_pii: false, description: 'Surrogate primary key for customer dimension' },
  { name: 'email', type: 'VARCHAR(255)', nullable: false, is_pii: true, pii_category: 'EMAIL', description: 'Primary contact email address' },
  { name: 'full_name', type: 'VARCHAR(150)', nullable: false, is_pii: true, pii_category: 'PERSON_NAME', description: 'Customer full legal name' },
  { name: 'phone_number', type: 'VARCHAR(32)', nullable: true, is_pii: true, pii_category: 'PHONE_NUMBER', description: 'SMS-enabled mobile phone' },
  { name: 'credit_card_mask', type: 'VARCHAR(20)', nullable: true, is_pii: true, pii_category: 'CREDIT_CARD', description: 'Masked PAN token (first digit + last 4)' },
  { name: 'effective_from', type: 'TIMESTAMP', nullable: false, is_pii: false, description: 'SCD Type 2 record start validity' },
  { name: 'effective_to', type: 'TIMESTAMP', nullable: false, is_pii: false, description: 'SCD Type 2 record expiration timestamp' },
  { name: 'is_current', type: 'BOOLEAN', nullable: false, is_pii: false, description: 'True if active current dimension state' },
];

export default function CatalogDetailPage() {
  const router = useRouter();
  const { id } = router.query;

  const columns: DataGridColumn<ColumnDetail>[] = [
    { key: 'name', header: 'Column Name' },
    {
      key: 'type',
      header: 'Data Type',
      render: (c) => <span className="bg-slate-800 px-2 py-0.5 rounded text-cyan-400 font-mono text-xs">{c.type}</span>,
    },
    {
      key: 'nullable',
      header: 'Nullable',
      render: (c) => (c.nullable ? <span className="text-slate-500">NULL</span> : <span className="text-amber-400 font-semibold">NOT NULL</span>),
    },
    {
      key: 'is_pii',
      header: 'PII Classification',
      render: (c) =>
        c.is_pii ? (
          <span className="px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 text-[10px] font-bold">
            {c.pii_category}
          </span>
        ) : (
          <span className="text-slate-600">—</span>
        ),
    },
    { key: 'description', header: 'Description', sortable: false },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Asset Detail — {id || 'Catalog'} — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        {/* Navigation Breadcrumb */}
        <div>
          <Link href="/catalog" className="text-xs text-slate-400 hover:text-cyan-400 flex items-center gap-1.5 transition">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Data Catalog
          </Link>
        </div>

        {/* Asset Header Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3">
                <Database className="w-8 h-8 text-cyan-400" />
                <h1 className="text-2xl font-bold text-white tracking-tight">dim_customers_scd2</h1>
                <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 text-xs font-bold">
                  SILVER LAYER
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-red-950 text-red-400 border border-red-800 text-xs font-bold flex items-center gap-1">
                  <ShieldAlert className="w-3.5 h-3.5" /> GDPR RESTRICTED
                </span>
              </div>
              <p className="text-slate-400 text-sm mt-2">
                Slowly Changing Dimension Type 2 customer profile table containing cryptographic tokens and contact history.
              </p>
            </div>

            <div className="flex items-center gap-4 border-l border-slate-800 pl-6">
              <div>
                <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Quality Score</div>
                <div className="text-2xl font-extrabold text-emerald-400">98.2%</div>
              </div>
              <div>
                <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Total Columns</div>
                <div className="text-2xl font-extrabold text-cyan-400">{mockColumns.length}</div>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap items-center gap-6 text-xs text-slate-400">
            <span className="flex items-center gap-1.5">
              <User className="w-4 h-4 text-slate-500" /> Owner: <strong className="text-slate-300">crm-team@dataflowx.io</strong>
            </span>
            <span className="flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-slate-500" /> Domain: <strong className="text-slate-300">CRM & Marketing</strong>
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-slate-500" /> Last Profiled: <strong className="text-slate-300">Today at 14:00 UTC</strong>
            </span>
          </div>
        </div>

        {/* Schema Column DataGrid */}
        <DataGrid data={mockColumns} columns={columns} title="Column Schema & Classifications" />
      </div>
    </MainLayout>
  );
}
