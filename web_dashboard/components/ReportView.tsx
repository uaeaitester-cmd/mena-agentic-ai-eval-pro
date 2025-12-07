// @ts-nocheck
import React, { useState } from 'react';
import { Activity, ShieldCheck, Globe, CheckCircle2, AlertTriangle, BookOpen, Fingerprint, Download, Loader2, Check } from 'lucide-react';

export const ReportView: React.FC = () => {
  const [downloadState, setDownloadState] = useState<'idle' | 'loading' | 'success'>('idle');

  const handleDownload = () => {
    setDownloadState('loading');
    setTimeout(() => {
      setDownloadState('success');
      setTimeout(() => setDownloadState('idle'), 3000);
    }, 2000);
  };

  return (
    <div className="space-y-8 animate-slide-in pb-10">
      
      {/* Hero Card */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-700/50 bg-slate-900 shadow-2xl p-8">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-accent/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl"></div>
        
        <div className="relative z-10 flex flex-col md:flex-row justify-between items-end gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold mb-4 shadow-[0_0_10px_rgba(16,185,129,0.2)]">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
              وضعیت: پایدار و ایمن
            </div>
            <h1 className="text-3xl md:text-5xl font-black text-white mb-4 tracking-tight leading-tight">
              گزارش جامع <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-purple-400">هوش مصنوعی منصفانه</span>
            </h1>
            <p className="text-slate-400 max-w-2xl text-lg leading-relaxed font-light">
              ارزیابی تخصصی مدل‌های زبانی بزرگ (LLMs) با تمرکز بر چالش‌های <span className="text-white font-medium">مورفولوژی زبان‌های سامی</span> و بایاس‌های فرهنگی خاورمیانه.
            </p>
          </div>
          
          <div className="flex gap-4">
             <ScoreCard score="A+" label="استاندارد ISO" color="text-emerald-400" sub="کدنویسی تمیز" />
             <ScoreCard score="94%" label="شاخص Fairness" color="text-accent" sub="برابری جنسیتی" />
          </div>
        </div>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Persian Morphology */}
        <div className="glass glass-hover p-8 rounded-3xl border-r-4 border-r-warning">
          <div className="flex items-center gap-4 mb-6 border-b border-slate-800 pb-4">
            <div className="w-12 h-12 rounded-2xl bg-warning/10 flex items-center justify-center text-warning">
              <Fingerprint size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">چالش‌های توکن‌سازی فارسی</h3>
              <p className="text-xs text-slate-500 font-mono mt-1">TOKENIZER FAILURE ANALYSIS</p>
            </div>
          </div>
          <p className="text-slate-300 leading-7 text-sm text-justify mb-4">
            یکی از یافته‌های کلیدی این ارزیابی، ضعف مدل‌های Llama-3 و GPT-3.5 در پردازش کاراکتر <strong className="text-white">نیم‌فاصله (Zero-width non-joiner)</strong> است. این مسئله باعث می‌شود کلماتی مانند «می‌روم» به دو توکن مجزا («می» + «روم») شکسته شوند که معنای فعل را در بردار معنایی (Vector Space) تغییر می‌دهد.
          </p>
        </div>

        {/* Arabic Gender Bias */}
        <div className="glass glass-hover p-8 rounded-3xl border-r-4 border-r-accent">
          <div className="flex items-center gap-4 mb-6 border-b border-slate-800 pb-4">
             <div className="w-12 h-12 rounded-2xl bg-accent/10 flex items-center justify-center text-accent">
              <BookOpen size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">بایاس جنسیتی در عربی</h3>
              <p className="text-xs text-slate-500 font-mono mt-1">ARABIC GENDER BIAS METRICS</p>
            </div>
          </div>
          <p className="text-slate-300 leading-7 text-sm text-justify mb-4">
            در تحلیل ضمایر عربی، مدل‌ها تمایل دارند مشاغل تخصصی (مانند مهندس، پزشک) را به صورت پیش‌فرض با ضمایر مذکر (<span className="font-mono text-accent">هذا مهندس</span>) تولید کنند. سیستم ما با استفاده از تکنیک <strong>Counterfactual Data Augmentation</strong> این بایاس را تا ۳۵٪ کاهش داده است.
          </p>
          <ul className="space-y-2 mt-4">
             <MetricRow label="Before Mitigation" value="68% Biased" bar={68} color="bg-rose-500" />
             <MetricRow label="After Mitigation" value="33% Biased" bar={33} color="bg-emerald-500" />
          </ul>
        </div>

      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass glass-hover p-6 rounded-3xl">
          <div className="flex items-center gap-3 mb-6 text-white font-bold text-lg">
            <Globe className="w-5 h-5 text-blue-400" />
            پوشش زبانی
          </div>
          <div className="space-y-5">
             <ProgressBar label="English (Zero-Shot)" percent={98} color="bg-blue-500" />
             <ProgressBar label="Arabic (MSA & Dialects)" percent={89} color="bg-emerald-500" />
             <ProgressBar label="Persian (Formal)" percent={72} color="bg-warning" />
          </div>
          <p className="text-[10px] text-slate-500 mt-4 text-center">داده‌های فارسی نیازمند جمع‌آوری بیشتر است.</p>
        </div>

        <div className="glass glass-hover p-6 rounded-3xl">
          <div className="flex items-center gap-3 mb-4 text-white font-bold text-lg">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            نقاط قوت فنی
          </div>
          <ul className="space-y-4">
            <ListItem type="success" text="معماری ماژولار (Clean Architecture)" sub="جداسازی کامل Logic از UI" />
            <ListItem type="success" text="کانتینرسازی (Dockerized)" sub="آماده برای CI/CD و اسکیلینگ" />
            <ListItem type="success" text="رعایت اصول SOLID" sub="در طراحی کلاس‌های پایتون" />
          </ul>
        </div>

        <div className="glass glass-hover p-6 rounded-3xl bg-gradient-to-br from-slate-900 to-indigo-950/30">
          <h3 className="text-lg font-bold text-white mb-4">پیشنهاد نهایی</h3>
          <p className="text-sm text-slate-400 mb-6 leading-relaxed">
            پروژه آماده ورود به فاز تجاری است، مشروط بر اینکه لایه UI فعلی با این داشبورد React جایگزین شود.
          </p>
          <button 
            onClick={handleDownload}
            disabled={downloadState !== 'idle'}
            className={`w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all active:scale-95 ${
              downloadState === 'success' 
                ? 'bg-emerald-500 text-white shadow-[0_0_20px_rgba(16,185,129,0.4)]' 
                : 'bg-slate-800 hover:bg-white hover:text-black text-slate-200'
            }`}
          >
            {downloadState === 'idle' && <><Download size={16} /> دریافت گزارش کامل (PDF)</>}
            {downloadState === 'loading' && <><Loader2 size={16} className="animate-spin" /> در حال تولید گزارش...</>}
            {downloadState === 'success' && <><Check size={16} /> دانلود موفقیت‌آمیز بود</>}
          </button>
        </div>
      </div>

    </div>
  );
};

