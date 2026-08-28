import React from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle, Lock, ShieldAlert } from 'lucide-react';

interface ComplianceFrameworkScore {
  framework: string;
  score_pct: number;
  passed_checks: number;
  total_checks: number;
  status: 'COMPLIANT' | 'NEEDS_REVIEW' | 'NON_COMPLIANT';
}

const mockFrameworks: ComplianceFrameworkScore[] = [
  { framework: 'GDPR (EU General Data Protection Regulation)', score_pct: 100.0, passed_checks: 18, total_checks: 18, status: 'COMPLIANT' },
  { framework: 'CCPA / CPRA (California Consumer Privacy)', score_pct: 100.0, passed_checks: 14, total_checks: 14, status: 'COMPLIANT' },
  { framework: 'HIPAA Security Rule (ePHI Encryption)', score_pct: 95.0, passed_checks: 19, total_checks: 20, status: 'COMPLIANT' },
  { framework: 'SOX Section 404 (Financial Internal Controls)', score_pct: 100.0, passed_checks: 12, total_checks: 12, status: 'COMPLIANT' },
  { framework: 'PCI-DSS v4.0 (Cardholder Data Protection)', score_pct: 92.0, passed_checks: 23, total_checks: 25, status: 'NEEDS_REVIEW' },
];

export function ComplianceScorecard() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Global Compliance & Regulatory Audit Scorecard
          </h3>
          <p className="text-xs text-slate-400">Automated statutory audit verification checks across enterprise frameworks</p>
        </div>
        <span className="text-xs font-bold text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded-full">
          Overall: 97.4% Compliant
        </span>
      </div>

      <div className="space-y-3">
        {mockFrameworks.map((f) => (
          <div key={f.framework} className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-xs text-white">{f.framework}</span>
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                {f.passed_checks} of {f.total_checks} automated control tests passed
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-32 bg-slate-800 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full rounded-full ${f.score_pct >= 95 ? 'bg-emerald-500' : 'bg-amber-500'}`}
                  style={{ width: `${f.score_pct}%` }}
                />
              </div>
              <span className="text-xs font-mono font-bold text-white w-12 text-right">{f.score_pct}%</span>
              <span
                className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                  f.status === 'COMPLIANT'
                    ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                    : 'bg-amber-950 text-amber-400 border border-amber-800'
                }`}
              >
                {f.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
