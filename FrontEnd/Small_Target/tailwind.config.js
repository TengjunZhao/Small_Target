/** @type {import('tailwindcss').Config} */
export default {
  // 扫描所有Vue/JS/TS文件，确保样式能被编译
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
