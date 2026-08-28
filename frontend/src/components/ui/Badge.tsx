import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'neutral' | 'bronze' | 'silver' | 'gold';
  size?: 'sm' | 'md';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  className,
  variant = 'neutral',
  size = 'md',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center font-medium rounded-full';

  const variantStyles = {
    primary: 'bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800/50',
    success: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50',
    warning: 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800/50',
    danger: 'bg-red-100 dark:bg-red-950/60 text-red-800 dark:text-red-300 border border-red-200 dark:border-red-800/50',
    info: 'bg-indigo-100 dark:bg-indigo-950/60 text-indigo-800 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800/50',
    neutral: 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700',
    bronze: 'bg-amber-900/10 text-amber-800 dark:text-amber-400 border border-amber-600/30',
    silver: 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-400/40',
    gold: 'bg-yellow-500/15 text-yellow-800 dark:text-yellow-400 border border-yellow-500/40',
  };

  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs',
  };

  return (
    <span className={twMerge(clsx(baseStyles, variantStyles[variant], sizeStyles[size], className))} {...props}>
      {children}
    </span>
  );
};
