import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileArchive, Database, Layers, CheckCircle, Flame, HardDrive } from 'lucide-react';

interface CodecBenchmarkItem {
  codec_name: string;
  format_target: 'PARQUET_V2' | 'ORC_V2' | 'AVRO_OCF' | 'ARROW_IPC';
  compression_ratio: string;
  decompression_speed_mb_s: number;
  cpu_overhead_pct: number;
  recommended_workload: string;
}

const mockCodecs: CodecBenchmarkItem[] = [
  { codec_name: 'Zstandard (ZSTD Level 3)', format_target: 'PARQUET_V2', compression_ratio: '4.2x (76% reduction)', decompression_speed_mb_s: 1850, cpu_overhead_pct: 12.4, recommended_workload: 'General Analytics / Gold Tables' },
  { codec_name: 'Snappy (Framed Block)', format_target: 'PARQUET_V2', compression_ratio: '2.8x (64% reduction)', decompression_speed_mb_s: 3400, cpu_overhead_pct: 4.8, recommended_workload: 'High-Throughput Streaming Ingestion' },
  { codec_name: 'LZ4 (Fast Columnar)', format_target: 'ARROW_IPC', compression_ratio: '2.6x (61% reduction)', decompression_speed_mb_s: 4100, cpu_overhead_pct: 3.2, recommended_workload: 'Zero-Copy Microsecond IPC' },
  { codec_name: 'RLE + Bit-Packing Hybrid', format_target: 'ORC_V2', compression_ratio: '8.4x (88% reduction)', decompression_speed_mb_s: 2200, cpu_overhead_pct: 6.5, recommended_workload: 'Low-Cardinality Categorical Columns' },
];

export default function CodecsManagerPage() {
  const columns: DataGridColumn<CodecBenchmarkItem>[] = [
    { key: 'codec_name', header: 'Compression Codec', render: (c) => <strong className="text-white font-mono text-xs">{c.codec_name}</strong> },
    {
      key: 'format_target',
      header: 'Lakehouse Target Format',
      render: (c) => <span className="bg-slate-800 text-cyan-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.format_target}</span>,
    },
    {
      key: 'compression_ratio',
      header: 'Compression Factor',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.compression_ratio}</span>,
    },
    {
      key: 'decompression_speed_mb_s',
      header: 'Decompression Throughput',
      render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.decompression_speed_mb_s.toLocaleString()} MB/s</span>,
    },
    { key: 'cpu_overhead_pct', header: 'CPU Overhead', render: (c) => <span className="font-mono text-slate-300">{c.cpu_overhead_pct}%</span> },
    { key: 'recommended_workload', header: 'Recommended Workload', render: (c) => <span className="text-slate-300 text-xs">{c.recommended_workload}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Columnar Codecs & Compression — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileArchive className="w-7 h-7 text-cyan-400" />
            Parquet, ORC & Arrow Columnar Compression Codecs
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zstandard, Snappy, LZ4, and bit-packing hybrid codecs optimized for high-throughput decompression and maximum storage reduction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Platform Compression</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">4.2x Storage Savings</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Fastest Decompression Codec</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">LZ4 (4.1 GB/s)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">SIMD Vector Acceleration</div>
            <div className="text-2xl font-bold text-white mt-1">AVX2 / NEON Active</div>
          </div>
        </div>

        <DataGrid data={mockCodecs} columns={columns} title="Managed Compression Algorithms" />
      </div>
    </MainLayout>
  );
}
