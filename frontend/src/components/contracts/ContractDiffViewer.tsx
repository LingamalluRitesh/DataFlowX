import React from 'react';
import { AlertTriangle, CheckCircle, ArrowRight, ShieldAlert } from 'lucide-react';

export interface ColumnDiffItem {
  column_name: str;
  old_type?: string;
  new_type?: string;
  change_type: 'ADDED' | 'REMOVED' | 'TYPE_CHANGED' | 'NULLABILITY_CHANGED' | 'UNCHANGED';
  is_breaking: boolean;
}

interface ContractDiffViewerProps {
  contractId: string;
  datasetName: string;
  diffs: ColumnDiffItem[];
}

export function ContractDiffViewer({ contractId, datasetName, diffs }: ContractDiffViewerProps) {
  const breakingCount = diffs.filter((d) => d.is_breaking).length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/80">
        <div>
          <h4 className="text-sm font-semibold text-white">Schema Contract Diff Analyzer</h4>
          <p className="text-xs text-slate-400">Dataset: <span className="font-mono text-cyan-400">{datasetName}</span> ({contractId})</p>
        </div>

        {breakingCount > 0 ? (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-950/80 text-red-400 border border-red-800 text-xs font-semibold">
            <ShieldAlert className="w-4 h-4" /> {breakingCount} Breaking Changes Detected
          </span>
        ) : (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-800 text-xs font-semibold">
            <CheckCircle className="w-4 h-4" /> 100% Backwards Compatible
          </span>
        )}
      </div>

      <div className="divide-y divide-slate-800/60 font-mono text-xs">
        {diffs.map((d, idx) => (
          <div key={idx} className={`p-3.5 flex items-center justify-between ${d.is_breaking ? 'bg-red-950/20' : ''}`}>
            <div className="flex items-center gap-3">
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  d.change_type === 'ADDED'
                    ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                    : d.change_type === 'REMOVED'
                    ? 'bg-red-950 text-red-400 border border-red-800'
                    : d.change_type === 'TYPE_CHANGED'
                    ? 'bg-amber-950 text-amber-400 border border-amber-800'
                    : 'bg-slate-800 text-slate-400'
                }`}
              >
                {d.change_type}
              </span>
              <span className="font-semibold text-slate-200">{d.column_name}</span>
            </div>

            <div className="flex items-center gap-3 text-slate-400">
              {d.old_type && <span className="bg-slate-800 px-2 py-0.5 rounded">{d.old_type}</span>}
              {d.old_type && d.new_type && <ArrowRight className="w-3.5 h-3.5 text-slate-500" />}
              {d.new_type && <span className="bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded">{d.new_type}</span>}
              {d.is_breaking && (
                <span className="text-red-400 text-xs flex items-center gap-1 font-sans font-medium">
                  <AlertTriangle className="w-3.5 h-3.5" /> Breaking Change
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
