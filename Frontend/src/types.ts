export type StationState = 'Active' | 'Blocked' | 'Starved' | 'Down';
export type ConfidenceTier = 'Measured' | 'Inferred' | 'Dark';
export type ZoneType = 'Body Shop' | 'Paint Shop' | 'Final Assembly';
export type VariantType = 'SUV-A' | 'Sedan-B' | 'EV-C';
export type AlertType = 'Bottleneck Forming' | 'Defect Risk' | 'Sensor Degraded' | 'Throughput Drift';
export type AlertStatus = 'New' | 'Acknowledged' | 'Snoozed' | 'Resolved' | 'Expired';
export type SimulationHorizon = 'now' | '+1h' | '+2h' | '+4h';
export type UserRole = 'supervisor' | 'manager' | 'leadership';
export type ScreenId =
  | 'live-line'          // Screen 1
  | 'alert-queue'       // Screen 2
  | 'alert-detail'      // Screen 3
  | 'station-detail'    // Screen 4
  | 'bottleneck-history'// Screen 5
  | 'defect-explorer'   // Screen 6
  | 'sensor-coverage'   // Screen 7
  | 'model-trust'       // Screen 8
  | 'impact-business'   // Screen 9
  | 'line-portfolio'    // Screen 10
  | 'line-onboarding'   // Screen 11
  | 'settings';         // Screen 12

export interface StationData {
  id: string; // e.g. "S-14"
  number: number;
  name: string; // e.g. "E-Coat"
  zone: ZoneType;
  confidence: ConfidenceTier;
  inferredSource?: string;
  darkReason?: string;
  darkUpgradeCost?: string;
  darkUpgradeSignal?: string;
  nextMaintenanceWindow?: string;
  currentState: StationState;
  simulatedState: {
    '+1h': StationState;
    '+2h': StationState;
    '+4h': StationState;
  };
  cycleTimeSec: number;
  taktTimeSec: number;
  activePeriodDurationSec: number; // e.g. 760s (12m 40s)
  bufferRight: {
    current: number;
    max: number;
  };
  bufferLeft?: {
    current: number;
    max: number;
  };
  bottleneckPrediction?: {
    probabilityPct: number;
    timeStr: string;
    minutesToImpact: number;
    isPrimary: boolean;
  };
  shiftStateBreakdown: {
    activePct: number;
    blockedPct: number;
    starvedPct: number;
    downPct: number;
  };
  cycleTimesByVariant: {
    'SUV-A': number;
    'Sedan-B': number;
    'EV-C': number;
  };
  unitsProcessedThisShift: number;
  equipmentVintage: 'Modern Instrumented' | 'Legacy Automated' | 'Manual Workstation';
  lastVins: string[];
  historicalDefectsCausedCount: number;
  defectNotes?: string;
}

export interface AlertItem {
  id: string;
  rank: number;
  type: AlertType;
  stationId: string;
  stationName: string;
  zone: ZoneType;
  summary: string;
  confidencePct: number;
  timeToImpactMin: number;
  unitsAtRisk?: number;
  ageMin: number;
  status: AlertStatus;
  evidence: string[];
  calibrationNote: string;
  recommendedActions: string[];
  expectedEffectTaken: string;
  expectedEffectNotTaken: string;
  assignedTo?: string;
  notes?: string[];
  isSuppressedByBudget?: boolean;
}

export interface DefectRelationship {
  id: string;
  sourceStationId: string;
  sourceStationName: string;
  detectedStationId: string;
  detectedStationName: string;
  typicalLagMinutes: number;
  typicalLagFormatted: string;
  observedCases: number;
  correlationStrengthPct: number;
  statisticalConfidence: string;
  defectDescription: string;
  recentVinExamples: string[];
}

export interface VinGenealogy {
  vin: string;
  variant: VariantType;
  timestampStart: string;
  currentStationId: string;
  status: 'In Progress' | 'Completed' | 'Quarantined';
  steps: {
    stationId: string;
    stationName: string;
    operatorId: string;
    operatorName: string;
    toolId: string;
    cycleTimeSec: number;
    torqueNm?: number;
    torqueTargetNm?: number;
    timestamp: string;
    anomalyDetected?: boolean;
    anomalyNote?: string;
  }[];
}

export interface LinePortfolioItem {
  id: string;
  name: string;
  plant: string;
  line: string;
  status: 'Live' | 'Shadow' | 'Discovering' | 'Not started';
  measuredCoveragePct: number;
  daysInShadow: number;
  precisionPct: number;
  taktTimeSec: number;
  targetJph: number;
  actualJph: number;
  rolloutEffortWeeks: number;
}

export interface ModelTrustMetrics {
  totalPredictions: number;
  correctPredictions: number;
  incorrectPredictions: number;
  precisionPct: number;
  recallPct: number;
  falseAlarmRatePct: number;
  meanLeadTimeMin: number;
  daysInShadowMode: number;
  operatorDisagreementsCount: number;
  promotionGatePassed: boolean;
  promotionGateCriteria: string;
  calibrationBuckets: {
    confidenceBucket: string;
    predictionsCount: number;
    actualCorrectCount: number;
    empiricalAccuracyPct: number;
  }[];
}

export type ModelTrustMetric = ModelTrustMetrics;

export interface LineAssumptions {
  downtimeCostPerMinute: number; // e.g. $2,400
  reworkCostPerUnit: number; // e.g. $850
  laborRatePerHour: number; // e.g. $78
  unitsPerShift: number; // e.g. 350
  taktTimeSeconds: number; // 58s
  targetJph: number; // 62
}

export interface LineOnboardingStage {
  stageNumber: number;
  title: string;
  description: string;
  status: 'completed' | 'in-progress' | 'pending';
  details: string;
}
