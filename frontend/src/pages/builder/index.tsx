import React, { useState } from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { AdvancedDagEditor } from '@/components/studio/AdvancedDagEditor';
import { GitBranch, Play, Save, CheckCircle, Sparkles, Plus, Code } from 'lucide-react';

export default function PipelineVisualBuilderPage() {
  const [pipelineName, setPipelineName] = useState('enterprise_order_intelligence_dag');

  return (
    <MainLayout>
      <Head>
        <title>Visual DAG Pipeline Builder — DataFlowX</title>
      </Head>

      <div className="space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <GitBranch className="w-7 h-7 text-cyan-400" />
              Visual DAG Pipeline Studio & Workflow Composer
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Drag-and-drop workflow canvas for assembling heterogeneous data ingestion, vectorized transformations, and quality assertions.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <input
              type="text"
              value={pipelineName}
              onChange={(e) => setPipelineName(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
            />
            <button className="flex items-center gap-1 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
              <Play className="w-3.5 h-3.5 fill-white" /> Execute Pipeline
            </button>
          </div>
        </div>

        {/* Visual Canvas Container */}
        <div className="h-[680px] w-full">
          <AdvancedDagEditor />
        </div>
      </div>
    </MainLayout>
  );
}
