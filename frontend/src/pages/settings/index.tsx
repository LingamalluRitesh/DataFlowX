import React, { useState } from 'react';
import { Database, Key, Lock, Save, Server, Shield, Sliders } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

export default function SettingsPage() {
  const [retentionDays, setRetentionDays] = useState('90');
  const [rateLimit, setRateLimit] = useState('120');

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Settings saved successfully!');
  };

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Platform Settings</h1>
        <p className="text-sm text-slate-400 mt-1">Configure workspace parameters, security rules, and retention policies</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <Card className="p-6 space-y-4">
          <CardTitle>Data Retention & Storage Lifecycle</CardTitle>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Execution Log Retention (Days)</label>
              <input
                type="number"
                value={retentionDays}
                onChange={(e) => setRetentionDays(e.target.value)}
                className="w-full px-3.5 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">API Rate Limit (Requests / Min)</label>
              <input
                type="number"
                value={rateLimit}
                onChange={(e) => setRateLimit(e.target.value)}
                className="w-full px-3.5 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
              />
            </div>
          </div>
        </Card>

        <Card className="p-6 space-y-4">
          <CardTitle>Security & Credential Encryption</CardTitle>
          <div className="space-y-2 text-xs text-slate-300">
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Vault Master Key Encryption:</span>
              <span className="font-mono text-emerald-400">AES-256-GCM ACTIVE</span>
            </div>
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>JWT Secret Algorithm:</span>
              <span className="font-mono text-blue-400">HS256 (60m access / 30d refresh)</span>
            </div>
          </div>
        </Card>

        <div className="flex justify-end">
          <Button type="submit" variant="primary" size="sm">
            <Save className="w-4 h-4 mr-1.5" /> Save Configuration
          </Button>
        </div>
      </form>
    </div>
  );
}
