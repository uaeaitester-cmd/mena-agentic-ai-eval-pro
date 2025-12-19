// @ts-nocheck
import React, { useEffect, useRef, useState } from 'react';
import { X, Terminal, Cpu, CheckCircle2, AlertTriangle } from 'lucide-react';

interface TerminalLogsProps {
  onComplete: () => void;
  onClose: () => void;
}

const MOCK_LOGS = [
  { msg: "Initializing ALIM AI Security Protocol v2.1...", type: "info", delay: 100 },
  { msg: "Connecting to Secure Docker Container...", type: "info", delay: 800 },
  { msg: "Loading Tokenizer: sentencepiece_model.pb", type: "info", delay: 1500 },
  { msg: "Warning: ZWNJ (Zero-width non-joiner) detected in stream", type: "warn", delay: 2200 },
  { msg: "Applying Persian Morphology Filters...", type: "success", delay: 3000 },
  { msg: "Scanning 'pipeline.py' for hardcoded credentials...", type: "info", delay: 3800 },
  { msg: "Analyzing 'benchmarks_ar.json' for cultural bias...", type: "info", delay: 4500 },
  { msg: "Running Counterfactual Augmentation (CDA)...", type: "info", delay: 5200 },
  { msg: "Calculating ISO-27001 Compliance Score...", type: "info", delay: 6000 },
  { msg: "Generating Enterprise Audit Report...", type: "success", delay: 7000 },
  { msg: "Process Complete. Dashboard Updated.", type: "done", delay: 7500 },
];

export const TerminalLogs: React.FC<TerminalLogsProps> = ({ onComplete, onClose }) => {
  const [logs, setLogs] = useState<any[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let timeouts: ReturnType<typeof setTimeout>[] = [];
    
    MOCK_LOGS.forEach((log) => {
      const timeout = setTimeout(() => {
        setLogs(prev => [...prev, log]);
        if (log.type === 'done') {
          setTimeout(onComplete, 1000);
        }
      }, log.delay);
      timeouts.push(timeout);
    });

    return () => timeouts.forEach(clearTimeout);
  }, [onComplete]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="fixed inset-0 z-[1200] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-fade-in p-4">
      <div className="w-full max-w-2xl bg-[#0c0c0c] border border-slate-700 rounded-xl shadow-2xl overflow-hidden font-mono text-sm relative">
        
        {/* Terminal Header */}
        <div className="bg-[#1a1a1a] px-4 py-2 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-400">
            <Terminal size={14} />
            <span className="text-xs font-bold">root@alim-ai-core:~# ./run_audit.sh</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors">
            <X size={16} />
          </button>
        </div>

        {/* Logs Area */}
        <div ref={scrollRef} className="h-80 overflow-y-auto p-4 space-y-2 custom-scrollbar">
          {logs.map((log, idx) => (
            <div key={idx} className="flex items-start gap-3 animate-slide-in-fast">
              <span className="text-slate-600 min-w-[50px] text-[10px] pt-1">
                [{(new Date().getSeconds() + idx * 0.5).toFixed(3)}]
              </span>
              <div className="flex-1 break-words">
                {log.type === 'info' && <span className="text-slate-300">{log.msg}</span>}
                {log.type === 'warn' && <span className="text-yellow-400 flex items-center gap-2"><AlertTriangle size={12}/> {log.msg}</span>}
                {log.type === 'success' && <span className="text-emerald-400 flex items-center gap-2"><CheckCircle2 size={12}/> {log.msg}</span>}
                {log.type === 'done' && <span className="text-accent font-bold blink">{log.msg}</span>}
              </div>
            </div>
          ))}
          <div className="w-2 h-4 bg-slate-500 animate-pulse mt-2 inline-block"></div>
        </div>

        {/* Footer Status */}
        <div className="bg-[#1a1a1a] px-4 py-1.5 border-t border-slate-800 flex justify-between items-center text-[10px] text-slate-500">
          <div className="flex items-center gap-2">
            <Cpu size={12} className={logs.length < MOCK_LOGS.length ? "text-accent animate-spin" : "text-emerald-500"} />
            <span>CPU Usage: {Math.floor(Math.random() * 30 + 40)}%</span>
          </div>
          <span>Mem: 4.2GB / 16GB</span>
        </div>
      </div>
    </div>
  );
};