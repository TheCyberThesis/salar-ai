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
      className={`focus-ring inline-flex items-center gap-2 rounded-lg border px-3 py-2 font-mono text-xs font-bold uppercase tracking-wider transition ${
        copied
          ? "border-civic-green/30 bg-civic-green/10 text-civic-green"
          : "border-civic-border bg-civic-elevated text-civic-muted hover:border-civic-muted/40 hover:text-civic-text"
      }`}
    >
      {copied
        ? <Check className="h-3.5 w-3.5" aria-hidden="true" />
        : <Copy className="h-3.5 w-3.5" aria-hidden="true" />}
      {copied ? "Copied" : label}
    </button>
  );
}
