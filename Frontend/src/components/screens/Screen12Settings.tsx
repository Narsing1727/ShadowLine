import React, { useState } from 'react';
import {
  Settings as SettingsIcon,
  BellRing,
  Clock,
  Layers,
  Wrench,
  Save,
  CheckCircle2,
  Server,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

export function Screen12Settings() {
  const [supervisorBudget, setSupervisorBudget] = useState(6);
  const [managerBudget, setManagerBudget] = useState(12);
  const [leadershipBudget, setLeadershipBudget] = useState(2);
  const [minConfidence, setMinConfidence] = useState(65);
  const [simHorizon, setSimHorizon] = useState('4h');
  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  const variants = [
    { name: 'SUV-A', targetCycle: '61s', takt: '58s', scheduledMix: '45%', priority: 'High Margin' },
    { name: 'Sedan-B', targetCycle: '54s', takt: '58s', scheduledMix: '35%', priority: 'Standard' },
    { name: 'EV-C', targetCycle: '66s', takt: '58s', scheduledMix: '20%', priority: 'Battery Limited' },
  ];

  const maintenanceWindows = [
    { station: 'S-10 (Metal Finish)', date: '14 Nov 2026', scope: 'Optical sensor install & framing bracket ($14.2k)' },
    { station: 'S-14 (E-Coat Tank)', date: '18 Nov 2026', scope: 'Thermal bath circulation pump replacement' },
    { station: 'S-22 (Polish & Repair)', date: '21 Nov 2026', scope: 'Manual bay barcode scanner integration ($9.8k)' },
    { station: 'S-30 (Engine Drop)', date: '25 Nov 2026', scope: 'Atlas Copco nutrunner torque recalibration' },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <SettingsIcon className="w-3.5 h-3.5 text-zinc-700" />
              <span>Digital Twin Engine Calibration</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              System Settings & Parameter Tuning
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Configure alarm budget limits, confidence cutoffs, variant mix targets, and real-time PLC broker integration endpoints.
            </p>
          </div>

          <Button
            type="button"
            onClick={handleSave}
            variant="default"
            className="flex items-center gap-2"
          >
            <Save className="w-4 h-4 text-amber-400" />
            <span>Save All Configurations</span>
          </Button>
        </div>

        {savedSuccess && (
          <div className="mt-4 p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-950 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Configuration parameters successfully committed and hot-reloaded to simulator instances.</span>
          </div>
        )}
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Section 1: Alarm Budget Configuration per Role */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <BellRing className="w-3.5 h-3.5 text-amber-600" />
              Hourly Alarm Budget Limits (Fatigue Prevention)
            </h3>
            <span className="text-[11px] text-zinc-500 font-mono">Alerts / Operator / Hour</span>
          </div>

          <p className="text-xs text-zinc-600">
            Strict ceiling on push alerts to ensure operator attention is focused on high-confidence, actionable line interventions.
          </p>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3 rounded-lg border border-zinc-200 bg-zinc-50/50">
              <div>
                <div className="font-semibold text-zinc-900">Floor Supervisor Budget</div>
                <div className="text-[11px] text-zinc-500">Line floor operations</div>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  value={supervisorBudget}
                  onChange={(e) => setSupervisorBudget(Number(e.target.value))}
                  className="w-16 h-8 rounded-md border border-zinc-200 text-center font-semibold font-mono bg-white text-sm focus:outline-none focus:ring-1 focus:ring-zinc-950"
                />
                <span className="text-zinc-600 font-mono">/ hour</span>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg border border-zinc-200 bg-zinc-50/50">
              <div>
                <div className="font-semibold text-zinc-900">Plant Manager Budget</div>
                <div className="text-[11px] text-zinc-500">Engineering & bottleneck analysis</div>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  value={managerBudget}
                  onChange={(e) => setManagerBudget(Number(e.target.value))}
                  className="w-16 h-8 rounded-md border border-zinc-200 text-center font-semibold font-mono bg-white text-sm focus:outline-none focus:ring-1 focus:ring-zinc-950"
                />
                <span className="text-zinc-600 font-mono">/ hour</span>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg border border-zinc-200 bg-zinc-50/50">
              <div>
                <div className="font-semibold text-zinc-900">Executive Leadership Budget</div>
                <div className="text-[11px] text-zinc-500">High-level plant notifications</div>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  value={leadershipBudget}
                  onChange={(e) => setLeadershipBudget(Number(e.target.value))}
                  className="w-16 h-8 rounded-md border border-zinc-200 text-center font-semibold font-mono bg-white text-sm focus:outline-none focus:ring-1 focus:ring-zinc-950"
                />
                <span className="text-zinc-600 font-mono">/ hour</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Section 2: Model Inference & Simulation Horizon */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-indigo-600" />
              Simulation Horizon & Statistical Thresholds
            </h3>
          </div>

          <div className="space-y-3 text-xs">
            <div className="space-y-1.5">
              <label className="text-zinc-700 font-semibold uppercase text-[11px]">
                Minimum Alerting Confidence Cutoff: {minConfidence}%
              </label>
              <input
                type="range"
                min="50"
                max="90"
                value={minConfidence}
                onChange={(e) => setMinConfidence(Number(e.target.value))}
                className="w-full accent-zinc-900 cursor-pointer"
              />
              <div className="flex justify-between text-[11px] text-zinc-500">
                <span>50% (Permissive)</span>
                <span>65% (Recommended Default)</span>
                <span>90% (Strict)</span>
              </div>
            </div>

            <div className="space-y-2 pt-3 border-t border-zinc-100">
              <label className="text-zinc-700 font-semibold uppercase text-[11px]">
                Forward Simulation Horizon:
              </label>
              <div className="inline-flex w-full h-9 items-center justify-center rounded-lg bg-zinc-100 p-1 text-zinc-500 border border-zinc-200/60 text-xs">
                {['1h', '2h', '4h', '8h'].map((h) => (
                  <button
                    key={h}
                    type="button"
                    onClick={() => setSimHorizon(h)}
                    className={`flex-1 inline-flex items-center justify-center whitespace-nowrap rounded-md py-1 text-xs font-medium transition-all cursor-pointer ${
                      simHorizon === h
                        ? 'bg-white text-zinc-950 shadow-xs font-semibold'
                        : 'text-zinc-600 hover:text-zinc-900'
                    }`}
                  >
                    {h} Ahead
                  </button>
                ))}
              </div>
              <p className="text-[11px] text-zinc-500">
                Twin executes 200 Monte-Carlo forward paths spanning this horizon every 5 minutes.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Section 3: Configured Vehicle Variants */}
      <Card className="p-5 space-y-3">
        <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
            <Layers className="w-3.5 h-3.5 text-zinc-600" />
            Configured Vehicle Assembly Variants (Mixed-Model Schedule)
          </h3>
          <span className="text-xs text-zinc-500">Plant 2 Line A Model Mix</span>
        </div>

        <div className="rounded-lg border border-zinc-200 overflow-hidden divide-y divide-zinc-200 text-xs">
          <div className="grid grid-cols-5 p-2.5 bg-zinc-50 font-semibold text-zinc-600 uppercase text-[11px]">
            <div>Variant Code</div>
            <div>Target Cycle</div>
            <div>Line Takt</div>
            <div>Scheduled Mix</div>
            <div>Production Priority</div>
          </div>
          {variants.map((v) => (
            <div key={v.name} className="grid grid-cols-5 p-3 items-center hover:bg-zinc-50/60 transition-colors">
              <div className="font-semibold text-zinc-900">{v.name}</div>
              <div className="font-mono text-zinc-600">{v.targetCycle}</div>
              <div className="font-mono text-zinc-600">{v.takt}</div>
              <div className="font-semibold text-indigo-900 font-mono">{v.scheduledMix}</div>
              <div>
                <Badge variant="secondary">
                  {v.priority}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Section 4: Scheduled Maintenance Windows & Integration Endpoints */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Maintenance Calendar */}
        <Card className="p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <Wrench className="w-3.5 h-3.5 text-amber-600" />
              Scheduled Station Maintenance Windows
            </h3>
          </div>
          <div className="space-y-2 text-xs">
            {maintenanceWindows.map((m, i) => (
              <div key={i} className="p-3 rounded-lg border border-zinc-200 bg-zinc-50/50">
                <div className="flex items-center justify-between font-semibold">
                  <span className="text-zinc-900">{m.station}</span>
                  <Badge variant="outline" className="bg-amber-50 text-amber-900 border-amber-300 font-mono text-[11px]">
                    {m.date}
                  </Badge>
                </div>
                <div className="text-zinc-600 text-xs mt-1">{m.scope}</div>
              </div>
            ))}
          </div>
        </Card>

        {/* Real-time Integration Endpoints */}
        <Card className="p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <Server className="w-3.5 h-3.5 text-emerald-600" />
              Industrial Telemetry & SCADA Connectors
            </h3>
          </div>
          <div className="space-y-2 text-xs">
            <div className="p-3 rounded-lg border border-zinc-200 bg-zinc-50/50 flex items-center justify-between">
              <div>
                <div className="font-semibold text-zinc-900">OPC UA Industrial Gateway</div>
                <div className="text-[11px] text-zinc-500 font-mono">opc.tcp://plant2-kepware.local:4840</div>
              </div>
              <Badge variant="success">
                Connected
              </Badge>
            </div>

            <div className="p-3 rounded-lg border border-zinc-200 bg-zinc-50/50 flex items-center justify-between">
              <div>
                <div className="font-semibold text-zinc-900">MQTT Event Broker</div>
                <div className="text-[11px] text-zinc-500 font-mono">mqtts://broker.shadowline.internal:8883</div>
              </div>
              <Badge variant="success">
                Streaming
              </Badge>
            </div>

            <div className="p-3 rounded-lg border border-zinc-200 bg-zinc-50/50 flex items-center justify-between">
              <div>
                <div className="font-semibold text-zinc-900">MES Genealogy Ingest (Kafka)</div>
                <div className="text-[11px] text-zinc-500 font-mono">kafka://mes-cluster.automotive.net:9092</div>
              </div>
              <Badge variant="success">
                Active
              </Badge>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

