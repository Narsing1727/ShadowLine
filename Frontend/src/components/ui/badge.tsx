import * as React from 'react';
import { cn } from '../../lib/utils';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
  className?: string;
  title?: string;
  variant?:
    | 'default'
    | 'secondary'
    | 'destructive'
    | 'outline'
    | 'success'
    | 'warning'
    | 'amber'
    | 'indigo'
    | 'zinc';
}

function Badge({ className, variant = 'default', children, ...props }: BadgeProps) {
  const variants = {
    default: 'border-transparent bg-zinc-900 text-zinc-50 shadow-xs',
    secondary: 'border-transparent bg-zinc-100 text-zinc-900 hover:bg-zinc-200/80',
    destructive:
      'border-rose-200 bg-rose-50 text-rose-700 hover:bg-rose-100',
    outline: 'text-zinc-950 border-zinc-200 bg-white',
    success:
      'border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100',
    warning:
      'border-amber-200 bg-amber-50 text-amber-800 hover:bg-amber-100',
    amber:
      'border-amber-200 bg-amber-50 text-amber-800 hover:bg-amber-100',
    indigo:
      'border-indigo-200 bg-indigo-50 text-indigo-700 hover:bg-indigo-100',
    zinc: 'border-zinc-200 bg-zinc-50 text-zinc-600',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-950 focus:ring-offset-2',
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export { Badge };

