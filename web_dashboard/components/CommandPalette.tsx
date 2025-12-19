// @ts-nocheck
import React from 'react';
export const CommandPalette = ({ isOpen, onClose }: any) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[1000] flex items-start justify-center pt-[15vh] px-4 animate-fade-in" onClick={onClose}>
      <div className="w-full max-w-2xl bg-[#0f172a] border border-slate-700 rounded-xl p-4 shadow-2xl">
        <input autoFocus className="w-full bg-transparent text-white text-lg outline-none" placeholder="Type a command..." />
      </div>
    </div>
  );
};