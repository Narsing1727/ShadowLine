import React, { useState } from 'react';
import { DEFECT_RELATIONSHIPS, VIN_GENEALOGY_DATABASE } from '../../data/mockData';
import {
  GitBranch,
  Search,
  ArrowRight,
  User,
  Wrench,
  Info,
  Lock,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Alert, AlertDescription, AlertTitle } from '../ui/alert';

interface Screen6DefectPropagationProps {
  onSelectStation: (stationId: string) => void;
}

export function Screen6DefectPropagation({
  onSelectStation,
}: Screen6DefectPropagationProps) {
  const [selectedRelId, setSelectedRelId] = useState<string>('REL-01');
  const [searchedVin, setSearchedVin] = useState<string>('MA1TA2XX7R1234536');
  const [containmentStation, setContainmentStation] = useState<string>('S-30');
  const [containmentTime, setContainmentTime] = useState<string>('13:10');

  const selectedRel =
    DEFECT_RELATIONSHIPS.find((r) => r.id === selectedRelId) || DEFECT_RELATIONSHIPS[0];

  const searchedGenealogy =
    VIN_GENEALOGY_DATABASE.find((v) => v.vin.toLowerCase() === searchedVin.toLowerCase()) ||
    VIN_GENEALOGY_DATABASE[2];

  // Containment affected VINs list (47 units)
  const affectedVins = Array.from({ length: 47 }, (_, i) => ({
    vin: `MA1TA2XX7R12345${String(50 - i).padStart(2, '0')}`,
    timestamp: `13:${String(10 + (i % 50)).padStart(2, '0')}:14`,
    currentLocation: i < 15 ? 'In Transit S-30 to S-38' : i < 30 ? 'Final Assembly (S-32..S-36)' : 'Buy-Off Yard',
    status: i < 15 ? 'Quarantined at S-38' : 'Flagged for Inspection',
  }));

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <GitBranch className="w-3.5 h-3.5 text-rose-600" />
              <span>Causal Association Network</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Defect Propagation Explorer & Genealogy
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Answers which upstream station is causing downstream defects, calculates defect lag time, and estimates surgical containment boundaries.
            </p>
          </div>

          {/* Statistical Association Caution */}
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 max-w-md text-xs text-amber-950 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold">Statistical Caution:</strong> Relationships represent empirical correlation and time-lag distributions across production runs, not hardwired physical causality. A human inspector must verify tooling root cause.
            </div>
          </div>
        </div>
      </Card>

      {/* 1. Defect Propagation Network Visual Grid */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
          <span className="text-amber-600">/</span>
          Active Upstream-to-Downstream Defect Propagation Channels
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {DEFECT_RELATIONSHIPS.map((rel) => {
            const isSelected = rel.id === selectedRel.id;
            return (
              <Card
                key={rel.id}
                onClick={() => setSelectedRelId(rel.id)}
                className={`p-4 transition-all cursor-pointer ${
                  isSelected
                    ? 'border-rose-500 shadow-sm ring-2 ring-rose-500/20'
                    : 'hover:border-zinc-300'
                }`}
              >
                <div className="flex items-center justify-between text-xs mb-2">
                  <span className="font-mono font-bold text-zinc-500">{rel.id}</span>
                  <Badge variant="destructive" className="text-[10px]">
                    {rel.observedCases} Cases Logged
                  </Badge>
                </div>

                <div className="flex items-center justify-between gap-2 py-2 border-y border-zinc-100 text-xs">
                  <div className="text-zinc-900 font-semibold">
                    <div className="font-mono">{rel.sourceStationId}</div>
                    <div className="text-[11px] text-zinc-500 font-normal">{rel.sourceStationName}</div>
                  </div>
                  <div className="flex flex-col items-center px-1">
                    <span className="text-[10px] text-rose-700 font-bold font-mono">{rel.typicalLagFormatted} lag</span>
                    <ArrowRight className="w-4 h-4 text-rose-600 my-0.5" />
                  </div>
                  <div className="text-right text-zinc-900 font-semibold">
                    <div className="font-mono">{rel.detectedStationId}</div>
                    <div className="text-[11px] text-zinc-500 font-normal">{rel.detectedStationName}</div>
                  </div>
                </div>

                <div className="mt-2.5 text-[11px] text-zinc-600 line-clamp-2">
                  {rel.defectDescription}
                </div>

                <div className="mt-2 pt-2 border-t border-zinc-100 flex items-center justify-between text-[10px]">
                  <span className="text-zinc-400">Correlation:</span>
                  <span className="font-semibold text-zinc-900 font-mono">{rel.correlationStrengthPct}%</span>
                </div>
              </Card>
            );
          })}
        </div>
      </div>

      {/* 2. Selected Relationship Evidence Detail */}
      <Card className="p-5 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-zinc-100 pb-3">
          <div>
            <h3 className="text-sm font-bold text-zinc-950">
              Selected Channel: {selectedRel.sourceStationId} ({selectedRel.sourceStationName}) → {selectedRel.detectedStationId} ({selectedRel.detectedStationName})
            </h3>
            <p className="text-xs text-zinc-600 mt-0.5">{selectedRel.defectDescription}</p>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <Badge variant="outline">
              Confidence: <strong className="ml-1">{selectedRel.statisticalConfidence}</strong>
            </Badge>
            <Badge variant="secondary" className="bg-rose-50 text-rose-900 border-rose-200">
              Typical Lag: {selectedRel.typicalLagFormatted}
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/70 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[10px]">Total Observed Occurrences</div>
            <div className="text-lg font-bold text-zinc-950">{selectedRel.observedCases} validated incidents</div>
            <div className="text-zinc-500 text-[11px]">Across 6 months production telemetry</div>
          </div>

          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/70 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[10px]">Association Strength</div>
            <div className="text-lg font-bold text-emerald-700">{selectedRel.correlationStrengthPct}% statistical match</div>
            <div className="text-zinc-500 text-[11px]">p &lt; 0.001 ANOVA regression fit</div>
          </div>

          <div className="p-3.5 rounded-lg border border-zinc-200 bg-zinc-50/70 space-y-1">
            <div className="text-zinc-500 uppercase font-semibold text-[10px]">Recent Impacted VIN Samples</div>
            <div className="text-xs font-semibold text-amber-900 font-mono space-y-0.5">
              {selectedRel.recentVinExamples.map((v) => (
                <div
                  key={v}
                  onClick={() => setSearchedVin(v)}
                  className="hover:underline cursor-pointer"
                >
                  {v}
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* 3. VIN Genealogy Lookup & Containment Estimator (2-Column Grid) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Genealogy Lookup */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-zinc-400" />
              VIN Full Build Genealogy Lookup
            </h3>
            <span className="text-xs text-zinc-500 font-medium">Every Station, Tool & Operator</span>
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={searchedVin}
              onChange={(e) => setSearchedVin(e.target.value)}
              placeholder="Enter VIN e.g. MA1TA2XX7R1234536"
              className="flex-1 px-3 py-1.5 rounded-md border border-zinc-200 text-xs font-mono uppercase bg-white focus:outline-none focus:ring-1 focus:ring-zinc-900"
            />
            <Button
              size="sm"
              onClick={() => {}}
            >
              Lookup
            </Button>
          </div>

          {/* Genealogy Record Details */}
          <div className="rounded-lg border border-zinc-200 bg-zinc-50/50 p-3 space-y-3 text-xs">
            <div className="flex items-center justify-between border-b border-zinc-200/80 pb-2">
              <div>
                <span className="font-mono font-bold text-zinc-950">{searchedGenealogy.vin}</span>
                <span className="text-zinc-500 ml-2 font-medium">({searchedGenealogy.variant})</span>
              </div>
              <Badge variant="outline" className="bg-amber-50 text-amber-900 border-amber-300 font-semibold">
                {searchedGenealogy.status}
              </Badge>
            </div>

            {/* Station steps list */}
            <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
              {searchedGenealogy.steps.map((step, idx) => (
                <div
                  key={idx}
                  className={`p-2.5 rounded-md border text-xs ${
                    step.anomalyDetected
                      ? 'border-rose-300 bg-rose-50 text-rose-950'
                      : 'border-zinc-200 bg-white text-zinc-800'
                  }`}
                >
                  <div className="flex items-center justify-between font-semibold">
                    <span className="font-mono">{step.stationId} {step.stationName}</span>
                    <span className="text-zinc-400 font-normal font-mono">{step.timestamp}</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-zinc-500 mt-1">
                    <span className="flex items-center gap-1">
                      <User className="w-3 h-3 text-zinc-400" />
                      {step.operatorName} ({step.operatorId})
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Wrench className="w-3 h-3 text-zinc-400" />
                      {step.toolId}
                    </span>
                  </div>
                  {step.torqueNm && (
                    <div className="mt-1 text-[11px] text-zinc-700">
                      Torque: <strong className="font-mono">{step.torqueNm} Nm</strong> (Target: <span className="font-mono">{step.torqueTargetNm} Nm</span>)
                    </div>
                  )}
                  {step.anomalyDetected && (
                    <div className="mt-1.5 p-1.5 rounded bg-rose-100/90 border border-rose-300 text-[10px] text-rose-900 font-medium">
                      ⚠️ {step.anomalyNote}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </Card>

        {/* Containment Scope Estimator */}
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <Lock className="w-3.5 h-3.5 text-rose-600" />
              Surgical Containment Scope Estimator
            </h3>
            <Badge variant="destructive">47 Units Affected</Badge>
          </div>

          <Alert variant="destructive">
            <AlertTitle className="text-xs font-semibold">
              "If a defect is confirmed at S-30 starting 13:10, 47 units are affected. Listed below."
            </AlertTitle>
            <AlertDescription className="text-[11px] text-zinc-600 mt-0.5">
              ShadowLine limits containment to exact affected vehicles rather than quarantining full 350-unit shifts.
            </AlertDescription>
          </Alert>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-zinc-500 uppercase font-semibold text-[10px]">Source Station:</span>
            <input
              type="text"
              value={containmentStation}
              onChange={(e) => setContainmentStation(e.target.value)}
              className="w-20 p-1 rounded border border-zinc-200 bg-white text-center font-mono font-semibold"
            />
            <span className="text-zinc-500 uppercase font-semibold text-[10px] ml-2">Fault Start:</span>
            <input
              type="text"
              value={containmentTime}
              onChange={(e) => setContainmentTime(e.target.value)}
              className="w-20 p-1 rounded border border-zinc-200 bg-white text-center font-mono font-semibold"
            />
          </div>

          {/* Containment List */}
          <div className="rounded-lg border border-zinc-200 divide-y divide-zinc-200 max-h-56 overflow-y-auto text-xs">
            {affectedVins.slice(0, 10).map((u, i) => (
              <div key={i} className="p-2 flex items-center justify-between hover:bg-zinc-50">
                <div>
                  <span className="font-mono font-bold text-zinc-900">{u.vin}</span>
                  <span className="text-zinc-400 ml-2 text-[11px] font-mono">{u.timestamp}</span>
                </div>
                <div className="text-right">
                  <Badge variant="secondary" className="text-[10px] bg-rose-50 text-rose-800 border-rose-200 font-semibold">
                    {u.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
          <div className="text-[11px] text-zinc-400 text-center">
            Showing 10 of 47 quarantined VINs · Export manifest available in Settings
          </div>
        </Card>
      </div>
    </div>
  );
}

