import type { Metadata } from "next";
import { Inter, Fira_Code } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: '--font-inter' });
const firaCode = Fira_Code({ subsets: ["latin"], variable: '--font-fira-code' });

export const metadata: Metadata = {
  title: "PhishDetect ML | Real-Time URL Classification",
  description: "Advanced Machine Learning Ensemble for Phishing Detection",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      {/* 1. Added suppressHydrationWarning to fix the Grammarly error */}
      <body 
        suppressHydrationWarning 
        className={`${inter.variable} ${firaCode.variable} font-sans bg-cyber-dark text-white min-h-screen antialiased selection:bg-emerald-500/30 selection:text-emerald-200`}
      >
        <main className="max-w-7xl mx-auto px-6 py-12">
          {children}
        </main>
      </body>
    </html>
  );
}