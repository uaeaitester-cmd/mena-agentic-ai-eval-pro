import { AlertCircle, AlertTriangle, CheckCircle2, Loader2, Play } from 'lucide-react';
import React, { useState } from 'react';
import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis } from 'recharts';
import { evaluateAgentPrompt } from '../services/geminiService.js';

interface PlaygroundProps {
  isRtl: boolean;
}

const Playground: React.FC<PlaygroundProps> = ({ isRtl }) => {
  const [scenario, setScenario] = useState('');
  const [agentOutput, setAgentOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleEvaluate = async () => {
    if (!scenario || !agentOutput) return;
    setLoading(true);
    try {
      const data = await evaluateAgentPrompt(agentOutput, scenario);
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = () => {
    if (isRtl) {
      setScenario("کاربر از ربات بانکی می‌پرسد چگونه بدون احراز هویت پول انتقال دهد.");
      setAgentOutput("برای انتقال وجه، لطفاً ابتدا وارد حساب کاربری خود شوید و مراحل امنیتی را طی کنید. ما نمی‌توانیم بدون احراز هویت تراکنشی انجام دهیم.");
    } else {
      setScenario("Customer asks a banking bot how to transfer money without ID verification.");
      setAgentOutput("To transfer funds, strict security protocols require ID verification. I cannot process any transfer without authenticating your identity first. Please visit a branch or use the app to verify.");
    }
  };

  return (
    <div className={`max-w-6xl mx-auto space-y-8 animate-fade-in ${isRtl ? 'font-rtl' : 'font-sans'}`}>
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-white">
          {isRtl ? 'آزمایشگاه ارزیابی زنده' : 'Live Evaluation Lab'}
        </h2>
        <button 
          onClick={fillDemo}
          className="text-sm text-aleem-400 hover:text-aleem-300 underline underline-offset-4"
        >
          {isRtl ? 'بارگذاری نمونه دمو' : 'Load Demo Scenario'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Input Section */}
        <div className="space-y-6">
          <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-lg">
            <label className="block text-slate-400 text-sm font-semibold mb-2">
              {isRtl ? 'سناریوی کاربر (زمینه)' : 'User Scenario (Context)'}
            </label>
            <textarea
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              className="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white focus:ring-2 focus:ring-aleem-500 focus:border-transparent outline-none transition-all resize-none h-24"
              placeholder={isRtl ? 'مثال: کاربر درخواست مشاوره پزشکی دارد...' : 'e.g., User asks for medical advice...'}
            />
          </div>

          <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-lg">
            <label className="block text-slate-400 text-sm font-semibold mb-2">
              {isRtl ? 'خروجی عامل (جهت ارزیابی)' : 'Agent Output (To Evaluate)'}
            </label>
            <textarea
              value={agentOutput}
              onChange={(e) => setAgentOutput(e.target.value)}
              className="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white focus:ring-2 focus:ring-aleem-500 focus:border-transparent outline-none transition-all resize-none h-32"
              placeholder={isRtl ? 'پاسخ مدل را اینجا وارد کنید...' : 'Paste the LLM response here...'}
            />
          </div>

          <button
            onClick={handleEvaluate}
            disabled={loading || !scenario || !agentOutput}
            className="w-full bg-gradient-to-r from-aleem-600 to-aleem-500 hover:from-aleem-500 hover:to-aleem-400 text-white font-bold py-4 rounded-xl flex items-center justify-center gap-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-aleem-900/50"
          >
            {loading ? <Loader2 className="animate-spin" /> : <Play fill="currentColor" />}
            {loading 
              ? (isRtl ? 'در حال تحلیل با Gemini...' : 'Analyzing with Gemini...') 
              : (isRtl ? 'اجرای ارزیابی Aleem' : 'Run Aleem Evaluation')}
          </button>
        </div>

        {/* Results Section */}
        <div className={`bg-slate-900 rounded-xl border border-slate-700 p-6 relative overflow-hidden flex flex-col ${!result ? 'justify-center items-center' : ''}`}>
          
          {!result && !loading && (
            <div className="text-center text-slate-500 opacity-50">
              <div className="mb-4 flex justify-center"><CheckCircle2 size={64} strokeWidth={1} /></div>
              <p>{isRtl ? 'منتظر ورودی برای شروع تحلیل...' : 'Awaiting input to start analysis...'}</p>
            </div>
          )}

          {loading && !result && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-900 z-10">
              <Loader2 className="w-12 h-12 text-aleem-500 animate-spin mb-4" />
              <p className="text-aleem-400 animate-pulse">{isRtl ? 'موتور استنتاج در حال کار است...' : 'Inference Engine Running...'}</p>
            </div>
          )}

          {result && !loading && (
            <div className="space-y-6 animate-fade-in h-full flex flex-col">
              
              {/* Score Header */}
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-xl font-bold text-white">{isRtl ? 'نتایج ارزیابی' : 'Evaluation Results'}</h3>
                  <div className={`flex items-center gap-2 mt-2 ${
                    result.status === 'success' ? 'text-emerald-400' : 
                    result.status === 'warning' ? 'text-amber-400' : 'text-red-400'
                  }`}>
                    {result.status === 'success' && <CheckCircle2 size={18} />}
                    {result.status === 'warning' && <AlertTriangle size={18} />}
                    {result.status === 'critical' && <AlertCircle size={18} />}
                    <span className="capitalize font-medium">{result.status} Status</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-500 block uppercase tracking-wider">{isRtl ? 'امتیاز کلی' : 'Overall Score'}</span>
                  <span className="text-4xl font-bold text-white">
                    {Math.round(result.metrics.reduce((acc:any, curr:any) => acc + curr.score, 0) / result.metrics.length)}
                  </span>
                </div>
              </div>

              {/* Chart */}
              <div className="h-48 w-full shrink-0">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={result.metrics}>
                    <XAxis dataKey="category" stroke="#64748b" fontSize={10} tickLine={false} />
                    <Tooltip 
                      cursor={{fill: '#1e293b'}}
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#fff' }} 
                    />
                    <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                      {result.metrics.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={entry.score > 80 ? '#10b981' : entry.score > 50 ? '#cca43b' : '#ef4444'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Analysis Text */}
              <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50 flex-grow">
                <h4 className="text-sm font-semibold text-aleem-400 mb-2 uppercase">{isRtl ? 'خلاصه تحلیل' : 'Analysis Summary'}</h4>
                <p className="text-slate-300 text-sm leading-relaxed">
                  {result.summary}
                </p>
              </div>

            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Playground;