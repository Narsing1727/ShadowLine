import React, { useState } from 'react';
import { StationData } from '../../types';
import {
  Compass,
  CheckCircle2,
  Sliders,
  RotateCcw,
  Sparkles,
  Save,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

interface Screen11LineOnboardingProps {
  stations: StationData[];
}

export function Screen11LineOnboarding({ stations }: Screen11LineOnboardingProps) {
  const [activeStep, setActiveStep] = useState<number>(3); // Shadow Mode is currently active
  const [stationOrderConfidence, setStationOrderConfidence] = useState<number>(96);
  const [isSimulatingDiscovery, setIsSimulatingDiscovery] = useState<boolean>(false);
  const [customBufferCapacity, setCustomBufferCapacity] = useState<number>(12);
  const [showOverrideSuccess, setShowOverrideSuccess] = useState<boolean>(false);

  const steps = [
    {
      num: 1,
      title: 'Data Stream Ingestion',
      subtitle: 'Connect OPC UA / MQTT / MES broker',
      status: 'Complete',
      detail: 'Connected to Plant 2 Kepware OPC UA server. Streaming 140 tags/sec.',
    },
    {
      num: 2,
      title: 'Automated Topology Discovery',
      subtitle: 'Infer station order, buffers, variants',
      status: 'Complete',
      detail: 'Discovered 42 stations, 41 intermediate buffers, and 3 variants from 14 days event logs.',
    },
    {
      num: 3,
      title: 'Shadow Mode Simulation',
      subtitle: 'Run twin forward, log predictions silently',
      status: 'In Progress (Day 91)',
      detail: 'Running 200 Monte-Carlo forward simulations every 5 minutes. Predictions logged for trust audit.',
    },
    {
      num: 4,
      title: 'Promotion Gate & Live Cutover',
      subtitle: 'Verify precision > 65% before alerting',
      status: 'Ready for Promotion',
      detail: 'Criteria met: 71.0% precision across 4 consecutive weeks. Ready for live alerting.',
    },
  ];

  const handleSimulateDiscovery = () => {
    setIsSimulatingDiscovery(true);
    setTimeout(() => {
      setIsSimulatingDiscovery(false);
      setStationOrderConfidence(98);
    }, 1200);
  };

  const handleSaveOverrides = (e: React.FormEvent) => {
    e.preventDefault();
    setShowOverrideSuccess(true);
    setTimeout(() => setShowOverrideSuccess(false), 3000);
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <Compass className="w-3.5 h-3.5 text-amber-600" />
              <span>Automated Digital Twin Provisioning</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Line Auto-Discovery & Onboarding Engine
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              ShadowLine learns line physics and station topology automatically from standard PLC event logs without requiring manual CAD imports or expensive months-long simulation engineering.
            </p>
          </div>

          <Button
            type="button"
            onClick={handleSimulateDiscovery}
            disabled={isSimulatingDiscovery}
            variant="default"
            className="flex items-center gap-2"
          >
            {isSimulatingDiscovery ? (
              <>
                <RotateCcw className="w-4 h-4 animate-spin" />
                <span>Re-Inferring Topology...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run Topology Auto-Scan</span>
              </>
            )}
          </Button>
        </div>
      </Card>

      {/* 4-Step Onboarding Workflow Progress */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {steps.map((step) => {
          const isCurrent = step.num === activeStep;
          const isDone = step.num < activeStep || step.status === 'Complete';

          return (
            <Card
              key={step.num}
              onClick={() => setActiveStep(step.num)}
              className={`p-4 transition-all cursor-pointer ${
                isCurrent
                  ? 'border-amber-500 bg-amber-50/50 ring-1 ring-amber-400/50'
                  : isDone
                  ? 'border-zinc-200 hover:border-zinc-300'
                  : 'border-zinc-200/60 bg-zinc-50/50'
              }`}
            >
              <div className="flex items-center justify-between text-xs mb-2">
                <span className="font-semibold text-zinc-900 font-mono">Step 0{step.num}</span>
                {isDone ? (
                  <Badge variant="success">
                    {step.status}
                  </Badge>
                ) : isCurrent ? (
                  <Badge variant="outline" className="bg-amber-100 text-amber-900 border-amber-300">
                    {step.status}
                  </Badge>
                ) : (
                  <Badge variant="secondary">
                    {step.status}
                  </Badge>
                )}
              </div>

              <h4 className="text-sm font-semibold text-zinc-950">{step.title}</h4>
              <p className="text-xs text-zinc-500 mt-0.5">{step.subtitle}</p>

              <div className="mt-3 pt-2 border-t border-zinc-100 text-[11px] text-zinc-600 leading-relaxed">
                {step.detail}
              </div>
            </Card>
          );
        })}
      </div>

      {/* Auto-Discovery Metrics Card */}
      <Card className="p-5 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-zinc-100 pb-3">
          <div>
            <h3 className="text-sm font-semibold uppercase text-zinc-950 flex items-center gap-2">
              <span className="text-amber-600">/</span>
              Auto-Discovery Model Synthesis (Plant 2 — Line A)
            </h3>
            <p className="text-xs text-zinc-600 mt-0.5">
              Confidence score calculated via continuous markov-chain sequence verification over 14 days of real PLC timestamps.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-zinc-500">Topology Confidence:</span>
            <Badge variant="success">
              {stationOrderConfidence}% Match
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/50 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[11px]">Station Order Discovered</div>
            <div className="text-2xl font-bold text-zinc-950 font-mono">42 of 42</div>
            <div className="text-emerald-700 text-[11px] font-medium">100% Sequence Validated</div>
          </div>

          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/50 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[11px]">Inter-Station Buffers Mapped</div>
            <div className="text-2xl font-bold text-zinc-950 font-mono">41 of 41</div>
            <div className="text-emerald-700 text-[11px] font-medium">Max Capacity Inferred</div>
          </div>

          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/50 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[11px]">Vehicle Variants Identified</div>
            <div className="text-2xl font-bold text-zinc-950 font-mono">3 Variants</div>
            <div className="text-zinc-600 text-[11px]">SUV-A, Sedan-B, EV-C</div>
          </div>
        </div>
      </Card>

      {/* Manual Overrides & Expert Tuning */}
      <Card className="p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-zinc-100 pb-3">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
            <Sliders className="w-3.5 h-3.5 text-zinc-500" />
            Manual Engineering Overrides & Capacity Tuning
          </h3>
          <span className="text-xs text-zinc-500">Allows Process Engineers to fine-tune auto-inferred parameters</span>
        </div>

        {showOverrideSuccess && (
          <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-950 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Digital twin parameters updated successfully. Simulations recalibrated.</span>
          </div>
        )}

        <form onSubmit={handleSaveOverrides} className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="space-y-1.5">
            <label className="text-zinc-700 uppercase font-semibold text-[11px]">Default Inter-Station Buffer Ceiling:</label>
            <input
              type="number"
              value={customBufferCapacity}
              onChange={(e) => setCustomBufferCapacity(Number(e.target.value))}
              className="w-full h-9 px-3 rounded-md border border-zinc-200 bg-white font-mono text-sm focus:outline-none focus:ring-1 focus:ring-zinc-950"
            />
            <p className="text-[11px] text-zinc-500">Max carrier slots between consecutive line stations</p>
          </div>

          <div className="space-y-1.5">
            <label className="text-zinc-700 uppercase font-semibold text-[11px]">Dark Station Handling Mode:</label>
            <select className="w-full h-9 px-3 rounded-md border border-zinc-200 bg-white text-xs focus:outline-none focus:ring-1 focus:ring-zinc-950">
              <option>Dynamic Soft-Sensor Interpolation (Recommended)</option>
              <option>Fixed Average Dwell Time (Conservative)</option>
              <option>Strict Conveyor Synchronous Pass-Through</option>
            </select>
            <p className="text-[11px] text-zinc-500">Fall-back logic for non-instrumented stations</p>
          </div>

          <div className="space-y-1.5 flex flex-col justify-end">
            <Button
              type="submit"
              variant="default"
              className="w-full flex items-center justify-center gap-2"
            >
              <Save className="w-4 h-4 text-amber-400" />
              <span>Save & Recalibrate Twin</span>
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}

