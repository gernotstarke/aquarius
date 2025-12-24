/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      spacing: {
        // Base-8 grid for ample whitespace
        '18': '4.5rem',
        '22': '5.5rem',
        '26': '6.5rem',
      },
      fontSize: {
        // Large, readable typography
        'display': ['3rem', { lineHeight: '1.2', letterSpacing: '-0.02em' }],
        'h1': ['2.5rem', { lineHeight: '1.3', letterSpacing: '-0.01em' }],
        'h2': ['2rem', { lineHeight: '1.4' }],
        'h3': ['1.5rem', { lineHeight: '1.5' }],
        'body-lg': ['1.125rem', { lineHeight: '1.6' }],
        'body': ['1rem', { lineHeight: '1.6' }],
      },
      colors: {
        // Simple, accessible color palette
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
      },
      minHeight: {
        'touch': '44px', // Touch-friendly minimum
      },
      minWidth: {
        'touch': '44px',
      },
    },
  },
  plugins: [],
}
