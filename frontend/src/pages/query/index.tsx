import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { SqlStudioEditor } from '@/components/sql/SqlStudioEditor';
import { Database, Terminal, Sparkles } from 'lucide-react';

export default function QueryStudioPage() {
  return (
    <MainLayout>
      <Head>
        <title>SQL Analytics Studio — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Terminal className="w-7 h-7 text-cyan-400" />
            Interactive SQL Analytics Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Execute high-performance ad-hoc SQL queries against Bronze, Silver, and Gold Parquet/Delta tables powered by vectorized MPP engines.
          </p>
        </div>

        <SqlStudioEditor />
      </div>
    </MainLayout>
  );
}
