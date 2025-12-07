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
    <div className="h-full flex flex-col bg-[#1e1e1e] border border-slate-700 rounded-2xl overflow-hidden shadow-2xl animate-slide-in group/container">
      
      {/* Header */}
      <div className="h-12 bg-[#252526] border-b border-[#333] flex items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <FileCode size={16} className="text-blue-400" />
          <span className="text-sm font-mono text-slate-300 font-bold">{fileName}</span>
          <span className="text-[10px] bg-slate-700 text-slate-400 px-2 py-0.5 rounded-full ml-2 uppercase tracking-wide opacity-80">
            {language || 'text'}
          </span>
        </div>
        
        <div className="flex gap-2">
           <button 
             onClick={() => onAnalyze(content)}
             className="flex items-center gap-2 px-3 py-1.5 bg-accent/20 hover:bg-accent/30 text-accent hover:text-white text-xs font-bold rounded-lg transition-all border border-accent/30 hover:border-accent/60 active:scale-95 group/btn"
           >
             <Sparkles size={14} className="group-hover/btn:scale-110 transition-transform" />
             AI Audit
           </button>
           
           <button 
             onClick={handleCopy}
             className="p-1.5 hover:bg-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors relative"
             title="Copy Code"
           >
             <div className={`absolute inset-0 flex items-center justify-center transition-all duration-300 ${copied ? 'scale-100 opacity-100' : 'scale-50 opacity-0'}`}>
               <Check size={16} className="text-emerald-400" />
             </div>
             <div className={`absolute inset-0 flex items-center justify-center transition-all duration-300 ${copied ? 'scale-50 opacity-0' : 'scale-100 opacity-100'}`}>
               <Copy size={16} />
             </div>
           </button>
        </div>
      </div>

      {/* Code Area */}
      <div className="flex-1 overflow-auto custom-scrollbar font-mono text-sm leading-6 bg-[#1e1e1e] dir-ltr text-left relative">
        <div className="flex min-h-full">
          
          {/* Line Numbers */}
          <div className="w-12 bg-[#1e1e1e] border-r border-[#333] flex flex-col items-end pr-3 pt-4 text-slate-600 select-none shrink-0 opacity-50 group-hover/container:opacity-100 transition-opacity">
            {lines.map((_, i) => (
              <span key={i} className="text-[11px] leading-6 hover:text-slate-400 cursor-pointer">{i + 1}</span>
            ))}
          </div>

          {/* Actual Code */}
          <div className="flex-1 p-4 pt-4">
            {lines.map((line, i) => (
              <div key={i} className="whitespace-pre text-slate-300 hover:bg-white/5 transition-colors rounded-sm px-1 -mx-1">
                <SyntaxHighlighter line={line} />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="h-7 bg-[#007acc] text-white flex items-center px-4 justify-between text-[10px] font-mono">
        <div className="flex gap-4">
          <span className="flex items-center gap-1"><ShieldCheck size={10}/> Secure Mode</span>
          <span>UTF-8</span>
        </div>
        <div className="flex gap-4">
          <span>Ln {lines.length}, Col 0</span>
          <span>Spaces: 4</span>
        </div>
      </div>
    </div>
  );
};

const SyntaxHighlighter = ({ line }: { line: string }) => {
  // Comment detection (Simple)
  if (line.trim().startsWith('#') || line.trim().startsWith('//')) {
    return <span className="text-green-600/80 italic">{line}</span>;
  }

  return (
    <>
      {line.split(/(\s+|[().,=:\[\]{}'"])/g).map((part, wIdx) => {
         let color = 'text-slate-300';
         // Keywords
         if (['import', 'from', 'def', 'class', 'return', 'if', 'else', 'elif', 'try', 'except', 'async', 'await', 'for', 'in', 'while', 'break', 'continue', 'pass', 'raise'].includes(part)) color = 'text-purple-400 font-bold';
         // Built-ins
         else if (['print', 'len', 'range', 'open', 'str', 'int', 'float', 'super', 'list', 'dict', 'set'].includes(part)) color = 'text-yellow-300';
         // Strings
         else if (part.startsWith('"') || part.startsWith("'") || part.endsWith('"') || part.endsWith("'")) color = 'text-orange-300';
         // Booleans/None
         else if (['True', 'False', 'None'].includes(part)) color = 'text-blue-400';
         // Class/Self/Decorators
         else if (['self', 'cls'].includes(part)) color = 'text-rose-300 italic';
         else if (part.startsWith('@')) color = 'text-yellow-500';
         
         return <span key={wIdx} className={color}>{part}</span>;
      })}
    </>
  );
};