import React, { useState, useEffect, useCallback } from 'react';
import { ScreenId, UserRole, AlertStatus, StationData } from './types';
import {
  INITIAL_STATIONS,
  INITIAL_ALERTS,
  SUPPRESSED_ALERTS,
  MODEL_TRUST_METRICS,
} from './data/mockData';
import { ApplicationShell2 } from './components/layout/ApplicationShell2';
import { HeaderNav } from './components/layout/HeaderNav';
import { ShadowLineApiClient } from './services/api';

// Screens
import { Screen1LiveLineView } from './components/screens/Screen1LiveLineView';
import { Screen2AlertQueue } from './components/screens/Screen2AlertQueue';
import { Screen3AlertDetail } from './components/screens/Screen3AlertDetail';
import { Screen4StationDetail } from './components/screens/Screen4StationDetail';
import { Screen5BottleneckHistory } from './components/screens/Screen5BottleneckHistory';
import { Screen6DefectPropagation } from './components/screens/Screen6DefectPropagation';
import { Screen7SensorCoverage } from './components/screens/Screen7SensorCoverage';
import { Screen8ModelTrustScorecard } from './components/screens/Screen8ModelTrustScorecard';
import { Screen9ImpactBusinessCase } from './components/screens/Screen9ImpactBusinessCase';
import { Screen10LinePortfolio } from './components/screens/Screen10LinePortfolio';
import { Screen11LineOnboarding } from './components/screens/Screen11LineOnboarding';
import { Screen12Settings } from './components/screens/Screen12Settings';

