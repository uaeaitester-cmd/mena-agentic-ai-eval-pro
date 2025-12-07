
// @ts-nocheck
import React, { useEffect, useState } from 'react';
import { ShieldCheck, Fingerprint, Cpu, Lock } from 'lucide-react';

interface IntroScreenProps {
  onComplete: () => void;
}

export const IntroScreen: React.FC<IntroScreenProps> = ({ onComplete }) => {
  const [step, setStep] = useState(0);

  const steps = [
    { msg: "INITIALIZING CORE KERNEL...", delay: 800 },
    { msg: "MOUNTING SECURE VOLUMES...", delay: 1600 },
    { msg: "BYPASSING FIREWALL PROXY...", delay: 2400 },
    { msg: "ESTABLISHING NEURAL LINK...", delay: 3200 },
    { msg: "ACCESS GRANTED", delay: 4000 }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setStep(prev => {
        if (prev >= steps.length - 1) {
          clearInterval(timer);
          setTimeout(onComplete, 800);
          return prev;
        }
        return prev + 1;
      });
    }, 900);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="fixed inset-0 z-[999] bg-[#020617] flex flex-col items-center justify-center text-emerald-500 font-mono overflow-hidden">
      
      {/* Background Grid Animation */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(16,185,129,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.03)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_80%)]"></div>

      <div className="relative z-10 flex flex-col items-center gap-8 w-80">
        
        {/* Central Logo / Fingerprint */}
        <div className="relative">
          <div className="w-24 h-24 rounded-full border-2 border-emerald-500/30 flex items-center justify-center animate-[spin_10s_linear_infinite]">
            <div className="w-20 h-20 rounded-full border border-emerald-500/50 border-dashed"></div>
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
             {step < 3 ? (
               <Fingerprint size={48} className="text-emerald-500/80 animate-pulse" />
             ) : (
               <ShieldCheck size={48} className="text-emerald-400 animate-bounce" />
             )}
          </div>
        </div>

        {/* Loading Bar & Text */}
        <div className="w-full space-y-2">
          <div className="flex justify-between text-xs font-bold tracking-widest text-emerald-600">
            <span>SYSTEM_CHECK</span>
            <span>{Math.min((step + 1) * 20, 100)}%</span>
          </div>
          <div className="h-1 bg-emerald-900/50 rounded-full overflow-hidden">
            <div 
              className="h-full bg-emerald-500 shadow-[0_0_15px_#10b981] transition-all duration-700 ease-out"
              style={{ width: `${Math.min((step + 1) * 20, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Console Log */}
        <div className="h-16 flex flex-col items-center justify-center space-y-1">
          {steps.map((s, i) => (
            i === step && (
              <div key={i} className="flex items-center gap-2 animate-slide-up text-xs font-bold tracking-wider">
                {i < steps.length - 1 ? <Cpu size={14} className="animate-spin" /> : <Lock size={14} />}
                {s.msg}
              </div>
            )
          ))}
        </div>

      </div>

      {/* Footer ID */}
      <div className="absolute bottom-8 text-[10px] text-emerald-800 tracking-[0.5em] opacity-50">
        ID: 8492-X-ALPHA
      </div>
    </div>
  );
};
