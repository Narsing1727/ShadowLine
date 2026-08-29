import React, { useState } from 'react';
import { ScreenId, UserRole } from '../../types';
import {
  Activity,
  AlertOctagon,
  FileText,
  Sliders,
  History,
  GitBranch,
  Network,
  Award,
  DollarSign,
  Boxes,
  Compass,
  Settings as SettingsIcon,
  ChevronDown,
  PanelLeftClose,
  PanelLeftOpen,
  Cpu,
} from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';

interface ApplicationShell2Props {
  currentRole: UserRole;
  activeScreen: ScreenId;
  onNavigate: (screen: ScreenId) => void;
  children: React.ReactNode;
}

export function ApplicationShell2({
  currentRole,
  activeScreen,
  onNavigate,
  children,
}: ApplicationShell2Props) {
  const [collapsed, setCollapsed] = useState(false);
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({
    supervisor: true,
    manager: true,
    leadership: true,
    system: true,
  });

  const toggleGroup = (group: string) => {
    setOpenGroups((prev) => ({ ...prev, [group]: !prev[group] }));
  };

  const navItems = [
    {
      group: 'supervisor',
      groupTitle: 'Floor Supervisor',
      items: [
        { id: 'live-line' as ScreenId, label: 'Live Line View', icon: Activity, screenNum: '01' },
        { id: 'alert-queue' as ScreenId, label: 'Alert Queue', icon: AlertOctagon, screenNum: '02' },
        { id: 'alert-detail' as ScreenId, label: 'Alert Detail', icon: FileText, screenNum: '03' },
        { id: 'station-detail' as ScreenId, label: 'Station Detail', icon: Sliders, screenNum: '04' },
      ],
    },
    {
      group: 'manager',
      groupTitle: 'Plant Manager',
      items: [
        { id: 'bottleneck-history' as ScreenId, label: 'Bottleneck History', icon: History, screenNum: '05' },
        { id: 'defect-explorer' as ScreenId, label: 'Defect Propagation', icon: GitBranch, screenNum: '06' },
        { id: 'sensor-coverage' as ScreenId, label: 'Sensor Coverage Map', icon: Network, screenNum: '07' },
        { id: 'model-trust' as ScreenId, label: 'Model Trust Scorecard', icon: Award, screenNum: '08' },
      ],
    },
    {
      group: 'leadership',
      groupTitle: 'Executive Leadership',
      items: [
        { id: 'impact-business' as ScreenId, label: 'Impact & Business Case', icon: DollarSign, screenNum: '09' },
        { id: 'line-portfolio' as ScreenId, label: 'Line Portfolio', icon: Boxes, screenNum: '10' },
      ],
    },
    {
      group: 'system',
      groupTitle: 'System & Config',
      items: [
        { id: 'line-onboarding' as ScreenId, label: 'Line Auto-Discovery', icon: Compass, screenNum: '11' },
        { id: 'settings' as ScreenId, label: 'System Settings', icon: SettingsIcon, screenNum: '12' },
      ],
    },
  ];

  return (
    <div className="flex min-h-screen bg-zinc-50 text-zinc-950 font-sans">
      {/* Sidebar */}
      <aside
        className={`border-r border-zinc-200/80 bg-white flex flex-col justify-between transition-all duration-200 shrink-0 z-30 ${
          collapsed ? 'w-16' : 'w-64'
        }`}
      >
        {/* Sidebar Header: Brand & Collapse Toggle */}
        <div className="p-4 border-b border-zinc-100 flex items-center justify-between">
          {!collapsed ? (
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-lg bg-zinc-900 text-white flex items-center justify-center font-bold text-sm tracking-tight shrink-0 shadow-xs">
                SL
              </div>
              <div className="truncate">
                <div className="text-sm font-semibold tracking-tight text-zinc-900 leading-none">
                  ShadowLine
                </div>
                <div className="text-[11px] text-zinc-500 font-normal mt-1">
                  Predictive Digital Twin
                </div>
              </div>
            </div>
          ) : (
            <div className="w-8 h-8 mx-auto rounded-lg bg-zinc-900 text-white flex items-center justify-center font-bold text-xs shadow-xs">
              SL
            </div>
          )}

          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCollapsed(!collapsed)}
            className="h-8 w-8 text-zinc-500 hover:text-zinc-900"
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? (
              <PanelLeftOpen className="w-4 h-4" />
            ) : (
              <PanelLeftClose className="w-4 h-4" />
            )}
          </Button>
        </div>

        {/* Sidebar Navigation Groups */}
        <div className="flex-1 overflow-y-auto p-3 space-y-4">
          {navItems.map((group) => {
            const isRoleFocused =
              (currentRole === 'supervisor' && group.group === 'supervisor') ||
              (currentRole === 'manager' && group.group === 'manager') ||
              (currentRole === 'leadership' && group.group === 'leadership');

            return (
              <div key={group.group} className="space-y-1">
                {!collapsed ? (
                  <button
                    type="button"
                    onClick={() => toggleGroup(group.group)}
                    className="w-full flex items-center justify-between px-2 py-1 text-[11px] font-semibold uppercase tracking-wider text-zinc-400 hover:text-zinc-700 cursor-pointer"
                  >
                    <span className={isRoleFocused ? 'text-zinc-900 font-bold' : ''}>
                      {group.groupTitle}
                    </span>
                    <ChevronDown
                      className={`w-3 h-3 transition-transform ${
                        openGroups[group.group] ? 'rotate-0' : '-rotate-90'
                      }`}
                    />
                  </button>
                ) : (
                  <div className="border-t border-zinc-100 my-2" />
                )}

                {(collapsed || openGroups[group.group]) && (
                  <div className="space-y-0.5">
                    {group.items.map((item) => {
                      const isActive = activeScreen === item.id;
                      const Icon = item.icon;

                      return (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => onNavigate(item.id)}
                          title={collapsed ? `${item.screenNum} - ${item.label}` : undefined}
                          className={`w-full flex items-center gap-2.5 px-3 py-2 text-xs font-medium rounded-lg transition-all cursor-pointer ${
                            isActive
                              ? 'bg-zinc-900 text-white shadow-xs'
                              : 'text-zinc-600 hover:bg-zinc-100/80 hover:text-zinc-900'
                          }`}
                        >
                          <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-zinc-500'}`} />
                          {!collapsed && (
                            <div className="flex items-center justify-between w-full truncate">
                              <span className="truncate">{item.label}</span>
                              <span
                                className={`text-[10px] ml-1 font-mono font-normal ${
                                  isActive ? 'text-zinc-300' : 'text-zinc-400'
                                }`}
                              >
                                {item.screenNum}
                              </span>
                            </div>
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Sidebar Footer / User Profile */}
        <div className="p-3 border-t border-zinc-100 bg-zinc-50/50">
          {!collapsed ? (
            <div className="flex items-center gap-2.5 px-1 py-0.5">
              <div className="w-8 h-8 rounded-full bg-zinc-200 text-zinc-700 flex items-center justify-center font-medium text-xs shrink-0">
                JD
              </div>
              <div className="truncate text-xs">
                <div className="font-semibold text-zinc-900 truncate">John Doe</div>
                <div className="text-[11px] text-zinc-500 truncate capitalize">
                  {currentRole} · Plant 2
                </div>
              </div>
            </div>
          ) : (
            <div className="w-8 h-8 mx-auto rounded-full bg-zinc-200 text-zinc-700 flex items-center justify-center font-medium text-xs">
              JD
            </div>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-x-hidden">
        {children}
      </main>
    </div>
  );
}

