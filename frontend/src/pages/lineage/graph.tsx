import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { GitBranch, Layers, Database, ArrowRight, ShieldCheck, Search, Filter } from 'lucide-react';

interface LineageNodeItem {
  id: string;
  name: string;
  type: 'SOURCE' | 'TRANSFORM' | 'MODEL' | 'DASHBOARD';
  columns: string[];
}

const mockNodes: LineageNodeItem[] = [
  { id: 'node_src_pg', name: 'postgres_oltp.orders', type: 'SOURCE', columns: ['order_id', 'cust_id', 'amount', 'created_at'] },
  { id: 'node_bronze', name: 'bronze.raw_orders', type: 'MODEL', columns: ['order_id', 'cust_id', 'amount', 'created_at', '_ingest_time'] },
  { id: 'node_silver', name: 'silver.cleaned_orders', type: 'MODEL', columns: ['order_id', 'customer_id', 'order_total', 'created_at'] },
  { id: 'node_gold', name: 'gold.fact_orders_daily', type: 'MODEL', columns: ['order_id', 'customer_id', 'order_total', 'tax_amount', 'shipping_cost'] },
  { id: 'node_bi_report', name: 'Executive Revenue Dashboard', type: 'DASHBOARD', columns: ['lifetime_revenue', 'arpu', 'monthly_active_users'] },
];

export default function LineageGraphStudioPage() {
  const [selectedColumn, setSelectedColumn] = useState<string>('order_id');

  return (
    <MainLayout>
      <Head>
        <title>Column-Level Lineage Graph — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <GitBranch className="w-7 h-7 text-cyan-400" />
              Column-Level Provenance & Lineage Graph
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Trace upstream origin sources and downstream impact analysis for every column across Bronze, Silver, and Gold datasets.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400 font-mono bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg">
              Tracing Column: <strong className="text-cyan-400">{selectedColumn}</strong>
            </span>
          </div>
        </div>

        {/* Visual Lineage Pipeline Flow */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl overflow-x-auto">
          <div className="flex items-center justify-between min-w-[800px] gap-6">
            {mockNodes.map((node, idx) => (
              <React.Fragment key={node.id}>
                <div className="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-4 shadow-lg min-w-[180px]">
                  <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800">
                      {node.type}
                    </span>
                  </div>
                  <h4 className="font-semibold text-white text-xs mb-3 truncate">{node.name}</h4>

                  <div className="space-y-1 font-mono text-[11px]">
                    {node.columns.map((col) => {
                      const isHighlighted = col.toLowerCase().includes('order') || col.toLowerCase().includes('id');
                      return (
                        <div
                          key={col}
                          onClick={() => setSelectedColumn(col)}
                          className={`px-2 py-1 rounded cursor-pointer transition ${
                            isHighlighted
                              ? 'bg-cyan-950/60 text-cyan-300 border border-cyan-800/80 font-bold'
                              : 'text-slate-400 hover:bg-slate-800'
                          }`}
                        >
                          {col}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {idx < mockNodes.length - 1 && (
                  <div className="flex flex-col items-center justify-center text-slate-600">
                    <ArrowRight className="w-5 h-5 text-cyan-500 animate-pulse" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
