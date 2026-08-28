import React from 'react';
import { Gauge, Zap, TrendingUp, CheckCircle } from 'lucide-react';

interface ThroughputSlaGaugeProps {
  currentThroughputEps?: number;
  slaTargetEps?: number;
}

export function ThroughputSlaGauge({ currentThroughputEps = 48500, slaTargetEps = 50000 }: ThroughputSlaGaugeProps) {
  const percentage = Math.min(100, Math.round((currentThroughputEps / slaTargetEps) * 100));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between">
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-500 font-semibold uppercase flex items-center gap-1.5">
          <Zap className="w-3.5 h-3.5 text-amber-400" /> Real-Time Throughput SLA
        </span>
        <span className="text-[10px] font-bold text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
          Target: {slaTargetEps.toLocaleString()} eps
        </span>
      </div>

      <div className="my-4">
        <div className="flex items-baseline justify-between">
          <div className="text-3xl font-extrabold text-white font-mono">
            {currentThroughputEps.toLocaleString()} <span className="text-xs text-slate-400 font-normal">events/sec</span>
          </div>
          <div className="text-sm font-bold text-cyan-400 font-mono">{percentage}%</div>
        </div>

        <div className="w-full bg-slate-800 rounded-full h-3 mt-2 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-emerald-500 transition-all duration-500"
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between text-[11px] text-slate-400">
        <span>Zero Data Loss (At-Least-Once ACK)</span>
        <span className="text-emerald-400 font-semibold flex items-center gap-1">
          <CheckCircle className="w-3 h-3" /> SLA Met
        </span>
      </div>
    </div>
  );
}
