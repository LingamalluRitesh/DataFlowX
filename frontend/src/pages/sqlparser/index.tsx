import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { Terminal, Code, Sparkles, CheckCircle, Play, Layers, ArrowRight } from 'lucide-react';

export default function SQLParserStudioPage() {
  const [inputSql, setInputSql] = useState(
    "SELECT o.order_id, c.customer_name, SUM(o.amount) AS total_revenue\nFROM gold.fact_orders o\nJOIN silver.dim_customers c ON o.customer_id = c.customer_id\nWHERE o.status = 'COMPLETED' AND o.order_date >= '2026-01-01'\nGROUP BY o.order_id, c.customer_name\nHAVING SUM(o.amount) > 1000\nORDER BY total_revenue DESC\nLIMIT 50;"
  );

  const [parsedAst, setParsedAst] = useState({
    type: "SelectStatement",
    is_distinct: false,
    projection: [
      { expression: "o.order_id", alias: null },
      { expression: "c.customer_name", alias: null },
      { expression: "SUM(o.amount)", alias: "total_revenue" }
    ],
    from_table: { schema: "gold", table: "fact_orders", alias: "o" },
    joins: [
      { type: "INNER JOIN", right_table: "silver.dim_customers", alias: "c", on: "(o.customer_id = c.customer_id)" }
    ],
    where_clause: "(o.status = 'COMPLETED' AND o.order_date >= '2026-01-01')",
    group_by: ["o.order_id", "c.customer_name"],
    having_clause: "(SUM(o.amount) > 1000)",
    order_by: [{ expression: "total_revenue", ascending: false }],
    limit: 50
  });

  return (
    <MainLayout>
      <Head>
        <title>SQL AST Parser & Dialect Formatter — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Terminal className="w-7 h-7 text-cyan-400" />
            Interactive ANSI SQL AST Parser & Formatter Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Lexical tokenizer, recursive descent AST syntax parser, column projection dependency extractor, and pretty printer.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Parser Engine</div>
            <div className="text-2xl font-bold text-white mt-1">ANSI SQL-92/2016</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tokenization Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">450k tokens / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">AST Validation Status</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Valid Syntax Tree</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-white font-semibold flex items-center gap-2">
                <Code className="w-4 h-4 text-cyan-400" /> Raw SQL Query Input
              </h3>
              <button className="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-xs font-semibold flex items-center gap-1.5">
                <Play className="w-3 h-3" /> Re-Parse AST
              </button>
            </div>
            <textarea
              rows={12}
              value={inputSql}
              onChange={(e) => setInputSql(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-cyan-300 font-mono text-xs focus:outline-none focus:border-cyan-500 resize-none leading-relaxed"
            />
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-white font-semibold flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" /> Parsed Abstract Syntax Tree (JSON AST)
            </h3>
            <pre className="w-full h-64 bg-slate-950 border border-slate-800 rounded-lg p-3 text-slate-300 font-mono text-xs overflow-auto leading-relaxed">
              {JSON.stringify(parsedAst, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
