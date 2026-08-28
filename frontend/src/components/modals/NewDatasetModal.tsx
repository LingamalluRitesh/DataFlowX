import React, { useState } from 'react';
import { X, Layers, Sparkles, CheckCircle, Database } from 'lucide-react';

interface NewDatasetModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function NewDatasetModal({ isOpen, onClose, onSuccess }: NewDatasetModalProps) {
  const [datasetName, setDatasetName] = useState('');
  const [layer, setLayer] = useState('BRONZE');
  const [format, setFormat] = useState('PARQUET');
  const [description, setDescription] = useState('');

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
            <Layers className="w-5 h-5 text-purple-400" />
            Register Lakehouse Dataset
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Dataset Name
            </label>
            <input
              type="text"
              required
              placeholder="e.g. fact_daily_orders"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Lakehouse Layer
              </label>
              <select
                value={layer}
                onChange={(e) => setLayer(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
              >
                <option value="BRONZE">BRONZE (Raw Lake)</option>
                <option value="SILVER">SILVER (Cleansed)</option>
                <option value="GOLD">GOLD (Analytics Aggregations)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Storage Format
              </label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
              >
                <option value="DELTA">Delta Lake (ACID)</option>
                <option value="ICEBERG">Apache Iceberg</option>
                <option value="PARQUET">Apache Parquet</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Dataset Business Description
            </label>
            <textarea
              rows={3}
              placeholder="Canonical enterprise dataset representing captured customer invoices."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
            />
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
              <CheckCircle className="w-3.5 h-3.5" /> Register Dataset
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
