import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { TrendingUp, Activity, Sparkles, CheckCircle, Flame, Layers } from 'lucide-react';

interface ForecastMetricItem {
  metric_name: string;
  historical_data_points: number;
  model: 'HOLT_WINTERS_TRIPLE' | 'ARIMA_AUTO' | 'FOURIER_PERIODICITY';
  detected_cycle_length: string;
  horizon_7d_projection: string;
  forecast_mape_pct: number;
  status: 'PREDICTED' | 'TRAINING';
}

const mockForecasts: ForecastMetricItem[] = [
  { metric_name: 'fact_orders.daily_revenue_usd', historical_data_points: 365, model: 'HOLT_WINTERS_TRIPLE', detected_cycle_length: '7.0 Days (Weekly Seasonality)', horizon_7d_projection: '$45,200.00 / day', forecast_mape_pct: 3.2, status: 'PREDICTED' },
  { metric_name: 'iot_telemetry.power_consumption_kwh', historical_data_points: 720, model: 'FOURIER_PERIODICITY', detected_cycle_length: '24.0 Hours (Diurnal Cycle)', horizon_7d_projection: '142.5 kWh', forecast_mape_pct: 2.1, status: 'PREDICTED' },
  { metric_name: 'raw_clickstream.active_sessions', historical_data_points: 180, model: 'ARIMA_AUTO', detected_cycle_length: '7.0 Days', horizon_7d_projection: '18,900 users', forecast_mape_pct: 4.8, status: 'PREDICTED' },
];

export default function ForecastingStudioPage() {
  const columns: DataGridColumn<ForecastMetricItem>[] = [
    { key: 'metric_name', header: 'Target Metric', render: (f) => <strong className="text-white font-mono text-xs">{f.metric_name}</strong> },
    {
      key: 'model',
      header: 'Forecasting Algorithm',
      render: (f) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{f.model}</span>,
    },
    { key: 'detected_cycle_length', header: 'Fourier Cyclic Period', render: (f) => <span className="font-mono text-cyan-300 text-xs">{f.detected_cycle_length}</span> },
    {
      key: 'horizon_7d_projection',
      header: '7-Day Projection',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.horizon_7d_projection}</span>,
    },
    { key: 'forecast_mape_pct', header: 'Forecast MAPE Error', render: (f) => <span className="font-mono text-slate-300">{f.forecast_mape_pct}% error</span> },
    {
      key: 'status',
      header: 'Status',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Time-Series Forecasting & Fourier Analysis — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <TrendingUp className="w-7 h-7 text-cyan-400" />
            Lakehouse Time-Series Forecasting & Fourier Periodicity Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Holt-Winters triple exponential smoothing, Auto-ARIMA baseline estimations, and Fast Fourier Transform (FFT) seasonal periodicity analysis.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Forecast Models</div>
            <div className="text-2xl font-bold text-white mt-1">3 Models</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Mean Absolute Percentage Error</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">3.36% (High Accuracy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Seasonal Decomposition</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Additive & Multiplicative</div>
          </div>
        </div>

        <DataGrid data={mockForecasts} columns={columns} title="Automated Time-Series Predictions" />
      </div>
    </MainLayout>
  );
}
