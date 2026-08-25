import React from 'react';

export default function AnimatedLogo({ className = "w-12 h-12" }: { className?: string }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 512 512" 
      fill="none"
      className={className}
    >
      <defs>
        {/* Shield Clipping Path to keep the laser inside the borders */}
        <clipPath id="shield-clip">
          <path d="M256 32 L464 128 V384 L256 480 L48 384 V128 Z" />
        </clipPath>

        {/* Glow Filter */}
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="8" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>

        {/* Text Gradient */}
        <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6ee7b7" />   {/* Emerald 300 */}
          <stop offset="100%" stopColor="#047857" /> {/* Emerald 700 */}
        </linearGradient>

        {/* Laser Scanner Aura Gradient */}
        <linearGradient id="scan-aura" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#10b981" stopOpacity="0" />
          <stop offset="50%" stopColor="#10b981" stopOpacity="0.5" />
          <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
        </linearGradient>

        <style>
          {`
            .scanner-line {
              animation: scan 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
            }
            @keyframes scan {
              0% { transform: translateY(0px); }
              100% { transform: translateY(512px); }
            }
          `}
        </style>
      </defs>

      {/* Subtle Shield Background */}
      <path 
        d="M256 32 L464 128 V384 L256 480 L48 384 V128 Z" 
        fill="#064e3b" 
        fillOpacity="0.2" 
      />

      {/* The Initials: PD */}
      <text 
        x="256" 
        y="305" 
        fontFamily="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" 
        fontWeight="900" 
        fontSize="170" 
        fill="url(#text-grad)" 
        textAnchor="middle" 
        letterSpacing="-8"
        filter="url(#glow)"
      >
        PD
      </text>

      {/* Animated Laser Scanner (Clipped strictly inside the shield) */}
      <g clipPath="url(#shield-clip)">
        <g className="scanner-line">
          {/* Glowing Aura around the line */}
          <rect x="0" y="-30" width="512" height="60" fill="url(#scan-aura)" />
          {/* Solid Laser Line */}
          <line x1="0" y1="0" x2="512" y2="0" stroke="#34d399" strokeWidth="6" filter="url(#glow)" />
        </g>
      </g>

      {/* Outer Shield Border */}
      <path 
        d="M256 32 L464 128 V384 L256 480 L48 384 V128 Z" 
        stroke="#10b981" 
        strokeWidth="24" 
        strokeLinejoin="round" 
        filter="url(#glow)" 
      />
    </svg>
  );
}