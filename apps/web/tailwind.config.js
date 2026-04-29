/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Background
        'void': '#0A0E14',
        'surface': '#12171F',
        'card': '#1A212B',
        'border': '#2A3340',
        
        // Accent
        'active': '#00E676',
        'processing': '#448AFF',
        'warning': '#FF9100',
        'innovation': '#B388FF',
        'error': '#FF5252',
        
        // Agent specific
        'strategist': '#448AFF',
        'mentor': '#FF9100',
        'executor': '#00E676',
        'innovator': '#B388FF',
        'amplifier': '#40C4FF',
        'reflector': '#FF80AB',
        
        // Text
        'text-primary': '#E0E6ED',
        'text-secondary': '#8899AA',
        'text-muted': '#556677',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'system': ['12px', { lineHeight: '1.5', fontFeatureSettings: '"tnum"' }],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}