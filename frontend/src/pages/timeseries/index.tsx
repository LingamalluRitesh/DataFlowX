import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { LineChart, Activity, TrendingUp, DollarSign, CheckCircle, Zap } from 'lucide-react';

interface TimeSeriesSignalItem {
  symbol: string;
  current_price: number;
  ema_14: number;
  bollinger_upper: number;
  bollinger_lower: number;
  volatility_pct: number;
  trend_signal: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
}

const mockSignals: TimeSeriesSignalItem[] = [
  { symbol: 'ETH-USD', current_price: 3420.50, ema_14: 3380.10, bollinger_upper: 3550.00, bollinger_lower: 3210.00, volatility_pct: 3.4, trend_signal: 'BULLISH' },
  { symbol: 'BTC-USD', current_price: 64200.00, ema_14: 63900.50, bollinger_upper: 66000.00, bollinger_lower: 61800.00, volatility_pct: 2.1, trend_signal: 'BULLISH' },
  { symbol: 'SOL-USD', current_price: 145.20, ema_14: 148.00, bollinger_upper: 155.00, bollinger_lower: 139.00, volatility_pct: 5.8, trend_signal: 'BEARISH' },
];

export default function TimeSeriesSignalPage() {
  const columns: DataGridColumn<TimeSeriesSignalItem>[] = [
    { key: 'symbol', header: 'Asset Symbol', render: (s) => <strong className="text-white font-mono">{s.symbol}</strong> },
    { key: 'current_price', header: 'Current Price', render: (s) => <span className="font-mono text-cyan-400 font-bold">${s.current_price.toLocaleString()}</span> },
    { key: 'ema_14', header: '14-Period EMA', render: (s) => <span className="font-mono text-slate-300">${s.ema_14.toLocaleString()}</span> },
    {
      key: 'bollinger_upper',
      header: 'Bollinger Bands (2σ)',
      render: (s) => (
        <span className="font-mono text-xs text-slate-400">
          [{s.bollinger_lower} — {s.bollinger_upper}]
        </span>
      ),
    },
    { key: 'volatility_pct', header: 'Rolling Volatility', render: (s) => <span className="font-mono text-purple-400">{s.volatility_pct}%</span> },
    {
      key: 'trend_signal',
      header: 'Signal Indicator',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.trend_signal === 'BULLISH'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-red-950 text-red-400 border border-red-800'
          }`}
        >
          {s.trend_signal}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Time-Series & Financial Signal Processing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <TrendingUp className="w-7 h-7 text-cyan-400" />
            Time-Series & Financial Signal Processing Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Exponential Moving Averages, Bollinger Bands, rolling volatility, and financial metric calculations in vectorized pipelines.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Tickers</div>
            <div className="text-2xl font-bold text-white mt-1">3 Tickers</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Calculated Signals</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">12 Signals/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0.6 ms</div>
          </div>
        </div>

        <DataGrid data={mockSignals} columns={columns} title="Live Financial & Time-Series Signal Stream" />
      </div>
    </MainLayout>
  );
}
