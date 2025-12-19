// @ts-nocheck
import React from 'react';
export const SettingsModal = ({ isOpen, onClose }: any) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[150] bg-black/60 flex items-center justify-center backdrop-blur-sm" onClick={onClose}>
      <div className="bg-[#0f172a] p-6 rounded-2xl border border-slate-700 text-white w-96">
        <h3 className="font-bold mb-4">Settings</h3>
        <button onClick={onClose} className="bg-accent px-4 py-2 rounded text-sm">Close</button>
      </div>
    </div>
  );
};