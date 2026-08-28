import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileArchive, CheckCircle, Cpu, Zap, Activity, HardDrive } from 'lucide-react';

interface CodecBenchmarkItem {
  codec_name: string;
  compression_ratio: number;
  compress_speed_mb_s: number;
  decompress_speed_mb_s: number;
  cpu_overhead: 'LOW' | 'MEDIUM' | 'HIGH';
  recommended_for: string;
}

const mockCodecs: CodecBenchmarkItem[] = [
  { codec_name: 'Snappy', compression_ratio: 2.1, compress_speed_mb_s: 480.0, decompress_speed_mb_s: 1450.0, cpu_overhead: 'LOW', recommended_for: 'General analytical queries & low latency' },
  { codec_name: 'LZ4', compression_ratio: 2.3, compress_speed_mb_s: 520.0, decompress_speed_mb_s: 1820.0, cpu_overhead: 'LOW', recommended_for: 'High-throughput stream ingestion' },
  { codec_name: 'ZSTD (Level 3)', compression_ratio: 3.4, compress_speed_mb_s: 210.0, decompress_speed_mb_s: 980.0, cpu_overhead: 'MEDIUM', recommended_for: 'Cold historical archiving & Bronze lake' },
  { codec_name: 'RLE / Bit-Packing', compression_ratio: 8.5, compress_speed_mb_s: 1200.0, decompress_speed_mb_s: 2400.0, cpu_overhead: 'LOW', recommended_for: 'Low cardinality categorical & boolean columns' },
  { codec_name: 'Delta Binary Packing', compression_ratio: 6.2, compress_speed_mb_s: 950.0, decompress_speed_mb_s: 2100.0, cpu_overhead: 'LOW', recommended_for: 'Monotonic timestamps & autoincrement IDs' },
];

export default function CodecsBenchmarkPage() {
  const columns: DataGridColumn<CodecBenchmarkItem>[] = [
    { key: 'codec_name', header: 'Codec / Encoding Algorithm', render: (c) => <strong className="text-white font-mono">{c.codec_name}</strong> },
    {
      key: 'compression_ratio',
      header: 'Compression Ratio',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.compression_ratio}x reduction</span>,
    },
    { key: 'compress_speed_mb_s', header: 'Encode Speed', render: (c) => <span className="font-mono text-cyan-300">{c.compress_speed_mb_s} MB/s</span> },
    { key: 'decompress_speed_mb_s', header: 'Decode Speed', render: (c) => <span className="font-mono text-purple-300 font-semibold">{c.decompress_speed_mb_s} MB/s</span> },
    {
      key: 'cpu_overhead',
      header: 'CPU Overhead',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.cpu_overhead === 'LOW'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {c.cpu_overhead}
        </span>
      ),
    },
    { key: 'recommended_for', header: 'Optimal Workload Fit', sortable: false },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Parquet Codecs & Compression Benchmarks — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileArchive className="w-7 h-7 text-cyan-400" />
            Parquet Codecs & Compression Benchmarking Suite
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Pure-Python Snappy, LZ4, RLE/Bit-packing, and Delta Binary Packing benchmarks and storage space savings.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Lakehouse Compression</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">3.1x Space Savings</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Decompression Throughput</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.82 GB/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Default Lakehouse Codec</div>
            <div className="text-2xl font-bold text-white mt-1">Snappy + RLE</div>
          </div>
        </div>

        <DataGrid data={mockCodecs} columns={columns} title="Compression Codec Benchmark Matrix" />
      </div>
    </MainLayout>
  );
}
