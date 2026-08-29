import React from 'react';
import { StationData } from '../../types';
import { ConfidenceBadge, StateBadge } from '../common/Badges';
import { StatsCard6 } from '../common/StatsCard6';
import { ChartCard25 } from '../common/ChartCard25';
import { List3Section } from '../common/List3Section';
import {
  ChevronLeft,
  ChevronRight,
  Wrench,
  EyeOff,
  Cpu,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';

interface Screen4StationDetailProps {
  stations: StationData[];
  selectedStationId: string;
  onSelectStation: (stationId: string) => void;
}

export function Screen4StationDetail({
  stations,
  selectedStationId,
  onSelectStation,
}: Screen4StationDetailProps) {
  const station = stations.find((s) => s.id === selectedStationId) || stations[13]; // S-14 default

  const currentIndex = stations.findIndex((s) => s.id === station.id);
  const prevStation = stations[currentIndex > 0 ? currentIndex - 1 : stations.length - 1];
  const nextStation = stations[currentIndex < stations.length - 1 ? currentIndex + 1 : 0];

  // Simulated 2-hour cycle time trend data for the 3 variants
  const cycleTimeTrendData = [
    { name: '12:10', 'SUV-A': station.cycleTimesByVariant['SUV-A'] - 1, 'Sedan-B': station.cycleTimesByVariant['Sedan-B'] - 1, 'EV-C': station.cycleTimesByVariant['EV-C'], value: station.cycleTimeSec - 2 },
    { name: '12:30', 'SUV-A': station.cycleTimesByVariant['SUV-A'] + 1, 'Sedan-B': station.cycleTimesByVariant['Sedan-B'], 'EV-C': station.cycleTimesByVariant['EV-C'] + 1, value: station.cycleTimeSec - 1 },
    { name: '12:50', 'SUV-A': station.cycleTimesByVariant['SUV-A'], 'Sedan-B': station.cycleTimesByVariant['Sedan-B'] - 1, 'EV-C': station.cycleTimesByVariant['EV-C'] - 1, value: station.cycleTimeSec },
    { name: '13:10', 'SUV-A': station.cycleTimesByVariant['SUV-A'] + 2, 'Sedan-B': station.cycleTimesByVariant['Sedan-B'] + 1, 'EV-C': station.cycleTimesByVariant['EV-C'] + 2, value: station.cycleTimeSec + 1 },
    { name: '13:30', 'SUV-A': station.cycleTimesByVariant['SUV-A'] + 1, 'Sedan-B': station.cycleTimesByVariant['Sedan-B'], 'EV-C': station.cycleTimesByVariant['EV-C'] + 1, value: station.cycleTimeSec + 2 },
    { name: '13:50', 'SUV-A': station.cycleTimesByVariant['SUV-A'] + 3, 'Sedan-B': station.cycleTimesByVariant['Sedan-B'] + 2, 'EV-C': station.cycleTimesByVariant['EV-C'] + 2, value: station.cycleTimeSec + 1 },
    { name: '14:05', 'SUV-A': station.cycleTimesByVariant['SUV-A'], 'Sedan-B': station.cycleTimesByVariant['Sedan-B'], 'EV-C': station.cycleTimesByVariant['EV-C'], value: station.cycleTimeSec },
  ];

  // VIN list formatting for List3Section
  const vinHistoryItems = station.lastVins.map((vin, i) => ({
    col1: `14:${String(5 - i).padStart(2, '0')}:20`,
    col2: vin,
    col3: i % 3 === 0 ? 'SUV-A' : i % 3 === 1 ? 'Sedan-B' : 'EV-C',
  }));

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Station Selector Bar & Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-zinc-200/80 pb-3">
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onSelectStation(prevStation.id)}
            className="gap-1"
            title={`Previous Station: ${prevStation.id}`}
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Prev ({prevStation.id})</span>
          </Button>

          {/* Direct Station Quick Dropdown */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase text-zinc-500">Jump to:</span>
            <select
              value={station.id}
              onChange={(e) => onSelectStation(e.target.value)}
              className="px-2.5 py-1 text-xs font-medium rounded-md border border-zinc-200 bg-white text-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
            >
              {stations.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.id} — {s.name} ({s.zone})
                </option>
              ))}
            </select>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => onSelectStation(nextStation.id)}
            className="gap-1"
            title={`Next Station: ${nextStation.id}`}
          >
            <span>Next ({nextStation.id})</span>
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>

        <div className="text-xs text-zinc-500">
          Position: <strong className="text-zinc-900 font-mono">#{station.number}</strong> of 42 on Plant 2 Line A
        </div>
      </div>

      {/* Main Station Header Hero */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2.5">
              <span className="text-2xl font-black text-zinc-950 font-mono">
                {station.id}
              </span>
              <span className="text-2xl font-bold text-zinc-800 tracking-tight">
                {station.name}
              </span>
              <ConfidenceBadge tier={station.confidence} />
              <StateBadge state={station.currentState} />
            </div>
            <div className="text-xs text-zinc-600 flex flex-wrap items-center gap-3">
              <span>Zone: <strong className="text-zinc-900">{station.zone}</strong></span>
              <span className="text-zinc-300">·</span>
              <span>Equipment: <strong className="text-zinc-900">{station.equipmentVintage}</strong></span>
              <span className="text-zinc-300">·</span>
              <span>Units Processed Shift: <strong className="text-zinc-900 font-mono">{station.unitsProcessedThisShift}</strong></span>
            </div>
          </div>

          {/* Maintenance window pill */}
          <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-3 text-right text-xs shrink-0">
            <div className="text-[10px] uppercase font-semibold text-zinc-400 flex items-center justify-end gap-1">
              <Wrench className="w-3 h-3 text-zinc-400" />
              Next Scheduled Maintenance
            </div>
            <div className="text-sm font-semibold text-zinc-900 mt-0.5">
              {station.nextMaintenanceWindow || '14 Nov 2026'}
            </div>
          </div>
        </div>

        {/* Confidence Explanation Banner */}
        {station.confidence === 'Inferred' && (
          <div className="mt-4 p-3 rounded-md bg-amber-50 border border-amber-200 text-xs text-amber-950 flex items-start gap-2">
            <Cpu className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <strong>Soft Sensor Telemetry:</strong> {station.inferredSource}
            </div>
          </div>
        )}

        {station.confidence === 'Dark' && (
          <div className="mt-4 p-3 rounded-md bg-rose-50 border border-rose-200 text-xs text-rose-950 space-y-1">
            <div className="flex items-center gap-2 font-semibold uppercase">
              <EyeOff className="w-4 h-4 text-rose-700 shrink-0" />
              <span>Dark Station — No Telemetry Sensor</span>
            </div>
            <p className="text-zinc-800">{station.darkReason}</p>
            <div className="pt-1 text-[11px] text-zinc-700">
              <strong>Upgrade Pathway:</strong> {station.darkUpgradeSignal} (Estimated cost: {station.darkUpgradeCost})
            </div>
          </div>
        )}
      </Card>

      {/* Grid: Shift Breakdown, Buffers, Variant Offsets */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* StatsCard 6: Shift State Breakdown */}
        <StatsCard6
          title="Shift State Distribution"
          totalValue={`${station.shiftStateBreakdown.activePct}% Active`}
          subtitle="Proportion of shift time spent in each state"
          breakdown={[
            { label: 'Active (Processing)', value: `${station.shiftStateBreakdown.activePct}%`, colorClass: 'bg-emerald-500' },
            { label: 'Blocked (Downstream Full)', value: `${station.shiftStateBreakdown.blockedPct}%`, colorClass: 'bg-amber-500' },
            { label: 'Starved (Upstream Empty)', value: `${station.shiftStateBreakdown.starvedPct}%`, colorClass: 'bg-sky-500' },
            { label: 'Down (Fault/Stop)', value: `${station.shiftStateBreakdown.downPct}%`, colorClass: 'bg-rose-500' },
          ]}
        />

        {/* StatsCard 6: Buffers & Active Period Duration */}
        <StatsCard6
          title="Buffer Levels & APM Metric"
          totalValue={`${Math.floor(station.activePeriodDurationSec / 60)}m ${station.activePeriodDurationSec % 60}s`}
          subtitle="Longest uninterrupted active period duration"
          breakdown={[
            { label: 'Upstream Inflow Buffer', value: `${station.bufferLeft?.current || 4} / ${station.bufferLeft?.max || 10}`, colorClass: 'bg-indigo-500' },
            { label: 'Downstream Outflow Buffer', value: `${station.bufferRight.current} / ${station.bufferRight.max}`, colorClass: 'bg-indigo-700' },
            { label: 'Historical Defects Caused', value: station.historicalDefectsCausedCount, colorClass: 'bg-rose-500' },
          ]}
        />

        {/* StatsCard 6: Cycle Time Per Variant */}
        <StatsCard6
          title="Cycle Times By Variant"
          totalValue={`${station.cycleTimeSec}s Actual`}
          subtitle={`Design Takt: ${station.taktTimeSec}s Target`}
          breakdown={[
            { label: 'SUV-A Cycle Time', value: `${station.cycleTimesByVariant['SUV-A']} s`, percentage: `${station.cycleTimesByVariant['SUV-A'] > station.taktTimeSec ? '+' : ''}${station.cycleTimesByVariant['SUV-A'] - station.taktTimeSec}s takt`, colorClass: 'bg-amber-500' },
            { label: 'Sedan-B Cycle Time', value: `${station.cycleTimesByVariant['Sedan-B']} s`, percentage: `${station.cycleTimesByVariant['Sedan-B'] - station.taktTimeSec}s takt`, colorClass: 'bg-emerald-500' },
            { label: 'EV-C Cycle Time', value: `${station.cycleTimesByVariant['EV-C']} s`, percentage: `${station.cycleTimesByVariant['EV-C'] > station.taktTimeSec ? '+' : ''}${station.cycleTimesByVariant['EV-C'] - station.taktTimeSec}s takt`, colorClass: 'bg-purple-500' },
          ]}
        />
      </div>

      {/* ChartCard25: 2-Hour Cycle Time Trend with Takt Reference Line */}
      <ChartCard25
        title="2-Hour Cycle Time Drift with Takt Benchmark"
        subtitle="Tracking actual unit cycle durations vs 58s line takt target benchmark"
        data={cycleTimeTrendData}
        dataKey="value"
        targetValue={station.taktTimeSec}
        targetLabel="Takt Target (58s)"
        unit="s"
        height={260}
      />

      {/* List3Section: Last 10 VINs Processed */}
      <List3Section
        sectionTitle={`Recent VIN Genealogy Trail (${station.id} ${station.name})`}
        items={vinHistoryItems}
        col1Header="Exit Timestamp"
        col2Header="Vehicle Identification Number (VIN)"
        col3Header="Vehicle Variant"
      />
    </div>
  );
}

