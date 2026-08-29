import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link' | 'subtle';
  size?: 'default' | 'sm' | 'lg' | 'icon' | 'xs';
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    const baseStyles =
      'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer select-none';

    const variants = {
      default: 'bg-zinc-900 text-zinc-50 hover:bg-zinc-800 shadow-sm active:scale-[0.98]',
      destructive: 'bg-rose-600 text-white hover:bg-rose-700 shadow-sm active:scale-[0.98]',
      outline: 'border border-zinc-200 bg-white text-zinc-900 hover:bg-zinc-100 hover:text-zinc-900 shadow-xs active:scale-[0.98]',
      secondary: 'bg-zinc-100 text-zinc-900 hover:bg-zinc-200 shadow-xs active:scale-[0.98]',
      ghost: 'text-zinc-700 hover:bg-zinc-100 hover:text-zinc-900',
      link: 'text-zinc-900 underline-offset-4 hover:underline p-0 h-auto',
      subtle: 'bg-zinc-50 text-zinc-700 hover:bg-zinc-100 border border-zinc-200/80',
    };

    const sizes = {
      default: 'h-9 px-4 py-2',
      xs: 'h-7 px-2.5 text-xs rounded',
      sm: 'h-8 rounded-md px-3 text-xs',
      lg: 'h-10 rounded-md px-6 text-base',
      icon: 'h-9 w-9 p-0',
    };

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button };
