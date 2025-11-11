// tailwind.config.cjs
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',   // Deep Blue
        secondary: '#06B6D4', // Cyan
        accent: '#FACC15',    // Yellow for warnings
        bgLight: '#F8FAFC',   // Background
        textDark: '#0F172A',  // Headings
        textGray: '#475569',  // Body text
      },
      boxShadow: {
        soft: '0 4px 14px rgba(37, 99, 235, 0.1)',   // Blue glow
        card: '0 4px 20px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [],
};
