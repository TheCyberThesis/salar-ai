"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";

export function CopyButton({ text, label = "Copy" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <button
      type="button"
      onClick={copy}
      className="focus-ring inline-flex items-center gap-2 rounded-md border border-civic-line bg-white px-3 py-2 text-sm font-semibold text-civic-ink hover:bg-civic-mint"
    >
      {copied ? <Check className="h-4 w-4 text-civic-green" aria-hidden="true" /> : <Copy className="h-4 w-4 text-civic-blue" aria-hidden="true" />}
      {copied ? "Copied" : label}
    </button>
  );
}
