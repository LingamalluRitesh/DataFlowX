import React, { useState } from 'react';
import { Play, Download, Copy, Database, Check, Clock, Layers } from 'lucide-react';
import { DataGrid, DataGridColumn } from '../grid/DataGrid';

export function SqlStudioEditor() {
  const [query, setQuery] = useState(
    `SELECT \n  c.customer_id,\n  c.customer_name,\n  COUNT(o.order_id) as total_orders,\n  SUM(o.order_total) as lifetime_revenue,\n  MAX(o.created_at) as last_order_date\nFROM gold.fact_orders o\nJOIN silver.dim_customers c ON o.customer_id = c.customer_id\nWHERE o.order_status = 'DELIVERED'\nGROUP BY c.customer_id, c.customer_name\nHAVING SUM(o.order_total) > 5000\nORDER BY lifetime_revenue DESC\nLIMIT 50;`
  );
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<any[] | null>([
    { customer_id: 'cust_101', customer_name: 'Apex Global Enterprises', total_orders: 142, lifetime_revenue: 125430.50, last_order_date: '2026-08-28 14:22:00' },
    { customer_id: 'cust_102', customer_name: 'Nexus Data Technologies', total_orders: 98, lifetime_revenue: 89340.00, last_order_date: '2026-08-27 18:15:30' },
    { customer_id: 'cust_103', customer_name: 'Quantum Systems Inc', total_orders: 64, lifetime_revenue: 45200.25, last_order_date: '2026-08-28 09:45:12' },
    { customer_id: 'cust_104', customer_name: 'Starlight Retailers Ltd', total_orders: 45, lifetime_revenue: 32100.80, last_order_date: '2026-08-26 21:02:18' },
  ]);
  const [executionStats, setExecutionStats] = useState({ duration_ms: 34.2, rows: 4, bytes: 4096 });
  const [copied, setCopied] = useState(false);

  const handleRun = () => {
    setIsRunning(true);
    setTimeout(() => {
      setIsRunning(false);
      setExecutionStats({ duration_ms: Math.round(Math.random() * 40 + 15), rows: results?.length || 0, bytes: 8192 });
    }, 600);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(query);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const columns: DataGridColumn<any>[] = [
    { key: 'customer_id', header: 'Customer ID' },
    { key: 'customer_name', header: 'Customer Name' },
    { key: 'total_orders', header: 'Total Orders' },
    {
      key: 'lifetime_revenue',
      header: 'Lifetime Revenue ($)',
      render: (r) => `$${Number(r.lifetime_revenue).toLocaleString(undefined, { minimumFractionDigits: 2 })}`,
    },
    { key: 'last_order_date', header: 'Last Order Date' },
  ];

  return (
    <div className="space-y-4">
      {/* Editor Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
        <div className="p-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-cyan-400" />
            <span className="text-sm font-semibold text-white">Interactive SQL Scratchpad</span>
            <span className="text-xs text-slate-500 font-mono">Engine: DuckDB MPP Engine</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied' : 'Copy SQL'}
            </button>
            <button
              onClick={handleRun}
              disabled={isRunning}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold shadow-md shadow-cyan-600/20 transition"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              {isRunning ? 'Executing...' : 'Run Query (F5)'}
            </button>
          </div>
        </div>

        {/* Textarea code editor */}
        <div className="p-4 bg-slate-950/80 font-mono text-sm text-slate-200">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={8}
            className="w-full bg-transparent resize-none focus:outline-none text-emerald-300 selection:bg-cyan-900 font-mono text-xs leading-relaxed"
          />
        </div>

        {/* Execution Metadata Bar */}
        <div className="px-4 py-2 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-cyan-400" /> {executionStats.duration_ms} ms
            </span>
            <span className="flex items-center gap-1">
              <Layers className="w-3.5 h-3.5 text-purple-400" /> {executionStats.rows} rows returned
            </span>
          </div>
          <span className="text-slate-500">Auto-limit: 1,000 rows</span>
        </div>
      </div>

      {/* Query Results DataGrid */}
      {results && <DataGrid data={results} columns={columns} title="Query Results" />}
    </div>
  );
}