export default function App() {
  const [currentRole, setCurrentRole] = useState<UserRole>('supervisor');
  const [activeScreen, setActiveScreen] = useState<ScreenId>('live-line');
  const [selectedStationId, setSelectedStationId] = useState<string>('S-14');
  const [selectedAlertId, setSelectedAlertId] = useState<string>('ALT-01');

  // Backend connection state
  const [isBackendConnected, setIsBackendConnected] = useState<boolean>(false);

  // Simulation states
  const [isShadowMode, setIsShadowMode] = useState<boolean>(true);
  const [isLineStopped, setIsLineStopped] = useState<boolean>(false);
  const [isDegradedData, setIsDegradedData] = useState<boolean>(false);

  // Dynamic telemetry
  const [stations, setStations] = useState<StationData[]>(INITIAL_STATIONS);
  const [alerts, setAlerts] = useState(INITIAL_ALERTS);
  const [suppressedAlerts, setSuppressedAlerts] = useState(SUPPRESSED_ALERTS);
  const [alarmBudgetUsed, setAlarmBudgetUsed] = useState<number>(3);
  const alarmBudgetMax = 6;

  const [currentJph, setCurrentJph] = useState<number>(58);
  const targetJph = 62;
  const [unitsBuilt, setUnitsBuilt] = useState<number>(312);

  // Time simulation clock
  const [currentTimeStr, setCurrentTimeStr] = useState<string>('14:07');
  const currentShiftStr = 'Shift B';

  // Check backend health & connect
  const refreshBackendData = useCallback(async () => {
    const health = await ShadowLineApiClient.getHealth();
    if (health && health.status === 'UP') {
      setIsBackendConnected(true);
      setIsShadowMode(health.mode === 'SHADOW');

      // Fetch live alerts
      const liveAlerts = await ShadowLineApiClient.getAlerts();
      if (liveAlerts && liveAlerts.length > 0) {
        setAlerts((prev) => {
          // Map backend alert schemas
          return prev;
        });
      }
    } else {
      setIsBackendConnected(false);
    }
  }, []);

  useEffect(() => {
    refreshBackendData();
    const interval = setInterval(refreshBackendData, 10000);
    const disconnectWs = ShadowLineApiClient.connectWebSocket(
      (data) => {
        setIsBackendConnected(true);
        console.log('[ShadowLine Live Event]', data);
      },
      () => setIsBackendConnected(false)
    );

    return () => {
      clearInterval(interval);
      disconnectWs();
    };
  }, [refreshBackendData]);

  // Navigation helpers
  const handleSelectStation = (stationId: string) => {
    setSelectedStationId(stationId);
    setActiveScreen('station-detail');
  };

  const handleSelectAlert = (alertId: string) => {
    setSelectedAlertId(alertId);
    setActiveScreen('alert-detail');
  };

  const handleUpdateAlertStatus = async (alertId: string, status: AlertStatus) => {
    setAlerts((prev) =>
      prev.map((a) => (a.id === alertId ? { ...a, status } : a))
    );

    if (isBackendConnected) {
      if (status === 'Acknowledged') {
        await ShadowLineApiClient.acknowledgeAlert(alertId);
      } else if (status === 'Snoozed') {
        await ShadowLineApiClient.snoozeAlert(alertId, 30);
      } else if (status === 'Resolved') {
        await ShadowLineApiClient.markFalseAlarm(alertId, 'Resolved by operator');
      }
    }
  };

  const handleToggleShadowMode = async () => {
    const nextMode = !isShadowMode;
    setIsShadowMode(nextMode);
    if (isBackendConnected) {
      await ShadowLineApiClient.updateSettings({
        mode: nextMode ? 'SHADOW' : 'LIVE',
      });
    }
  };

  const handleInjectWhatIfFault = async (stationId: string, faultType: string) => {
    if (isBackendConnected) {
      const res = await ShadowLineApiClient.injectFault(stationId, faultType as any, 0.6);
      console.log('[What-If Fault Injected]', res);
    }

    // Visual feedback in UI: flag station S-14 as bottleneck risk
    setStations((prev) =>
      prev.map((s) =>
        s.id === stationId
          ? {
              ...s,
              cycleTimeSec: Math.round(s.cycleTimeSec ? s.cycleTimeSec * 1.35 : 74),
              bottleneckPrediction: {
                probabilityPct: 88,
                timeStr: '+1h 45m',
                minutesToImpact: 105,
                isPrimary: true,
              },
            }
          : s
      )
    );
    setSelectedStationId(stationId);
  };

  // Find currently selected alert for Screen 3
  const currentAlert =
    alerts.find((a) => a.id === selectedAlertId) ||
    suppressedAlerts.find((a) => a.id === selectedAlertId) ||
    alerts[0];

  return (
    <ApplicationShell2
      currentRole={currentRole}
      activeScreen={activeScreen}
      onNavigate={(screen) => setActiveScreen(screen)}
    >
      {/* Persistent Read-Only & Telemetry Header */}
      <HeaderNav
        currentRole={currentRole}
        onRoleChange={setCurrentRole}
        activeScreen={activeScreen}
        onNavigate={setActiveScreen}
        isShadowMode={isShadowMode}
        onToggleShadowMode={handleToggleShadowMode}
        alarmBudgetUsed={alarmBudgetUsed}
        alarmBudgetMax={alarmBudgetMax}
        currentTimeStr={currentTimeStr}
        currentShiftStr={currentShiftStr}
        currentJph={currentJph}
        targetJph={targetJph}
        unitsBuilt={unitsBuilt}
        isLineStopped={isLineStopped}
        onToggleLineStopped={() => setIsLineStopped(!isLineStopped)}
        isDegradedData={isDegradedData}
        onToggleDegradedData={() => setIsDegradedData(!isDegradedData)}
        isBackendConnected={isBackendConnected}
        onInjectWhatIfFault={handleInjectWhatIfFault}
      />

      {/* Screen Router */}
      <div className="flex-1 overflow-y-auto pb-12">
        {activeScreen === 'live-line' && (
          <Screen1LiveLineView
            stations={stations}
            onSelectStation={handleSelectStation}
            onSelectAlert={handleSelectAlert}
            isLineStopped={isLineStopped}
            isDegradedData={isDegradedData}
          />
        )}

        {activeScreen === 'alert-queue' && (
          <Screen2AlertQueue
            alerts={alerts}
            suppressedAlerts={suppressedAlerts}
            onSelectAlert={handleSelectAlert}
            onUpdateAlertStatus={handleUpdateAlertStatus}
            alarmBudgetUsed={alarmBudgetUsed}
            alarmBudgetMax={alarmBudgetMax}
          />
        )}

        {activeScreen === 'alert-detail' && (
          <Screen3AlertDetail
            alert={currentAlert}
            onBack={() => setActiveScreen('alert-queue')}
            onUpdateAlertStatus={handleUpdateAlertStatus}
            onSelectStation={handleSelectStation}
          />
        )}

        {activeScreen === 'station-detail' && (
          <Screen4StationDetail
            stations={stations}
            selectedStationId={selectedStationId}
            onSelectStation={setSelectedStationId}
          />
        )}

        {activeScreen === 'bottleneck-history' && (
          <Screen5BottleneckHistory
            stations={stations}
            onSelectStation={handleSelectStation}
          />
        )}

        {activeScreen === 'defect-explorer' && (
          <Screen6DefectPropagation onSelectStation={handleSelectStation} />
        )}

        {activeScreen === 'sensor-coverage' && (
          <Screen7SensorCoverage
            stations={stations}
            onSelectStation={handleSelectStation}
          />
        )}

        {activeScreen === 'model-trust' && (
          <Screen8ModelTrustScorecard
            metrics={MODEL_TRUST_METRICS}
            isShadowMode={isShadowMode}
          />
        )}

        {activeScreen === 'impact-business' && (
          <Screen9ImpactBusinessCase />
        )}

        {activeScreen === 'line-portfolio' && (
          <Screen10LinePortfolio
            onSelectLineA={() => {
              setActiveScreen('live-line');
            }}
          />
        )}

        {activeScreen === 'line-onboarding' && (
          <Screen11LineOnboarding stations={stations} />
        )}

        {activeScreen === 'settings' && (
          <Screen12Settings />
        )}
      </div>
    </ApplicationShell2>
  );
}
