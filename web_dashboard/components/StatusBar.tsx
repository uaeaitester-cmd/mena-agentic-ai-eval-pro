
// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { GitBranch, Wifi, Cpu, Bell, Check, XCircle, Zap, Server } from 'lucide-react';
import { backend } from '../services/backendService';

export const StatusBar: React.FC = () => {
  const [ping, setPing] = useState(24);
  const [cpu, setCpu] = useState(12);
  const [connection, setConnection] = useState<{ connected: boolean; source: string }>({ connected: false, source: 'Checking...' });

  // شبیه‌سازی تغییرات زنده و بررسی اتصال
  useEffect(() => {
    // بررسی وضعیت اتصال
    backend.getConnectionStatus().then(setConnection);

    const interval = setInterval(() => {
      setPing(prev => Math.max(10, prev + Math.floor(Math.random() * 5) - 2));
      setCpu(prev => Math.min(100, Math.max(5, prev + Math.floor(Math.random() * 5) - 2)));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-6 bg-[#0f172a] border-t border-slate-800 flex items-center justify-between px-3 text-[10px] font-mono text-slate-400 select-none z-50 animate-slide-up">
      
      {/* Left Section */}
      <div className="flex items-center gap-4 h-full">
        <div className="flex items-center gap-1.5 hover:text-white cursor-pointer transition-colors">
          <div className="w-2 h-2 rounded-full bg-accent animate-pulse"></div>
          <span className="font-bold text-accent">MENA EVAL CORE</span>
        </div>
        
        <div className="flex items-center gap-1 hover:text-white cursor-pointer transition-colors">
          <GitBranch size={10} />
          <span>main*</span>
        </div>

        <div className="hidden md:flex items-center gap-1 hover:text-white cursor-pointer transition-colors">
          <Server size={10} className={connection.connected ? "text-emerald-500" : "text-rose-500"} />
          <span className={connection.connected ? "text-emerald-500" : "text-rose-500"}>{connection.source}</span>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4 h-full">
        
        {/* AI Model Status */}
        <div className="flex items-center gap-1.5 text-emerald-500 hover:text-emerald-400 cursor-pointer transition-colors">
          <Zap size={10} />
          <span className="font-bold">Gemini 2.5-Flash</span>
        </div>

        {/* Metrics */}
        <div className="hidden md:flex items-center gap-3 border-l border-slate-800 pl-3 ml-1">
          <div className="flex items-center gap-1 w-16">
            <Cpu size={10} />
            <span>{cpu}%</span>
          </div>
          <div className="flex items-center gap-1 w-16">
            <Wifi size={10} />
            <span>{ping}ms</span>
          </div>
        </div>

        {/* Notification Bell */}
        <div className="flex items-center gap-1 hover:text-white cursor-pointer transition-colors border-l border-slate-800 pl-3">
          <Bell size={10} />
        </div>
        
        <div className="text-slate-600 pl-1">v2.1.0</div>
      </div>
    </div>
  );
};
