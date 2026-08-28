import React, { useState } from 'react';
import { X, Bell, CheckCircle, Send, Slack, Mail } from 'lucide-react';

interface AlertConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function AlertConfigModal({ isOpen, onClose, onSuccess }: AlertConfigModalProps) {
  const [channelType, setChannelType] = useState('SLACK');
  const [targetEndpoint, setTargetEndpoint] = useState('https://hooks.slack.com/services/...');
  const [severity, setSeverity] = useState('CRITICAL');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSuccess) onSuccess();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Bell className="w-5 h-5 text-amber-400" />
            Configure SLA & Incident Alert Channel
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Channel Dispatcher
              </label>
              <select
                value={channelType}
                onChange={(e) => setChannelType(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="SLACK">Slack Incoming Webhook</option>
                <option value="PAGERDUTY">PagerDuty Incident API</option>
                <option value="EMAIL">SMTP Email Notification</option>
                <option value="OPSGENIE">Opsgenie Alerting</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
                Trigger Severity Threshold
              </label>
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
              >
                <option value="CRITICAL">CRITICAL (SLA Breaches)</option>
                <option value="HIGH">HIGH (Pipeline Failures)</option>
                <option value="WARNING">WARNING (Quality Warnings)</option>
                <option value="INFO">INFO (All Run Events)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1.5">
              Webhook URL / Endpoint / Email Recipient
            </label>
            <input
              type="text"
              required
              value={targetEndpoint}
              onChange={(e) => setTargetEndpoint(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition flex items-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" /> Save Notification Channel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
