/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
        jarvis: {
          bg: '#080c14',
          surface: '#0d1421',
          card: '#0f1928',
          border: '#1a2740',
          cyan: '#00d4ff',
          green: '#10b981',
          purple: '#8b5cf6',
          orange: '#f97316',
          amber: '#f59e0b',
          pink: '#ec4899',
          red: '#ef4444',
          text: '#e2e8f0',
          muted: '#64748b',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'blink': 'blink 1.2s step-end infinite',
      },
      keyframes: {
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
      },
    },
  },
  plugins: [],
}
