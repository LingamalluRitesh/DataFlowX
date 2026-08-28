import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Clock, TrendingUp, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface AsOfMatchItem {
  trade_id: string;
  symbol: string;
  trade_time: string;
  trade_price: number;
  matched_quote_time: string;
  matched_bid_price: number;
  matched_ask_price: number;
  time_delta_ms: number;
}

const mockAsOf: AsOfMatchItem[] = [
  { trade_id: 'tr_AAPL_901', symbol: 'AAPL', trade_time: '2026-08-29 00:24:00.124', trade_price: 224.50, matched_quote_time: '2026-08-29 00:24:00.118', matched_bid_price: 224.48, matched_ask_price: 224.52, time_delta_ms: 6 },
  { trade_id: 'tr_MSFT_902', symbol: 'MSFT', trade_time: '2026-08-29 00:24:00.340', trade_price: 448.20, matched_quote_time: '2026-08-29 00:24:00.332', matched_bid_price: 448.18, matched_ask_price: 448.22, time_delta_ms: 8 },
  { trade_id: 'tr_NVDA_903', symbol: 'NVDA', trade_time: '2026-08-29 00:24:00.512', trade_price: 128.90, matched_quote_time: '2026-08-29 00:24:00.510', matched_bid_price: 128.88, matched_ask_price: 128.92, time_delta_ms: 2 },
];

export default function AsOfJoinsStudioPage() {
  const columns: DataGridColumn<AsOfMatchItem>[] = [
    {
      key: 'trade_id',
      header: 'Trade Event',
      render: (a) => (
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{a.trade_id}</strong>
        </div>
      ),
    },
    { key: 'symbol', header: 'Ticker Symbol', render: (a) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{a.symbol}</span> },
    { key: 'trade_time', header: 'Trade Timestamp', render: (a) => <span className="font-mono text-slate-300 text-xs">{a.trade_time}</span> },
    {
      key: 'trade_price',
      header: 'Executed Price',
      render: (a) => <span className="font-mono text-white font-bold">${a.trade_price.toFixed(2)}</span>,
    },
    { key: 'matched_quote_time', header: 'Matched BBO Quote Time', render: (a) => <span className="font-mono text-cyan-300 text-xs">{a.matched_quote_time}</span> },
    {
      key: 'matched_bid_price',
      header: 'BBO Spread (Bid / Ask)',
      render: (a) => <span className="font-mono text-emerald-400 font-bold">${a.matched_bid_price.toFixed(2)} / ${a.matched_ask_price.toFixed(2)}</span>,
    },
    {
      key: 'time_delta_ms',
      header: 'Temporal Delta',
      render: (a) => <span className="font-mono text-emerald-400 font-bold">{a.time_delta_ms} ms</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Temporal As-Of Joins & Time Alignment — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Clock className="w-7 h-7 text-cyan-400" />
            Financial & IoT Temporal As-Of Join Alignment Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            High-precision temporal matching joining high-frequency trade ticks against preceding BBO market quotes and IoT sensor metrics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">As-Of Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4.2M matches / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Temporal Delta</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">5.3 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Temporal Tolerance</div>
            <div className="text-2xl font-bold text-white mt-1">100 ms Max Window</div>
          </div>
        </div>

        <DataGrid data={mockAsOf} columns={columns} title="Active Temporal As-Of Aligned Streams" />
      </div>
    </MainLayout>
  );
}
