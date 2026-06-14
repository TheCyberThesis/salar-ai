import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        civic: {
          ink: "#102027",
          muted: "#5e6b73",
          green: "#157f63",
          blue: "#1864ab",
          sky: "#dff5ff",
          mint: "#e8f7ef",
          line: "#d9e5e8",
          warning: "#fff7df"
        }
      },
      fontFamily: {
        heading: ["Space Grotesk", "Inter", "Arial", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Consolas", "monospace"]
      },
      boxShadow: {
        soft: "0 18px 60px rgba(16, 32, 39, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;
