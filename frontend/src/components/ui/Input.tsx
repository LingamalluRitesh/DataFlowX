import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  leftIcon,
  className = '',
  id,
  ...props
}) => {
  return (
    <div className="w-full space-y-1.5">
      {label && (
        <label htmlFor={id} className="block text-xs font-semibold uppercase text-slate-300">
          {label}
        </label>
      )}
      <div className="relative">
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            {leftIcon}
          </div>
        )}
        <input
          id={id}
          className={`w-full bg-slate-950 border rounded-lg px-3.5 py-2 text-sm text-white placeholder-slate-500 focus:outline-none transition ${
            leftIcon ? 'pl-9' : ''
          } ${
            error
              ? 'border-red-500 focus:border-red-400'
              : 'border-slate-800 focus:border-cyan-500'
          } ${className}`}
          {...props}
        />
      </div>
      {error && <p className="text-xs text-red-400 font-medium">{error}</p>}
      {helperText && !error && <p className="text-[11px] text-slate-500">{helperText}</p>}
    </div>
  );
};
