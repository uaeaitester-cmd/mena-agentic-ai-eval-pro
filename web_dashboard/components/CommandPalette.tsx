
// @ts-nocheck
import React, { useState, useEffect, useRef } from 'react';
import { Search, LayoutDashboard, BarChart3, FlaskConical, FolderTree, MessageSquare, Play, Trash2, Download, ArrowRight } from 'lucide-react';
import { Tab } from '../types';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (tab: Tab) => void;
  onAction: (action: string) => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose, onNavigate, onAction }) => {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on open
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  // Command List
  const commands = [
    { 
      section: 'Navigation (ناوبری)', 
      items: [
        { id: 'nav-dash', label: 'Go to Dashboard', icon: LayoutDashboard, action: () => onNavigate(Tab.DASHBOARD) },
        { id: 'nav-metrics', label: 'Go to Metrics', icon: BarChart3, action: () => onNavigate(Tab.METRICS) },
        { id: 'nav-lab', label: 'Go to NLP Lab', icon: FlaskConical, action: () => onNavigate(Tab.LAB) },
        { id: 'nav-files', label: 'Go to File Explorer', icon: FolderTree, action: () => onNavigate(Tab.FILES) },
        { id: 'nav-ai', label: 'Ask AI Architect', icon: MessageSquare, action: () => onNavigate(Tab.AI_AGENT) },
      ]
    },
    { 
      section: 'System Actions (عملیات)', 
      items: [
        { id: 'act-scan', label: 'Run Live Scan', icon: Play, action: () => onAction('RUN_SCAN') },
        { id: 'act-report', label: 'Download PDF Report', icon: Download, action: () => onAction('DOWNLOAD_REPORT') },
        { id: 'act-clear', label: 'Clear Chat History', icon: Trash2, action: () => onAction('CLEAR_CHAT') },
      ]
    }
  ];

  // Filter commands
  const filteredCommands = commands.map(section => ({
    ...section,
    items: section.items.filter(item => item.label.toLowerCase().includes(query.toLowerCase()))
  })).filter(section => section.items.length > 0);

  return (
    <div className="fixed inset-0 z-[1000] flex items-start justify-center pt-[15vh] px-4 animate-fade-in">
      
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl bg-[#0f172a] border border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col animate-slide-up-sm ring-1 ring-white/10">
        
        {/* Search Header */}
        <div className="flex items-center px-4 py-4 border-b border-slate-800">
          <Search size={20} className="text-slate-400 mr-3" />
          <input
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent text-lg text-white placeholder-slate-500 focus:outline-none font-sans"
            placeholder="Type a command or search..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Escape') onClose();
            }}
          />
          <div className="flex items-center gap-2">
            <kbd className="hidden md:inline-block px-2 py-1 bg-slate-800 border border-slate-700 rounded text-[10px] text-slate-400 font-mono">ESC</kbd>
          </div>
        </div>

        {/* List */}
        <div className="max-h-[60vh] overflow-y-auto custom-scrollbar p-2">
          {filteredCommands.length > 0 ? (
            filteredCommands.map((section, idx) => (
              <div key={idx} className="mb-2">
                <div className="px-3 py-2 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                  {section.section}
                </div>
                <div className="space-y-1">
                  {section.items.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => {
                        item.action();
                        onClose();
                      }}
                      className="w-full flex items-center justify-between px-3 py-3 rounded-lg hover:bg-slate-800 group transition-all text-left"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-slate-800 group-hover:bg-slate-700 flex items-center justify-center transition-colors border border-slate-700/50">
                          <item.icon size={16} className="text-slate-400 group-hover:text-white" />
                        </div>
                        <span className="text-sm text-slate-300 group-hover:text-white font-medium">{item.label}</span>
                      </div>
                      <ArrowRight size={14} className="text-slate-600 group-hover:text-accent opacity-0 group-hover:opacity-100 transition-all -translate-x-2 group-hover:translate-x-0" />
                    </button>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="py-12 text-center text-slate-500">
              <p>دستوری یافت نشد.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 bg-slate-900 border-t border-slate-800 flex justify-between items-center text-[10px] text-slate-500">
          <div className="flex gap-4">
            <span><strong>↑↓</strong> to navigate</span>
            <span><strong>↵</strong> to select</span>
          </div>
          <div className="font-mono">MENA Eval Pro v2.1</div>
        </div>

      </div>
    </div>
  );
};
