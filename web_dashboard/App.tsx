import { FileText, Globe, LayoutDashboard, Menu, PlayCircle, X } from 'lucide-react';
import React, { useState } from 'react';
import Dashboard from './components/Dashboard.js';
import Playground from './components/Playground.js';
import StrategyDoc from './components/StrategyDoc.js';
import { ViewState } from './types.js';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewState>('strategy');
  const [lang, setLang] = useState<'en' | 'ar' | 'fa'>('en');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Derived state for RTL
  const isRtl = lang === 'ar' || lang === 'fa';
  const direction = isRtl ? 'rtl' : 'ltr';

  // Fonts mapping
  const fontClass = isRtl ? 'font-rtl' : 'font-sans';

  const navItems = [
    { id: 'strategy', label: isRtl ? 'استراتژی محصول' : 'Product Strategy', icon: FileText },
    { id: 'dashboard', label: isRtl ? 'داشبورد' : 'Dashboard', icon: LayoutDashboard },
    { id: 'playground', label: isRtl ? 'آزمایشگاه' : 'Evaluation Lab', icon: PlayCircle },
  ];

  const handleNavClick = (view: ViewState) => {
    setCurrentView(view);
    setIsMobileMenuOpen(false);
  };

  return (
    <div className={`min-h-screen bg-slate-950 text-slate-200 transition-all duration-300 ${fontClass}`} dir={direction}>
      
      {/* Navigation Bar */}
      <nav className="fixed top-0 w-full z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 h-16">
        <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
          
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-aleem-500 to-aleem-700 rounded-lg flex items-center justify-center text-white font-bold text-xl">
              A
            </div>
            <span className="text-xl font-bold tracking-tight text-white hidden md:block">
              ALEEM <span className="text-slate-500 font-light">PLATFORM</span>
            </span>
          </div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1 bg-slate-800/50 p-1 rounded-full border border-slate-700">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id as ViewState)}
                  className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 transition-all ${
                    isActive 
                      ? 'bg-aleem-600 text-white shadow-lg shadow-aleem-900/50' 
                      : 'text-slate-400 hover:text-white hover:bg-slate-700'
                  }`}
                >
                  <Icon size={16} />
                  {item.label}
                </button>
              );
            })}
          </div>

          {/* Settings / Lang */}
          <div className="flex items-center gap-4">
            <div className="relative group">
              <button className="p-2 text-slate-400 hover:text-white transition-colors flex items-center gap-2">
                <Globe size={20} />
                <span className="uppercase text-xs font-bold">{lang}</span>
              </button>
              {/* Dropdown */}
              <div className={`absolute top-full ${isRtl ? 'left-0' : 'right-0'} mt-2 w-32 bg-slate-800 border border-slate-700 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 invisible group-hover:visible transition-all`}>
                <button onClick={() => setLang('en')} className="w-full text-left px-4 py-2 text-sm hover:bg-slate-700 text-slate-300 hover:text-white first:rounded-t-lg">English</button>
                <button onClick={() => setLang('ar')} className="w-full text-right px-4 py-2 text-sm hover:bg-slate-700 text-slate-300 hover:text-white font-rtl">العربية</button>
                <button onClick={() => setLang('fa')} className="w-full text-right px-4 py-2 text-sm hover:bg-slate-700 text-slate-300 hover:text-white font-rtl last:rounded-b-lg">فارسی</button>
              </div>
            </div>

            {/* Mobile Menu Toggle */}
            <button 
              className="md:hidden p-2 text-slate-400"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-slate-950 pt-20 px-6 md:hidden">
          <div className="flex flex-col gap-4">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id as ViewState)}
                className={`p-4 rounded-xl text-lg font-medium flex items-center gap-4 border ${
                  currentView === item.id 
                    ? 'bg-aleem-900/30 border-aleem-500 text-aleem-400' 
                    : 'bg-slate-900 border-slate-800 text-slate-400'
                }`}
              >
                <item.icon size={24} />
                {item.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <main className="pt-24 pb-12 px-4 md:px-8 max-w-7xl mx-auto min-h-screen">
        {currentView === 'strategy' && <StrategyDoc isRtl={isRtl} />}
        {currentView === 'dashboard' && <Dashboard isRtl={isRtl} />}
        {currentView === 'playground' && <Playground isRtl={isRtl} />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 text-center text-slate-600 text-sm">
        <p>
          © 2024 Aleem Platform. {isRtl ? 'ساخته شده برای آینده هوش مصنوعی در خاورمیانه.' : 'Built for the future of AI in MENA.'}
        </p>
      </footer>

    </div>
  );
};

export default App;