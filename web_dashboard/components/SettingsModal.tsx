// @ts-nocheck
import React, { useState } from 'react';
import { X, Save, Shield, Sliders, Zap } from 'lucide-react';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose }) => {
  const [threshold, setThreshold] = useState(85);
  const [autoMitigate, setAutoMitigate] = useState(true);
  const [useCache, setUseCache] = useState(true);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[150] flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in p-4">
      <div className="w-full max-w-md bg-[#0f172a] border border-slate-700 rounded-2xl shadow-2xl overflow-hidden relative">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
          <h3 className="text-white font-bold flex items-center gap-2">
            <Sliders size={18} className="text-accent" />
            تنظیمات سیستم
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-6">
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <label className="text-slate-300 font-medium flex items-center gap-2">
                <Shield size={14} className="text-emerald-400" />
                آستانه حساسیت بایاس
              </label>
              <span className="text-accent font-mono font-bold">{threshold}%</span>
            </div>
            <input 
              type="range" 
              min="50" 
              max="99" 
              value={threshold} 
              onChange={(e) => setThreshold(Number(e.target.value))}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-accent"
            />
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800">
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${autoMitigate ? 'bg-accent/20 text-accent' : 'bg-slate-800 text-slate-500'}`}>
                  <Zap size={16} />
                </div>
                <div>
                  <div className="text-sm font-bold text-slate-200">Auto-Mitigation</div>
                </div>
              </div>
              <button 
                onClick={() => setAutoMitigate(!autoMitigate)}
                className={`w-10 h-5 rounded-full transition-colors relative ${autoMitigate ? 'bg-emerald-500' : 'bg-slate-700'}`}
              >
                <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${autoMitigate ? 'left-6' : 'left-1'}`}></div>
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/30 flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 text-xs font-bold text-slate-400 hover:text-white transition-colors">
            انصراف
          </button>
          <button onClick={onClose} className="px-6 py-2 bg-accent hover:bg-indigo-500 text-white text-xs font-bold rounded-lg shadow-lg flex items-center gap-2">
            <Save size={14} />
            ذخیره
          </button>
        </div>

      </div>
    </div>
  );
};
