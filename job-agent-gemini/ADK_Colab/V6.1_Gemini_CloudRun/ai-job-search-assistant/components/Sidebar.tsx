import React, { useState } from 'react';
import { HelpCircle, FileText, X, UploadCloud } from 'lucide-react';

interface SidebarProps {
  jobUrl: string;
  setJobUrl: (url: string) => void;
  resumeFile: File | null;
  setResumeFile: (file: File | null) => void;
  onRunAnalysis: () => void;
  isLoading: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({
  jobUrl,
  setJobUrl,
  resumeFile,
  setResumeFile,
  onRunAnalysis,
  isLoading
}) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
    }
  };

  const removeFile = () => {
    setResumeFile(null);
  };

  return (
    <div className="w-full md:w-80 lg:w-96 bg-white border-r border-gray-200 flex flex-col h-full p-6 shrink-0 overflow-y-auto">
      <h2 className="text-xl font-bold text-gray-800 mb-6">User Inputs</h2>

      {/* Job URL Input */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <label htmlFor="jobUrl" className="text-sm font-medium text-gray-700">
            Job Description URL
          </label>
          <HelpCircle size={16} className="text-gray-400 cursor-help" />
        </div>
        <input
          id="jobUrl"
          type="url"
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
          placeholder="https://www.linkedin.com/jobs/..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-sm transition-shadow"
        />
      </div>

      {/* File Upload */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-medium text-gray-700">
            Upload Your Resume (PDF)
          </label>
          <HelpCircle size={16} className="text-gray-400 cursor-help" />
        </div>

        {!resumeFile ? (
          <div className="relative group">
            <input
              type="file"
              id="resume-upload"
              accept="application/pdf"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col items-center justify-center bg-gray-50 group-hover:bg-gray-100 transition-colors text-center">
               <div className="bg-white p-2 rounded-full shadow-sm mb-3">
                  <UploadCloud className="text-green-600" size={24} />
               </div>
              <p className="text-sm font-medium text-gray-900 mb-1">Click or drop file here</p>
              <p className="text-xs text-gray-500">Limit 200MB per file • PDF</p>
              <span className="mt-4 px-3 py-1.5 bg-white border border-gray-300 rounded-md text-xs font-medium text-gray-700 shadow-sm group-hover:bg-gray-50">
                Browse files
              </span>
            </div>
          </div>
        ) : (
          <div className="flex items-center p-3 bg-gray-50 border border-gray-200 rounded-lg shadow-sm">
            <div className="bg-blue-100 p-2 rounded-md mr-3">
               <FileText className="text-blue-600" size={20} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {resumeFile.name}
              </p>
              <p className="text-xs text-gray-500">
                {(resumeFile.size / 1024).toFixed(1)} KB
              </p>
            </div>
            <button
              onClick={removeFile}
              className="p-1 hover:bg-gray-200 rounded-full text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X size={18} />
            </button>
          </div>
        )}
      </div>

      {/* Action Button */}
      <button
        onClick={onRunAnalysis}
        disabled={isLoading || !jobUrl || !resumeFile}
        className={`w-full py-2.5 px-4 rounded-md font-medium text-sm shadow-sm transition-all
          ${
            isLoading || !jobUrl || !resumeFile
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
              : 'bg-white text-green-600 border border-green-500 hover:bg-green-50 active:bg-green-100'
          }
        `}
      >
        {isLoading ? 'Analyzing...' : 'Run Analysis'}
      </button>
      
      <div className="mt-auto pt-6 text-xs text-gray-400">
        <p>Powered by Gemini 2.5 Flash</p>
      </div>
    </div>
  );
};

export default Sidebar;
