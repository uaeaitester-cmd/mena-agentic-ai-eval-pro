import React from 'react';
import { 
  LayoutDashboard, PlayCircle, History, Settings, Shield, 
  Users, BarChart3, Database, Globe, Lock, Workflow,
  ChevronRight, Network
} from 'lucide-react';
import { ViewState } from '../types.js';

interface SidebarProps {
  currentView: ViewState;
  onChangeView: (view: ViewState) => void;
  isCollapsed?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ currentView, onChangeView, isCollapsed = false }) => {
  const menuGroups = [
    {
      title: 'OBSERVABILITY',
      items: [
        { id: 'dashboard', label: 'Mission Control', icon: <LayoutDashboard size={16} /> },
        { id: 'incidents', label: 'Incident Response', icon: <Shield size={16} /> },
        { id: 'network', label: 'Network Map', icon: <Globe size={16} /> },
      ]
    },
    {
      title: 'LABORATORY',
      items: [
        { id: 'playground', label: 'Neural Playground', icon: <PlayCircle size={16} /> },
        { id: 'models', label: 'Model Registry', icon: <Database size={16} /> },
        { id: 'evals', label: 'Batch Evals', icon: <BarChart3 size={16} /> },
      ]
    },
    {
      title: 'GOVERNANCE',
      items: [
        { id: 'users', label: 'Access Control', icon: <Users size={16} /> },
        { id: 'audit', label: 'Audit Logs', icon: <History size={16} /> },
        { id: 'compliance', label: 'Compliance Rules', icon: <Lock size={16} /> },
      ]
    },
    {
      title: 'SYSTEM',
      items: [
        { id: 'settings', label: 'Configuration', icon: <Settings size={16} /> },
        { id: 'api', label: 'API Keys', icon: <Network size={16} /> },
      ]
    }
  ];

  return (
    <div className="w-64 h-full bg-alim-panel border-r border-alim-border flex flex-col flex-shrink-0 z-30 shadow-2xl">
      {/* Branding */}
      <div className="h-14 flex items-center px-5 border-b border-alim-border bg-[#02050a]">
        <div className="flex items-center gap-3">
           <div className="w-6 h-6 rounded bg-blue-600 flex items-center justify-center">
             <Workflow className="text-white w-4 h-4" />
           </div>
           <div className="font-bold text-white tracking-wider text-sm flex gap-2">
             ALIM <span className="text-blue-500">PLATFORM</span>
           </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-4 custom-scrollbar">
        {menuGroups.map((group, groupIndex) => (
          <div key={groupIndex} className="mb-6">
            <div className="px-5 mb-2 text-[10px] font-bold text-slate-500 tracking-widest uppercase">
              {group.title}
            </div>
            <div className="space-y-[1px]">
              {group.items.map((item) => (
                <button
                  key={item.id}
                  onClick={() => onChangeView(item.id as ViewState)}
                  className={`w-full flex items-center justify-between px-5 py-2 text-xs transition-colors border-l-2 ${
                    currentView === item.id
                      ? 'bg-blue-500/10 text-blue-400 border-blue-500'
                      : 'text-slate-400 hover:text-white border-transparent hover:bg-white/5'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {item.icon}
                    <span>{item.label}</span>
                  </div>
                  {currentView === item.id && <ChevronRight size={12} />}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Connection Status Footer */}
      <div className="p-4 border-t border-alim-border bg-[#02050a] text-[10px]">
         <div className="flex justify-between items-center mb-2">
            <span className="text-slate-500">Connection</span>
            <span className="text-emerald-500">Encrypted (TLS 1.3)</span>
         </div>
         <div className="flex items-center gap-2 text-slate-400">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span>Socket: Connected</span>
         </div>
         <div className="mt-2 text-slate-600 font-mono">
            Latency: 14ms
         </div>
      </div>
    </div>
  );
};

export default Sidebar;