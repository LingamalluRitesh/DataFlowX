import React from 'react';
import { Card } from './Card';
import { clsx } from 'clsx';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: {
    value: string;
    isPositive: boolean;
  };
  description?: string;
}

export const StatCard: React.FC<StatCardProps> = ({ title, value, icon, trend, description }) => {
  return (
    <Card hover className="p-6">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</span>
        <div className="p-2.5 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400">
          {icon}
        </div>
      </div>
      <div className="mt-4 flex items-baseline justify-between">
        <span className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">{value}</span>
        {trend && (
          <span
            className={clsx(
              'text-xs font-semibold px-2 py-0.5 rounded-full',
              trend.isPositive
                ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400'
                : 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-400'
            )}
          >
            {trend.isPositive ? '+' : ''}
            {trend.value}
          </span>
        )}
      </div>
      {description && <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{description}</p>}
    </Card>
  );
};
