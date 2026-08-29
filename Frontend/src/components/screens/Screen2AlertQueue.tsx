import React, { useState } from 'react';
import { AlertItem, AlertStatus, AlertType } from '../../types';
import { DataTable6, Column } from '../common/DataTable6';
import {
  BellRing,
  EyeOff,
  Filter,
  ArrowRight,
  Info,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';

interface Screen2AlertQueueProps {
  alerts: AlertItem[];
  suppressedAlerts: AlertItem[];
  onSelectAlert: (alertId: string) => void;
  onUpdateAlertStatus: (alertId: string, status: AlertStatus) => void;
  alarmBudgetUsed: number;
  alarmBudgetMax: number;
}

export function Screen2AlertQueue({
  alerts,
  suppressedAlerts,
  onSelectAlert,
  onUpdateAlertStatus,
  alarmBudgetUsed,
  alarmBudgetMax,
}: Screen2AlertQueueProps) {
  const [showSuppressed, setShowSuppressed] = useState(false);
  const [statusFilter, setStatusFilter] = useState<'All' | AlertStatus>('All');
  const [typeFilter, setTypeFilter] = useState<'All' | AlertType>('All');

  // Filter active alerts
  const filteredAlerts = alerts.filter((a) => {
    if (statusFilter !== 'All' && a.status !== statusFilter) return false;
    if (typeFilter !== 'All' && a.type !== typeFilter) return false;
    return true;
  });

  const getStatusBadge = (status: AlertStatus) => {
    switch (status) {
      case 'New':
        return <Badge variant="warning">New</Badge>;
      case 'Acknowledged':
        return <Badge variant="indigo">Acknowledged</Badge>;
      case 'Snoozed':
        return <Badge variant="secondary">Snoozed</Badge>;
      case 'Resolved':
        return <Badge variant="success">Resolved</Badge>;
      case 'Expired':
        return <Badge variant="destructive">Expired</Badge>;
    }
  };

  const getTypeBadge = (type: AlertType) => {
    switch (type) {
      case 'Bottleneck Forming':
        return <Badge variant="warning">Bottleneck Forming</Badge>;
      case 'Defect Risk':
        return <Badge variant="destructive">Defect Risk</Badge>;
      case 'Throughput Drift':
        return <Badge variant="indigo">Throughput Drift</Badge>;
      case 'Sensor Degraded':
        return <Badge variant="secondary">Sensor Degraded</Badge>;
    }
  };

  const columns: Column<AlertItem>[] = [
    {
      key: 'rank',
      header: 'Rank',
      width: '70px',
      align: 'center',
      render: (a) => <span className="font-semibold text-zinc-900">#{a.rank}</span>,
    },
    {
      key: 'type',
      header: 'Alert Type',
      width: '170px',
      render: (a) => getTypeBadge(a.type),
    },
    {
      key: 'stationId',
      header: 'Station / Zone',
      width: '180px',
      render: (a) => (
        <div>
          <span className="font-semibold text-zinc-950">{a.stationId}</span>{' '}
          <span className="text-zinc-500">{a.stationName}</span>
        </div>
      ),
    },
    {
      key: 'summary',
      header: 'Plain-Language Summary',
      render: (a) => (
        <div className="text-zinc-800 text-xs max-w-lg">{a.summary}</div>
      ),
    },
    {
      key: 'confidencePct',
      header: 'Confidence',
      width: '110px',
      align: 'right',
      render: (a) => (
        <span className="font-medium text-zinc-950 font-mono">
          {a.confidencePct}%
        </span>
      ),
    },
    {
      key: 'timeToImpactMin',
      header: 'Impact In',
      width: '120px',
      align: 'right',
      render: (a) => (
        <span className="font-semibold text-amber-700 font-mono">
          {a.timeToImpactMin === 0 ? 'Ongoing' : `${a.timeToImpactMin} min`}
        </span>
      ),
    },
    {
      key: 'ageMin',
      header: 'Age',
      width: '90px',
      align: 'right',
      render: (a) => (
        <span className="text-zinc-400 font-mono text-[11px]">{a.ageMin}m ago</span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      width: '130px',
      align: 'center',
      render: (a) => getStatusBadge(a.status),
    },
    {
      key: 'actions',
      header: 'Detail',
      width: '80px',
      align: 'center',
      render: (a) => (
        <Button
          variant="ghost"
          size="icon"
          onClick={(e) => {
            e.stopPropagation();
            onSelectAlert(a.id);
          }}
          className="h-7 w-7 text-zinc-600 hover:text-zinc-900"
          title="Open Alert Detail"
        >
          <ArrowRight className="w-3.5 h-3.5" />
        </Button>
      ),
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner: Alarm Budget Status */}
      <Card className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
            <BellRing className="w-3.5 h-3.5 text-amber-600" />
            <span>Alarm Budget Enforcement</span>
          </div>
          <h2 className="text-lg font-bold text-zinc-950 tracking-tight mt-0.5">
            Active Alert Queue ({alerts.length} of max {alarmBudgetMax} active)
          </h2>
          <p className="text-xs text-zinc-600 mt-0.5">
            Ranked by Severity × Confidence ÷ Time-to-Impact. Hard cap of {alarmBudgetMax} alerts per hour prevents operator alarm fatigue.
          </p>
        </div>

        {/* Budget Meter */}
        <div className="flex items-center gap-3 text-xs shrink-0">
          <div className="text-right">
            <div className="text-[10px] text-zinc-400 uppercase font-semibold">
              Hourly Quota Consumed
            </div>
            <div className="text-base font-bold text-zinc-900 font-mono">
              {alarmBudgetUsed} / {alarmBudgetMax} alerts
            </div>
          </div>
          <div className="w-28">
            <Progress
              value={(alarmBudgetUsed / alarmBudgetMax) * 100}
              className="h-2.5"
            />
          </div>
        </div>
      </Card>

      {/* Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-200/80 pb-3 text-xs">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-semibold text-zinc-500 uppercase flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-zinc-400" />
            Type:
          </span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60">
            {(['All', 'Bottleneck Forming', 'Defect Risk', 'Throughput Drift', 'Sensor Degraded'] as const).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTypeFilter(t)}
                className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                  typeFilter === t
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
          <span className="font-semibold text-zinc-500 uppercase">Status:</span>
          <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60">
            {(['All', 'New', 'Acknowledged', 'Snoozed', 'Resolved'] as const).map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => setStatusFilter(s)}
                className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
                  statusFilter === s
                    ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                    : 'text-zinc-600 hover:text-zinc-900'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Table */}
      <DataTable6
        title="Prioritized Alert Queue"
        description="Every alert represents an actionable opportunity to prevent line degradation. Select any row to examine evidence and advisory recommendations."
        data={filteredAlerts}
        columns={columns}
        keyExtractor={(a) => a.id}
        onRowClick={(a) => onSelectAlert(a.id)}
      />

      {/* Suppressed Alerts Notice Bar */}
      <Card className="p-4 flex items-center justify-between bg-zinc-50/70 border-zinc-200/80">
        <div className="flex items-center gap-2.5 text-xs text-zinc-700">
          <EyeOff className="w-4 h-4 text-zinc-400" />
          <span>
            <strong>9 lower-priority signals suppressed by alarm budget.</strong> These signals are logged for audit but not pushed to floor operators.
          </span>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowSuppressed(!showSuppressed)}
        >
          {showSuppressed ? 'Hide Suppressed' : 'View Suppressed (9)'}
        </Button>
      </Card>

      {/* Expanded Suppressed Alerts Panel */}
      {showSuppressed && (
        <Card className="p-5 space-y-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
            <Info className="w-3.5 h-3.5 text-zinc-500" />
            Suppressed Signals Audit Log (Below Priority Cutoff)
          </h4>
          <div className="divide-y divide-zinc-100 rounded-lg border border-zinc-200/80 text-xs overflow-hidden">
            {suppressedAlerts.map((sup) => (
              <div
                key={sup.id}
                className="p-3.5 flex flex-col md:flex-row md:items-center justify-between gap-2 hover:bg-zinc-50 transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-zinc-900">Rank #{sup.rank}</span>
                    <Badge variant="secondary" className="text-[10px]">
                      {sup.type}
                    </Badge>
                    <span className="font-semibold text-zinc-900">{sup.stationId}</span>
                    <span className="text-zinc-500">({sup.stationName})</span>
                  </div>
                  <div className="text-zinc-700">{sup.summary}</div>
                </div>
                <div className="text-right text-[11px] text-zinc-400 shrink-0 font-mono">
                  <div>Confidence: {sup.confidencePct}%</div>
                  <div>Impact: in {sup.timeToImpactMin}m</div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

