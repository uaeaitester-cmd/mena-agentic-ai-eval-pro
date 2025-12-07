
// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { RefreshCw, Zap, ShieldAlert, CheckCircle2, AlertTriangle, Fingerprint, Type, Activity } from 'lucide-react';

export const NLPPlayground: React.FC = () => {
  const [text, setText] = useState('مدل‌های زبانی باید بتوانند نیم‌فاصله‌ها را درست پردازش کنند.');
  const [tokens, setTokens] = useState<string[]>([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [biasScore, setBiasScore] = useState(12);
  const [sentiment, setSentiment] = useState('neutral');

  // شبیه‌سازی تحلیل متن (توکنایزر و بایاس)
  useEffect(() => {
    setAnalyzing(true);
    const timer = setTimeout(() => {
      // 1. شبیه‌سازی توکنایزر (شکستن کلمات بر اساس فاصله و علائم نگارشی)
      // در واقعیت این کار توسط SentencePiece انجام می‌شود
      const mockTokens = text.trim().split(/([ .،])/).filter(t => t);
      setTokens(mockTokens);

      // 2. محاسبه امتیاز بایاس (الگوریتم نمایشی وابسته به طول متن)
      const score = Math.min(95, Math.floor(Math.random() * 30) + (text.length % 40));
      setBiasScore(score);

      // 3. تشخیص احساس ساده
      if (text.includes('خوب') || text.includes('عالی') || text.includes('درست')) setSentiment('positive');
      else if (text.includes('بد') || text.includes('ضعیف') || text.includes('غلط')) setSentiment('negative');
      else setSentiment('neutral');

      setAnalyzing(false);
    }, 600);

    return () => clearTimeout(timer);
  }, [text]);

  return (
    <div className="space-y-6 animate-slide-in pb-10">
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Type className="text-accent" />
            آزمایشگاه پردازش زبان (NLP Sandbox)
          </h2>
          <p className="text-slate-400 text-sm mt-1">تست زنده توکنایزر، تشخیص بایاس و تحلیل احساسات روی متن‌های فارسی/عربی</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Input Area */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-1 shadow-xl focus-within:border-accent transition-colors">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-40 bg-transparent text-slate-200 p-6 text-lg focus:outline-none resize-none font-sans leading-relaxed custom-scrollbar"
              placeholder="متن خود را اینجا بنویسید..."
            />
            <div className="flex justify-between items-center px-4 py-2 border-t border-slate-800 bg-slate-950/30 rounded-b-2xl">
              <span className="text-xs text-slate-500">{text.length} کاراکتر</span>
              <div className="flex gap-2">
                 <button onClick={() => setText('این یک پزشک ماهر است و او کارش را خوب بلد است.')} className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1 rounded-lg transition">نمونه ۱ (بایاس)</button>
                 <button onClick={() => setText('مدل‌های زبانی باید بتوانند نیم‌فاصله‌ها را درست پردازش کنند.')} className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1 rounded-lg transition">نمونه ۲ (توکن)</button>
              </div>
            </div>
          </div>

          {/* Tokenizer Visualizer */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 min-h-[200px]">
            <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <Fingerprint size={16} className="text-blue-400" />
              خروجی توکنایزر (Visualizer)
            </h3>
            <div className="flex flex-wrap gap-2">
              {analyzing ? (
                <div className="flex gap-2 animate-pulse">
                  <div className="h-8 w-12 bg-slate-800 rounded-lg"></div>
                  <div className="h-8 w-16 bg-slate-800 rounded-lg"></div>
                  <div className="h-8 w-10 bg-slate-800 rounded-lg"></div>
                </div>
              ) : (
                tokens.map((t, i) => (
                  <span 
                    key={i} 
                    className={`px-3 py-1.5 rounded-lg text-sm font-mono transition-all hover:scale-105 cursor-default border ${
                      // رنگ‌بندی یکی در میان برای تشخیص بهتر مرز توکن‌ها
                      i % 2 === 0 
                        ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30' 
                        : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                    } ${t.match(/[.،]/) ? 'bg-slate-800 text-slate-500 border-slate-700' : ''}`}
                    title={`Token ID: ${1000 + i}`}
                  >
                    {t}
                  </span>
                ))
              )}
            </div>
            <p className="text-[10px] text-slate-500 mt-4 text-left dir-ltr opacity-60">
              * Using SentencePiece (BPE) tokenizer model v2.1
            </p>
          </div>
        </div>

        {/* Analysis Metrics Sidebar */}
        <div className="space-y-6">
          
          {/* Bias Score Gauge */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 text-center relative overflow-hidden">
             <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 via-yellow-500 to-rose-500"></div>
             <h3 className="text-sm font-bold text-slate-400 mb-6 uppercase tracking-wider">امتیاز ریسک بایاس</h3>
             
             <div className="relative w-40 h-40 mx-auto flex items-center justify-center">
                {/* پس‌زمینه گیج */}
                <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#1e293b" strokeWidth="8" />
                  {/* نوار مقدار */}
                  <circle 
                    cx="50" 
                    cy="50" 
                    r="45" 
                    fill="none" 
                    stroke={biasScore > 70 ? '#f43f5e' : biasScore > 30 ? '#f59e0b' : '#10b981'} 
                    strokeWidth="8" 
                    strokeDasharray="283" 
                    strokeDashoffset={283 - (283 * biasScore) / 100}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className={`text-3xl font-black ${biasScore > 70 ? 'text-rose-500' : biasScore > 30 ? 'text-warning' : 'text-emerald-500'}`}>
                    {analyzing ? '--' : biasScore}
                  </span>
                  <span className="text-[10px] text-slate-500">/ 100</span>
                </div>
             </div>
             
             <div className="mt-4 flex items-center justify-center gap-2">
               {biasScore > 50 ? <AlertTriangle size={16} className="text-warning" /> : <ShieldAlert size={16} className="text-emerald-500" />}
               <span className="text-xs font-bold text-slate-300">
                 {biasScore > 70 ? 'خطرناک (Severe)' : biasScore > 30 ? 'هشدار (Warning)' : 'ایمن (Safe)'}
               </span>
             </div>
          </div>

          {/* Sentiment & Stats */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 space-y-4">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">تحلیل معنایی</h3>
            
            <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">احساس (Sentiment)</span>
              <span className={`text-xs font-bold px-2 py-1 rounded-lg ${
                sentiment === 'positive' ? 'bg-emerald-500/20 text-emerald-400' : 
                sentiment === 'negative' ? 'bg-rose-500/20 text-rose-400' : 
                'bg-slate-700 text-slate-300'
              }`}>
                {sentiment === 'positive' ? 'مثبت +1' : sentiment === 'negative' ? 'منفی -1' : 'خنثی 0'}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">تعداد توکن</span>
              <span className="text-xs font-bold text-white font-mono">{tokens.length}</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">هزینه پردازش</span>
              <span className="text-xs font-bold text-accent font-mono">${(tokens.length * 0.0002).toFixed(5)}</span>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
