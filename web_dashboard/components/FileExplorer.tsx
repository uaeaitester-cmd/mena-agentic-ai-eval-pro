
// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { Folder, FileCode, FileJson, FileText, ChevronRight, ChevronDown, Container, Loader2 } from 'lucide-react';
import { FileNode } from '../types';
import { backend } from '../services/backendService';

interface FileExplorerProps {
  onSelectFile: (file: FileNode) => void;
  selectedFile: FileNode | null;
}

export const FileExplorer: React.FC<FileExplorerProps> = ({ onSelectFile, selectedFile }) => {
  const [files, setFiles] = useState<FileNode[]>([]);
  const [loading, setLoading] = useState(true);

  // دریافت ساختار فایل‌ها از سرویس
  useEffect(() => {
    const loadFiles = async () => {
      setLoading(true);
      try {
        const data = await backend.getFileStructure();
        setFiles(data);
      } catch (error) {
        console.error("Failed to load files", error);
      } finally {
        setLoading(false);
      }
    };
    loadFiles();
  }, []);

  return (
    <div className="h-full flex flex-col bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl animate-slide-up">
       <div className="p-3 border-b border-slate-800 bg-slate-950 flex justify-between items-center">
         <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Project Explorer</span>
       </div>
       
       <div className="p-2 space-y-1 font-mono text-sm overflow-y-auto flex-1 dir-ltr text-left custom-scrollbar relative">
         {loading ? (
           <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500 gap-2">
             <Loader2 size={24} className="animate-spin text-accent" />
             <span className="text-xs">Loading structure...</span>
           </div>
         ) : (
           files.map((node, i) => (
             <FileItem key={i} node={node} onSelect={onSelectFile} selectedNode={selectedFile} isOpen={true} />
           ))
         )}
       </div>
    </div>
  );
};

const FileItem = ({ node, onSelect, selectedNode, isOpen: defaultOpen }: any) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const isSelected = selectedNode?.name === node.name;
  
  const getIcon = () => {
    if (node.type === 'folder') return Folder;
    if (node.type === 'docker') return Container;
    if (node.name.endsWith('.py')) return FileCode;
    if (node.name.endsWith('.json')) return FileJson;
    return FileText;
  };
  
  const Icon = getIcon();
  
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (node.type === 'folder') {
      setIsOpen(!isOpen);
    } else {
      if (onSelect) onSelect(node);
    }
  };
  
  return (
    <div className="pl-4 select-none">
      <div 
        className={`flex items-center gap-2 py-1.5 px-2 rounded-lg cursor-pointer transition-all group ${
          isSelected ? 'bg-accent/20 text-white' : 'hover:bg-slate-800 text-slate-400'
        }`}
        onClick={handleClick}
      >
        <span className="opacity-50 min-w-[12px] flex justify-center">
           {node.type === 'folder' && (isOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />)}
        </span>
        <Icon size={15} className={`${
          node.type === 'folder' ? 'text-blue-400' : 
          isSelected ? 'text-white' : 'opacity-70'
        }`} />
        <span className={`${node.type === 'folder' ? 'font-semibold' : ''} truncate`}>{node.name}</span>
      </div>
      {isOpen && node.children && (
        <div className="border-l border-slate-800 ml-2.5">
          {node.children.map((child: any, idx: number) => (
            <FileItem key={idx} node={child} onSelect={onSelect} selectedNode={selectedNode} />
          ))}
        </div>
      )}
    </div>
  );
};