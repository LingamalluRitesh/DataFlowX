import React from 'react';
import { Layers, Database, ArrowRight, ShieldCheck, Share2, Server } from 'lucide-react';

interface DomainProductNode {
  domain: string;
  products: { name: string; type: string; quality_score: number }[];
}

const mockDomains: DomainProductNode[] = [
  {
    domain: 'Core Banking & Payments',
    products: [
      { name: 'fact_financial_transactions', type: 'GOLD DELTA', quality_score: 100.0 },
      { name: 'dim_merchant_accounts', type: 'SILVER ICEBERG', quality_score: 99.4 },
    ],
  },
  {
    domain: 'Customer 360 & Marketing',
    products: [
      { name: 'dim_customers_scd2', type: 'SILVER DELTA', quality_score: 98.2 },
      { name: 'clickstream_attribution_agg', type: 'GOLD SNOWFLAKE', quality_score: 96.5 },
    ],
  },
  {
    domain: 'Logistics & Supply Chain',
    products: [
      { name: 'fact_order_fulfillments', type: 'GOLD BIGQUERY', quality_score: 99.1 },
      { name: 'iot_warehouse_telemetry', type: 'BRONZE S3', quality_score: 94.8 },
    ],
  },
];

export function DataMeshTopology() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Share2 className="w-4 h-4 text-cyan-400" />
            Data Mesh Federated Domain Topology
          </h3>
          <p className="text-xs text-slate-400">Decentralized domain ownership with standardized governance ports</p>
        </div>
        <span className="text-xs font-mono bg-cyan-950 text-cyan-400 border border-cyan-800 px-2.5 py-0.5 rounded-full">
          3 Active Domains
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {mockDomains.map((dom) => (
          <div key={dom.domain} className="bg-slate-950 border border-slate-800 rounded-xl p-4 shadow-lg flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] uppercase font-bold text-slate-500">Domain</span>
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <h4 className="font-bold text-white text-xs mb-3">{dom.domain}</h4>

              <div className="space-y-2">
                {dom.products.map((p) => (
                  <div key={p.name} className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs text-cyan-300 font-semibold truncate max-w-[150px]">{p.name}</span>
                      <span className="text-[9px] font-bold bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">{p.type}</span>
                    </div>
                    <div className="flex items-center justify-between mt-1 text-[10px] text-slate-500">
                      <span>Quality SLA</span>
                      <strong className="text-emerald-400 font-mono">{p.quality_score}%</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
              <span>Federated Ports: <strong>4</strong></span>
              <span className="text-cyan-400 font-semibold cursor-pointer hover:underline">Inspect Contracts &rarr;</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
