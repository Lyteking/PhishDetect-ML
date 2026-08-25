import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: "#0a0a0f",
          gray: "#1e1e24",
          light: "#a1a1aa",
          primary: "#00f0ff", // Neon Cyan
          secondary: "#7000ff", // Deep Purple
          danger: "#ff0055", // Neon Red
          safe: "#00ff88", // Neon Green
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        mono: ['var(--font-fira-code)', 'monospace'],
      },
    },
  },
  plugins: [],
};
export default config;