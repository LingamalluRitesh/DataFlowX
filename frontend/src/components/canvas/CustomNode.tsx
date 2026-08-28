import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import {
  Activity,
  Code,
  CornerDownRight,
  Database,
  FileCode,
  Filter,
  Layers,
  Settings,
  ShieldCheck,
  Table,
} from 'lucide-react';
import { clsx } from 'clsx';

const nodeIcons: Record<string, any> = {
  extract: Database,
  source: Database,
  transform: Layers,
  filter: Filter,
  aggregate: Table,
  quality: ShieldCheck,
  validate: ShieldCheck,
  sql: FileCode,
  python: Code,
  warehouse_load: Database,
  branch: CornerDownRight,
};

const nodeColors: Record<string, { border: string; bg: string; icon: string }> = {
  extract: { border: 'border-blue-500', bg: 'bg-blue-50 dark:bg-blue-950/40', icon: 'text-blue-600 dark:text-blue-400' },
  source: { border: 'border-blue-500', bg: 'bg-blue-50 dark:bg-blue-950/40', icon: 'text-blue-600 dark:text-blue-400' },
  transform: { border: 'border-purple-500', bg: 'bg-purple-50 dark:bg-purple-950/40', icon: 'text-purple-600 dark:text-purple-400' },
  filter: { border: 'border-amber-500', bg: 'bg-amber-50 dark:bg-amber-950/40', icon: 'text-amber-600 dark:text-amber-400' },
  aggregate: { border: 'border-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-950/40', icon: 'text-emerald-600 dark:text-emerald-400' },
  quality: { border: 'border-rose-500', bg: 'bg-rose-50 dark:bg-rose-950/40', icon: 'text-rose-600 dark:text-rose-400' },
  validate: { border: 'border-rose-500', bg: 'bg-rose-50 dark:bg-rose-950/40', icon: 'text-rose-600 dark:text-rose-400' },
  sql: { border: 'border-cyan-500', bg: 'bg-cyan-50 dark:bg-cyan-950/40', icon: 'text-cyan-600 dark:text-cyan-400' },
  python: { border: 'border-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-950/40', icon: 'text-yellow-600 dark:text-yellow-400' },
  warehouse_load: { border: 'border-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-950/40', icon: 'text-indigo-600 dark:text-indigo-400' },
  branch: { border: 'border-orange-500', bg: 'bg-orange-50 dark:bg-orange-950/40', icon: 'text-orange-600 dark:text-orange-400' },
};

export const CustomPipelineNode = memo(({ data, selected }: any) => {
  const nodeType = data.type?.toLowerCase() || 'transform';
  const Icon = nodeIcons[nodeType] || Layers;
  const theme = nodeColors[nodeType] || nodeColors.transform;

  return (
    <div
      className={clsx(
        'w-64 rounded-xl bg-white dark:bg-slate-900 border-2 shadow-lg transition-all duration-150',
        selected ? 'border-blue-500 ring-2 ring-blue-500/20 shadow-blue-500/10' : theme.border,
        'overflow-hidden'
      )}
    >
      {/* Input Handle */}
      {nodeType !== 'source' && nodeType !== 'extract' && (
        <Handle
          type="target"
          position={Position.Left}
          className="w-3 h-3 bg-blue-500 border-2 border-white dark:border-slate-900"
        />
      )}

      {/* Node Header */}
      <div className={clsx('px-4 py-3 flex items-center justify-between border-b border-slate-100 dark:border-slate-800', theme.bg)}>
        <div className="flex items-center gap-2.5">
          <div className={clsx('p-1.5 rounded-lg bg-white dark:bg-slate-900 shadow-xs', theme.icon)}>
            <Icon className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100 truncate max-w-[130px]">
              {data.name || data.label || 'Node'}
            </h4>
            <span className="text-[10px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              {nodeType}
            </span>
          </div>
        </div>
      </div>

      {/* Node Body Details */}
      <div className="p-3 text-[11px] text-slate-600 dark:text-slate-400 space-y-1">
        {data.config?.connector_type && (
          <div className="flex justify-between">
            <span className="text-slate-400">Connector:</span>
            <span className="font-mono font-medium text-slate-800 dark:text-slate-200">{data.config.connector_type}</span>
          </div>
        )}
        {data.config?.table_name && (
          <div className="flex justify-between">
            <span className="text-slate-400">Table:</span>
            <span className="font-mono font-medium text-slate-800 dark:text-slate-200">{data.config.table_name}</span>
          </div>
        )}
        {data.config?.rules && (
          <div className="flex justify-between">
            <span className="text-slate-400">Rules:</span>
            <span className="font-medium text-slate-800 dark:text-slate-200">{data.config.rules.length} checks</span>
          </div>
        )}
        {!data.config?.connector_type && !data.config?.table_name && !data.config?.rules && (
          <p className="italic text-slate-400 truncate">Configured & ready</p>
        )}
      </div>

      {/* Output Handle */}
      {nodeType !== 'warehouse_load' && (
        <Handle
          type="source"
          position={Position.Right}
          className="w-3 h-3 bg-blue-500 border-2 border-white dark:border-slate-900"
        />
      )}
    </div>
  );
});

CustomPipelineNode.displayName = 'CustomPipelineNode';
