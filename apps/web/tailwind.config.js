/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'jarvis-bg': '#f3f4f6',
        'jarvis-primary': '#6366f1',
        'jarvis-secondary': '#8b5cf6',
      }
    },
  },
  plugins: [],
}
