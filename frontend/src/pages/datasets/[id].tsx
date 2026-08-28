import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Activity, ArrowLeft, BarChart2, Database, Layers, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Dataset } from '@/types';

export default function DatasetDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [profiling, setProfiling] = useState(false);

  const fetchDataset = async () => {
    if (!id) return;
    try {
      const res = await apiClient.get(`/datasets/${id}`);
      setDataset(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDataset();
  }, [id]);

  const handleProfile = async () => {
    if (!id) return;
    setProfiling(true);
    try {
      const res = await apiClient.post(`/datasets/${id}/profile`);
      setProfile(res.data);
    } catch (err: any) {
      alert(`Profiling failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setProfiling(false);
    }
  };

  if (loading) return <div>Loading dataset...</div>;
  if (!dataset) return <div>Dataset not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/datasets">
            <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
              <ArrowLeft className="w-4 h-4" />
            </button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-slate-100">{dataset.name}</h1>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant={dataset.layer as any}>{dataset.layer.toUpperCase()}</Badge>
              <span className="text-xs text-slate-400 font-mono">Format: {dataset.format.toUpperCase()}</span>
            </div>
          </div>
        </div>

        <Button variant="outline" size="sm" onClick={handleProfile} isLoading={profiling}>
          <BarChart2 className="w-3.5 h-3.5 mr-1.5" />
          Run Data Profiler
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Record Count</span>
          <p className="text-xl font-bold text-slate-100 mt-2">{dataset.record_count?.toLocaleString() || 0}</p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Quality Score</span>
          <p className="text-xl font-bold text-emerald-400 mt-2">{dataset.quality_score ? `${dataset.quality_score}%` : '100%'}</p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Storage Lake</span>
          <p className="text-sm font-mono text-blue-400 mt-2 truncate">{dataset.storage_path}</p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Version</span>
          <p className="text-xl font-bold text-purple-400 mt-2">v1.0</p>
        </Card>
      </div>

      {profile && (
        <Card>
          <CardHeader>
            <CardTitle>Column Profiling Report & Statistical Distributions</CardTitle>
          </CardHeader>
          <CardContent>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-2.5 px-4">Column</th>
                  <th className="py-2.5 px-4">Data Type</th>
                  <th className="py-2.5 px-4">Null Count</th>
                  <th className="py-2.5 px-4">Distinct Values</th>
                  <th className="py-2.5 px-4">Min / Max</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {profile.columns_profile?.map((cp: any) => (
                  <tr key={cp.name}>
                    <td className="py-3 px-4 font-mono text-blue-400 font-semibold">{cp.name}</td>
                    <td className="py-3 px-4 font-mono text-purple-400">{cp.inferred_type}</td>
                    <td className="py-3 px-4">{cp.null_count} ({cp.null_percentage}%)</td>
                    <td className="py-3 px-4">{cp.distinct_count}</td>
                    <td className="py-3 px-4 font-mono text-slate-400">
                      {cp.min_value !== undefined ? `${cp.min_value} / ${cp.max_value}` : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
