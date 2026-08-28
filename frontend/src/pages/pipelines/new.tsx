import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { ArrowLeft, CheckCircle2, Play, Save, Workflow } from 'lucide-react';
import { apiClient } from '@/services/api';
import { PipelineCanvas } from '@/components/canvas/PipelineCanvas';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { DAGEdgeData, DAGNodeData } from '@/types';

export default function NewPipelineBuilderPage() {
  const router = useRouter();
  const [name, setName] = useState('New Enterprise Data Pipeline');
  const [description, setDescription] = useState('Automated ingestion and transformation pipeline');
  const [pipelineType, setPipelineType] = useState('batch');
  const [environment, setEnvironment] = useState('production');
  const [isSaving, setIsSaving] = useState(false);

  const initialNodes: DAGNodeData[] = [
    {
      id: 'node_extract',
      type: 'extract',
      name: 'Extract CRM Data',
      config: { connector_type: 'csv', file_path: './storage/temp/raw_customers_demo.csv' },
      position: { x: 50, y: 150 },
    },
    {
      id: 'node_quality',
      type: 'quality',
      name: 'Validate & Quarantine',
      config: { failure_action: 'QUARANTINE_RECORDS', rules: [{ rule_type: 'NOT_NULL', target_column: 'customer_id' }] },
      position: { x: 320, y: 150 },
    },
    {
      id: 'node_silver',
      type: 'transform',
      name: 'Silver Normalization',
      config: { steps: [{ type: 'deduplicate', config: { subset: ['customer_id'] } }] },
      position: { x: 600, y: 150 },
    },
    {
      id: 'node_warehouse',
      type: 'warehouse_load',
      name: 'Load Gold Warehouse',
      config: { table_name: 'mart_customer_analytics', mode: 'overwrite' },
      position: { x: 880, y: 150 },
    },
  ];

  const initialEdges: DAGEdgeData[] = [
    { source: 'node_extract', target: 'node_quality' },
    { source: 'node_quality', target: 'node_silver' },
    { source: 'node_silver', target: 'node_warehouse' },
  ];

  const handleSavePipeline = async (nodes: DAGNodeData[], edges: DAGEdgeData[]) => {
    setIsSaving(true);
    try {
      // Validate DAG first
      const valRes = await apiClient.post('/pipelines/validate-dag', {
        nodes,
        edges,
        globals: {},
      });

      if (!valRes.data.is_valid) {
        alert(`DAG Validation Error:\n${valRes.data.errors.join('\n')}`);
        setIsSaving(false);
        return;
      }

      const res = await apiClient.post('/pipelines', {
        name,
        description,
        pipeline_type: pipelineType,
        environment,
        concurrency_limit: 4,
        timeout_seconds: 3600,
        retry_count: 3,
        retry_delay_seconds: 5,
        dag: {
          nodes,
          edges,
          globals: {},
        },
      });

      alert(`Pipeline '${res.data.name}' created successfully!`);
      router.push(`/pipelines/${res.data.id}`);
    } catch (err: any) {
      alert(`Save failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link href="/pipelines">
            <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
              <ArrowLeft className="w-4 h-4" />
            </button>
          </Link>
          <div>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="text-xl font-bold text-slate-100 bg-transparent border-b border-dashed border-slate-700 focus:outline-none focus:border-blue-500"
            />
            <p className="text-xs text-slate-400 mt-1">Visual DAG Pipeline Editor • Kahn's Cycle Detection Enabled</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={environment}
            onChange={(e) => setEnvironment(e.target.value)}
            className="px-3 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-slate-200"
          >
            <option value="production">Production</option>
            <option value="staging">Staging</option>
            <option value="development">Development</option>
          </select>
        </div>
      </div>

      {/* Visual Canvas */}
      <PipelineCanvas
        initialNodes={initialNodes}
        initialEdges={initialEdges}
        onSave={handleSavePipeline}
        isSaving={isSaving}
      />
    </div>
  );
}
