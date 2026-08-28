import React, { useEffect, useState } from 'react';
import { ArrowRight, Database, GitFork, Layers, RefreshCw, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { LineageGraph } from '@/types';

export default function LineagePage() {
  const [lineage, setLineage] = useState<LineageGraph>({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(true);

  const fetchLineage = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/lineage/graph');
      setLineage(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLineage();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">End-to-End Data Lineage</h1>
          <p className="text-sm text-slate-400 mt-1">
            Visual data provenance tracking from Ingestion Sources → Bronze Lake → Silver Lake → Gold Marts → Warehouses
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchLineage}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh Graph
        </Button>
      </div>

      {/* Visual Provenance Flow Diagram */}
      <Card className="p-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 py-6 overflow-x-auto">
          {/* Source Node */}
          <div className="flex flex-col items-center text-center p-6 bg-slate-900 border-2 border-blue-500 rounded-2xl w-60 shadow-lg shadow-blue-500/10">
            <div className="p-3 bg-blue-500/20 text-blue-400 rounded-xl mb-3">
              <Database className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-bold text-slate-100">Customer CRM Source</h4>
            <span className="text-[10px] uppercase font-mono text-blue-400 mt-1">External Ingestion</span>
          </div>

          <ArrowRight className="w-8 h-8 text-slate-600 hidden md:block" />

          {/* Bronze Lake */}
          <div className="flex flex-col items-center text-center p-6 bg-slate-900 border-2 border-amber-500 rounded-2xl w-60 shadow-lg shadow-amber-500/10">
            <div className="p-3 bg-amber-500/20 text-amber-400 rounded-xl mb-3">
              <Database className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-bold text-slate-100">Bronze Raw Lake</h4>
            <span className="text-[10px] uppercase font-mono text-amber-400 mt-1">Immutable Parquet</span>
          </div>

          <ArrowRight className="w-8 h-8 text-slate-600 hidden md:block" />

          {/* Silver Lake */}
          <div className="flex flex-col items-center text-center p-6 bg-slate-900 border-2 border-slate-400 rounded-2xl w-60 shadow-lg shadow-slate-400/10">
            <div className="p-3 bg-slate-700 text-slate-200 rounded-xl mb-3">
              <Layers className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-bold text-slate-100">Silver Curated Lake</h4>
            <span className="text-[10px] uppercase font-mono text-slate-400 mt-1">Deduplicated & Cleaned</span>
          </div>

          <ArrowRight className="w-8 h-8 text-slate-600 hidden md:block" />

          {/* Gold Mart & Warehouse */}
          <div className="flex flex-col items-center text-center p-6 bg-slate-900 border-2 border-yellow-500 rounded-2xl w-60 shadow-lg shadow-yellow-500/10">
            <div className="p-3 bg-yellow-500/20 text-yellow-400 rounded-xl mb-3">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-bold text-slate-100">Gold Customer Mart</h4>
            <span className="text-[10px] uppercase font-mono text-yellow-400 mt-1">Warehouse Analytical Table</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
