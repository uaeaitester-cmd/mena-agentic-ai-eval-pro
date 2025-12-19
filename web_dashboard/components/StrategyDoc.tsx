import { AlertTriangle, Globe, Shield, Target, TrendingUp, Users } from 'lucide-react';
import React from 'react';

const StrategyDoc: React.FC<{ isRtl: boolean }> = ({ isRtl }) => {
  return (
    <div className={`max-w-5xl mx-auto space-y-12 pb-20 animate-fade-in ${isRtl ? 'font-rtl' : 'font-sans'}`}>
      
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-aleem-500 to-aleem-100">
          {isRtl ? 'پلتفرم ارزیابی عامل‌های هوش مصنوعی علیم' : 'Aleem AI Agent Evaluation Platform'}
        </h1>
        <p className="text-xl text-slate-400">
          {isRtl ? 'سند استراتژی محصول | محرمانه | نسخه ۱.۰' : 'Product Strategy Brief | Confidential | v1.0'}
        </p>
      </div>

      {/* North Star */}
      <div className="bg-gradient-to-r from-aleem-900/50 to-slate-900 border border-aleem-500/30 p-8 rounded-2xl relative overflow-hidden group hover:border-aleem-500/60 transition-all duration-500">
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <Target size={120} />
        </div>
        <h2 className="text-aleem-500 font-bold uppercase tracking-widest text-sm mb-2">
          {isRtl ? 'ستاره شمالی (North Star)' : 'NORTH STAR STATEMENT'}
        </h2>
        <blockquote className="text-2xl md:text-3xl font-light leading-relaxed italic text-white">
          "{isRtl 
            ? 'استانداردسازی اعتماد در هوش مصنوعی: تبدیل شدن به "حقیقت واحد" برای ارزیابی، ایمنی و انطباق عامل‌های هوش مصنوعی در خاورمیانه و فراتر از آن.'
            : 'Standardizing Trust in Intelligence: To become the single source of truth for AI Agent evaluation, safety, and compliance across the MENA region and beyond.'}"
        </blockquote>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Value Proposition */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:bg-slate-800 transition-colors">
          <div className="flex items-center gap-3 mb-4 text-aleem-400">
            <Shield className="w-6 h-6" />
            <h3 className="text-xl font-bold">{isRtl ? 'ارزش پیشنهادی و تمایز' : 'Core Value Proposition'}</h3>
          </div>
          <ul className={`space-y-3 text-slate-300 ${isRtl ? 'list-disc pr-5' : 'list-disc pl-5'}`}>
            <li>
              <strong className="text-white">{isRtl ? 'دقت بومی‌سازی شده:' : 'Localized Precision:'}</strong> 
              {isRtl ? ' موتور ارزیابی معنایی عمیق برای عربی (خلیجی، شامی، مصری) و فارسی.' : ' Deep semantic evaluation engine optimized for Arabic (Gulf, Levantine, Egyptian) and Persian dialects.'}
            </li>
            <li>
              <strong className="text-white">{isRtl ? 'انطباق حاکمیتی:' : 'Sovereign Compliance:'}</strong> 
              {isRtl ? ' استقرار کاملاً On-Premise برای رعایت قوانین اقامت داده GCC.' : ' Full on-premise deployment capabilities ensuring adherence to GCC data residency laws.'}
            </li>
            <li>
              <strong className="text-white">{isRtl ? 'بازتولیدپذیری قطعی:' : 'Deterministic Reproducibility:'}</strong> 
              {isRtl ? ' فریم‌ورک تست رگرسیون برای اطمینان از پایداری نسخه به نسخه.' : ' Regression frameworks guaranteeing agent behavior remains stable across updates.'}
            </li>
          </ul>
        </div>

        {/* Use Cases */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:bg-slate-800 transition-colors">
          <div className="flex items-center gap-3 mb-4 text-emerald-400">
            <TrendingUp className="w-6 h-6" />
            <h3 className="text-xl font-bold">{isRtl ? 'موارد استفاده اولویت‌دار' : 'Priority Use Cases'}</h3>
          </div>
          <ul className={`space-y-3 text-slate-300 ${isRtl ? 'list-disc pr-5' : 'list-disc pl-5'}`}>
            <li>{isRtl ? 'بنچمارکینگ عامل‌ها در برابر مدل‌های انسانی و SOTA.' : 'Agent Benchmarking against human baselines and SOTA models.'}</li>
            <li>{isRtl ? 'تست ایمنی و Red-Teaming خودکار برای کشف جیل‌بریک‌ها.' : 'Automated Red-Teaming & Safety Scoring.'}</li>
            <li>{isRtl ? 'ارکستراسیون چند عاملی (Multi-Agent) و تست تعارض.' : 'Multi-Agent Orchestration & Conflict Testing.'}</li>
            <li>{isRtl ? 'ارزیابی RAG (صحت بازیابی و وفاداری تولید).' : 'RAG Evaluation (Retrieval Accuracy & Generation Faithfulness).'}</li>
          </ul>
        </div>

        {/* Target Users */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:bg-slate-800 transition-colors">
          <div className="flex items-center gap-3 mb-4 text-purple-400">
            <Users className="w-6 h-6" />
            <h3 className="text-xl font-bold">{isRtl ? 'کاربران هدف' : 'Target Users'}</h3>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-900/50 p-3 rounded border border-slate-700/50">
              <span className="block font-semibold text-white">{isRtl ? 'مهندس ML' : 'ML Engineer'}</span>
              <span className="text-xs text-slate-400">{isRtl ? 'بهینه‌سازی هایپرپارامترها' : 'Hyperparameter optimization'}</span>
            </div>
            <div className="bg-slate-900/50 p-3 rounded border border-slate-700/50">
              <span className="block font-semibold text-white">{isRtl ? 'تحلیلگر QA' : 'QA Analyst'}</span>
              <span className="text-xs text-slate-400">{isRtl ? 'تست رگرسیون و لبه‌ای' : 'Regression & Edge cases'}</span>
            </div>
            <div className="bg-slate-900/50 p-3 rounded border border-slate-700/50">
              <span className="block font-semibold text-white">{isRtl ? 'مدیر محصول' : 'Product Manager'}</span>
              <span className="text-xs text-slate-400">{isRtl ? 'تصمیم‌گیری انتشار' : 'Go/No-Go decisions'}</span>
            </div>
            <div className="bg-slate-900/50 p-3 rounded border border-slate-700/50">
              <span className="block font-semibold text-white">{isRtl ? 'مسئول انطباق' : 'Compliance Officer'}</span>
              <span className="text-xs text-slate-400">{isRtl ? 'ممیزی سوگیری و ایمنی' : 'Bias & Safety auditing'}</span>
            </div>
          </div>
        </div>

        {/* Risks */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:bg-slate-800 transition-colors">
          <div className="flex items-center gap-3 mb-4 text-red-400">
            <AlertTriangle className="w-6 h-6" />
            <h3 className="text-xl font-bold">{isRtl ? 'تحلیل ریسک و کاهش آن' : 'Risk Analysis & Mitigation'}</h3>
          </div>
          <div className="space-y-4">
            <div>
              <h4 className="text-white font-semibold text-sm">{isRtl ? '۱. سوگیری در ارزیابی خودکار (LLM-as-a-Judge)' : '1. Evaluation Bias (LLM-as-a-Judge)'}</h4>
              <p className="text-slate-400 text-sm">{isRtl ? 'راهکار: استفاده از هیئت منصفه مدل‌های ترکیبی (Ensemble Judges) و کالیبراسیون انسانی.' : 'Mitigation: Use Ensemble Judges and human-in-the-loop calibration.'}</p>
            </div>
            <div>
              <h4 className="text-white font-semibold text-sm">{isRtl ? '۲. تست‌های ناپایدار (Flaky Tests)' : '2. Flaky Tests (Non-determinism)'}</h4>
              <p className="text-slate-400 text-sm">{isRtl ? 'راهکار: اجرای چندگانه (Monte Carlo) و تثبیت Seed.' : 'Mitigation: Monte Carlo execution runs and Seed locking.'}</p>
            </div>
          </div>
        </div>

      </div>

      {/* Regional Focus */}
      <div className="bg-indigo-900/20 border border-indigo-500/30 p-8 rounded-2xl flex flex-col md:flex-row items-center gap-8">
        <div className="bg-indigo-500/20 p-4 rounded-full">
          <Globe className="w-12 h-12 text-indigo-400" />
        </div>
        <div className="flex-1">
          <h3 className="text-2xl font-bold text-white mb-2">{isRtl ? 'برتری منطقه‌ای (MENA/GCC)' : 'Regional Dominance (MENA/GCC)'}</h3>
          <p className="text-indigo-200">
            {isRtl 
             ? 'طراحی شده از پایه برای پشتیبانی کامل از RTL (راست‌به‌چپ)، تقویم‌های هجری/شمسی، و حساسیت‌های فرهنگی خاص منطقه در ارزیابی ایمنی محتوا.' 
             : 'Architected from the ground up for native RTL support, Hijri/Solar calendar integrations, and specific cultural sensitivity safety filters critical for regional enterprise adoption.'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default StrategyDoc;