import React from 'react';
import { ModelTrustMetrics } from '../../types';
import { StatsCard6 } from '../common/StatsCard6';
import { ChartCard25 } from '../common/ChartCard25';
import { DataTable6, Column } from '../common/DataTable6';
import {
  Award,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';

interface Screen8ModelTrustScorecardProps {
  metrics: ModelTrustMetrics;
  isShadowMode: boolean;
}

export function Screen8ModelTrustScorecard({
  metrics,
  isShadowMode,
}: Screen8ModelTrustScorecardProps) {
  // Weekly accuracy trend data for ChartCard25
  const accuracyTrendData = [
    { name: 'W1', value: 62.4, precision: 62.4 },
    { name: 'W2', value: 64.1, precision: 64.1 },
    { name: 'W3', value: 65.8, precision: 65.8 },
    { name: 'W4', value: 67.2, precision: 67.2 },
    { name: 'W5', value: 69.0, precision: 69.0 },
    { name: 'W6', value: 70.4, precision: 70.4 },
    { name: 'W7', value: 71.0, precision: 71.0 },
  ];

  const calibrationColumns: Column<typeof metrics.calibrationBuckets[0]>[] = [
    {
      key: 'confidenceBucket',
      header: 'Predicted Confidence Tier',
      width: '200px',
      render: (b) => <span className="font-semibold text-zinc-900 font-mono">{b.confidenceBucket}</span>,
    },
    {
      key: 'predictionsCount',
      header: 'Total Predictions Made',
      align: 'right',
      width: '180px',
      render: (b) => <span className="font-mono text-zinc-600">{b.predictionsCount}</span>,
    },
    {
      key: 'actualCorrectCount',
      header: 'Actual Correct (Validated)',
      align: 'right',
      width: '190px',
      render: (b) => <span className="font-mono text-zinc-900 font-semibold">{b.actualCorrectCount}</span>,
    },
    {
      key: 'empiricalAccuracyPct',
      header: 'Empirical Accuracy (Realized)',
      align: 'right',
      width: '220px',
      render: (b) => {
        const diff = Math.abs(b.empiricalAccuracyPct - parseInt(b.confidenceBucket));
        return (
          <div className="flex items-center justify-end gap-2">
            <Badge variant="success">
              {b.empiricalAccuracyPct}% Actual
            </Badge>
            <span className="text-[10px] text-zinc-400 font-mono">
              (Δ {diff.toFixed(1)}%)
            </span>
          </div>
        );
      },
    },
    {
      key: 'calibrationRating',
      header: 'Statistical Calibration Status',
      render: (b) => (
        <span className="text-xs text-emerald-800 font-medium flex items-center gap-1">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          Well-calibrated (within ±1.8% target envelope)
        </span>
      ),
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Top Header */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <Award className="w-3.5 h-3.5 text-amber-600" />
              <span>Predictive Trust & Mathematical Calibration</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Model Trust Scorecard (91 Days in Shadow Mode)
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Proves that ShadowLine predictions are statistically grounded, well-calibrated, and meet the promotion gate criteria for live operator alerting.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-2.5 text-right text-xs">
              <div className="text-[10px] text-zinc-400 uppercase font-semibold">Total Forecasts Logged</div>
              <div className="text-lg font-bold text-zinc-950 font-mono">{metrics.totalPredictions.toLocaleString()}</div>
            </div>
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-2.5 text-right text-xs">
              <div className="text-[10px] text-emerald-700 uppercase font-semibold">Mean Advance Warning</div>
              <div className="text-lg font-bold text-emerald-950 font-mono">{metrics.meanLeadTimeMin} min before impact</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Promotion Gate Status Card */}
      <Card className="p-5 border-indigo-200 bg-indigo-50/40">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-indigo-900">
              <ShieldCheck className="w-4 h-4 text-indigo-600" />
              <span>Live Deployment Promotion Gate Status: PASSED</span>
            </div>
            <h3 className="text-sm font-semibold text-zinc-950">
              "{metrics.promotionGateCriteria}"
            </h3>
            <p className="text-xs text-zinc-600">
              4 consecutive weeks completed at {metrics.precisionPct}% precision (required &gt; 65%) and 3.2 avg hourly alerts (ceiling &lt; 6.0).
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="success" className="px-3 py-1.5 uppercase tracking-wider text-xs">
              Ready for Live Mode
            </Badge>
          </div>
        </div>
      </Card>

      {/* 3 Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard6
          title="Precision & Recall Performance"
          totalValue={`${metrics.precisionPct}% Precision`}
          subtitle={`${metrics.recallPct}% of all bottlenecks detected in advance`}
          breakdown={[
            { label: 'Validated Predictions', value: `${metrics.correctPredictions} / ${metrics.totalPredictions}`, colorClass: 'bg-emerald-500' },
            { label: 'Unrealized Predictions', value: `${metrics.incorrectPredictions}`, colorClass: 'bg-amber-500' },
            { label: 'False Alarm Rate', value: `${metrics.falseAlarmRatePct}%`, colorClass: 'bg-indigo-500' },
          ]}
        />

        <StatsCard6
          title="Advance Warning Lead Time"
          totalValue={`${metrics.meanLeadTimeMin} Minutes`}
          subtitle="Average notification lead before line cycle degradation"
          breakdown={[
            { label: 'Bottleneck Predictions', value: '41 min lead', colorClass: 'bg-amber-500' },
            { label: 'Defect Propagation Warnings', value: '28 min lead', colorClass: 'bg-rose-500' },
            { label: 'Throughput Drift Notices', value: '52 min lead', colorClass: 'bg-sky-500' },
          ]}
        />

        <StatsCard6
          title="Operator Feedback & Audit"
          totalValue={`${metrics.operatorDisagreementsCount} Reports`}
          subtitle="Direct supervisor feedback logged as training data"
          breakdown={[
            { label: 'Total Operator Disagreements', value: `${metrics.operatorDisagreementsCount} events`, colorClass: 'bg-rose-500' },
            { label: 'Retrained Model Iterations', value: '14 updates', colorClass: 'bg-emerald-500' },
            { label: 'Consecutive Stable Weeks', value: '4 weeks', colorClass: 'bg-indigo-500' },
          ]}
        />
      </div>

      {/* Accuracy Trend Chart (ChartCard25) */}
      <ChartCard25
        title="Weekly Precision Trend Over 91 Days Shadow Mode"
        subtitle="Tracking empirical model precision against the 65% live promotion threshold"
        data={accuracyTrendData}
        dataKey="precision"
        targetValue={65}
        targetLabel="Promotion Threshold (65%)"
        unit="%"
        height={240}
        gradientFrom="#0284c7"
        gradientTo="#bae6fd"
        strokeColor="#0369a1"
      />

      {/* Calibration Table: When model says 70% confident, is it 70% accurate? */}
      <DataTable6
        title="Probabilistic Calibration Matrix"
        description="For predictions made at 70% confidence, how often were they right? Proper calibration ensures operators can trust the stated percentages."
        data={metrics.calibrationBuckets}
        columns={calibrationColumns}
        keyExtractor={(b) => b.confidenceBucket}
      />
    </div>
  );
}

