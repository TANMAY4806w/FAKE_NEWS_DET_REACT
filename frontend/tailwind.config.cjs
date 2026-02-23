// tailwind.config.cjs
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',     // Vibrant Blue
        secondary: '#8B5CF6',   // Neon Purple
        accent: '#10B981',      // Emerald Green (Real)
        danger: '#EF4444',      // Neon Red (Fake)
        bgDark: '#0B0F19',      // Deep Space background
        cardDark: 'rgba(15, 23, 42, 0.6)',   // Glass panel base
        textWhite: '#F8FAFC',
        textGray: '#94A3B8',
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        glowBlue: '0 0 20px rgba(59, 130, 246, 0.5)',
        glowRed: '0 0 20px rgba(239, 68, 68, 0.4)',
        glowGreen: '0 0 20px rgba(16, 185, 129, 0.4)',
      },
      animation: {
        'blob': 'blob 7s infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        blob: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
          '100%': { transform: 'translate(0px, 0px) scale(1)' },
        }
      }
    },
  },
  plugins: [],
};
