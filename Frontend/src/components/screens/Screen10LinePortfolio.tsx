import React from 'react';
import { StatsCard6 } from '../common/StatsCard6';
import { DataTable6, Column } from '../common/DataTable6';
import {
  Boxes,
  ArrowRight,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

interface LinePortfolioItem {
  id: string;
  name: string;
  facility: string;
  status: 'Live Mode' | 'Shadow Mode' | 'Onboarding' | 'Planned';
  stationsCount: number;
  currentJph: number;
  targetJph: number;
  oeePct: number;
  alarmCompliancePct: number;
  modelTrustPct: number;
  annualizedSavings: string;
}

interface Screen10LinePortfolioProps {
  onSelectLineA: () => void;
}

export function Screen10LinePortfolio({ onSelectLineA }: Screen10LinePortfolioProps) {
  const lines: LinePortfolioItem[] = [
    {
      id: 'P2-LA',
      name: 'Plant 2 — Line A (Current)',
      facility: 'Plant 2 (Crossover & SUV)',
      status: 'Live Mode',
      stationsCount: 42,
      currentJph: 58,
      targetJph: 62,
      oeePct: 88.4,
      alarmCompliancePct: 98.2,
      modelTrustPct: 71.0,
      annualizedSavings: '$5,184,000',
    },
    {
      id: 'P2-LB',
      name: 'Plant 2 — Line B (Truck)',
      facility: 'Plant 2 (Body-on-Frame)',
      status: 'Shadow Mode',
      stationsCount: 38,
      currentJph: 48,
      targetJph: 52,
      oeePct: 83.1,
      alarmCompliancePct: 94.0,
      modelTrustPct: 68.4,
      annualizedSavings: '$2,840,000 (Proj)',
    },
    {
      id: 'P1-L1',
      name: 'Plant 1 — Line 1 (Sedan)',
      facility: 'Plant 1 (Passenger Vehicles)',
      status: 'Onboarding',
      stationsCount: 54,
      currentJph: 64,
      targetJph: 68,
      oeePct: 79.5,
      alarmCompliancePct: 89.0,
      modelTrustPct: 58.2,
      annualizedSavings: 'Discovery Phase',
    },
    {
      id: 'P3-LC',
      name: 'Plant 3 — Line C (EV Dedicated)',
      facility: 'Plant 3 (New Energy)',
      status: 'Planned',
      stationsCount: 48,
      currentJph: 36,
      targetJph: 45,
      oeePct: 72.0,
      alarmCompliancePct: 0,
      modelTrustPct: 0,
      annualizedSavings: 'Pending Ingestion',
    },
  ];

  const columns: Column<LinePortfolioItem>[] = [
    {
      key: 'name',
      header: 'Line / Facility',
      width: '240px',
      render: (l) => (
        <div>
          <div className="font-semibold text-zinc-900">{l.name}</div>
          <div className="text-zinc-500 text-[11px]">{l.facility}</div>
        </div>
      ),
    },
    {
      key: 'status',
      header: 'Twin Status',
      width: '150px',
      render: (l) => {
        if (l.status === 'Live Mode') {
          return (
            <Badge variant="success">
              Live Mode
            </Badge>
          );
        }
        if (l.status === 'Shadow Mode') {
          return (
            <Badge variant="outline" className="bg-amber-50 text-amber-900 border-amber-300">
              Shadow Mode (Day 44)
            </Badge>
          );
        }
        if (l.status === 'Onboarding') {
          return (
            <Badge variant="secondary" className="bg-indigo-50 text-indigo-900 border-indigo-200">
              Discovery 82%
            </Badge>
          );
        }
        return (
          <Badge variant="secondary">
            Planned
          </Badge>
        );
      },
    },
    {
      key: 'stationsCount',
      header: 'Stations',
      align: 'center',
      width: '100px',
      render: (l) => <span className="font-semibold text-zinc-900 font-mono">{l.stationsCount}</span>,
    },
    {
      key: 'currentJph',
      header: 'JPH vs Target',
      align: 'right',
      width: '140px',
      render: (l) => (
        <span className="font-semibold text-zinc-900 font-mono">
          {l.currentJph} / {l.targetJph}
        </span>
      ),
    },
    {
      key: 'oeePct',
      header: 'Line OEE',
      align: 'right',
      width: '110px',
      render: (l) => (
        <span className="font-semibold text-zinc-900 font-mono">{l.oeePct}%</span>
      ),
    },
    {
      key: 'modelTrustPct',
      header: 'Model Precision',
      align: 'right',
      width: '140px',
      render: (l) => (
        <span className="font-semibold text-indigo-900 font-mono">
          {l.modelTrustPct > 0 ? `${l.modelTrustPct}%` : '—'}
        </span>
      ),
    },
    {
      key: 'annualizedSavings',
      header: 'Annualized Impact',
      align: 'right',
      width: '170px',
      render: (l) => (
        <span className="font-semibold font-mono text-emerald-700">
          {l.annualizedSavings}
        </span>
      ),
    },
    {
      key: 'action',
      header: 'Access',
      width: '90px',
      align: 'center',
      render: (l) => (
        <Button
          variant="outline"
          size="icon"
          className="h-7 w-7"
          onClick={onSelectLineA}
          title="Switch to Line A"
        >
          <ArrowRight className="w-3.5 h-3.5" />
        </Button>
      ),
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <Boxes className="w-3.5 h-3.5 text-indigo-600" />
              <span>Multi-Plant Fleet Intelligence</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Enterprise Line Portfolio
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Cross-facility digital twin fleet rollup comparing throughput efficiency, model calibration maturity, and aggregate enterprise savings.
            </p>
          </div>

          <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-2.5 text-right text-xs">
            <div className="text-[10px] text-zinc-400 uppercase font-semibold">Fleet Total Projected ROI</div>
            <div className="text-xl font-bold text-emerald-950 font-mono">$8,024,000 / year</div>
          </div>
        </div>
      </Card>

      {/* 3 Rollup Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard6
          title="Digital Twin Fleet Rollout"
          totalValue="4 Production Lines"
          subtitle="182 total monitored assembly stations"
          breakdown={[
            { label: 'Live Active Lines', value: '1 line (Line A)', colorClass: 'bg-emerald-500' },
            { label: 'Shadow Mode Calibration', value: '1 line (Line B)', colorClass: 'bg-amber-500' },
            { label: 'Discovery / Ingestion', value: '2 lines', colorClass: 'bg-indigo-500' },
          ]}
        />

        <StatsCard6
          title="Fleet Throughput Index"
          totalValue="52.8 Average JPH"
          subtitle="Weighted across all operating plants"
          breakdown={[
            { label: 'Plant 2 — Line A (Live)', value: '58.4 JPH (88% OEE)', colorClass: 'bg-emerald-600' },
            { label: 'Plant 2 — Line B (Shadow)', value: '48.2 JPH (83% OEE)', colorClass: 'bg-amber-600' },
            { label: 'Plant 1 — Line 1 (Pilot)', value: '64.0 JPH (79% OEE)', colorClass: 'bg-indigo-600' },
          ]}
        />

        <StatsCard6
          title="Alarm Budget Adherence"
          totalValue="96.1% Compliance"
          subtitle="Alarm fatigue prevention ceiling"
          breakdown={[
            { label: 'Average Hourly Alerts', value: '3.1 / 6.0 ceiling', colorClass: 'bg-emerald-500' },
            { label: 'Operator Disagreement Rate', value: '4.8% false alarm', colorClass: 'bg-sky-500' },
            { label: 'Mean Warning Lead Time', value: '37 minutes', colorClass: 'bg-purple-500' },
          ]}
        />
      </div>

      {/* Lines Table */}
      <DataTable6
        title="Active Factory Lines"
        description="Select any line to switch the digital twin context and review real-time predictive simulation models."
        data={lines}
        columns={columns}
        keyExtractor={(l) => l.id}
      />
    </div>
  );
}

