import React, { useState } from 'react';
import { AlertItem, AlertStatus } from '../../types';
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  FileQuestion,
  UserCheck,
  MessageSquare,
  Info,
  TrendingDown,
  TrendingUp,
} from 'lucide-react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription, AlertTitle } from '../ui/alert';

interface Screen3AlertDetailProps {
  alert: AlertItem;
  onBack: () => void;
  onUpdateAlertStatus: (alertId: string, status: AlertStatus) => void;
  onSelectStation: (stationId: string) => void;
}

export function Screen3AlertDetail({
  alert,
  onBack,
  onUpdateAlertStatus,
  onSelectStation,
}: Screen3AlertDetailProps) {
  const [newNote, setNewNote] = useState('');
  const [notes, setNotes] = useState<string[]>(alert.notes || [
    '14:08 - Supervisor verified bath temperature sensor on PLC cabinet 14A.',
  ]);
  const [assignedPerson, setAssignedPerson] = useState(alert.assignedTo || 'Unassigned');
  const [falseAlarmReason, setFalseAlarmReason] = useState('');
  const [showFalseAlarmModal, setShowFalseAlarmModal] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  const handleAddNote = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    setNotes([...notes, `${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - ${newNote}`]);
    setNewNote('');
  };

  const handleMarkFalseAlarm = () => {
    onUpdateAlertStatus(alert.id, 'Resolved');
    setFeedbackSubmitted(true);
    setShowFalseAlarmModal(false);
  };

  return (
    <div className="p-6 space-y-6 max-w-[1400px] mx-auto w-full">
      {/* Back button & Title Bar */}
      <div className="flex items-center justify-between border-b border-zinc-200/80 pb-3">
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={onBack}
            className="gap-1.5"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Alert Queue</span>
          </Button>
          <div className="flex items-center gap-2">
            <Badge variant="default">Rank #{alert.rank}</Badge>
            <Badge variant="warning">{alert.type}</Badge>
          </div>
        </div>

        {/* Status indicator */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-zinc-500 font-medium">Status:</span>
          <Badge variant="secondary">{alert.status}</Badge>
        </div>
      </div>

      {/* Hero Alert Title & Plain Language Summary */}
      <Card className="p-5 space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => onSelectStation(alert.stationId)}
                className="text-sm font-semibold text-zinc-900 hover:text-amber-700 underline cursor-pointer"
              >
                {alert.stationId} {alert.stationName}
              </button>
              <span className="text-zinc-300">·</span>
              <span className="text-xs text-zinc-500">{alert.zone}</span>
            </div>
            <h2 className="text-xl font-bold text-zinc-950 mt-1 tracking-tight">
              "{alert.summary}"
            </h2>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-right">
              <div className="text-[10px] text-zinc-400 uppercase font-semibold">Confidence</div>
              <div className="text-xl font-bold text-zinc-900 font-mono">{alert.confidencePct}%</div>
            </div>
            <div className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-right">
              <div className="text-[10px] text-amber-700 uppercase font-semibold">Time To Impact</div>
              <div className="text-xl font-bold text-amber-900 font-mono">
                {alert.timeToImpactMin === 0 ? 'Ongoing' : `${alert.timeToImpactMin} min`}
              </div>
            </div>
          </div>
        </div>

        {feedbackSubmitted && (
          <Alert variant="success">
            <CheckCircle2 className="h-4 w-4" />
            <AlertTitle>Operator feedback recorded</AlertTitle>
            <AlertDescription>
              Model weights will incorporate this disagreement in the next calibration cycle.
            </AlertDescription>
          </Alert>
        )}
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Evidence & Recommended Actions */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section 1: Why We Think This (Evidence List) */}
          <Card className="p-5 space-y-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              Why We Think This (Telemetry Evidence)
            </h3>
            <ul className="space-y-2 text-xs text-zinc-800">
              {alert.evidence.map((ev, idx) => (
                <li
                  key={idx}
                  className="p-3 rounded-md border border-zinc-200/80 bg-zinc-50/70 flex items-start gap-2.5"
                >
                  <span className="w-5 h-5 rounded-full bg-zinc-200 text-zinc-700 flex items-center justify-center font-bold text-[10px] shrink-0">
                    {idx + 1}
                  </span>
                  <span className="leading-relaxed font-medium text-zinc-900">
                    {ev}
                  </span>
                </li>
              ))}
            </ul>

            {/* Calibration note */}
            <div className="mt-4 p-3 rounded-md bg-amber-50/70 border border-amber-200 text-xs text-amber-950 flex items-start gap-2">
              <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <div>
                <strong>Calibration Reference:</strong> {alert.calibrationNote}
              </div>
            </div>
          </Card>

          {/* Section 2: Recommended Advisory Actions */}
          <Card className="p-5 space-y-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900">
              Advisory Recommendations (Human Decision Required)
            </h3>
            <div className="space-y-2 text-xs">
              {alert.recommendedActions.map((rec, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-md border border-emerald-200 bg-emerald-50/50 text-zinc-900 font-medium leading-relaxed"
                >
                  {rec}
                </div>
              ))}
            </div>

            {/* Expected Effect: Taken vs Not Taken */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="p-3.5 rounded-lg border border-emerald-200 bg-emerald-50/40 space-y-1">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-900 uppercase">
                  <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Expected if Action Taken</span>
                </div>
                <p className="text-xs text-zinc-700">{alert.expectedEffectTaken}</p>
              </div>

              <div className="p-3.5 rounded-lg border border-rose-200 bg-rose-50/40 space-y-1">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-rose-900 uppercase">
                  <TrendingDown className="w-3.5 h-3.5 text-rose-600" />
                  <span>Expected if Not Taken</span>
                </div>
                <p className="text-xs text-zinc-700">{alert.expectedEffectNotTaken}</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Col: Human Actions & Operator Feedback */}
        <div className="space-y-6">
          {/* Action Center */}
          <Card className="p-5 space-y-4">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900">
              Operator Control Actions
            </h3>

            <div className="space-y-2">
              <Button
                onClick={() => onUpdateAlertStatus(alert.id, 'Acknowledged')}
                className="w-full gap-2 bg-zinc-900 hover:bg-zinc-800"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Acknowledge Alert</span>
              </Button>

              <Button
                variant="outline"
                onClick={() => onUpdateAlertStatus(alert.id, 'Snoozed')}
                className="w-full gap-2"
              >
                <Clock className="w-4 h-4 text-zinc-500" />
                <span>Snooze 30 Minutes</span>
              </Button>

              {/* PROMINENT "Mark as False Alarm" */}
              <Button
                variant="destructive"
                onClick={() => setShowFalseAlarmModal(true)}
                className="w-full gap-2 bg-rose-50 border border-rose-300 text-rose-700 hover:bg-rose-100 shadow-none"
              >
                <FileQuestion className="w-4 h-4 text-rose-600" />
                <span>Mark as False Alarm</span>
              </Button>
              <p className="text-[11px] text-zinc-500 text-center">
                * Operator disagreement is critical model training feedback.
              </p>
            </div>

            {/* Assignment */}
            <div className="pt-3 border-t border-zinc-100 space-y-2 text-xs">
              <label className="font-semibold text-zinc-700 uppercase flex items-center gap-1.5">
                <UserCheck className="w-3.5 h-3.5 text-zinc-500" />
                Assigned Responder:
              </label>
              <select
                value={assignedPerson}
                onChange={(e) => setAssignedPerson(e.target.value)}
                className="w-full p-2 rounded-md border border-zinc-200 bg-white text-xs focus:ring-1 focus:ring-zinc-900 focus:outline-none"
              >
                <option value="Unassigned">Unassigned</option>
                <option value="D. Miller (Body Shop Lead)">D. Miller (Body Shop Lead)</option>
                <option value="M. Vance (Paint Process Eng)">M. Vance (Paint Process Eng)</option>
                <option value="J. Kowalski (Final Assembly Sup)">J. Kowalski (Final Assembly Sup)</option>
                <option value="K. Patel (Tooling Maintenance)">K. Patel (Tooling Maintenance)</option>
              </select>
            </div>
          </Card>

          {/* Shift Log / Operator Notes */}
          <Card className="p-5 space-y-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-900 flex items-center gap-2">
              <MessageSquare className="w-3.5 h-3.5 text-zinc-500" />
              Operator Shift Log ({notes.length})
            </h3>

            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {notes.map((n, i) => (
                <div
                  key={i}
                  className="p-2.5 rounded-md border border-zinc-200/80 bg-zinc-50 text-xs text-zinc-800 leading-normal"
                >
                  {n}
                </div>
              ))}
            </div>

            <form onSubmit={handleAddNote} className="flex gap-2 pt-2">
              <input
                type="text"
                placeholder="Add shift observation note..."
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                className="flex-1 px-3 py-1.5 rounded-md border border-zinc-200 text-xs bg-white focus:outline-none focus:border-zinc-800"
              />
              <Button
                type="submit"
                size="sm"
              >
                Add
              </Button>
            </form>
          </Card>
        </div>
      </div>

      {/* False Alarm Modal */}
      {showFalseAlarmModal && (
        <div className="fixed inset-0 bg-zinc-950/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <Card className="p-6 max-w-lg w-full space-y-4 shadow-xl border-zinc-300">
            <div className="flex items-center gap-2 text-rose-700">
              <FileQuestion className="w-5 h-5" />
              <h3 className="text-sm font-bold uppercase tracking-tight">
                Mark as False Alarm (Training Feedback)
              </h3>
            </div>
            <p className="text-xs text-zinc-600">
              Thank you for verifying. Please describe why this prediction or alert is invalid. This explanation will be fed into ShadowLine's reinforcement fine-tuning loop.
            </p>

            <textarea
              rows={3}
              placeholder="e.g. Tank heater setpoint was manually changed for experimental primer run; not a thermal fault."
              value={falseAlarmReason}
              onChange={(e) => setFalseAlarmReason(e.target.value)}
              className="w-full p-2.5 rounded-md border border-zinc-200 text-xs focus:outline-none focus:border-zinc-900"
            />

            <div className="flex items-center justify-end gap-2 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFalseAlarmModal(false)}
              >
                Cancel
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={handleMarkFalseAlarm}
              >
                Submit Feedback & Dismiss
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

