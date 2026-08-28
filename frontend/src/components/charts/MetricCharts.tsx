import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
} from 'recharts';

interface ThroughputChartProps {
  data: { timestamp: string; rows_per_sec: number; bytes_kb: number }[];
  height?: number;
}

export function ThroughputAreaChart({ data, height = 280 }: ThroughputChartProps) {
  return (
    <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-semibold text-white">Pipeline Ingestion Throughput</h4>
          <p className="text-xs text-slate-400">Events processed per second over time</p>
        </div>
        <span className="text-xs font-mono bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded">
          Real-Time
        </span>
      </div>

      <div style={{ width: '100%', height }}>
        <ResponsiveContainer>
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorRows" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="timestamp" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            />
            <Area type="monotone" dataKey="rows_per_sec" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#colorRows)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

interface LatencyBarChartProps {
  data: { stage: string; latency_ms: number; p99_ms: number }[];
  height?: number;
}

export function LatencyBarChart({ data, height = 280 }: LatencyBarChartProps) {
  return (
    <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-semibold text-white">Task Stage Latency Breakdown</h4>
          <p className="text-xs text-slate-400">Execution time (Avg vs P99) in milliseconds</p>
        </div>
      </div>

      <div style={{ width: '100%', height }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="stage" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            <Bar dataKey="latency_ms" name="Average Latency (ms)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            <Bar dataKey="p99_ms" name="P99 Tail Latency (ms)" fill="#ef4444" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
