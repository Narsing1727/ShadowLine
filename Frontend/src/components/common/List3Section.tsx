import React from 'react';
import { Card } from '../ui/card';

export interface List3Item {
  col1: string; // e.g. Timestamp / Date / Station
  col2: string; // e.g. Title / Action / Anomaly
  col3: string; // e.g. System / Tool / Operator / Location
  badge?: React.ReactNode;
}

interface List3SectionProps {
  sectionTitle: string;
  items: List3Item[];
  className?: string;
  col1Header?: string;
  col2Header?: string;
  col3Header?: string;
}

export function List3Section({
  sectionTitle,
  items,
  className = '',
  col1Header,
  col2Header,
  col3Header,
}: List3SectionProps) {
  return (
    <Card className={`p-4 space-y-3 ${className}`}>
      <h3 className="text-sm font-semibold tracking-tight text-zinc-900">
        {sectionTitle}
      </h3>

      <div className="space-y-0 divide-y divide-zinc-100 rounded-lg border border-zinc-200/70 overflow-hidden bg-white">
        {(col1Header || col2Header || col3Header) && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 py-2 px-3 text-[11px] uppercase font-semibold text-zinc-500 bg-zinc-50/80">
            <div>{col1Header}</div>
            <div>{col2Header}</div>
            <div className="text-right sm:text-left">{col3Header}</div>
          </div>
        )}

        {items.map((item, idx) => (
          <div
            key={idx}
            className="grid grid-cols-1 sm:grid-cols-3 gap-2 py-2.5 px-3 text-xs transition-colors hover:bg-zinc-50/70"
          >
            <div className="text-zinc-500 font-mono text-[11px] flex items-center gap-2">
              <span>{item.col1}</span>
              {item.badge}
            </div>
            <div className="text-zinc-900 font-medium">
              {item.col2}
            </div>
            <div className="text-zinc-600 text-right sm:text-left">
              {item.col3}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

