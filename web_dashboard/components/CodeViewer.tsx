// @ts-nocheck
import React, { useState } from 'react';
import { Copy, FileCode, Sparkles, Check, ShieldCheck } from 'lucide-react';

interface CodeViewerProps {
  fileName: string;
  content: string;
  language?: string;
  onAnalyze: (code: string) => void;
}

export const CodeViewer: React.FC<CodeViewerProps> = ({ fileName, content, language, onAnalyze }) => {
  const lines = content.split('\n');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="h-full flex flex-col bg-[#1e1e1e] border border-slate-700 rounded-2xl overflow-hidden shadow-2xl animate-slide-in">
      <div className="h-12 bg-[#252526] border-b border-[#333] flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <FileCode size={16} className="text-blue-400" />
          <span className="text-sm font-mono text-slate-300 font-bold">{fileName}</span>
        </div>
        <div className="flex gap-2">
           <button onClick={() => onAnalyze(content)} className="flex items-center gap-2 px-3 py-1.5 bg-accent/20 hover:bg-accent/30 text-accent hover:text-white text-xs font-bold rounded-lg transition-all border border-accent/30">
             <Sparkles size={14} /> AI Audit
           </button>
           <button onClick={handleCopy} className="p-1.5 hover:bg-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors">
             {copied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
           </button>
        </div>
      </div>
      <div className="flex-1 overflow-auto custom-scrollbar font-mono text-sm leading-6 bg-[#1e1e1e] dir-ltr text-left relative">
        <div className="flex min-h-full">
          <div className="w-12 bg-[#1e1e1e] border-r border-[#333] flex flex-col items-end pr-3 pt-4 text-slate-600 select-none shrink-0">
            {lines.map((_, i) => <span key={i} className="text-[11px] leading-6">{i + 1}</span>)}
          </div>
          <div className="flex-1 p-4 pt-4">
            {lines.map((line, i) => <div key={i} className="whitespace-pre text-slate-300">{line}</div>)}
          </div>
        </div>
      </div>
    </div>
  );
};