import React from 'react';
import { Search, CheckCircle, Activity, AlertCircle, Briefcase, UserCheck, ArrowRight } from 'lucide-react';
import { AnalysisResult, LogEntry } from '../types';

interface MainContentProps {
  logs: LogEntry[];
  result: AnalysisResult | null;
  isLoading: boolean;
}

const MainContent: React.FC<MainContentProps> = ({ logs, result, isLoading }) => {
  return (
    <div className="flex-1 h-full overflow-y-auto bg-white p-6 md:p-10">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Search className="text-gray-700" size={32} />
            <h1 className="text-3xl font-bold text-green-600">AI Job Search Assistant</h1>
          </div>
          <p className="text-gray-600">Discover tailored job recommendations powered by Agentic AI.</p>
        </div>

        {/* Live Logs & Status Area */}
        <div className="space-y-3 mb-8">
          {logs.map((log) => (
            <div 
              key={log.id}
              className={`
                flex items-start gap-3 p-3 rounded-lg text-sm animate-fade-in
                ${log.type === 'success' ? 'bg-green-50 text-green-800 border border-green-100' : ''}
                ${log.type === 'agent' ? 'bg-gray-50 text-gray-700 font-mono text-xs border border-gray-100' : ''}
                ${log.type === 'info' ? 'bg-blue-50 text-blue-800 border border-blue-100' : ''}
              `}
            >
              {log.type === 'success' && <CheckCircle size={16} className="mt-0.5 shrink-0" />}
              {log.type === 'agent' && <Activity size={14} className="mt-0.5 shrink-0 text-purple-500" />}
              {log.type === 'info' && <AlertCircle size={16} className="mt-0.5 shrink-0" />}
              <span>{log.message}</span>
            </div>
          ))}
        </div>

        {/* Results Section */}
        {result && !isLoading && (
          <div className="animate-slide-up">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Analysis Report</h2>

            {/* Summary Card */}
            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm mb-8 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
              <div className="flex justify-between items-start mb-4">
                 <h3 className="text-lg font-semibold text-gray-900">Overall Fit Summary</h3>
                 <div className="flex items-center gap-1 bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-bold">
                    <span>Match Score:</span>
                    <span>{result.matchScore}%</span>
                 </div>
              </div>
              <p className="text-gray-700 leading-relaxed">
                {result.overallFitSummary}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              {/* Candidate Skills */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <UserCheck className="text-blue-600" size={20} />
                  <h3 className="text-lg font-semibold text-gray-800">Candidate Skills</h3>
                </div>
                <ul className="space-y-2">
                  {result.candidateSkills.map((skill, idx) => (
                    <li key={idx} className="flex items-center text-gray-700 text-sm bg-gray-50 p-2 rounded border border-gray-100">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></div>
                      {skill}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Required Job Skills */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Briefcase className="text-purple-600" size={20} />
                  <h3 className="text-lg font-semibold text-gray-800">Required Job Skills</h3>
                </div>
                <ul className="space-y-2">
                  {result.requiredJobSkills.map((skill, idx) => (
                    <li key={idx} className="flex items-center text-gray-700 text-sm bg-gray-50 p-2 rounded border border-gray-100">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2"></div>
                      {skill}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Gap Analysis */}
            {result.gapAnalysis.length > 0 && (
               <div className="bg-orange-50 border border-orange-100 rounded-xl p-6">
                  <div className="flex items-center gap-2 mb-4">
                     <AlertCircle className="text-orange-600" size={20} />
                     <h3 className="text-lg font-semibold text-orange-800">Gap Analysis & Recommendations</h3>
                  </div>
                  <ul className="space-y-3">
                     {result.gapAnalysis.map((gap, idx) => (
                        <li key={idx} className="flex items-start gap-3 text-sm text-gray-800">
                           <ArrowRight size={16} className="text-orange-400 mt-0.5 shrink-0" />
                           <span>{gap}</span>
                        </li>
                     ))}
                  </ul>
               </div>
            )}
          </div>
        )}
        
        {!result && !isLoading && logs.length === 0 && (
           <div className="flex flex-col items-center justify-center h-64 text-gray-400 border-2 border-dashed border-gray-200 rounded-xl">
              <Search size={48} className="mb-4 opacity-20" />
              <p className="text-sm font-medium">Enter a job URL and upload a resume to start</p>
           </div>
        )}

      </div>
    </div>
  );
};

export default MainContent;
