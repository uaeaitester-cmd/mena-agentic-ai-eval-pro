// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { LayoutDashboard, BarChart3, MessageSquare, FolderTree, CheckCircle, AlertCircle, Settings as SettingsIcon, Menu, X, FlaskConical, Command, ChevronRight, ShieldCheck } from 'lucide-react';
import { Tab, FileNode } from './types';

// اصلاح مسیرها (از @/ به ./)
import { ReportView } from './components/ReportView';
import { MetricsDashboard } from './components/MetricsDashboard';
import { AIChat } from './components/AIChat';
import { FileExplorer } from './components/FileExplorer';
import { TerminalLogs } from './components/TerminalLogs';
import { SettingsModal } from './components/SettingsModal';
import { CodeViewer } from './components/CodeViewer';
import { IntroScreen } from './components/IntroScreen';
import { NLPPlayground } from './components/NLPPlayground';
import { CommandPalette } from './components/CommandPalette';
import { StatusBar } from './components/StatusBar';
import { ShortcutsModal } from './components/ShortcutsModal';

export default function App() {
  const [showIntro, setShowIntro] = useState(() => {
    return !sessionStorage.getItem('introShown');
  });

  const [activeTab, setActiveTab] = useState<Tab>(Tab.DASHBOARD);
  const [toast, setToast] = useState<{msg: string, type: 'success' | 'info'} | null>(null);
  const [showTerminal, setShowTerminal] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showCmdPalette, setShowCmdPalette] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [aiPrompt, setAiPrompt] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<any[]>([]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setShowCmdPalette(prev => !prev);
      }
      if (e.key === '?' && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        setShowShortcuts(prev => !prev);
      }
      if (e.shiftKey && (e.key === 'R' || e.key === 'r')) {
        e.preventDefault();
        handleRunScan();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleIntroComplete = () => {
    setShowIntro(false);
    sessionStorage.setItem('introShown', 'true');
  };

  if (showIntro) {
    return <IntroScreen onComplete={handleIntroComplete} />;
  }

  const showToast = (msg: string, type: 'success' | 'info' = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleRunScan = () => setShowTerminal(true);
  
  const handleScanComplete = () => {
    setShowTerminal(false);
    showToast('تحلیل هوشمند با موفقیت به پایان رسید', 'success');
  };

  const handleAnalyzeCode = (code: string) => {
    const prompt = `لطفاً این قطعه کد را از نظر "امنیت"، "پرفورمنس" و "بایاس‌های احتمالی" تحلیل کن. اگر مشکلی دیدی، راه حل جایگزین (Refactored Code) را بنویس:\n\n\`\`\`python\n${code}\n\`\`\``;
    setAiPrompt(prompt);
    setActiveTab(Tab.AI_AGENT);
    showToast('کد به آزمایشگاه هوش مصنوعی ارسال شد', 'info');
  };

  const handleCommandAction = (action: string) => {
    switch (action) {
      case 'RUN_SCAN':
        handleRunScan();
        break;
      case 'DOWNLOAD_REPORT':
        setActiveTab(Tab.DASHBOARD);
        showToast('لطفاً از دکمه دانلود در داشبورد استفاده کنید', 'info');
        break;
      case 'CLEAR_CHAT':
        setChatMessages([]);
        showToast('تاریخچه چت پاکسازی شد', 'success');
        break;
    }
  };

  return (
    <div className="flex flex-col h-screen w-full bg-obsidian text-slate-200 font-sans selection:bg-accent/30 overflow-hidden animate-fade-in">
      
      <div className="flex flex-1 overflow-hidden relative">
        {showTerminal && <TerminalLogs onComplete={handleScanComplete} onClose={() => setShowTerminal(false)} />}
        <SettingsModal isOpen={showSettings} onClose={() => setShowSettings(false)} />
        <ShortcutsModal isOpen={showShortcuts} onClose={() => setShowShortcuts(false)} />
        <CommandPalette 
          isOpen={showCmdPalette} 
          onClose={() => setShowCmdPalette(false)} 
          onNavigate={setActiveTab}
          onAction={handleCommandAction}
        />

        {toast && (
          <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[200] animate-slide-in pointer-events-none">
            <div className={`px-4 py-2 rounded-xl border shadow-2xl flex items-center gap-2 backdrop-blur-md pointer-events-auto ${
              toast.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/50 text-emerald-400' : 'bg-slate-800/80 border-slate-700 text-white'
            }`}>
              {toast.type === 'success' ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
              <span className="text-sm font-bold">{toast.msg}</span>
            </div>
          </div>
        )}

        <div 
          className={`fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-md transition-all duration-500 ease-in-out ${
            isSidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
          }`}
          onClick={() => setIsSidebarOpen(false)}
        />

        <aside className={`
          fixed lg:static inset-y-0 right-0 z-50 w-72 bg-charcoal border-l border-slate-800 flex flex-col shadow-2xl
          transition-transform duration-500 cubic-bezier(0.4, 0, 0.2, 1)
          ${isSidebarOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'}
        `}>
          <div className="h-24 flex items-center justify-between px-6 border-b border-slate-800/50 bg-slate-900/50">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-accent to-purple-600 flex items-center justify-center shadow-lg shadow-accent/20 shrink-0">
                <ShieldCheck className="text-white" size={28} />
              </div>
              <div>
                <h1 className="font-black text-white tracking-tight text-xl">ALIM AI</h1>
                <p className="text-[10px] text-emerald-400 font-mono tracking-widest uppercase">Guardian Engine</p>
              </div>
            </div>
            <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden text-slate-400 hover:text-white transition-colors p-1 rounded-md hover:bg-slate-800">
              <X size={24} />
            </button>
          </div>

          <nav className="flex-1 py-6 px-3 space-y-2 overflow-y-auto custom-scrollbar">
            <NavButton active={activeTab === Tab.DASHBOARD} onClick={() => { setActiveTab(Tab.DASHBOARD); setIsSidebarOpen(false); }} icon={LayoutDashboard} label="داشبورد اصلی" />
            <NavButton active={activeTab === Tab.METRICS} onClick={() => { setActiveTab(Tab.METRICS); setIsSidebarOpen(false); }} icon={BarChart3} label="تحلیل متریک‌ها" />
            <NavButton active={activeTab === Tab.LAB} onClick={() => { setActiveTab(Tab.LAB); setIsSidebarOpen(false); }} icon={FlaskConical} label="آزمایشگاه NLP" />
            <NavButton active={activeTab === Tab.FILES} onClick={() => { setActiveTab(Tab.FILES); setIsSidebarOpen(false); }} icon={FolderTree} label="ساختار کد" />
            
            <div className="border-t border-slate-800 my-4 pt-4 px-2">
               <div className="text-[10px] text-slate-500 font-bold uppercase mb-2 px-2 tracking-wider">هوش مصنوعی</div>
               <NavButton active={activeTab === Tab.AI_AGENT} onClick={() => { setActiveTab(Tab.AI_AGENT); setIsSidebarOpen(false); }} icon={MessageSquare} label="دستیار علیم (Alim)" isSpecial />
            </div>
          </nav>
          
          <div className="p-4 border-t border-slate-800/50 bg-slate-900/30">
            <button onClick={() => setShowSettings(true)} className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-slate-800 transition-colors text-left group">
              <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center border border-slate-600 group-hover:border-white transition-colors shadow-sm">
                 <SettingsIcon size={16} className="text-slate-300 group-hover:text-white" />
              </div>
              <div>
                 <div className="text-xs font-bold text-white group-hover:text-accent transition-colors">تنظیمات</div>
                 <div className="text-[10px] text-slate-500">پیکربندی سیستم</div>
              </div>
            </button>
          </div>
        </aside>

        <main className="flex-1 flex flex-col relative overflow-hidden bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-indigo-950/20 via-obsidian to-obsidian">
          <header className="h-20 flex items-center justify-between px-4 lg:px-8 border-b border-slate-800/50 backdrop-blur-sm z-40">
            <div className="flex items-center gap-4">
              <button onClick={() => setIsSidebarOpen(true)} className="lg:hidden p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"><Menu size={24} /></button>
              <h2 className="text-lg lg:text-xl font-bold text-white flex items-center gap-2 truncate">
                {activeTab === Tab.DASHBOARD && 'گزارش وضعیت پروژه'}
                {activeTab === Tab.METRICS && 'آمار و ارقام فنی'}
                {activeTab === Tab.LAB && 'آزمایشگاه پردازش زبان (Sandbox)'}
                {activeTab === Tab.FILES && 'بازرسی کد (Code Inspection)'}
                {activeTab === Tab.AI_AGENT && 'دستیار هوشمند علیم'}
              </h2>
            </div>
            
            <div className="flex items-center gap-2 lg:gap-3">
               <button onClick={handleRunScan} className="px-3 py-2 lg:px-4 lg:py-2 bg-accent hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition shadow-lg shadow-accent/20 flex items-center gap-2 active:scale-95 group">
                <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse group-hover:scale-150 transition-transform"></span>
                <span className="hidden lg:inline">اجرای اسکن زنده</span><span className="lg:hidden">اسکن</span>
              </button>
            </div>
          </header>

          <div className="flex-1 overflow-y-auto p-4 lg:p-10 custom-scrollbar scroll-smooth">
            <div className="max-w-7xl mx-auto h-full">
              {activeTab === Tab.DASHBOARD && <ReportView />}
              {activeTab === Tab.METRICS && <MetricsDashboard />}
              {activeTab === Tab.LAB && <NLPPlayground />}
              {activeTab === Tab.AI_AGENT && <AIChat initialPrompt={aiPrompt} onClearPrompt={() => setAiPrompt(null)} messages={chatMessages} setMessages={setChatMessages} />}
              {activeTab === Tab.FILES && (
                <div className="grid grid-cols-12 gap-6 h-[calc(100vh-12rem)]">
                  <div className="col-span-12 lg:col-span-3 h-[40%] lg:h-full"><FileExplorer onSelectFile={setSelectedFile} selectedFile={selectedFile} /></div>
                  <div className="col-span-12 lg:col-span-9 h-[60%] lg:h-full">
                    {selectedFile && selectedFile.content ? (
                      <CodeViewer fileName={selectedFile.name} content={selectedFile.content} language={selectedFile.language} onAnalyze={handleAnalyzeCode} />
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center bg-slate-900/30 border border-slate-800/50 rounded-2xl border-dashed">
                        <FolderTree size={32} className="text-slate-500 mb-4" />
                        <h3 className="text-slate-400 font-bold mb-1">فایلی انتخاب نشده است</h3>
                        <p className="text-xs text-slate-600">یک فایل را برای مشاهده انتخاب کنید</p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
      <StatusBar />
    </div>
  );
}

const NavButton = ({ active, onClick, icon: Icon, label, isSpecial }: any) => (
  <button onClick={onClick} className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden ${active ? (isSpecial ? 'bg-accent text-white shadow-lg shadow-accent/25' : 'bg-slate-800 text-white shadow-md') : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'}`}>
    <Icon size={20} className={`relative z-10 ${active ? 'text-white' : isSpecial ? 'text-accent' : 'text-slate-400 group-hover:text-white transition-colors'}`} />
    <span className="hidden lg:block text-sm font-medium relative z-10">{label}</span>
    {active && !isSpecial && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_10px_#34d399] relative z-10"></div>}
    {!active && <ChevronRight size={14} className="ml-auto opacity-0 group-hover:opacity-50 transition-opacity -translate-x-2 group-hover:translate-x-0 relative z-10" />}
  </button>
);