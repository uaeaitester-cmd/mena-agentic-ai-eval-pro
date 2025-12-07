
// @ts-nocheck
import React, { useState, useRef, useEffect } from 'react';
import { Bot, User, Sparkles, Zap, ArrowUp, Copy, Check, Download } from 'lucide-react';
import { askArchitect } from '../services/geminiService';

const SUGGESTED_QUESTIONS = [
  "تحلیل مشکلات توکنایزر فارسی",
  "راهکار کاهش بایاس جنسیتی در عربی",
  "بررسی امنیت کدهای پایتون",
  "مقایسه عملکرد Llama-3 و Gemini"
];

// تعریف دقیق تایپ پیام‌ها
interface Message {
  role: 'ai' | 'user';
  content: string;
}

// اینترفیس پراپ‌ها: دریافت وضعیت از والد
interface AIChatProps {
  initialPrompt?: string | null;
  onClearPrompt?: () => void;
  messages: Message[]; 
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>; 
}

export const AIChat: React.FC<AIChatProps> = ({ initialPrompt, onClearPrompt, messages, setMessages }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // اگر تاریخچه خالی است (اولین بار)، پیام خوش‌آمدگویی را ست کن
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        { role: 'ai', content: 'سلام! من دستیار هوشمند ارشد (Senior Architect Agent) هستم. تمام کدهای مخزن را تحلیل کرده‌ام. درباره چالش‌های NLP فارسی یا عربی سوالی دارید؟' }
      ]);
    }
  }, []); 

  // هندل کردن پرامپت‌های ارسالی از بخش‌های دیگر (مثل CodeViewer)
  useEffect(() => {
    if (initialPrompt && !loading) {
      handleSend(initialPrompt);
      if (onClearPrompt) onClearPrompt();
    }
  }, [initialPrompt]);

  // اسکرول خودکار به پایین
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;
    
    // ۱. افزودن پیام کاربر
    const userMsg: Message = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    // ۲. دریافت پاسخ از سرویس
    const response = await askArchitect(text);
    
    // ۳. افزودن پاسخ هوش مصنوعی
    setMessages(prev => [...prev, { role: 'ai', content: response }]);
    setLoading(false);
  };

  const handleExportChat = () => {
    const text = messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n\n---\n\n');
    const blob = new Blob([text], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat-history.md';
    a.click();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-14rem)] bg-slate-900/50 border border-slate-700/50 rounded-3xl overflow-hidden backdrop-blur-sm shadow-2xl relative">
      
      {/* Header */}
      <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-accent to-purple-600 flex items-center justify-center shadow-lg shadow-accent/20">
            <Bot size={20} className="text-white" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">دستیار تخصصی NLP</h3>
            <p className="text-[10px] text-emerald-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
              Persistent Memory | Online
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExportChat}
            className="text-xs text-slate-500 hover:text-white transition-colors flex items-center gap-1 bg-slate-800/50 px-2 py-1 rounded-lg"
            title="Export Chat"
          >
            <Download size={14} />
          </button>
          <button 
            className="text-xs text-slate-500 hover:text-rose-400 transition-colors flex items-center gap-1 bg-slate-800/50 px-2 py-1 rounded-lg" 
            onClick={() => setMessages([])}
            title="Clear Chat"
          >
            <Zap size={14} />
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scroll-smooth custom-scrollbar">
        {messages.map((m, i) => (
          <div key={i} className={`flex gap-4 ${m.role === 'user' ? 'flex-row-reverse' : ''} animate-slide-in`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 ${
              m.role === 'ai' ? 'bg-slate-800 border border-slate-700' : 'bg-accent border border-accent'
            }`}>
              {m.role === 'ai' ? <Sparkles size={14} className="text-accent" /> : <User size={14} className="text-white" />}
            </div>
            
            <div className={`flex flex-col max-w-[90%] lg:max-w-[80%] ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`p-4 rounded-2xl text-sm leading-7 shadow-sm overflow-hidden ${
                m.role === 'user' 
                  ? 'bg-accent text-white rounded-tr-none' 
                  : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700/50'
              }`}>
                <MessageContent 
                  content={m.content} 
                  shouldType={m.role === 'ai' && i === messages.length - 1 && !loading} 
                />
              </div>
              <span className="text-[10px] text-slate-600 mt-1 px-1">
                {new Date().toLocaleTimeString('fa-IR', {hour: '2-digit', minute:'2-digit'})}
              </span>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex gap-4 animate-pulse">
             <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
               <Sparkles size={14} className="text-accent" />
             </div>
             <div className="bg-slate-800/50 p-4 rounded-2xl rounded-tl-none border border-slate-700/50 flex gap-1 items-center h-12">
               <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></div>
               <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-100"></div>
               <div className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-200"></div>
             </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        {!loading && messages.length < 3 && (
          <div className="flex gap-2 overflow-x-auto pb-3 mb-1 no-scrollbar dir-rtl">
            {SUGGESTED_QUESTIONS.map((q, i) => (
              <button 
                key={i}
                onClick={() => handleSend(q)}
                className="whitespace-nowrap px-3 py-1.5 bg-slate-800/50 hover:bg-slate-700 border border-slate-700 hover:border-accent/50 rounded-full text-xs text-slate-300 hover:text-white transition-all"
              >
                {q}
              </button>
            ))}
          </div>
        )}

        <div className="relative group">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend(input)}
            placeholder="سوال تخصصی خود را بپرسید..."
            className="w-full bg-slate-950 border border-slate-700 rounded-xl py-4 pl-14 pr-4 text-slate-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all placeholder-slate-600 shadow-inner"
          />
          <button 
            onClick={() => handleSend(input)}
            disabled={loading || !input.trim()}
            className="absolute left-2 top-2 p-2 bg-accent hover:bg-indigo-500 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-accent/20 hover:scale-105 active:scale-95"
          >
            <ArrowUp size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

const MessageContent = ({ content, shouldType }: { content: string, shouldType: boolean }) => {
  const [displayedContent, setDisplayedContent] = useState(shouldType ? '' : content);

  useEffect(() => {
    if (!shouldType) {
      setDisplayedContent(content);
      return;
    }

    let i = 0;
    const speed = 10; 
    const step = 2;

    const timer = setInterval(() => {
      setDisplayedContent(content.slice(0, i));
      i += step;
      if (i > content.length) {
        setDisplayedContent(content);
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [content, shouldType]);

  const parts = displayedContent.split(/```/);

  return (
    <div className="space-y-2">
      {parts.map((part, index) => {
        if (index % 2 === 1) {
          const [lang, ...codeLines] = part.split('\n');
          const code = codeLines.join('\n').trim();
          return (
            <div key={index} className="my-3 rounded-lg overflow-hidden border border-slate-700/50 bg-[#0d1117] dir-ltr text-left relative group">
              <div className="flex justify-between items-center px-3 py-1.5 bg-slate-800/50 border-b border-slate-700/30">
                <span className="text-[10px] text-slate-400 font-mono uppercase">{lang || 'CODE'}</span>
                <CopyButton text={code} />
              </div>
              <pre className="p-3 overflow-x-auto text-xs font-mono leading-5 text-slate-300">
                <code>{code}</code>
              </pre>
            </div>
          );
        } else {
          return part.split('\n').map((line, i) => (
             line.trim() && <p key={`${index}-${i}`} className="min-h-[1rem] whitespace-pre-wrap">{line}</p>
          ));
        }
      })}
    </div>
  );
};

const CopyButton = ({ text }: { text: string }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button onClick={handleCopy} className="text-slate-500 hover:text-white transition-colors">
      {copied ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
    </button>
  );
};