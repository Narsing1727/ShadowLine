import React, { useState } from 'react';
import { StationData } from '../../types';
import { StatsCard6 } from '../common/StatsCard6';
import { DataTable6, Column } from '../common/DataTable6';
import {
  History,
  Clock,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';

interface Screen5BottleneckHistoryProps {
  stations: StationData[];
  onSelectStation: (stationId: string) => void;
}

interface BottleneckRecord {
  id: string;
  stationId: string;
  stationName: string;
  zone: string;
  primaryTimeMin: number;
  secondaryTimeMin: number;
  totalTimeMin: number;
  shiftSharePct: number;
  predictedVsActualMatchPct: number;
  triggerCause: string;
}

export function Screen5BottleneckHistory({
  stations,
  onSelectStation,
}: Screen5BottleneckHistoryProps) {
  const [timeRange, setTimeRange] = useState<'Shift B (Today)' | 'This Week' | 'Last 30 Days'>('Shift B (Today)');

  // Timeline representation of shifting bottleneck during Shift B (06:00 to 14:00)
  const timelineSegments = [
    { start: '06:00', end: '07:45', stationId: 'S-09', stationName: 'Hemming', zone: 'Body Shop', color: 'bg-amber-600' },
    { start: '07:45', end: '09:20', stationId: 'S-30', stationName: 'Engine Drop', zone: 'Final Assembly', color: 'bg-indigo-600' },
    { start: '09:20', end: '11:15', stationId: 'S-14', stationName: 'E-Coat', zone: 'Paint Shop', color: 'bg-rose-600' },
    { start: '11:15', end: '12:30', stationId: 'S-28', stationName: 'Door Line', zone: 'Final Assembly', color: 'bg-purple-600' },
    { start: '12:30', end: '14:00', stationId: 'S-14', stationName: 'E-Coat', zone: 'Paint Shop', color: 'bg-rose-600' },
  ];

  const bottleneckRanking: BottleneckRecord[] = [
    {
      id: 'BR-01',
      stationId: 'S-14',
      stationName: 'E-Coat',
      zone: 'Paint Shop',
      primaryTimeMin: 145,
      secondaryTimeMin: 40,
      totalTimeMin: 185,
      shiftSharePct: 38.5,
      predictedVsActualMatchPct: 88,
      triggerCause: 'Thermal bath dwell variation & SUV-A batching',
    },
    {
      id: 'BR-02',
      stationId: 'S-09',
      stationName: 'Hemming',
      zone: 'Body Shop',
      primaryTimeMin: 105,
      secondaryTimeMin: 35,
      totalTimeMin: 140,
      shiftSharePct: 29.1,
      predictedVsActualMatchPct: 79,
      triggerCause: 'Flange roller head wear & clamp reposition latency',
    },
    {
      id: 'BR-03',
      stationId: 'S-30',
      stationName: 'Engine Drop',
      zone: 'Final Assembly',
      primaryTimeMin: 95,
      secondaryTimeMin: 50,
      totalTimeMin: 145,
      shiftSharePct: 30.2,
      predictedVsActualMatchPct: 84,
      triggerCause: 'Nutrunner torque drift & powertrain alignment',
    },
    {
      id: 'BR-04',
      stationId: 'S-28',
      stationName: 'Door Line',
      zone: 'Final Assembly',
      primaryTimeMin: 75,
      secondaryTimeMin: 20,
      totalTimeMin: 95,
      shiftSharePct: 19.8,
      predictedVsActualMatchPct: 73,
      triggerCause: 'Sub-assembly carrier transfer buffering',
    },
    {
      id: 'BR-05',
      stationId: 'S-35',
      stationName: 'Battery Install',
      zone: 'Final Assembly',
      primaryTimeMin: 40,
      secondaryTimeMin: 30,
      totalTimeMin: 70,
      shiftSharePct: 14.5,
      predictedVsActualMatchPct: 82,
      triggerCause: 'EV-C heavy pack hoist alignment',
    },
  ];

  const columns: Column<BottleneckRecord>[] = [
    {
      key: 'stationId',
      header: 'Station',
      width: '180px',
      render: (r) => (
        <button
          type="button"
          onClick={() => onSelectStation(r.stationId)}
          className="text-left font-semibold text-zinc-900 hover:text-amber-700 underline cursor-pointer"
        >
          {r.stationId} {r.stationName}
        </button>
      ),
    },
    {
      key: 'zone',
      header: 'Zone',
      width: '140px',
    },
    {
      key: 'primaryTimeMin',
      header: 'Primary Bottleneck',
      align: 'right',
      width: '150px',
      render: (r) => <span className="font-semibold text-zinc-900 font-mono">{r.primaryTimeMin} min</span>,
    },
    {
      key: 'secondaryTimeMin',
      header: 'Secondary Bottleneck',
      align: 'right',
      width: '160px',
      render: (r) => <span className="text-zinc-500 font-mono">{r.secondaryTimeMin} min</span>,
    },
    {
      key: 'shiftSharePct',
      header: 'Shift Share',
      align: 'right',
      width: '120px',
      render: (r) => (
        <span className="font-semibold text-amber-800 font-mono">{r.shiftSharePct}%</span>
      ),
    },
    {
      key: 'predictedVsActualMatchPct',
      header: 'Forecast Accuracy',
      align: 'right',
      width: '150px',
      render: (r) => (
        <Badge variant="success">
          {r.predictedVsActualMatchPct}% match
        </Badge>
      ),
    },
    {
      key: 'triggerCause',
      header: 'Identified Root Dynamics',
      render: (r) => <span className="text-xs text-zinc-700">{r.triggerCause}</span>,
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Header & Concept Callout */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <History className="w-3.5 h-3.5 text-amber-600" />
              <span>Dynamic APM Analysis</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Shifting Bottleneck History
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Bottlenecks on mixed-model lines are dynamic and shift continuously between stations based on variant mix, active periods, and micro-buffer oscillations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase text-zinc-500">Period:</span>
            <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60 text-xs">
              {(['Shift B (Today)', 'This Week', 'Last 30 Days'] as const).map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setTimeRange(t)}
                  className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                    timeRange === t
                      ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                      : 'text-zinc-600 hover:text-zinc-900'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* Shifting Bottleneck Timeline across Shift */}
      <Card className="p-5 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-amber-600" />
            Shift B Bottleneck Migration Timeline (06:00 – 14:00)
          </h3>
          <span className="text-xs text-zinc-500 font-medium">
            Active Period Method (APM) Log
          </span>
        </div>

        {/* Timeline Bar */}
        <div className="w-full h-10 flex rounded-md overflow-hidden text-xs text-white font-semibold">
          {timelineSegments.map((seg, idx) => (
            <div
              key={idx}
              className={`${seg.color} flex flex-col justify-center px-2.5 border-r border-white/20 truncate transition-all hover:opacity-90 cursor-pointer`}
              style={{ width: `${(idx === 0 || idx === 4 ? 22 : 18.5)}%` }}
              title={`${seg.stationId} ${seg.stationName} (${seg.start} - ${seg.end})`}
              onClick={() => onSelectStation(seg.stationId)}
            >
              <div className="text-[11px] truncate uppercase">{seg.stationId} {seg.stationName}</div>
              <div className="text-[9px] opacity-80">{seg.start}–{seg.end}</div>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-between text-[11px] text-zinc-400 pt-1 font-mono">
          <span>06:00 Shift Start</span>
          <span>08:00</span>
          <span>10:00 Break</span>
          <span>12:00 Lunch</span>
          <span>14:00 Current Time</span>
        </div>
      </Card>

      {/* Top 3 Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard6
          title="Primary Bottleneck Station"
          totalValue="S-14 E-Coat"
          subtitle="38.5% of shift (145 total active minutes)"
          breakdown={[
            { label: 'Time as Primary Bottleneck', value: '145 min', percentage: '38.5%', colorClass: 'bg-rose-500' },
            { label: 'Time as Secondary Bottleneck', value: '40 min', percentage: '10.4%', colorClass: 'bg-amber-500' },
            { label: 'Average Active Duration', value: '12m 40s', colorClass: 'bg-indigo-500' },
          ]}
        />

        <StatsCard6
          title="Bottleneck Shifts Observed"
          totalValue="4 Shifts"
          subtitle="Frequency of primary constraint migration"
          breakdown={[
            { label: 'Body Shop (S-09)', value: '105 min', percentage: '29.1%', colorClass: 'bg-amber-500' },
            { label: 'Paint Shop (S-14)', value: '145 min', percentage: '38.5%', colorClass: 'bg-rose-500' },
            { label: 'Final Assembly (S-30, S-28)', value: '170 min', percentage: '32.4%', colorClass: 'bg-indigo-500' },
          ]}
        />

        <StatsCard6
          title="Prediction Accuracy"
          totalValue="82.4% Match"
          subtitle="Predicted constraint vs actual longest APM"
          breakdown={[
            { label: 'Predicted on Schedule', value: '28 / 34 events', colorClass: 'bg-emerald-500' },
            { label: 'Mean Lead Warning Time', value: '37 min before', colorClass: 'bg-sky-500' },
            { label: 'Secondary Drift Accuracy', value: '76.8%', colorClass: 'bg-purple-500' },
          ]}
        />
      </div>

      {/* Ranked Bottleneck Table */}
      <DataTable6
        title="Ranked Station Bottleneck Log (Shift B)"
        description="Cumulative time spent as primary vs secondary constraint on the line, with root dynamic triggers identified by ShadowLine simulations."
        data={bottleneckRanking}
        columns={columns}
        keyExtractor={(r) => r.id}
      />
    </div>
  );
}

