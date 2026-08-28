import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Binary, Database, CheckCircle, Clock, Layers, ArrowRight } from 'lucide-react';

interface AvroMessageItem {
  schema_id: number;
  schema_subject: string;
  magic_byte_valid: boolean;
  message_size_bytes: number;
  unpacked_fields_count: number;
  deserialization_speed: string;
}

const mockAvroMessages: AvroMessageItem[] = [
  { schema_id: 1042, schema_subject: 'events.orders.avro-value', magic_byte_valid: true, message_size_bytes: 342, unpacked_fields_count: 24, deserialization_speed: '1.4M msg/s' },
  { schema_id: 1043, schema_subject: 'events.users.avro-value', magic_byte_valid: true, message_size_bytes: 180, unpacked_fields_count: 12, deserialization_speed: '2.1M msg/s' },
  { schema_id: 1044, schema_subject: 'iot.sensor.avro-value', magic_byte_valid: true, message_size_bytes: 64, unpacked_fields_count: 8, deserialization_speed: '3.8M msg/s' },
];

export default function AvroDecodeStudioPage() {
  const columns: DataGridColumn<AvroMessageItem>[] = [
    {
      key: 'schema_id',
      header: 'Schema Registry ID',
      render: (a) => (
        <span className="font-mono text-cyan-300 font-bold flex items-center gap-1.5">
          <Binary className="w-3.5 h-3.5" /> #{a.schema_id}
        </span>
      ),
    },
    { key: 'schema_subject', header: 'Schema Subject', render: (a) => <strong className="text-white font-mono text-xs">{a.schema_subject}</strong> },
    {
      key: 'magic_byte_valid',
      header: 'Wire Protocol Magic Byte',
      render: (a) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          0x00 (VALID)
        </span>
      ),
    },
    { key: 'message_size_bytes', header: 'Wire Payload Size', render: (a) => <span className="font-mono text-slate-300">{a.message_size_bytes} Bytes</span> },
    { key: 'unpacked_fields_count', header: 'Decoded Fields', render: (a) => <span className="font-mono text-slate-300">{a.unpacked_fields_count} fields</span> },
    {
      key: 'deserialization_speed',
      header: 'Decoding Throughput',
      render: (a) => <span className="font-mono text-emerald-400 font-bold">{a.deserialization_speed}</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Confluent Avro Binary Deserializer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Binary className="w-7 h-7 text-cyan-400" />
            Confluent Avro Wire Protocol Deserializer & Schema Unpacker
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-copy parsing of magic-byte headers, Schema Registry ID resolution, and zigzag binary integer unpackers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Message Unpack Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">2.4M msg / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cached Schema Definitions</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">3 Active Schemas</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Serialization Standard</div>
            <div className="text-2xl font-bold text-white mt-1">Apache Avro 1.11 Spec</div>
          </div>
        </div>

        <DataGrid data={mockAvroMessages} columns={columns} title="Decoded Avro Message Streams" />
      </div>
    </MainLayout>
  );
}
