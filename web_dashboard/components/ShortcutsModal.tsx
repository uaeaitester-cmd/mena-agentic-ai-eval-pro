// @ts-nocheck
import React from 'react';
export const ShortcutsModal = ({ isOpen, onClose }: any) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[1100] flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-[#0f172a] p-6 rounded-2xl border border-slate-700 text-white">
        <h3 className="font-bold mb-4">Shortcuts</h3>
        <ul className="text-sm space-y-2 text-slate-400">
          <li>Cmd+K: Command Palette</li>
          <li>Shift+R: Run Scan</li>
        </ul>
      </div>
    </div>
  );
};