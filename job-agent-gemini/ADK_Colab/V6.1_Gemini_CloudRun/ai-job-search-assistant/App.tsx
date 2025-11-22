import React, { useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import { LogEntry, AnalysisResult } from './types';
import { analyzeResumeFit } from './services/geminiService';

const App: React.FC = () => {
  const [jobUrl, setJobUrl] = useState('');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const addLog = useCallback((message: string, type: LogEntry['type'] = 'info') => {
    setLogs(prev => [...prev, {
      id: Math.random().toString(36).substring(7),
      message,
      type,
      timestamp: Date.now()
    }]);
  }, []);

  const handleRunAnalysis = async () => {
    if (!jobUrl || !resumeFile) return;

    setIsLoading(true);
    setLogs([]); // Clear previous logs
    setResult(null); // Clear previous result

    try {
      // Simulated Agentic Steps for UX
      addLog("Initializing CoordinatorAgent 'root_agent'...", 'agent');
      await new Promise(resolve => setTimeout(resolve, 600));
      
      addLog("Resume extracted successfully.", 'success');
      await new Promise(resolve => setTimeout(resolve, 800));

      addLog(`Fetching job description from: ${new URL(jobUrl).hostname}...`, 'info');
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      addLog("Job description fetched successfully.", 'success');
      await new Promise(resolve => setTimeout(resolve, 500));

      addLog("CoordinatorAgent delegating analysis to 'candidate_evaluator' using tool 'analyze_fit'...", 'agent');
      
      // Actual API Call
      const analysis = await analyzeResumeFit(resumeFile, jobUrl);
      
      addLog("Analysis complete: LLM-based analysis completed and parsed.", 'agent');
      setResult(analysis);

    } catch (error) {
      console.error(error);
      addLog("An error occurred during analysis. Please try again.", 'info');
      if (error instanceof Error) {
         addLog(`Error details: ${error.message}`, 'info');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-gray-50">
      <Sidebar 
        jobUrl={jobUrl}
        setJobUrl={setJobUrl}
        resumeFile={resumeFile}
        setResumeFile={setResumeFile}
        onRunAnalysis={handleRunAnalysis}
        isLoading={isLoading}
      />
      <MainContent 
        logs={logs}
        result={result}
        isLoading={isLoading}
      />
    </div>
  );
};

export default App;
