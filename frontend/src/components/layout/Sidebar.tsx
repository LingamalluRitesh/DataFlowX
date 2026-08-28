import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  Activity,
  AlertCircle,
  Bell,
  Cpu,
  Database,
  GitFork,
  HardDrive,
  History,
  Layers,
  LayoutDashboard,
  Play,
  Settings,
  ShieldCheck,
  Users,
  Workflow,
} from 'lucide-react';
import { clsx } from 'clsx';

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Data Sources', href: '/sources', icon: Database },
  { name: 'Dataset Catalog', href: '/datasets', icon: Layers },
  { name: 'Pipelines & DAGs', href: '/pipelines', icon: Workflow },
  { name: 'Executions', href: '/executions', icon: Play },
  { name: 'Data Quality', href: '/quality', icon: ShieldCheck },
  { name: 'Data Lineage', href: '/lineage', icon: GitFork },
  { name: 'Worker Cluster', href: '/workers', icon: Cpu },
  { name: 'Platform Metrics', href: '/monitoring', icon: Activity },
  { name: 'Alerts & Incidents', href: '/alerts', icon: AlertCircle },
  { name: 'Audit Logs', href: '/audit', icon: History },
  { name: 'Team & RBAC', href: '/users', icon: Users },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  const router = useRouter();

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col flex-shrink-0 border-r border-slate-800">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800 gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20">
          X
        </div>
        <div>
          <span className="font-bold text-lg text-white tracking-tight">DataFlowX</span>
          <span className="ml-1.5 text-[10px] uppercase font-semibold tracking-wider px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400">
            Enterprise
          </span>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = router.pathname === item.href || (item.href !== '/dashboard' && router.pathname.startsWith(item.href));

          return (
            <Link
              key={item.name}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-600 text-white font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              )}
            >
              <Icon className={clsx('w-4 h-4', isActive ? 'text-white' : 'text-slate-400')} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </div>

      {/* Footer System Status */}
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Cluster Healthy</span>
          </div>
          <span className="text-slate-400">v1.0.0</span>
        </div>
      </div>
    </aside>
  );
};
