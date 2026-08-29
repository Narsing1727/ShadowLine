import React, { useState } from 'react';
import { StationData, ConfidenceTier, ZoneType } from '../../types';
import { ConfidenceBadge } from '../common/Badges';
import { StatsCard6 } from '../common/StatsCard6';
import { DataTable6, Column } from '../common/DataTable6';
import {
  Network,
  ShieldCheck,
} from 'lucide-react';
import { Card } from '../ui/card';

interface Screen7SensorCoverageProps {
  stations: StationData[];
  onSelectStation: (stationId: string) => void;
}

export function Screen7SensorCoverage({
  stations,
  onSelectStation,
}: Screen7SensorCoverageProps) {
  const [tierFilter, setTierFilter] = useState<'All' | ConfidenceTier>('All');
  const [zoneFilter, setZoneFilter] = useState<'All' | ZoneType>('All');

  const measuredCount = stations.filter((s) => s.confidence === 'Measured').length; // 27
  const inferredCount = stations.filter((s) => s.confidence === 'Inferred').length; // 11
  const darkCount = stations.filter((s) => s.confidence === 'Dark').length;         // 4
  const totalStations = stations.length; // 42

  const measuredPct = ((measuredCount / totalStations) * 100).toFixed(1);
  const inferredPct = ((inferredCount / totalStations) * 100).toFixed(1);
  const darkPct = ((darkCount / totalStations) * 100).toFixed(1);

  const filteredStations = stations.filter((s) => {
    if (tierFilter !== 'All' && s.confidence !== tierFilter) return false;
    if (zoneFilter !== 'All' && s.zone !== zoneFilter) return false;
    return true;
  });

  const columns: Column<StationData>[] = [
    {
      key: 'id',
      header: 'Station',
      width: '180px',
      render: (s) => (
        <button
          type="button"
          onClick={() => onSelectStation(s.id)}
          className="text-left font-semibold text-zinc-900 hover:text-amber-700 underline cursor-pointer"
        >
          {s.id} {s.name}
        </button>
      ),
    },
    {
      key: 'zone',
      header: 'Zone',
      width: '140px',
    },
    {
      key: 'confidence',
      header: 'Coverage Tier',
      width: '140px',
      render: (s) => <ConfidenceBadge tier={s.confidence} />,
    },
    {
      key: 'equipmentVintage',
      header: 'Vintage / Type',
      width: '180px',
      render: (s) => <span className="text-zinc-600">{s.equipmentVintage}</span>,
    },
    {
      key: 'telemetryDetails',
      header: 'Sensor Architecture & Soft-Model Inputs',
      render: (s) => {
        if (s.confidence === 'Measured') {
          return (
            <span className="text-xs text-zinc-600">
              Direct PLC bus telemetry (99.4% sensor precision). Takt pulse & cycle dwell recorded.
            </span>
          );
        }
        if (s.confidence === 'Inferred') {
          return (
            <span className="text-xs text-amber-900 font-medium">
              {s.inferredSource}
            </span>
          );
        }
        return (
          <span className="text-xs text-rose-900 font-medium">
            Dark Station: {s.darkReason}
          </span>
        );
      },
    },
    {
      key: 'upgradePlan',
      header: 'Next Maintenance / Upgrade',
      width: '220px',
      render: (s) => {
        if (s.confidence === 'Dark') {
          return (
            <div className="text-[11px]">
              <div className="text-rose-900 font-bold font-mono">{s.darkUpgradeCost}</div>
              <div className="text-zinc-400">Window: {s.nextMaintenanceWindow}</div>
            </div>
          );
        }
        return (
          <span className="text-zinc-500 text-[11px]">
            Window: {s.nextMaintenanceWindow || 'Routine'}
          </span>
        );
      },
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <Network className="w-3.5 h-3.5 text-indigo-600" />
              <span>Heterogeneous Instrumentation Topology</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Sensor Coverage Map (42 Stations)
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Factory lines mix modern instrumented machines with legacy automation and manual workstations. ShadowLine never assumes full sensor instrumentation.
            </p>
          </div>

          {/* Graceful Degradation Assurance */}
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 max-w-md text-xs text-emerald-950 flex items-start gap-2.5">
            <ShieldCheck className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold">Graceful Degradation:</strong> ShadowLine is designed from the ground up to operate reliably on incomplete telemetry. When a sensor drops, virtual soft-sensor models step in rather than failing.
            </div>
          </div>
        </div>
      </Card>

      {/* 3 Metric Cards for Coverage Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard6
          title="Measured Stations (Direct Sensors)"
          totalValue={`${measuredCount} of ${totalStations}`}
          subtitle={`${measuredPct}% of total assembly line`}
          breakdown={[
            { label: 'Body Shop Instrumented', value: '10 stations', colorClass: 'bg-emerald-500' },
            { label: 'Paint Shop Instrumented', value: '7 stations', colorClass: 'bg-emerald-600' },
            { label: 'Final Assembly Instrumented', value: '10 stations', colorClass: 'bg-emerald-700' },
          ]}
        />

        <StatsCard6
          title="Inferred Stations (Soft / Virtual)"
          totalValue={`${inferredCount} of ${totalStations}`}
          subtitle={`${inferredPct}% estimated by soft sensors`}
          breakdown={[
            { label: 'Buffer Delta Models', value: '5 stations', colorClass: 'bg-amber-500' },
            { label: 'Conveyor Speed / PLC Sync', value: '4 stations', colorClass: 'bg-amber-600' },
            { label: 'Average Estimation Error', value: '±1.2 seconds', colorClass: 'bg-amber-700' },
          ]}
        />

        <StatsCard6
          title="Dark Stations (Manual Workstations)"
          totalValue={`${darkCount} of ${totalStations}`}
          subtitle={`${darkPct}% manual (S-10, S-22, S-25, S-37)`}
          breakdown={[
            { label: 'S-10 Metal Finish (Body)', value: '$14.2k upgrade', colorClass: 'bg-rose-500' },
            { label: 'S-22 Polish & Repair (Paint)', value: '$9.8k upgrade', colorClass: 'bg-rose-600' },
            { label: 'S-25 Headliner & S-37 Door', value: '$28.3k upgrade', colorClass: 'bg-rose-700' },
          ]}
        />
      </div>

      {/* Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-200/80 pb-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-zinc-600 uppercase text-[11px]">Coverage Tier:</span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60 text-xs">
            {(['All', 'Measured', 'Inferred', 'Dark'] as const).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTierFilter(t)}
                className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                  tierFilter === t
                    ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                    : 'text-zinc-600 hover:text-zinc-900'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="font-semibold text-zinc-600 uppercase text-[11px]">Zone:</span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60 text-xs">
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

      {/* Coverage Table */}
      <DataTable6
        title="Line Instrumentation Inventory"
        description="Comprehensive sensor classification across all 42 stations, documenting soft-sensor inputs and dark station retrofit opportunities."
        data={filteredStations}
        columns={columns}
        keyExtractor={(s) => s.id}
      />
    </div>
  );
}

