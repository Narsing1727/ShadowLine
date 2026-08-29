/**
 * ShadowLine API Client & Real-Time WebSocket Service
 * Connects the Frontend to the FastAPI backend with seamless fallback to mock data.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

export class ShadowLineApiClient {
  private static async request<T>(endpoint: string, options?: RequestInit): Promise<T | null> {
    try {
      const res = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...(options?.headers || {}),
        },
        ...options,
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      return await res.json();
    } catch (err) {
      console.warn(`[ShadowLine API] Fallback on ${endpoint}:`, err);
      return null;
    }
  }

  // Health
  static async getHealth() {
    return this.request<{ status: string; mode: string }>('/health');
  }

  // Line & State
  static async getLineMetadata() {
    return this.request<any>('/api/line');
  }

  static async getLineState(horizon?: string) {
    const q = horizon ? `?horizon=${horizon}` : '';
    return this.request<any>(`/api/line/state${q}`);
  }

  // Stations
  static async getStations() {
    return this.request<any[]>('/api/stations');
  }

  static async getStationDetail(stationId: string) {
    return this.request<any>(`/api/stations/${stationId}`);
  }

  static async getStationHistory(stationId: string) {
    return this.request<any>(`/api/stations/${stationId}/history`);
  }

  // Alerts
  static async getAlerts() {
    return this.request<any[]>('/api/alerts');
  }

  static async getSuppressedAlerts() {
    return this.request<any[]>('/api/alerts/suppressed');
  }

  static async acknowledgeAlert(alertId: string, operatorId: string = 'OP-FLOOR-01') {
    return this.request(`/api/alerts/${alertId}/acknowledge`, {
      method: 'POST',
      body: JSON.stringify({ operator_id: operatorId }),
    });
  }

  static async snoozeAlert(alertId: string, snoozeMinutes: number = 30) {
    return this.request(`/api/alerts/${alertId}/snooze`, {
      method: 'POST',
      body: JSON.stringify({ snooze_minutes: snoozeMinutes }),
    });
  }

  static async markFalseAlarm(alertId: string, reason: string = 'Operator verified normal operation') {
    return this.request(`/api/alerts/${alertId}/false-alarm`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    });
  }

  // Predictions & Defects
  static async getBottleneckForecast() {
    return this.request<any>('/api/predictions/bottleneck');
  }

  static async getDefectPropagation() {
    return this.request<any>('/api/defects/propagation');
  }

  static async getDefectContainment(stationId: string, defectCode: string = 'D-GENERAL') {
    return this.request<any>(`/api/defects/containment?causing_station_id=${stationId}&defect_code=${defectCode}`);
  }

  // Coverage, Trust & Impact
  static async getCoverage() {
    return this.request<any>('/api/coverage');
  }

  static async getTrustScorecard() {
    return this.request<any>('/api/trust/scorecard');
  }

  static async getPromotionGate() {
    return this.request<any>('/api/trust/promotion-gate');
  }

  static async getImpactSummary() {
    return this.request<any>('/api/impact');
  }

  static async updateImpactAssumptions(assumptions: any) {
    return this.request('/api/impact/assumptions', {
      method: 'PUT',
      body: JSON.stringify(assumptions),
    });
  }

  // Interactive What-If Fault Injection
  static async injectFault(stationId: string, faultType: 'drift' | 'breakdown' | 'intermittent' = 'drift', severity: number = 0.5) {
    return this.request('/api/line/inject-fault', {
      method: 'POST',
      body: JSON.stringify({ station_id: stationId, fault_type: faultType, severity }),
    });
  }

  static async triggerPredictionCycle() {
    return this.request('/api/line/run-cycle', {
      method: 'POST',
    });
  }

  // Settings & Mode
  static async getSettings() {
    return this.request<any>('/api/settings');
  }

  static async updateSettings(settings: { mode?: string; alarm_budget_per_operator_per_hour?: number; fork_interval_seconds?: number }) {
    return this.request('/api/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  }

  // Live WebSocket Connection
  static connectWebSocket(onMessage: (data: any) => void, onError?: (err: any) => void): () => void {
    let ws: WebSocket | null = null;
    try {
      ws = new WebSocket(WS_BASE_URL);
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage(data);
        } catch (e) {
          onMessage(event.data);
        }
      };
      ws.onerror = (e) => {
        if (onError) onError(e);
      };
    } catch (e) {
      console.warn('WebSocket connection failed, running in polling/mock mode.');
    }

    return () => {
      if (ws) ws.close();
    };
  }
}
