import React from 'react';
import { StatsCard6 } from '../common/StatsCard6';
import { ChartCard25 } from '../common/ChartCard25';
import { List3Section } from '../common/List3Section';
import {
  DollarSign,
} from 'lucide-react';
import { Card } from '../ui/card';

export function Screen9ImpactBusinessCase() {
  const roiMonthlyTrendData = [
    { name: 'Month 1', value: 210, savings: 210 },
    { name: 'Month 2', value: 340, savings: 340 },
    { name: 'Month 3', value: 430, savings: 430 },
    { name: 'Month 4', value: 580, savings: 580 },
    { name: 'Month 5', value: 890, savings: 890 },
    { name: 'Month 6', value: 1296, savings: 1296 },
  ];

  const topInterventions = [
    {
      col1: '12 Oct · S-14 E-Coat',
      col2: 'Predictive thermal heater element replacement before burnout. Prevented 4.2h Paint Shop halt.',
      col3: '+$189,000 Saved',
    },
    {
      col1: '28 Sep · S-30 Engine Drop',
      col2: 'Torque drift advance notification. Prevented 47 powertrain harness pinch defects in containment.',
      col3: '+$117,000 Saved',
    },
    {
      col1: '04 Nov · S-09 Hemming',
      col2: 'Flange roller head wear APM alert. Prevented door gap fit rework on 84 SUV-A assemblies.',
      col3: '+$94,000 Saved',
    },
  ];

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto w-full">
      {/* Executive Hero Banner */}
      <Card className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-zinc-500">
              <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
              <span>Financial Return & Plant Productivity</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 tracking-tight mt-0.5">
              Impact & Business Case (Plant 2 — Line A)
            </h2>
            <p className="text-xs text-zinc-600 mt-0.5 max-w-3xl">
              Quantifies avoided downtime losses, scrap reduction, and OEE throughput gains realized through predictive simulation.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-2.5 text-right text-xs">
              <div className="text-[10px] text-emerald-700 uppercase font-semibold">Realized Net ROI</div>
              <div className="text-2xl font-bold text-emerald-950 font-mono">9.2x</div>
            </div>
            <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-2.5 text-right text-xs">
              <div className="text-[10px] text-zinc-400 uppercase font-semibold">Full Payback Period</div>
              <div className="text-lg font-bold text-zinc-900 font-mono">18 Days</div>
            </div>
          </div>
        </div>
      </Card>

      {/* 3 Large Value Pillar Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard6
          title="Total Financial Value Created"
          totalValue="$1,296,000"
          subtitle="Cumulative net value created this quarter"
          breakdown={[
            { label: 'Unplanned Downtime Avoided', value: '$828,000', percentage: '18.4 hours saved', colorClass: 'bg-emerald-600' },
            { label: 'Scrap & Rework Eliminated', value: '$468,000', percentage: '312 units saved', colorClass: 'bg-emerald-500' },
            { label: 'Annualized Run-Rate', value: '$5,184,000', colorClass: 'bg-indigo-600' },
          ]}
        />

        <StatsCard6
          title="Line OEE & Throughput Uplift"
          totalValue="+3.8% OEE"
          subtitle="Operational Equipment Effectiveness increase"
          breakdown={[
            { label: 'Current Line OEE', value: '88.4%', percentage: '+3.8% vs baseline', colorClass: 'bg-indigo-500' },
            { label: 'Line Takt Adherence', value: '94.2%', percentage: '+6.1%', colorClass: 'bg-indigo-600' },
            { label: 'Average JPH Rate', value: '58.4 JPH', percentage: 'vs 54.6 prev', colorClass: 'bg-indigo-700' },
          ]}
        />

        <StatsCard6
          title="Shift Performance Benchmarks"
          totalValue="Shift B Leading"
          subtitle="Cross-shift comparison on Line A"
          breakdown={[
            { label: 'Shift A (06:00 - 14:00)', value: '58.2 JPH', percentage: '88.1% OEE', colorClass: 'bg-amber-500' },
            { label: 'Shift B (14:00 - 22:00)', value: '59.1 JPH', percentage: '89.6% OEE', colorClass: 'bg-emerald-500' },
            { label: 'Shift C (22:00 - 06:00)', value: '55.4 JPH', percentage: '84.8% OEE', colorClass: 'bg-slate-500' },
          ]}
        />
      </div>

      {/* ChartCard25: Cumulative Savings Trend */}
      <ChartCard25
        title="Cumulative Realized Value vs Platform Cost"
        subtitle="Tracking net cost avoidance ($k) against initial ShadowLine investment"
        data={roiMonthlyTrendData}
        dataKey="value"
        targetValue={140}
        targetLabel="Platform Cost ($140k)"
        unit="$k"
        height={250}
        gradientFrom="#10b981"
        gradientTo="#a7f3d0"
        strokeColor="#059669"
      />

      {/* List3Section: Top 3 Value-Generating Interventions */}
      <List3Section
        sectionTitle="Highest-Value Autonomous Forecast Interventions (Shift / Quarter)"
        items={topInterventions}
        col1Header="Intervention Date & Station"
        col2Header="Predictive Action & Avoided Failure Mode"
        col3Header="Validated Net Cost Avoidance"
      />
    </div>
  );
}

