'use server'

import { revalidatePath } from "next/cache";

export type PredictionResult = {
  url: string;
  isPhishing: boolean;
  confidence: number;
  features: Record<string, any>;
  timestamp: string;
  error?: string;
  xai_diagnostics?: {
    shap_values: Record<string, number>;
    lime_top_features: Record<string, number>;
  };
};

export async function analyzeUrl(formData: FormData): Promise<PredictionResult> {
  const url = formData.get('url') as string;

  if (!url || typeof url !== 'string') {
    return { url: '', isPhishing: false, confidence: 0, features: {}, timestamp: '', error: 'Valid URL is required' };
  }

  try {
    // Send POST request to FastAPI backend
    const response = await fetch('https://phishdetect-ml.onrender.com/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
      cache: 'no-store' // Prevent Next.js from caching dynamic scan results
    });

    if (!response.ok) {
      throw new Error(`API responded with status: ${response.status}`);
    }

    const data = await response.json();
    
    // Refresh the UI state
    revalidatePath('/');
    return data;
    
  } catch (error) {
    console.error("Inference Connection Error:", error);
    return { url, isPhishing: false, confidence: 0, features: {}, timestamp: '', error: 'Failed to connect to ML Engine' };
  }
}