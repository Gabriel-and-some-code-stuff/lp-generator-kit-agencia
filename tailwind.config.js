/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
    },
    extend: {
      colors: {
        primary: {
          100: '#E0F7FA', // Light Cyan
          200: '#B2EBF2', // Pale Cyan
          300: '#80DEEA', // Light Blue-Cyan
          400: '#4DD0E1', // Medium Blue-Cyan
          500: '#00BCD4', // Primary Blue-Cyan (similar to original secondary button, good for cleaning)
          600: '#00ACC1', // Darker Blue-Cyan
          700: '#0097A7', // Even Darker Blue-Cyan
          800: '#00838F', // Deep Blue-Cyan
          900: '#006064', // Very Deep Blue-Cyan
        },
        gray: {
          50: '#F8FAFC',
          100: '#F1F5F9',
          200: '#E2E8F0',
          300: '#CBD5E1',
          400: '#94A3B8',
          500: '#64748B',
          600: '#475569',
          700: '#334155',
          800: '#1E293B',
          900: '#0F172A',
        },
      },
      lineHeight: {
        hero: '1.1',
      },
    },
  },
  plugins: [],
};
