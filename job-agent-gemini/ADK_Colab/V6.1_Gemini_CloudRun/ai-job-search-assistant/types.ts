export interface AnalysisResult {
  overallFitSummary: string;
  candidateSkills: string[];
  requiredJobSkills: string[];
  gapAnalysis: string[];
  matchScore: number; // 0 to 100
}

export interface LogEntry {
  id: string;
  message: string;
  type: 'info' | 'success' | 'agent';
  timestamp: number;
}

export interface AppState {
  jobUrl: string;
  resumeFile: File | null;
  isLoading: boolean;
  logs: LogEntry[];
  result: AnalysisResult | null;
  error: string | null;
}
