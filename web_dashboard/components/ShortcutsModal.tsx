
// @ts-nocheck
import React from 'react';
import { X, Command, Keyboard, CornerDownLeft, ArrowUp, ArrowDown } from 'lucide-react';

interface ShortcutsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ShortcutsModal: React.FC<ShortcutsModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const shortcuts = [
    { label: 'Open Command Palette', keys: [<Command size={12} />, 'K'] },
    { label: 'Run Live Scan', keys: ['Shift', 'R'] },
    { label: 'Close Modals', keys: ['Esc'] },
    { label: 'Show Shortcuts', keys: ['?'] },
    { label: 'Navigate Menu', keys: [<ArrowUp size={12} />, <ArrowDown size={12} />] },
    { label: 'Select Item', keys: [<CornerDownLeft size={12} />] },
  ];

  return (
    <div className="fixed inset-0 z-[1100] flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0" 
        onClick={onClose}
      />
      
      <div className="relative w-full max-w-md bg-[#0f172a] border border-slate-700 rounded-2xl shadow-2xl overflow-hidden animate-slide-up ring-1 ring-white/10">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center gap-2 text-white font-bold">
            <Keyboard size={18} className="text-accent" />
            <span>Keyboard Shortcuts</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="p-2">
          {shortcuts.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between px-4 py-3 hover:bg-slate-800/50 rounded-lg transition-colors group">
              <span className="text-sm text-slate-300 font-medium group-hover:text-white transition-colors">{item.label}</span>
              <div className="flex gap-1.5">
                {item.keys.map((k, i) => (
                  <kbd key={i} className="min-w-[24px] h-6 flex items-center justify-center px-1.5 bg-slate-800 border-b-2 border-slate-700 rounded text-[10px] font-mono text-slate-400 font-bold shadow-sm">
                    {k}
                  </kbd>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-900/50 border-t border-slate-800 text-[10px] text-slate-500 text-center">
          Press <span className="font-bold text-slate-400">Esc</span> to close
        </div>

      </div>
    </div>
  );
};