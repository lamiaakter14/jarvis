/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'jarvis-bg': '#0A0E14',
        'jarvis-surface': '#0F1419',
        'jarvis-card': '#151A22',
        'jarvis-border': '#232A34',
        'jarvis-text': '#DDE4ED',
        'jarvis-muted': '#8899AA',
        'jarvis-cyan': '#00d4ff',
        'jarvis-green': '#00E676',
        'jarvis-purple': '#B388FF',
        'jarvis-amber': '#FF9100',
        'jarvis-orange': '#FF80AB',
      },
      animation: {
        'pulse-slow': 'pulse 3s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
