'use client'

import { useState } from "react";
import { Shield, ShieldAlert, Activity, Lock, Globe, Server, ChevronRight, Loader2 } from "lucide-react";
import { analyzeUrl, type PredictionResult } from "./actions";
import AnimatedLogo from '@/components/AnimatedLogo';

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('url', url);
    
    const res = await analyzeUrl(formData);
    setResult(res);
    setLoading(false);
  };

  return (
    <div className="space-y-12">
      {/* Header Section */}
      <header className="border-b border-cyber-gray pb-8">
        <div className="flex items-center gap-3 mb-2">
          <AnimatedLogo className="w-16 h-16" />
          <h1 className="text-3xl font-bold tracking-tight">PhishDetect<span className="text-cyber-primary">.ML</span></h1>
        </div>
        <p className="text-cyber-light max-w-2xl">
          Real-time URL classification powered by an XGBoost & Random Forest hybrid ensemble. 
          Analyzes structural, domain, and client-scripting features to detect zero-day threats.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Input & Status */}
        <div className="lg:col-span-1 space-y-6">
          {/* Scanner Input */}
          <div className="bg-cyber-gray/50 border border-cyber-gray p-6 rounded-xl">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <Globe className="w-5 h-5 text-cyber-primary" />
              Target Analysis
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="url" className="sr-only">URL to scan</label>
                <input
                  type="url"
                  id="url"
                  name="url"
                  required
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full bg-cyber-dark border border-cyber-gray rounded-lg px-4 py-3 text-sm font-mono focus:outline-none focus:border-cyber-primary focus:ring-1 focus:ring-cyber-primary transition-colors"
                />
              </div>
              <button
                type="submit"
                disabled={loading || !url}
                className="w-full bg-cyber-primary hover:bg-cyber-primary/90 text-white border border-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing Vector...
                  </>
                ) : (
                  <>
                    Initialize Scan <ChevronRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </form>
          </div>

          {/* System Status Metrics */}
          <div className="bg-cyber-gray/50 border border-cyber-gray p-6 rounded-xl space-y-4">
             <h3 className="text-sm font-semibold text-cyber-light uppercase tracking-wider mb-4">Ensemble Status</h3>
             <div className="flex justify-between items-center pb-3 border-b border-cyber-gray/50">
               <span className="text-sm text-cyber-light flex items-center gap-2"><Server className="w-4 h-4"/> Active Model</span>
               <span className="text-sm font-mono text-white">XGBoost Ensemble</span>
             </div>
             <div className="flex justify-between items-center pb-3 border-b border-cyber-gray/50">
               <span className="text-sm text-cyber-light flex items-center gap-2"><Activity className="w-4 h-4"/> Base Accuracy</span>
               <span className="text-sm font-mono text-cyber-safe">97.52%</span>
             </div>
             <div className="flex justify-between items-center">
               <span className="text-sm text-cyber-light flex items-center gap-2"><Lock className="w-4 h-4"/>Precision</span>
               <span className="text-sm font-mono text-cyber-primary">97.50%</span>
             </div>
          </div>
        </div>

        {/* Right Column: Results & Diagnostics */}
        <div className="lg:col-span-2">
          {result ? (
            <div className="space-y-6">
              
              {/* Primary Verdict Card - MOBILE OPTIMIZED */}
              <div className={`p-4 sm:p-6 rounded-xl border ${result.isPhishing ? 'bg-cyber-danger/10 border-cyber-danger' : 'bg-cyber-safe/10 border-cyber-safe'} transition-all duration-500`}>
                
                {/* TOP SECTION: Icon and Title aligned together */}
                <div className="flex items-center gap-3 sm:gap-4">
                  <div className={`flex-shrink-0 p-2 sm:p-4 rounded-full ${result.isPhishing ? 'bg-cyber-danger/20 text-cyber-danger' : 'bg-cyber-safe/20 text-cyber-safe'}`}>
                    {result.isPhishing ? <ShieldAlert className="w-8 h-8 sm:w-10 sm:h-10" /> : <Shield className="w-8 h-8 sm:w-10 sm:h-10" />}
                  </div>
                  <h2 className={`text-lg sm:text-2xl font-bold leading-tight uppercase ${result.isPhishing ? 'text-cyber-danger' : 'text-cyber-safe'}`}>
                    {result.isPhishing ? 'MALICIOUS DOMAIN DETECTED' : 'LEGITIMATE DOMAIN'}
                  </h2>
                </div>

                {/* BOTTOM SECTION: URL and Badges stretching full width */}
                <div className="mt-3 sm:mt-2 sm:ml-[5.5rem]">
                  <p 
                    className="text-cyber-light font-mono text-sm break-all line-clamp-2" 
                    title={result.url}
                  >
                    {result.url}
                  </p>
                  <div className="flex flex-wrap gap-3 mt-4 text-sm">
                    <span className="bg-cyber-dark px-3 py-1.5 rounded-md border border-cyber-gray">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </span>
                    <span className="bg-cyber-dark px-3 py-1.5 rounded-md border border-cyber-gray text-cyber-light">
                      Time: {new Date(result.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>

              </div>

              {/* Diagnostic Breakdown */}
              <div className="bg-cyber-gray/50 border border-cyber-gray rounded-xl overflow-hidden">
                <div className="px-6 py-4 border-b border-cyber-gray bg-cyber-gray/30">
                  <h3 className="font-semibold">Feature Extraction Diagnostics</h3>
                  <p className="text-xs text-cyber-light mt-1">Explainable AI (XAI) Feature Breakdown</p>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(result.features).map(([key, value]) => {
              
                      // 1. Grab the exact mathematical SHAP impact from the FastAPI backend
                      const shapImpact = result.xai_diagnostics?.shap_values?.[key] || 0;
                      
                      // 2. Determine the threat level (Positive SHAP = Phishing Threat)
const isDanger = value === 1;                      
                      // 3. Dynamically apply Tailwind CSS Red or Green colors (MOBILE OPTIMIZED)
                      return (
                        <div 
                          key={key} 
                          className={`flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 p-3 border rounded-md transition-colors ${
                            isDanger 
                              ? 'bg-red-900/20 border-red-500/50 text-red-400' 
                              : 'bg-gray-800/30 border-gray-700/50 text-gray-300'
                          }`}
                        >
                          <span className="font-semibold tracking-wide capitalize text-sm sm:text-base break-words">
                            {key.replace(/_/g, ' ')}
                          </span>
                          <div className="text-left sm:text-right mt-1 sm:mt-0">
                            <span className="block font-bold text-base sm:text-lg">
                              {value === 1 ? 'Detected' : 'Clean'}
                            </span>
                            <span className="text-xs opacity-75">
                              XAI Impact: {shapImpact > 0 ? '+' : ''}{shapImpact.toFixed(3)}
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full min-h-[400px] border-2 border-dashed border-cyber-gray rounded-xl flex flex-col items-center justify-center text-cyber-light">
              <Activity className="w-12 h-12 mb-4 opacity-50" />
              <p>Awaiting URL input for classification...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Helper component for diagnostic visualization
function FeatureIndicator({ featureName, value }: { featureName: string, value: number }) {
  // NEW MAPPING: In the 17-feature model, 0 = Safe, 1 = Suspicious/Phishing
  let stateColor = "text-cyber-safe bg-cyber-safe/10 border-cyber-safe/20";
  let stateText = "Legitimate";

  if (value === 1) {
    stateColor = "text-cyber-danger bg-cyber-danger/10 border-cyber-danger/20";
    stateText = "Suspicious / Phishing";
  }

  return (
    <div className="flex items-center justify-between p-3 bg-cyber-dark border border-cyber-gray rounded-lg">
      <span className="font-mono text-sm text-gray-300">{featureName}</span>
      <span className={`text-xs px-2 py-1 border rounded font-semibold ${stateColor}`}>
        {stateText}
      </span>
    </div>
  );
}