import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { ArrowLeft, Database, Key, Server } from 'lucide-react';
import Link from 'next/link';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

const connectorTypes = [
  { id: 'postgres', name: 'PostgreSQL Database', category: 'Database' },
  { id: 'mysql', name: 'MySQL Database', category: 'Database' },
  { id: 'mongodb', name: 'MongoDB NoSQL', category: 'Database' },
  { id: 'rest', name: 'REST API Endpoint', category: 'API' },
  { id: 'csv', name: 'CSV File / Storage', category: 'File' },
  { id: 'excel', name: 'Excel Workbook (.xlsx)', category: 'File' },
  { id: 'json', name: 'JSON / NDJSON Files', category: 'File' },
  { id: 's3', name: 'Amazon S3 / MinIO Lake', category: 'Storage' },
  { id: 'kafka', name: 'Apache Kafka Topic', category: 'Stream' },
];

export default function NewSourcePage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [connectorType, setConnectorType] = useState('postgres');
  const [description, setDescription] = useState('');
  const [host, setHost] = useState('localhost');
  const [port, setPort] = useState('5432');
  const [database, setDatabase] = useState('postgres');
  const [username, setUsername] = useState('postgres');
  const [password, setPassword] = useState('');
  const [filePath, setFilePath] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const config: Record<string, any> = {};
      const credentials: Record<string, any> = {};

      if (['postgres', 'mysql', 'mongodb'].includes(connectorType)) {
        config.host = host;
        config.port = parseInt(port) || 5432;
        config.database = database;
        credentials.username = username;
        credentials.password = password;
      } else if (['csv', 'excel', 'json'].includes(connectorType)) {
        config.file_path = filePath;
      }

      await apiClient.post('/sources', {
        name,
        connector_type: connectorType,
        description,
        config,
        credentials,
        auth_type: 'basic',
      });

      router.push('/sources');
    } catch (err: any) {
      alert(`Error creating source: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <Link href="/sources">
          <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
            <ArrowLeft className="w-4 h-4" />
          </button>
        </Link>
        <div>
          <h1 className="text-xl font-bold text-slate-100">Connect New Data Source</h1>
          <p className="text-xs text-slate-400">Configure connection parameters and encrypted credentials</p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="p-6 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Source Name
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Production Customer DB"
                className="w-full px-3.5 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-slate-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Connector Type
              </label>
              <select
                value={connectorType}
                onChange={(e) => setConnectorType(e.target.value)}
                className="w-full px-3.5 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-slate-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                {connectorTypes.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.category})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Description
              </label>
              <textarea
                rows={2}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Core transactional database for customer accounts..."
                className="w-full px-3.5 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-slate-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Dynamic Configuration based on connector type */}
          {['postgres', 'mysql', 'mongodb'].includes(connectorType) ? (
            <div className="pt-4 border-t border-slate-800 space-y-4">
              <h3 className="text-xs font-bold text-blue-400 uppercase tracking-wider flex items-center gap-2">
                <Server className="w-4 h-4" /> Host & Connection Settings
              </h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="col-span-2">
                  <label className="block text-xs text-slate-400 mb-1">Host / Endpoint</label>
                  <input
                    type="text"
                    value={host}
                    onChange={(e) => setHost(e.target.value)}
                    className="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
                  />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Port</label>
                  <input
                    type="text"
                    value={port}
                    onChange={(e) => setPort(e.target.value)}
                    className="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1">Database Name</label>
                <input
                  type="text"
                  value={database}
                  onChange={(e) => setDatabase(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Username</label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
                  />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Password</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className="pt-4 border-t border-slate-800 space-y-4">
              <h3 className="text-xs font-bold text-blue-400 uppercase tracking-wider flex items-center gap-2">
                <Database className="w-4 h-4" /> File / Storage Path
              </h3>
              <div>
                <label className="block text-xs text-slate-400 mb-1">File or S3 URI</label>
                <input
                  type="text"
                  value={filePath}
                  onChange={(e) => setFilePath(e.target.value)}
                  placeholder="./storage/temp/raw_customers.csv or s3://bucket/path"
                  className="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100 font-mono"
                />
              </div>
            </div>
          )}

          <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
            <Link href="/sources">
              <Button variant="outline" size="sm">
                Cancel
              </Button>
            </Link>
            <Button type="submit" variant="primary" size="sm" isLoading={loading}>
              Create & Save Source
            </Button>
          </div>
        </Card>
      </form>
    </div>
  );
}
