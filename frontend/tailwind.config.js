/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // enable dark theme toggle if desired
  theme: {
    extend: {
      colors: {
        dark: "#1a1a1a",
        darker: "#121212",
        primary: "#4f46e5",
        accent: "#10b981",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};