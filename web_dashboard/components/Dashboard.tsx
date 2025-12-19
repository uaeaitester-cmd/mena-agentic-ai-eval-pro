import React from 'react';
import { Bar, BarChart, CartesianGrid, Legend, PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const data = [
  { name: 'Customer Service Agent v1', accuracy: 82, safety: 95, speed: 70 },
  { name: 'Financial Advisor v2.1', accuracy: 94, safety: 88, speed: 85 },
  { name: 'Legal Draftsman Beta', accuracy: 96, safety: 92, speed: 60 },
  { name: 'Creative Copywriter', accuracy: 75, safety: 98, speed: 95 },
];

const radarData = [
  { subject: 'Factuality', A: 120, B: 110, fullMark: 150 },
  { subject: 'Reasoning', A: 98, B: 130, fullMark: 150 },
  { subject: 'Safety', A: 86, B: 130, fullMark: 150 },
  { subject: 'Tone', A: 99, B: 100, fullMark: 150 },
  { subject: 'Regional Fit', A: 85, B: 90, fullMark: 150 },
  { subject: 'Latency', A: 65, B: 85, fullMark: 150 },
];

const Dashboard: React.FC<{ isRtl: boolean }> = ({ isRtl }) => {
  return (
    <div className={`space-y-8 animate-fade-in ${isRtl ? 'font-rtl' : 'font-sans'}`}>
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold text-white mb-1">{isRtl ? 'داشبورد اجرایی' : 'Executive Dashboard'}</h2>
          <p className="text-slate-400">{isRtl ? 'وضعیت بلادرنگ عملکرد ناوگان عامل‌ها' : 'Real-time Agent Fleet Performance'}</p>
        </div>
        <div className="bg-emerald-500/10 text-emerald-400 px-4 py-2 rounded border border-emerald-500/20 text-sm">
          {isRtl ? 'سیستم عملیاتی' : 'System Operational'} • 99.9% Uptime
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Main Bar Chart */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-6">{isRtl ? 'مقایسه بنچمارک مدل‌ها' : 'Model Benchmark Comparison'}</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis type="number" stroke="#94a3b8" />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" width={120} tick={{fontSize: 12}} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} 
                  itemStyle={{ color: '#fff' }}
                />
                <Legend />
                <Bar dataKey="accuracy" name={isRtl ? 'دقت' : 'Accuracy'} fill="#0ea5e9" radius={[0, 4, 4, 0]} barSize={20} />
                <Bar dataKey="safety" name={isRtl ? 'ایمنی' : 'Safety'} fill="#10b981" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Radar Chart */}
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-6">{isRtl ? 'تحلیل چندبعدی: نسخه ۱ در مقابل ۲' : 'Multidimensional Analysis: v1 vs v2'}</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} stroke="#475569" />
                <Radar name="Agent v1" dataKey="A" stroke="#cca43b" fill="#cca43b" fillOpacity={0.4} />
                <Radar name="Agent v2" dataKey="B" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.4} />
                <Legend />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: isRtl ? 'مجموع ارزیابی‌ها' : 'Total Evaluations', value: '14,205', color: 'text-white' },
          { label: isRtl ? 'نرخ عبور ایمنی' : 'Safety Pass Rate', value: '98.2%', color: 'text-emerald-400' },
          { label: isRtl ? 'میانگین تاخیر' : 'Avg. Latency', value: '420ms', color: 'text-aleem-400' },
          { label: isRtl ? 'هزینه هر توکن' : 'Cost / 1k Tokens', value: '$0.004', color: 'text-amber-400' },
        ].map((kpi, idx) => (
          <div key={idx} className="bg-slate-800/30 p-4 rounded-lg border border-slate-700">
            <p className="text-slate-500 text-sm mb-1">{kpi.label}</p>
            <p className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;