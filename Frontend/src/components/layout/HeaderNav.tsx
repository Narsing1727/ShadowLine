import React from 'react';
import { UserRole, ScreenId } from '../../types';
import {
  Radio,
  Clock,
  Gauge,
  Layers,
  BellRing,
  Info,
  Zap,
  PowerOff,
  WifiOff,
} from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';

interface HeaderNavProps {
  currentRole: UserRole;
  onRoleChange: (role: UserRole) => void;
  activeScreen: ScreenId;
  onNavigate: (screen: ScreenId) => void;
  isShadowMode: boolean;
  onToggleShadowMode: () => void;
  alarmBudgetUsed: number;
  alarmBudgetMax: number;
  currentTimeStr: string;
  currentShiftStr: string;
  currentJph: number;
  targetJph: number;
  unitsBuilt: number;
  isLineStopped: boolean;
  onToggleLineStopped: () => void;
  isDegradedData: boolean;
  onToggleDegradedData: () => void;
  isBackendConnected?: boolean;
  onInjectWhatIfFault?: (stationId: string, faultType: string) => void;
}

export function HeaderNav({
  currentRole,
  onRoleChange,
  activeScreen,
  onNavigate,
  isShadowMode,
  onToggleShadowMode,
  alarmBudgetUsed,
  alarmBudgetMax,
  currentTimeStr,
  currentShiftStr,
  currentJph,
  targetJph,
  unitsBuilt,
  isLineStopped,
  onToggleLineStopped,
  isDegradedData,
  onToggleDegradedData,
  isBackendConnected = false,
  onInjectWhatIfFault,
}: HeaderNavProps) {
  return (
    <header className="border-b border-zinc-200/80 bg-white sticky top-0 z-40 shadow-xs">
      {/* Top Banner: Read-Only Assurance & Mode Indicator */}
      <div
        className={`px-4 py-1.5 text-xs flex flex-wrap items-center justify-between gap-2 border-b ${
          isShadowMode
            ? 'bg-amber-50/70 border-amber-200/80 text-amber-900'
            : 'bg-emerald-50/70 border-emerald-200/80 text-emerald-900'
        }`}
      >
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 font-medium">
            {isShadowMode ? (
              <>
                <Radio className="w-3.5 h-3.5 text-amber-600 animate-pulse" />
                <span className="font-semibold">SHADOW MODE</span>
                <span className="text-zinc-500 font-normal">
                  — predictions logged silently, alerts suppressed
                </span>
              </>
            ) : (
              <>
                <Zap className="w-3.5 h-3.5 text-emerald-600" />
                <span className="font-semibold">LIVE MODE</span>
                <span className="text-zinc-500 font-normal">
                  — active operator alerting
                </span>
              </>
            )}
          </div>
          <span className="hidden md:inline text-zinc-300">|</span>
          <div className="flex items-center gap-1.5 text-zinc-600 text-xs">
            <Info className="w-3.5 h-3.5 text-zinc-400" />
            <span className="font-medium text-zinc-800">
              Read-only. ShadowLine does not control the line.
            </span>
          </div>
          <span className="hidden md:inline text-zinc-300">|</span>
          {/* Backend Connection Indicator */}
          <div className="flex items-center gap-1.5 text-xs">
            <span
              className={`w-2 h-2 rounded-full ${
                isBackendConnected ? 'bg-emerald-500 animate-ping' : 'bg-zinc-400'
              }`}
            />
            <span
              className={`font-medium ${
                isBackendConnected ? 'text-emerald-800 font-mono' : 'text-zinc-500'
              }`}
            >
              {isBackendConnected ? 'API: Connected (:8000)' : 'API: Standalone Mock'}
            </span>
          </div>
        </div>

        {/* Quick Simulation Toggles for Demonstration */}
        <div className="flex items-center gap-2">
          {onInjectWhatIfFault && (
            <Button
              variant="outline"
              size="xs"
              onClick={() => onInjectWhatIfFault('S-14', 'drift')}
              className="bg-indigo-50 border-indigo-200 text-indigo-900 hover:bg-indigo-100 text-[11px] font-medium"
            >
              ⚡ Test What-If (S-14 Drift)
            </Button>
          )}

          <Button
            variant="outline"
            size="xs"
            onClick={onToggleShadowMode}
            className="bg-white/80 hover:bg-white text-[11px] font-normal"
          >
            Switch to {isShadowMode ? 'Live Mode' : 'Shadow Mode'}
          </Button>

          <Button
            variant={isLineStopped ? 'destructive' : 'outline'}
            size="xs"
            onClick={onToggleLineStopped}
            className="text-[11px] font-normal"
          >
            <PowerOff className="w-3 h-3 mr-1" />
            {isLineStopped ? 'Line Stopped (Resume)' : 'Simulate Line Stop'}
          </Button>

          <Button
            variant={isDegradedData ? 'destructive' : 'outline'}
            size="xs"
            onClick={onToggleDegradedData}
            className="text-[11px] font-normal"
          >
            <WifiOff className="w-3 h-3 mr-1" />
            {isDegradedData ? 'Data Degraded (Fix)' : 'Simulate Data Drop'}
          </Button>
        </div>
      </div>

      {/* Main Bar: Line Metrics + Role Switcher */}
      <div className="px-4 py-2.5 flex flex-wrap items-center justify-between gap-4">
        {/* Plant / Shift / Production telemetry */}
        <div className="flex flex-wrap items-center gap-3 lg:gap-4 text-xs">
          <div className="flex items-center gap-2 pr-2 border-r border-zinc-200">
            <span className="font-semibold text-zinc-950 tracking-tight text-sm">
              Plant 2 · Line A
            </span>
            <Badge variant="secondary" className="text-[10px] font-normal">
              Final Assembly
            </Badge>
          </div>

          <div className="flex items-center gap-1.5 text-zinc-600 bg-zinc-50 px-2.5 py-1 rounded-md border border-zinc-200/60">
            <Clock className="w-3.5 h-3.5 text-zinc-400" />
            <span className="font-medium text-zinc-900 font-mono text-[11px]">
              {currentTimeStr}
            </span>
            <span className="text-zinc-400">·</span>
            <span className="text-zinc-600">{currentShiftStr}</span>
          </div>

          <div className="flex items-center gap-1.5 text-zinc-600 bg-zinc-50 px-2.5 py-1 rounded-md border border-zinc-200/60">
            <Gauge className="w-3.5 h-3.5 text-zinc-500" />
            <span>JPH:</span>
            <span className="font-semibold text-zinc-950 font-mono text-[11px]">
              {isLineStopped ? '0' : currentJph}
            </span>
            <span className="text-zinc-400">/ {targetJph} target</span>
          </div>

          <div className="flex items-center gap-1.5 text-zinc-600 bg-zinc-50 px-2.5 py-1 rounded-md border border-zinc-200/60">
            <Layers className="w-3.5 h-3.5 text-zinc-500" />
            <span>Shift Output:</span>
            <span className="font-semibold text-zinc-950 font-mono text-[11px]">
              {unitsBuilt}
            </span>
            <span className="text-zinc-400">units</span>
          </div>

          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs ${
              alarmBudgetUsed >= alarmBudgetMax
                ? 'bg-rose-50 border-rose-200 text-rose-900 font-medium'
                : 'bg-zinc-50 border-zinc-200/60 text-zinc-700'
            }`}
          >
            <BellRing className="w-3.5 h-3.5 text-zinc-500" />
            <span>Alarm Budget:</span>
            <span className="font-semibold font-mono text-[11px]">
              {alarmBudgetUsed}/{alarmBudgetMax}
            </span>
            <span className="text-zinc-400">this hr</span>
          </div>
        </div>

        {/* User Role Switcher Tabs */}
        <div className="inline-flex h-8 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60">
          <button
            type="button"
            onClick={() => {
              onRoleChange('supervisor');
              onNavigate('live-line');
            }}
            className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
              currentRole === 'supervisor'
                ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200/50'
            }`}
          >
            Floor Supervisor
          </button>
          <button
            type="button"
            onClick={() => {
              onRoleChange('manager');
              onNavigate('bottleneck-history');
            }}
            className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
              currentRole === 'manager'
                ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200/50'
            }`}
          >
            Plant Manager
          </button>
          <button
            type="button"
            onClick={() => {
              onRoleChange('leadership');
              onNavigate('impact-business');
            }}
            className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-2.5 py-0.5 text-xs font-medium transition-all cursor-pointer ${
              currentRole === 'leadership'
                ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200/50'
            }`}
          >
            Leadership
          </button>
        </div>
      </div>
    </header>
  );
}

