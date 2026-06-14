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
          bg:        "#f2f6fa",
          surface:   "#ffffff",
          elevated:  "#eaf1f7",
          border:    "#d8e8f2",
          "border-bright": "rgba(0,148,74,0.30)",
          green:     "#00944a",
          "green-dim": "#007a3d",
          "green-glow": "rgba(0,148,74,0.09)",
          blue:      "#1864ab",
          "blue-dim": "#104e8a",
          "blue-glow": "rgba(24,100,171,0.09)",
          amber:     "#b96c00",
          "amber-glow": "rgba(185,108,0,0.09)",
          text:      "#0c1d2c",
          muted:     "#4f6e84",
          dim:       "#c2d8e8",
          red:       "#c0392b",

          /* legacy aliases */
          ink:     "#0c1d2c",
          line:    "#d8e8f2",
          mint:    "rgba(0,148,74,0.07)",
          sky:     "rgba(24,100,171,0.07)",
          warning: "rgba(185,108,0,0.09)",
        }
      },
      fontFamily: {
        sans:    ["var(--font-grotesk)", "Space Grotesk", "Inter", "system-ui", "sans-serif"],
        heading: ["var(--font-grotesk)", "Space Grotesk", "Inter", "system-ui", "sans-serif"],
        mono:    ["var(--font-mono)",    "JetBrains Mono", "Consolas", "monospace"],
      },
      boxShadow: {
        soft:        "0 20px 60px rgba(12,29,44,0.13)",
        glow:        "0 0 24px rgba(0,148,74,0.18)",
        "glow-sm":   "0 0 12px rgba(0,148,74,0.14)",
        "glow-blue": "0 0 24px rgba(24,100,171,0.16)",
        card:        "0 2px 16px rgba(12,29,44,0.08), 0 1px 4px rgba(12,29,44,0.04)",
      },
      keyframes: {
        blink:      { "0%,49%": { opacity: "1" }, "50%,100%": { opacity: "0" } },
        pulse3:     { "0%,100%": { opacity: "0.3" }, "50%": { opacity: "1" } },
        "slide-up": { from: { opacity: "0", transform: "translateY(10px)" }, to: { opacity: "1", transform: "translateY(0)" } },
        shimmer:    { from: { backgroundPosition: "200% 0" }, to: { backgroundPosition: "-200% 0" } },
      },
      animation: {
        blink:      "blink 1.1s step-end infinite",
        pulse3:     "pulse3 1.4s ease-in-out infinite",
        "slide-up": "slide-up 0.35s ease-out forwards",
        shimmer:    "shimmer 2.4s linear infinite",
      }
    }
  },
  plugins: []
};

export default config;
