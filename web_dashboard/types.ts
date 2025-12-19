export interface NavItem {
  label: string;
  id: ViewState;
  icon: any;
}

export type ViewState = 'strategy' | 'dashboard' | 'playground';

export interface EvaluationMetric {
  category: string;
  score: number;
  fullMark: number;
  description: string;
}

export interface EvaluationResult {
  metrics: EvaluationMetric[];
  summary: string;
  status: 'success' | 'warning' | 'critical';
}

export interface LanguageContextType {
  lang: 'en' | 'fa' | 'ar';
  direction: 'ltr' | 'rtl';
  toggleLanguage: (lang: 'en' | 'fa' | 'ar') => void;
}
