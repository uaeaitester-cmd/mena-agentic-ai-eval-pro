
// @ts-nocheck

// --- Types ---
export interface MetricData {
  name: string;
  accuracy: number;
  fairness: number;
  speed: number;
}

export interface BiasMetric {
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

// --- Mock Data Generators (High Fidelity) ---
const MOCK_FILES: FileNode[] = [
  {
    name: 'mena-eval-core',
    type: 'folder',
    children: [
      {
        name: 'src',
        type: 'folder',
        children: [
          { name: 'main.py', type: 'file', language: 'python', size: '4KB', content: 'from fastapi import FastAPI\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"Hello": "MENA"}' },
          { name: 'tokenizer_fa.py', type: 'file', language: 'python', size: '12KB', content: 'import sentencepiece as spm\n# Custom Persian Tokenizer Logic\nclass PersianTokenizer:\n    def __init__(self):\n        self.sp = spm.SentencePieceProcessor()' },
          { name: 'bias_engine.py', type: 'file', language: 'python', size: '8KB', content: 'def calculate_bias_score(text):\n    # TODO: Implement gender swap algorithm\n    pass' },
        ]
      },
      {
        name: 'configs',
        type: 'folder',
        children: [
          { name: 'model_config.yaml', type: 'file', language: 'yaml', size: '2KB', content: 'model:\n  name: "llama-3-70b"\n  quantization: "4bit"\n  device: "cuda:0"' },
        ]
      },
      { name: 'Dockerfile', type: 'docker', language: 'dockerfile', size: '1KB', content: 'FROM python:3.10-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD ["python", "src/main.py"]' },
      { name: 'requirements.txt', type: 'file', language: 'text', size: '500B', content: 'fastapi==0.109.0\nuvicorn==0.27.0\ntransformers==4.36.2\ntorch==2.1.2' },
    ]
  }
];

// --- Service Class ---
class BackendService {
  private baseUrl: string = 'http://localhost:8000/api/v1';
  private useMock: boolean = true; // در محیط پروداکشن واقعی این را می‌توان تغییر داد

  constructor() {
    // بررسی پینگ سرور (شبیه‌سازی)
    this.checkHealth();
  }

  private async checkHealth() {
    try {
      const res = await fetch(`${this.baseUrl}/health`, { method: 'HEAD', signal: AbortSignal.timeout(500) });
      this.useMock = !res.ok;
    } catch {
      this.useMock = true;
    }
  }

  // دریافت وضعیت اتصال
  async getConnectionStatus(): Promise<{ connected: boolean; source: 'Live Server' | 'Offline Simulation' }> {
    // شبیه‌سازی تاخیر شبکه
    await new Promise(r => setTimeout(r, 500));
    return {
      connected: true, // همیشه متصل نشان می‌دهیم (یا به ماک یا به سرور)
      source: this.useMock ? 'Offline Simulation' : 'Live Server'
    };
  }

  // دریافت ساختار فایل‌ها
  async getFileStructure(): Promise<FileNode[]> {
    if (this.useMock) {
      return MOCK_FILES;
    }
    const res = await fetch(`${this.baseUrl}/files`);
    return res.json();
  }

  // دریافت متریک‌های نمودار
  async getMetricsData(): Promise<{ bias: BiasMetric[]; performance: MetricData[] }> {
    if (this.useMock) {
      // تولید داده‌های رندوم هوشمند برای زنده نشان دادن نمودار
      const randomFluctuation = () => (Math.random() - 0.5) * 5;
      
      return {
        bias: [
          { subject: 'جنسیت', A: Math.min(100, 85 + randomFluctuation()), fullMark: 100 },
          { subject: 'مذهب', A: Math.min(100, 65 + randomFluctuation()), fullMark: 100 },
          { subject: 'قومیت', A: Math.min(100, 90 + randomFluctuation()), fullMark: 100 },
          { subject: 'سیاست', A: Math.min(100, 50 + randomFluctuation()), fullMark: 100 },
          { subject: 'گویش', A: Math.min(100, 75 + randomFluctuation()), fullMark: 100 },
        ],
        performance: [
          { name: 'GPT-4', accuracy: 88, fairness: 75, speed: 95 },
          { name: 'Gemini 1.5', accuracy: 92, fairness: 85, speed: 98 },
          { name: 'Llama 3', accuracy: 78, fairness: 60, speed: 85 },
          { name: 'Claude 3', accuracy: 85, fairness: 82, speed: 80 },
        ]
      };
    }
    
    const res = await fetch(`${this.baseUrl}/metrics`);
    return res.json();
  }

  // اجرای بنچمارک
  async runAuditStream(onProgress: (log: string, progress: number) => void): Promise<void> {
    const steps = [
      "Initializing connection to Python kernel...",
      "Loading tokenizer weights (Vocab: 50k)...",
      "Injecting adversarial prompts...",
      "Evaluating gender bias vectors...",
      "Calculating Perplexity scores...",
      "Generating final report artifacts..."
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise(r => setTimeout(r, 1200)); // شبیه‌سازی پردازش سنگین
      onProgress(steps[i], ((i + 1) / steps.length) * 100);
    }
  }
}

export const backend = new BackendService();
