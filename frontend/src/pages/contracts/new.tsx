import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { MainLayout } from '@/components/layout/MainLayout';
import { ArrowLeft, Save, Plus, Trash2, ShieldCheck } from 'lucide-react';

interface ColumnSpec {
  name: string;
  data_type: string;
  is_required: boolean;
  is_unique: boolean;
}

export default function NewContractPage() {
  const router = useRouter();
  const [datasetName, setDatasetName] = useState('');
  const [version, setVersion] = useState('v1.0.0');
  const [producer, setProducer] = useState('');
  const [slaFreshnessHours, setSlaFreshnessHours] = useState('24');
  const [minQualityScore, setMinQualityScore] = useState('98');

  const [columns, setColumns] = useState<ColumnSpec[]>([
    { name: 'id', data_type: 'VARCHAR(64)', is_required: true, is_unique: true },
    { name: 'created_at', data_type: 'TIMESTAMP', is_required: true, is_unique: false },
  ]);

  const addColumn = () => {
    setColumns([...columns, { name: '', data_type: 'VARCHAR(255)', is_required: true, is_unique: false }]);
  };

  const removeColumn = (index: number) => {
    setColumns(columns.filter((_, idx) => idx !== index));
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    router.push('/contracts');
  };

  return (
    <MainLayout>
      <Head>
        <title>New Data Contract — DataFlowX</title>
      </Head>

      <div className="space-y-6 max-w-4xl mx-auto">
        <div>
          <Link href="/contracts" className="text-xs text-slate-400 hover:text-cyan-400 flex items-center gap-1.5 transition">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Data Contracts
          </Link>
        </div>

        <form onSubmit={handleSave} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h1 className="text-xl font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
              Define Producer-Consumer Data Contract
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Establish a binding contract between data producers and downstream consumer applications.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-medium">
            <div>
              <label className="text-slate-300 block mb-1">Dataset / Table Name</label>
              <input
                type="text"
                required
                value={datasetName}
                onChange={(e) => setDatasetName(e.target.value)}
                placeholder="e.g. fact_orders"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-slate-300 block mb-1">Contract Version</label>
              <input
                type="text"
                required
                value={version}
                onChange={(e) => setVersion(e.target.value)}
                placeholder="v1.0.0"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-slate-300 block mb-1">Producer Team / Owner</label>
              <input
                type="text"
                required
                value={producer}
                onChange={(e) => setProducer(e.target.value)}
                placeholder="e.g. Checkout Service Team"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-slate-300 block mb-1">Max Freshness SLA (Hours)</label>
                <input
                  type="number"
                  required
                  value={slaFreshnessHours}
                  onChange={(e) => setSlaFreshnessHours(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
              <div>
                <label className="text-slate-300 block mb-1">Min Quality Score (%)</label>
                <input
                  type="number"
                  required
                  value={minQualityScore}
                  onChange={(e) => setMinQualityScore(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
            </div>
          </div>

          {/* Column Schema Specs */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-white">Schema Specification & Constraints</h3>
              <button
                type="button"
                onClick={addColumn}
                className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300"
              >
                <Plus className="w-3.5 h-3.5" /> Add Column
              </button>
            </div>

            <div className="space-y-2">
              {columns.map((col, idx) => (
                <div key={idx} className="flex items-center gap-3 p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <input
                    type="text"
                    required
                    placeholder="Column name"
                    value={col.name}
                    onChange={(e) => {
                      const updated = [...columns];
                      updated[idx].name = e.target.value;
                      setColumns(updated);
                    }}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white"
                  />
                  <input
                    type="text"
                    required
                    placeholder="Data type"
                    value={col.data_type}
                    onChange={(e) => {
                      const updated = [...columns];
                      updated[idx].data_type = e.target.value;
                      setColumns(updated);
                    }}
                    className="w-36 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-cyan-400 font-mono"
                  />
                  <label className="flex items-center gap-1 text-xs text-slate-300">
                    <input
                      type="checkbox"
                      checked={col.is_required}
                      onChange={(e) => {
                        const updated = [...columns];
                        updated[idx].is_required = e.target.checked;
                        setColumns(updated);
                      }}
                      className="rounded bg-slate-900 border-slate-700 text-cyan-500"
                    />
                    Required
                  </label>
                  <label className="flex items-center gap-1 text-xs text-slate-300">
                    <input
                      type="checkbox"
                      checked={col.is_unique}
                      onChange={(e) => {
                        const updated = [...columns];
                        updated[idx].is_unique = e.target.checked;
                        setColumns(updated);
                      }}
                      className="rounded bg-slate-900 border-slate-700 text-cyan-500"
                    />
                    Unique
                  </label>
                  <button
                    type="button"
                    onClick={() => removeColumn(idx)}
                    className="text-slate-500 hover:text-red-400 p-1"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
            <Link
              href="/contracts"
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
            >
              Cancel
            </Link>
            <button
              type="submit"
              className="flex items-center gap-1.5 px-5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20"
            >
              <Save className="w-4 h-4" /> Publish Data Contract
            </button>
          </div>
        </form>
      </div>
    </MainLayout>
  );
}
