import React, { useState } from 'react';
import { StationData, SimulationHorizon, ZoneType } from '../../types';
import { ConfidenceBadge, StateBadge } from '../common/Badges';
import {
  AlertTriangle,
  Clock,
  ArrowRight,
  ChevronRight,
  Filter,
  Activity,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';

interface Screen1LiveLineViewProps {
  stations: StationData[];
  onSelectStation: (stationId: string) => void;
  onSelectAlert: (alertId: string) => void;
  isLineStopped: boolean;
  isDegradedData: boolean;
}

export function Screen1LiveLineView({
  stations,
  onSelectStation,
  onSelectAlert,
  isLineStopped,
  isDegradedData,
}: Screen1LiveLineViewProps) {
  const [horizon, setHorizon] = useState<SimulationHorizon>('now');
  const [zoneFilter, setZoneFilter] = useState<'All' | ZoneType>('All');
  const [selectedStationHover, setSelectedStationHover] = useState<string | null>(null);

  // Group stations by Zone
  const zones: ZoneType[] = ['Body Shop', 'Paint Shop', 'Final Assembly'];

  // Determine current active state based on horizon
  const getDisplayState = (st: StationData) => {
    if (isLineStopped) return 'Down';
    if (horizon === 'now') return st.currentState;
    return st.simulatedState[horizon] || st.currentState;
  };

  // Find longest active period (Active Period Method - Bottleneck)
  const maxActivePeriodSec = Math.max(...stations.map((s) => s.activePeriodDurationSec));

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* 1. Prominent Headline Prediction Banner */}
      <Card className="border-amber-200 bg-amber-50/50 p-5 shadow-xs">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <Badge variant="warning" className="font-semibold">
                Primary Bottleneck Forecast
              </Badge>
              <span className="text-xs text-zinc-500 font-medium">
                Active Period Method (APM)
              </span>
            </div>
            <h2 className="text-lg lg:text-xl font-bold text-zinc-950 tracking-tight">
              Station 14 (E-Coat) — 73% likely to become the bottleneck by 14:20.
            </h2>
            <p className="text-xs text-zinc-600">
              Predicted 41 minutes before impact. Based on 200 simulations of the next 4 hours.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <div className="text-right bg-white rounded-lg border border-amber-200/80 px-3.5 py-2 shadow-2xs">
              <div className="text-[10px] uppercase font-semibold text-zinc-500">
                Time to Impact
              </div>
              <div className="text-2xl font-bold text-amber-800 tracking-tight font-sans">
                13 min
              </div>
            </div>

            <Button
              onClick={() => onSelectAlert('ALT-01')}
              className="gap-2 bg-zinc-900 text-white hover:bg-zinc-800 shadow-xs"
            >
              <span>View Alert & Advice</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>

      {/* 2. Simulation Timeline Controls & Zone Filters */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-200/80 pb-3">
        {/* Horizon Switcher */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase text-zinc-500 flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-zinc-400" />
            Line Horizon:
          </span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60">
            {(['now', '+1h', '+2h', '+4h'] as SimulationHorizon[]).map((h) => (
              <button
                key={h}
                type="button"
                onClick={() => setHorizon(h)}
                className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                  horizon === h
                    ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                    : 'text-zinc-600 hover:text-zinc-900'
                }`}
              >
                {h === 'now' ? 'Now (Real-time)' : `Predicted ${h}`}
              </button>
            ))}
          </div>
        </div>

        {/* Zone Filter */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase text-zinc-500 flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-zinc-400" />
            Zone:
          </span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60">
            {(['All', 'Body Shop', 'Paint Shop', 'Final Assembly'] as const).map((z) => (
              <button
                key={z}
                type="button"
                onClick={() => setZoneFilter(z)}
                className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                  zoneFilter === z
                    ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                    : 'text-zinc-600 hover:text-zinc-900'
                }`}
              >
                {z}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Degradation Warning Banner if simulated */}
      {isDegradedData && (
        <div className="rounded-lg border border-amber-300 bg-amber-50 p-3.5 text-xs text-amber-950 flex items-center gap-2.5 shadow-2xs">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <strong>Data Stream Degraded:</strong> OPC UA broker dropped on Paint Shop segment. Stations S-13 through S-22 running on cached soft-sensor telemetry. Last good sync: 14:02:18.
          </span>
        </div>
      )}

      {/* 3. All 42 Stations in Line Order Grouped by Zone */}
      <div className="space-y-8">
        {zones
          .filter((z) => zoneFilter === 'All' || zoneFilter === z)
          .map((zoneName) => {
            const zoneStations = stations.filter((s) => s.zone === zoneName);
            return (
              <div key={zoneName} className="space-y-3">
                <div className="flex items-center justify-between border-b border-zinc-200/80 pb-2">
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-semibold tracking-tight text-zinc-900">
                      {zoneName}
                    </h3>
                    <span className="text-xs text-zinc-500">
                      ({zoneStations[0].id} to {zoneStations[zoneStations.length - 1].id} · {zoneStations.length} Stations)
                    </span>
                  </div>
                  <div className="text-xs text-zinc-500 flex items-center gap-4">
                    <span>Takt: <strong className="text-zinc-700 font-mono">58s</strong></span>
                    <span>Target: <strong className="text-zinc-700 font-mono">62 JPH</strong></span>
                  </div>
                </div>

                {/* Stations Horizontal/Grid Flow */}
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-3.5">
                  {zoneStations.map((st) => {
                    const displayState = getDisplayState(st);
                    const isLongestActive = st.activePeriodDurationSec === maxActivePeriodSec;
                    const hasBottleneckAlert = st.bottleneckPrediction !== undefined;
                    const minutesActive = Math.floor(st.activePeriodDurationSec / 60);
                    const secondsActive = st.activePeriodDurationSec % 60;

                    return (
                      <Card
                        key={st.id}
                        onClick={() => onSelectStation(st.id)}
                        onMouseEnter={() => setSelectedStationHover(st.id)}
                        onMouseLeave={() => setSelectedStationHover(null)}
                        className={`p-3.5 cursor-pointer transition-all hover:shadow-md ${
                          hasBottleneckAlert
                            ? 'border-amber-400 bg-amber-50/40 ring-1 ring-amber-400/50'
                            : isLongestActive
                            ? 'border-zinc-300 bg-zinc-50/60'
                            : 'border-zinc-200/80 bg-white hover:border-zinc-300'
                        }`}
                      >
                        {/* Header: ID, Name, Confidence */}
                        <div className="flex items-start justify-between gap-1 mb-2">
                          <div className="truncate">
                            <div className="text-xs font-semibold text-zinc-950 flex items-center gap-1.5">
                              <span className="font-mono">{st.id}</span>
                              <span className="text-zinc-300">·</span>
                              <span className="truncate max-w-[120px]" title={st.name}>
                                {st.name}
                              </span>
                            </div>
                          </div>
                          <ConfidenceBadge tier={st.confidence} showLabel={false} />
                        </div>

                        {/* State & Bottleneck tag */}
                        <div className="flex items-center justify-between gap-1 mb-3">
                          <StateBadge state={displayState} />
                          {hasBottleneckAlert && (
                            <Badge variant="warning" className="text-[10px] px-1.5 py-0 font-semibold font-mono">
                              {st.bottleneckPrediction?.probabilityPct}% @ {st.bottleneckPrediction?.timeStr}
                            </Badge>
                          )}
                        </div>

                        {/* Telemetry Metrics */}
                        <div className="space-y-1.5 text-xs text-zinc-600 border-t border-zinc-100 pt-2.5">
                          <div className="flex items-center justify-between">
                            <span className="text-zinc-500">Cycle vs Takt:</span>
                            <span
                              className={`font-mono text-[11px] font-medium ${
                                st.cycleTimeSec > st.taktTimeSec
                                  ? 'text-amber-700 font-semibold'
                                  : 'text-zinc-900'
                              }`}
                            >
                              {st.cycleTimeSec}s / {st.taktTimeSec}s
                            </span>
                          </div>

                          <div className="flex items-center justify-between">
                            <span className="text-zinc-500">Active Period:</span>
                            <span
                              className={`font-mono text-[11px] font-medium ${
                                isLongestActive
                                  ? 'text-amber-800 font-bold'
                                  : 'text-zinc-900'
                              }`}
                            >
                              {minutesActive}m {secondsActive}s
                            </span>
                          </div>

                          <div className="flex items-center justify-between">
                            <span className="text-zinc-500">Buffer Right:</span>
                            <div className="flex items-center gap-1.5">
                              <span className="font-mono text-[11px] font-medium text-zinc-900">
                                {st.bufferRight.current}/{st.bufferRight.max}
                              </span>
                              <div className="w-10 h-1.5 bg-zinc-100 rounded-full overflow-hidden">
                                <div
                                  className={`h-full rounded-full ${
                                    st.bufferRight.current / st.bufferRight.max >= 0.8
                                      ? 'bg-amber-500'
                                      : 'bg-emerald-500'
                                  }`}
                                  style={{
                                    width: `${Math.min(
                                      100,
                                      (st.bufferRight.current / st.bufferRight.max) * 100
                                    )}%`,
                                  }}
                                />
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Station vintage or soft sensor indicator */}
                        <div className="mt-2.5 pt-2 border-t border-zinc-100 flex items-center justify-between text-[11px] text-zinc-400">
                          <span className="truncate max-w-[110px]">{st.equipmentVintage}</span>
                          <span className="text-zinc-600 hover:text-zinc-950 flex items-center gap-0.5 font-medium">
                            Details <ChevronRight className="w-3 h-3" />
                          </span>
                        </div>
                      </Card>
                    );
                  })}
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
}

