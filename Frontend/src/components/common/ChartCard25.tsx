import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';

interface ChartCard25Props {
  title: string;
  subtitle?: string;
  data: Array<{ name: string; value: number; [key: string]: any }>;
  dataKey?: string;
  targetValue?: number;
  targetLabel?: string;
  unit?: string;
  height?: number;
  gradientFrom?: string;
  gradientTo?: string;
  strokeColor?: string;
  className?: string;
}

export function ChartCard25({
  title,
  subtitle,
  data,
  dataKey = 'value',
  targetValue,
  targetLabel = 'Target',
  unit = '',
  height = 240,
  gradientFrom = '#0284c7',
  gradientTo = '#bae6fd',
  strokeColor = '#0284c7',
  className = '',
}: ChartCard25Props) {
  const gradientId = `areaGrad-${title.replace(/\s+/g, '-').toLowerCase()}`;

  return (
    <Card className={`p-5 ${className}`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h4 className="text-sm font-semibold tracking-tight text-zinc-900">
            {title}
          </h4>
          {subtitle && (
            <p className="text-xs text-zinc-500 mt-0.5">{subtitle}</p>
          )}
        </div>
        {targetValue !== undefined && (
          <Badge variant="secondary" className="gap-1.5 font-normal">
            <span className="w-2 h-0.5 bg-zinc-600 border-b border-dashed border-zinc-600" />
            <span>{targetLabel}:</span>
            <span className="font-semibold text-zinc-900">
              {targetValue} {unit}
            </span>
          </Badge>
        )}
      </div>

      <div style={{ width: '100%', height }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 35, left: -20, bottom: 0 }}
          >
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={gradientFrom} stopOpacity={0.25} />
                <stop offset="95%" stopColor={gradientTo} stopOpacity={0.01} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis
              dataKey="name"
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <YAxis
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: '#e2e8f0' }}
              domain={['auto', 'auto']}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#ffffff',
                borderColor: '#e2e8f0',
                borderRadius: '8px',
                fontSize: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.07)',
              }}
              formatter={(val: any) => [`${val} ${unit}`, 'Actual']}
            />
            {targetValue !== undefined && (
              <ReferenceLine
                y={targetValue}
                stroke="#64748b"
                strokeDasharray="4 4"
                strokeWidth={1.5}
                label={{
                  value: targetLabel,
                  position: 'right',
                  fill: '#64748b',
                  fontSize: 11,
                }}
              />
            )}
            <Area
              type="monotone"
              dataKey={dataKey}
              stroke={strokeColor}
              strokeWidth={2}
              fillOpacity={1}
              fill={`url(#${gradientId})`}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

