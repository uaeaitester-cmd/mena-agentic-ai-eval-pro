
// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts';
import { Play, Activity, Server, Zap, RefreshCw } from 'lucide-react';
import { backend } from '../services/backendService';

// داده‌های هیت‌مپ ثابت (چون معمولاً استاتیک هستند)
const HEATMAP_DATA = {
  rows: ['سیاست', 'مذهب', 'جنسیت', 'قومیت'],
  cols: ['فارسی رسمی', 'فارسی محاوره', 'عربی MSA', 'عربی خلیجی', 'عربی مصری'],
  values: [
    [20, 45, 30, 85, 90],
    [15, 30, 80, 95, 60],
    [10, 60, 40, 70, 50],
    [5, 25, 20, 65, 40],
  ]
};

export const MetricsDashboard: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [biasData, setBiasData] = useState<any[]>([]);
  const [perfData, setPerfData] = useState<any[]>([]);
  const [status, setStatus] = useState('آماده اجرا');
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // بارگذاری اولیه داده‌ها از سرویس
  useEffect(() => {
    fetchData();
    // پولینگ برای زنده نشان دادن نمودارها (هر ۳ ثانیه)
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    if (!isRunning) {
      const data = await backend.getMetricsData();
      setBiasData(data.bias);
      setPerfData(data.performance);
      setLastUpdate(new Date());
    }
  };

  const runBenchmark = async () => {
    if (isRunning) return;
    setIsRunning(true);
    setProgress(0);
    setStatus('در حال اتصال به هسته پردازشی...');

    // استفاده از سرویس برای اجرای لاجیک
    await backend.runAuditStream((log, prog) => {
      setStatus(log);
      setProgress(prog);
    });

    setIsRunning(false);
    setStatus('تست با موفقیت تکمیل شد');
    setTimeout(() => setStatus('آماده اجرا'), 2000);
    fetchData(); // رفرش نهایی
  };

  return (
    <div className="space-y-6 animate-slide-in pb-10">
      
      {/* Control Panel */}
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-4 w-full md:w-auto">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-colors ${isRunning ? 'bg-accent/20 text-accent' : 'bg-slate-800 text-slate-400'}`}>
            {isRunning ? <Activity className="animate-pulse" /> : <Server />}
          </div>
          <div>
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              موتور بنچمارک زنده
              {!isRunning && <span className="text-[10px] font-normal text-slate-500 bg-slate-800 px-2 py-0.5 rounded-full flex items-center gap-1"><RefreshCw size={10}/> {lastUpdate.toLocaleTimeString()}</span>}
            </h3>
            <p className="text-[10px] text-emerald-400 font-mono">{status}</p>
          </div>
        </div>

        {isRunning && (
          <div className="flex-1 w-full md:mx-8">
            <div className="flex justify-between text-[10px] text-slate-400 mb-1">
              <span>Processing Batches...</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-accent transition-all duration-300 ease-out shadow-[0_0_10px_#6366f1]" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        <button 
          onClick={runBenchmark}
          disabled={isRunning}
          className={`px-6 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 transition-all ${
            isRunning 
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/20 active:scale-95'
          }`}
        >
          {isRunning ? <Zap size={16} className="animate-spin" /> : <Play size={16} />}
          {isRunning ? 'در حال پردازش...' : 'اجرای تست جدید'}
        </button>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard title="Total Tests" value="1,240" trend="+12%" icon="🧪" />
        <KPICard title="Avg Fairness" value="78.5%" trend="+5%" icon="⚖️" isGood />
        <KPICard title="Bias Detected" value="23" trend="-2" icon="🚩" isBad />
        <KPICard title="Cost / Run" value="$4.20" trend="0%" icon="💲" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Radar Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 flex flex-col h-[400px]">
          <div className="flex items-center justify-between mb-2">
             <h3 className="text-lg font-bold text-white flex items-center gap-2">
               <span className="w-2 h-6 bg-emerald-500 rounded-full"></span>
               پوشش بایاس (Live Data)
             </h3>
          </div>
          <div className="flex-1 w-full h-full dir-ltr">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={biasData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 600 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Score" dataKey="A" stroke="#10b981" strokeWidth={3} fill="#10b981" fillOpacity={0.2} />
                <Tooltip content={<CustomTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 flex flex-col h-[400px]">
          <div className="flex items-center justify-between mb-6">
             <h3 className="text-lg font-bold text-white flex items-center gap-2">
               <span className="w-2 h-6 bg-indigo-500 rounded-full"></span>
               مقایسه مدل‌ها (Real-time)
             </h3>
          </div>
          <div className="flex-1 w-full h-full dir-ltr">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={perfData} barSize={12}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} opacity={0.5} />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} dy={10} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{fill: '#1e293b', opacity: 0.5}} />
                <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy" radius={[4, 4, 0, 0]} isAnimationActive={false} />
                <Bar dataKey="fairness" fill="#10b981" name="Fairness" radius={[4, 4, 0, 0]} isAnimationActive={false} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Heatmap */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-700/50 bg-slate-900/50 lg:col-span-2 shadow-xl">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span className="w-1.5 h-6 bg-rose-500 rounded-full"></span>
            نقشه حرارتی ریسک (Risk Heatmap)
          </h3>
          <p className="text-xs text-slate-400 mb-6">این نمودار شدت بایاس شناسایی شده را در تقاطع "موضوعات حساس" و "گویش‌های زبانی" نشان می‌دهد.</p>
          
          <div className="overflow-x-auto">
            <div className="min-w-[600px]">
              <div className="grid grid-cols-6 gap-2 mb-2">
                <div className="col-span-1"></div>
                {HEATMAP_DATA.cols.map((col, i) => (
                  <div key={i} className="text-center text-[10px] text-slate-400 font-bold uppercase tracking-wider">{col}</div>
                ))}
              </div>
              
              {HEATMAP_DATA.rows.map((row, rIndex) => (
                <div key={rIndex} className="grid grid-cols-6 gap-2 mb-2">
                  <div className="col-span-1 flex items-center text-xs font-bold text-slate-300">{row}</div>
                  {HEATMAP_DATA.values[rIndex].map((val, cIndex) => {
                    let bgClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
                    if (val > 40) bgClass = 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
                    if (val > 70) bgClass = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
                    
                    return (
                      <div key={cIndex} className={`h-10 rounded-lg border flex items-center justify-center text-xs font-mono font-bold transition-all hover:scale-105 cursor-default ${bgClass}`}>
                        {val}%
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

const KPICard = ({ title, value, sub, trend, isGood, isBad }: any) => (
  <div className="bg-slate-800/40 border border-slate-700/50 p-4 rounded-2xl hover:bg-slate-800/60 transition-all cursor-default group">
    <div className="flex justify-between items-start mb-2">
      <h4 className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</h4>
      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${isGood ? 'text-emerald-400 bg-emerald-500/10' : isBad ? 'text-rose-400 bg-rose-500/10' : 'text-slate-400 bg-slate-700/30'}`}>{trend}</span>
    </div>
    <div className="text-2xl font-black text-white font-mono">{value}</div>
    <div className="text-[10px] text-slate-500 mt-1">{sub}</div>
  </div>
);

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-[#0f172a] border border-slate-700 p-4 rounded-xl shadow-2xl text-xs z-50">
        <p className="font-bold text-white mb-2 border-b border-slate-700 pb-2">{label}</p>
        {payload.map((p: any, idx: number) => (
          <div key={idx} className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 rounded-full" style={{backgroundColor: p.color}}></div>
            <span className="text-slate-300 capitalize">{p.name}:</span>
            <span className="text-white font-mono font-bold">{typeof p.value === 'number' ? p.value.toFixed(1) : p.value}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};