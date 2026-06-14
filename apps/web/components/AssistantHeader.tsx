import Link from "next/link";
import { Landmark, MessageSquareText, ShieldCheck } from "lucide-react";

export function AssistantHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-civic-line/80 bg-white/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-lg bg-civic-green text-white">
            <Landmark className="h-5 w-5" aria-hidden="true" />
          </span>
          <span>
            <span className="block font-heading text-lg font-bold tracking-normal text-civic-ink">Salaar AI</span>
            <span className="block font-mono text-[11px] uppercase tracking-normal text-civic-muted">Public guidance assistant</span>
          </span>
        </Link>
        <nav className="flex items-center gap-2 text-sm font-medium text-civic-muted">
          <Link className="hidden rounded-md px-3 py-2 hover:bg-civic-mint sm:inline-flex" href="/dashboard">
            Dashboard
          </Link>
          <Link className="inline-flex items-center gap-2 rounded-md bg-civic-blue px-3 py-2 text-white shadow-sm hover:bg-blue-800" href="/chat">
            <MessageSquareText className="h-4 w-4" aria-hidden="true" />
            Chat
          </Link>
        </nav>
      </div>
      <div className="border-t border-civic-line/70 bg-civic-warning">
        <div className="mx-auto flex max-w-7xl items-center gap-2 px-4 py-2 font-mono text-[11px] text-civic-ink sm:px-6 lg:px-8">
          <ShieldCheck className="h-4 w-4 shrink-0 text-civic-green" aria-hidden="true" />
          General AI guidance only. Verify requirements with the relevant Pakistani authority.
        </div>
      </div>
    </header>
  );
}
