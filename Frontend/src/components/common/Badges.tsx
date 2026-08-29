import React from 'react';
import { ConfidenceTier, StationState } from '../../types';
import { CheckCircle2, AlertTriangle, EyeOff } from 'lucide-react';
import { Badge } from '../ui/badge';

export function ConfidenceBadge({
  tier,
  showLabel = true,
  className = '',
}: {
  tier: ConfidenceTier;
  showLabel?: boolean;
  className?: string;
}) {
  if (tier === 'Measured') {
    return (
      <Badge
        variant="success"
        title="Measured: Direct physical sensor telemetry available (99.4% confidence)"
        className={`gap-1 font-medium ${className}`}
      >
        <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
        {showLabel && <span>Measured</span>}
      </Badge>
    );
  }

  if (tier === 'Inferred') {
    return (
      <Badge
        variant="warning"
        title="Inferred: Estimated by soft sensor model from adjacent buffers and takt deviation"
        className={`gap-1 font-medium ${className}`}
      >
        <AlertTriangle className="w-3 h-3 text-amber-600 shrink-0" />
        {showLabel && <span>Inferred</span>}
      </Badge>
    );
  }

  return (
    <Badge
      variant="destructive"
      title="Dark: No sensor and insufficient signal to infer state. Manual work position."
      className={`gap-1 font-medium ${className}`}
    >
      <EyeOff className="w-3 h-3 text-rose-600 shrink-0" />
      {showLabel && <span>Dark</span>}
    </Badge>
  );
}

export function StateBadge({
  state,
  className = '',
}: {
  state: StationState;
  className?: string;
}) {
  switch (state) {
    case 'Active':
      return (
        <Badge variant="success" className={className}>
          Active
        </Badge>
      );
    case 'Blocked':
      return (
        <Badge variant="warning" className={className}>
          Blocked
        </Badge>
      );
    case 'Starved':
      return (
        <Badge variant="indigo" className={className}>
          Starved
        </Badge>
      );
    case 'Down':
      return (
        <Badge variant="destructive" className={className}>
          Down
        </Badge>
      );
  }
}

