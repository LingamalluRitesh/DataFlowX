import React, { useEffect, useState } from 'react';
import { CheckCircle2, Filter, Plus, RefreshCw, ShieldCheck, XCircle } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { QualityRule, QualitySuite } from '@/types';

export default function QualityPage() {
  const [rules, setRules] = useState<QualityRule[]>([]);
  const [suites, setSuites] = useState<QualitySuite[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchQualityData = async () => {
    setLoading(true);
    try {
      const [rulesRes, suitesRes] = await Promise.all([
        apiClient.get('/quality/rules'),
        apiClient.get('/quality/suites'),
      ]);
      setRules(rulesRes.data || []);
      setSuites(suitesRes.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQualityData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Data Quality & Governance</h1>
          <p className="text-sm text-slate-400 mt-1">
            Automated test suites, rule definitions, SLA validations & quarantine management
          </p>
        </div>
      </div>

      {/* Rules Library */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Built-in & Custom Quality Rules</CardTitle>
          <Button variant="outline" size="sm" onClick={fetchQualityData}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-6">Rule Name</th>
                <th className="py-3 px-6">Type</th>
                <th className="py-3 px-6">Description</th>
                <th className="py-3 px-6">Default Severity</th>
                <th className="py-3 px-6">Type Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {rules.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-6 font-semibold text-slate-100 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-blue-400" />
                    <span>{r.name}</span>
                  </td>
                  <td className="py-3.5 px-6 font-mono text-purple-400 uppercase">{r.rule_type}</td>
                  <td className="py-3.5 px-6 text-slate-400">{r.description || '-'}</td>
                  <td className="py-3.5 px-6">
                    <Badge variant={r.default_severity === 'CRITICAL' ? 'danger' : 'warning'}>
                      {r.default_severity}
                    </Badge>
                  </td>
                  <td className="py-3.5 px-6">
                    <Badge variant={r.is_builtin ? 'primary' : 'neutral'}>
                      {r.is_builtin ? 'BUILT-IN' : 'CUSTOM'}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
