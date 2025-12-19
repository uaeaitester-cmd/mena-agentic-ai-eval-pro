// @ts-nocheck
import React from 'react';
import { GitBranch, Wifi, Zap } from 'lucide-react';

export const StatusBar: React.FC = () => {
  return (
    <div className="h-6 bg-[#0f172a] border-t border-slate-800 flex items-center justify-between px-3 text-[10px] font-mono text-slate-400 select-none z-50">
      <div className="flex items-center gap-4 h-full">
        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-accent animate-pulse"></div><span className="font-bold text-accent">ALIM AI CORE</span></div>
        <div className="flex items-center gap-1"><GitBranch size={10} /><span>main*</span></div>
      </div>
      <div className="flex items-center gap-4 h-full">
        <div className="flex items-center gap-1.5 text-emerald-500"><Zap size={10} /><span className="font-bold">Gemini 2.5-Flash</span></div>
        <div className="flex items-center gap-1"><Wifi size={10} /><span>Connected</span></div>
      </div>
    </div>
  );
};