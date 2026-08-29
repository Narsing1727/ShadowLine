import React from 'react';
import { Card } from '../ui/card';

export interface BreakdownItem {
  label: string;
  value: string | number;
  percentage?: number | string;
  colorClass: string;
}

interface StatsCard6Props {
  title: string;
  totalValue: string | number;
  subtitle?: string;
  breakdown: BreakdownItem[];
  className?: string;
}

export function StatsCard6({
  title,
  totalValue,
  subtitle,
  breakdown,
  className = '',
}: StatsCard6Props) {
  return (
    <Card className={`p-5 transition-shadow hover:shadow-md ${className}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
            {title}
          </p>
          <div className="text-2xl font-bold tracking-tight text-zinc-950 mt-1 font-sans">
            {totalValue}
          </div>
          {subtitle && (
            <p className="text-xs text-zinc-500 mt-0.5">{subtitle}</p>
          )}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-zinc-100 space-y-2">
        {breakdown.map((item, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between text-xs text-zinc-700"
          >
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full shrink-0 ${item.colorClass}`} />
              <span className="text-zinc-600 font-medium">{item.label}</span>
            </div>
            <div className="flex items-center gap-1.5 font-mono text-[11px]">
              <span className="font-semibold text-zinc-900">{item.value}</span>
              {item.percentage !== undefined && (
                <span className="text-zinc-400 font-normal">
                  ({typeof item.percentage === 'number'
                    ? `${item.percentage}%`
                    : item.percentage})
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

