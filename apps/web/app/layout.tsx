import type { Metadata } from "next";

import { AssistantHeader } from "@/components/AssistantHeader";
import "./globals.css";

export const metadata: Metadata = {
  title: "Salaar AI",
  description: "AI-powered civic guidance for Pakistani citizens."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AssistantHeader />
        {children}
      </body>
    </html>
  );
}
