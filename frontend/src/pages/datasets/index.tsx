import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Database, Layers, Plus, RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Dataset } from '@/types';

export default function DatasetsIndexPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchDatasets = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/datasets?search=${search}`);
      setDatasets(res.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Dataset Catalog</h1>
          <p className="text-sm text-slate-400 mt-1">
            Enterprise data lakes across Bronze (raw), Silver (curated), and Gold (analytics)
          </p>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div className="relative w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search datasets by name or layer..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <Button variant="outline" size="sm" onClick={fetchDatasets}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-6">Dataset Name</th>
                <th className="py-3.5 px-6">Medallion Layer</th>
                <th className="py-3.5 px-6">Format</th>
                <th className="py-3.5 px-6">Record Count</th>
                <th className="py-3.5 px-6">Quality Score</th>
                <th className="py-3.5 px-6">Storage Path</th>
                <th className="py-3.5 px-6">Last Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {datasets.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-12 text-slate-500">
                    No cataloged datasets found. Run pipeline executions to register Bronze/Silver/Gold datasets.
                  </td>
                </tr>
              ) : (
                datasets.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-semibold text-slate-100">
                      <Link href={`/datasets/${d.id}`} className="hover:text-blue-400">
                        {d.name}
                      </Link>
                    </td>
                    <td className="py-4 px-6">
                      <Badge variant={d.layer as any}>
                        {d.layer.toUpperCase()}
                      </Badge>
                    </td>
                    <td className="py-4 px-6 uppercase font-mono text-[11px] text-purple-400">
                      {d.format}
                    </td>
                    <td className="py-4 px-6 font-medium">
                      {d.record_count?.toLocaleString() || '0'}
                    </td>
                    <td className="py-4 px-6 font-semibold text-emerald-400">
                      {d.quality_score ? `${d.quality_score}%` : 'N/A'}
                    </td>
                    <td className="py-4 px-6 font-mono text-[11px] text-slate-400 truncate max-w-xs">
                      {d.storage_path}
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {new Date(d.updated_at || d.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
