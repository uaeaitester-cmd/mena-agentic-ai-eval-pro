
// @ts-nocheck
export enum Tab {
  DASHBOARD = 'DASHBOARD',
  METRICS = 'METRICS',
  FILES = 'FILES',
  AI_AGENT = 'AI_AGENT',
  LAB = 'LAB'
}

export interface MetricData {
  subject: string;
  A: number;
  fullMark: number;
}

export interface FileNode {
  name: string;
  type: 'file' | 'folder' | 'docker';
  children?: FileNode[];
  language?: string;
  content?: string;
  description?: string;
  size?: string;
}