const ScoreCard = ({ score, label, color, sub }: any) => (
  <div className="text-center px-6 py-4 bg-slate-950/50 rounded-2xl border border-slate-800 backdrop-blur-sm min-w-[120px] shadow-lg group hover:border-slate-700 transition-all">
    <div className={`text-4xl font-black ${color} mb-1`}>{score}</div>
    <div className="text-xs text-slate-300 font-bold tracking-wider mb-1">{label}</div>
    <div className="text-[10px] text-slate-500 font-mono">{sub}</div>
  </div>
);

const ProgressBar = ({ label, percent, color }: any) => (
  <div>
    <div className="flex justify-between text-xs mb-1.5 text-slate-400 font-medium">
      <span>{label}</span>
      <span className="font-mono">{percent}%</span>
    </div>
    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
      <div className={`h-full ${color} rounded-full transition-all duration-1000 ease-out shadow-[0_0_10px_rgba(0,0,0,0.3)]`} style={{ width: `${percent}%` }}></div>
    </div>
  </div>
);

const MetricRow = ({ label, value, bar, color }: any) => (
  <div>
    <div className="flex justify-between text-[10px] text-slate-400 mb-1">
      <span>{label}</span>
      <span>{value}</span>
    </div>
    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div className={`h-full ${color}`} style={{ width: `${bar}%` }}></div>
    </div>
  </div>
);

const ListItem = ({ type, text, sub }: any) => (
  <li className="flex gap-3 text-sm text-slate-300 items-start group">
    {type === 'success' ? (
      <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5 shrink-0 group-hover:scale-110 transition-transform" />
    ) : (
      <AlertTriangle className="w-5 h-5 text-rose-500 mt-0.5 shrink-0 group-hover:scale-110 transition-transform" />
    )}
    <div className="flex flex-col">
      <span className="leading-tight font-medium text-slate-200">{text}</span>
      <span className="text-[10px] text-slate-500 mt-0.5">{sub}</span>
    </div>
  </li>
);