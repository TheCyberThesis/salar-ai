import Link from "next/link";
import { MessageSquareText, Shield } from "lucide-react";

export function AssistantHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-civic-border bg-civic-bg/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">

        {/* Logo */}
        <Link href="/" className="group flex items-center gap-3">
          <span className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-civic-green/10 ring-1 ring-civic-green/30 transition-all group-hover:ring-civic-green/60 group-hover:shadow-glow-sm">
            <span className="font-mono text-sm font-bold text-civic-green">&gt;_</span>
          </span>
          <span>
            <span className="block font-mono text-sm font-bold uppercase tracking-widest text-civic-text">
              Salar<span className="text-civic-green">AI</span>
            </span>
            <span className="block font-mono text-[10px] uppercase tracking-widest text-civic-muted">
              civic guidance
            </span>
          </span>
        </Link>

        {/* Nav */}
        <nav className="flex items-center gap-2">
          <Link
            href="/dashboard"
            className="focus-ring hidden rounded-md px-3 py-2 font-mono text-xs uppercase tracking-wider text-civic-muted transition hover:bg-civic-elevated hover:text-civic-text sm:inline-flex"
          >
            Dashboard
          </Link>
          <Link
            href="/chat"
            className="focus-ring inline-flex items-center gap-2 rounded-md bg-civic-green px-4 py-2 font-mono text-xs font-bold uppercase tracking-wider text-white shadow-glow-sm transition hover:brightness-110"
          >
            <MessageSquareText className="h-3.5 w-3.5" aria-hidden="true" />
            Chat
          </Link>
        </nav>
      </div>

      {/* Disclaimer bar */}
      <div className="border-t border-civic-border/60 bg-civic-amber-glow">
        <div className="mx-auto flex max-w-7xl items-center gap-2 px-4 py-1.5 sm:px-6 lg:px-8">
          <Shield className="h-3.5 w-3.5 shrink-0 text-civic-amber" aria-hidden="true" />
          <span className="font-mono text-[10px] uppercase tracking-widest text-civic-amber/80">
            General AI guidance only — verify with the relevant Pakistani authority before submitting
          </span>
        </div>
      </div>
    </header>
  );
}
