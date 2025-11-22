import { GoogleGenAI, Type } from "@google/genai";
import { AnalysisResult } from "../types";

// Initialize Gemini Client
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

// Helper to convert File to Base64
const fileToGenerativePart = async (file: File): Promise<{ inlineData: { data: string; mimeType: string } }> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64Data = reader.result as string;
      // Remove the data URL prefix (e.g., "data:application/pdf;base64,")
      const base64Content = base64Data.split(',')[1];
      resolve({
        inlineData: {
          data: base64Content,
          mimeType: file.type,
        },
      });
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

export const analyzeResumeFit = async (
  resumeFile: File,
  jobUrl: string
): Promise<AnalysisResult> => {
  try {
    const resumePart = await fileToGenerativePart(resumeFile);

    // Use Gemini 2.5 Flash for speed and multimodal capabilities
    const model = 'gemini-2.5-flash';

    const prompt = `
      You are an expert Technical Recruiter and Hiring Manager.
      
      Task:
      1. Analyze the provided Resume (PDF).
      2. Find and analyze the Job Description located at this URL: "${jobUrl}".
         If you cannot directly access the URL content due to restrictions, infer the likely requirements based on the URL structure (e.g., job title, company) and use your internal knowledge base about standard requirements for such roles, or perform a Google Search if tools permit.
      
      Output Requirements:
      Provide a structured JSON report containing:
      - Overall Fit Summary: A professional assessment of the candidate's fit for the role.
      - Candidate Skills: A list of key skills found in the resume relevant to the role.
      - Required Job Skills: A list of key skills required by the job.
      - Gap Analysis: A list of specific missing skills or qualifications that the candidate lacks but the job requires.
      - Match Score: A generic integer score from 0 to 100 indicating the fit.
    `;

    const response = await ai.models.generateContent({
      model: model,
      contents: {
        parts: [
          resumePart,
          { text: prompt }
        ]
      },
      config: {
        tools: [{ googleSearch: {} }], // Enable Search to help find the Job Description if needed
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            overallFitSummary: { type: Type.STRING },
            candidateSkills: { 
              type: Type.ARRAY, 
              items: { type: Type.STRING } 
            },
            requiredJobSkills: { 
              type: Type.ARRAY, 
              items: { type: Type.STRING } 
            },
            gapAnalysis: { 
              type: Type.ARRAY, 
              items: { type: Type.STRING } 
            },
            matchScore: { type: Type.INTEGER }
          },
          required: ["overallFitSummary", "candidateSkills", "requiredJobSkills", "gapAnalysis", "matchScore"]
        }
      }
    });

    if (response.text) {
      return JSON.parse(response.text) as AnalysisResult;
    } else {
      throw new Error("No response text generated.");
    }

  } catch (error) {
    console.error("Error analyzing resume:", error);
    throw error;
  }
};
