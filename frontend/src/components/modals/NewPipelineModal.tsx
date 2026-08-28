import React, { useState } from 'react';
import { X, Play, Clock, Sparkles, AlertCircle } from 'lucide-react';

interface NewPipelineModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function NewPipelineModal({ isOpen, onClose, onSuccess }: NewPipelineModalProps) {
  const [pipelineName, setPipelineName] = useState('');
  const [scheduleCron, setScheduleCron] = useState('0 * * * *');
  const [sourceConnector, setSourceConnector] = useState('postgres');
  const [targetLayer, setTargetLayer] = useState('BRONZE');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSuccess) onSuccess();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-cyan-400" />
            Create Enterprise Data Pipeline
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Pipeline Identifier
            </label>
            <input
              type="text"
              required
              placeholder="e.g. etl_sales_daily_aggregator"
              value={pipelineName}
              onChange={(e) => setPipelineName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Source Connector
              </label>
              <select
                value={sourceConnector}
                onChange={(e) => setSourceConnector(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="postgres">PostgreSQL OLTP</option>
                <option value="mysql">MySQL Cluster</option>
                <option value="snowflake">Snowflake Warehouse</option>
                <option value="kafka">Kafka Real-Time</option>
                <option value="s3">Amazon S3</option>
                <option value="salesforce">Salesforce CRM</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Target Lakehouse Layer
              </label>
              <select
                value={targetLayer}
                onChange={(e) => setTargetLayer(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
              >
                <option value="BRONZE">BRONZE (Raw Lake)</option>
                <option value="SILVER">SILVER (Cleansed)</option>
                <option value="GOLD">GOLD (Aggregated)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5 flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-cyan-400" /> Cron Schedule Spec
            </label>
            <input
              type="text"
              value={scheduleCron}
              onChange={(e) => setScheduleCron(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
            />
            <span className="text-[11px] text-slate-500 mt-1 block">Default: Hourly at minute 0 (0 * * * *)</span>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition flex items-center gap-1.5"
            >
              <Play className="w-3.5 h-3.5 fill-white" /> Create Pipeline
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
