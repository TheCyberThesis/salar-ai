import Link from "next/link";
import { ArrowRight, CheckCircle2, FileText, MessageSquareText, Terminal, Zap } from "lucide-react";

import { QuickIssueCards } from "@/components/QuickIssueCards";

const steps = [
  { num: "01", title: "Describe your issue", body: "Type in English, Urdu, or Roman Urdu. Salar AI detects the domain automatically." },
  { num: "02", title: "Answer follow-up questions", body: "AI asks only the missing details needed to generate a complete application." },
  { num: "03", title: "Get a filled guidance report", body: "Department, procedure, complaint draft, nearest office, and proof checklist — all generated." },
  { num: "04", title: "Submit and collect proof", body: "Visit the relevant office and collect your diary number, FIR, or reference receipt." },
];

const domains = [
  "Lost/stolen phone, bike, or car",
  "Utility bill overcharging",
  "Workplace harassment against women",
];

export default function HomePage() {
  return (
    <main className="min-h-screen">

      {/* ── Hero ──────────────────────────────────────────────── */}
      <section className="relative overflow-hidden border-b border-civic-border">

        {/* Dot-grid bg */}
        <div className="civic-grid absolute inset-0 opacity-70" />

        {/* Radial blobs */}
        <div className="pointer-events-none absolute -left-40 top-0 h-[500px] w-[500px] rounded-full bg-civic-green/[0.04] blur-3xl" />
        <div className="pointer-events-none absolute -right-32 bottom-0 h-[400px] w-[400px] rounded-full bg-civic-blue/[0.05] blur-3xl" />

        <div className="relative mx-auto max-w-7xl px-4 pb-28 pt-20 sm:px-6 lg:px-8">

          {/* Terminal badge */}
          <div className="mb-8 inline-flex items-center gap-2.5 rounded-full border border-civic-green/25 bg-civic-green/8 px-4 py-2">
            <span className="h-2 w-2 animate-pulse rounded-full bg-civic-green shadow-glow-sm" />
            <span className="font-mono text-[11px] uppercase tracking-widest text-civic-green">Pakistan civic guidance · MVP</span>
          </div>

          {/* Headline */}
          <div className="mb-6 max-w-3xl">
            <p className="mb-3 font-mono text-sm font-medium text-civic-muted">
              <span className="text-civic-green">$</span> ./salar-ai --mode=guidance
            </p>
            <h1 className="font-heading text-6xl font-bold leading-none tracking-tight text-civic-text sm:text-7xl lg:text-8xl">
              Civic<br />
              <span className="gradient-text">Guidance</span><br />
              <span className="text-civic-text/40">for Pakistan.</span>
            </h1>
          </div>

          <p className="mb-10 max-w-xl text-lg leading-7 text-civic-muted">
            AI-powered assistance to identify the right department, prepare complaint drafts,
            and know exactly what proof to collect.
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap gap-3">
            <Link
              href="/chat"
              className="focus-ring group inline-flex items-center gap-2.5 rounded-lg bg-civic-green px-6 py-3.5 font-mono text-sm font-bold uppercase tracking-wider text-white shadow-glow transition-all hover:brightness-110 hover:shadow-glow"
            >
              Start guidance
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
            </Link>
            <Link
              href="/dashboard"
              className="focus-ring inline-flex items-center gap-2 rounded-lg border border-civic-border px-6 py-3.5 font-mono text-sm font-bold uppercase tracking-wider text-civic-text transition hover:border-civic-text/30 hover:bg-civic-elevated"
            >
              Dashboard
            </Link>
          </div>

          {/* Domain tags */}
          <div className="mt-10 flex flex-wrap gap-2">
            {domains.map((d) => (
              <span key={d} className="flex items-center gap-1.5 rounded-full border border-civic-border bg-civic-surface px-3 py-1.5 font-mono text-[11px] text-civic-muted">
                <CheckCircle2 className="h-3.5 w-3.5 text-civic-green" aria-hidden="true" />
                {d}
              </span>
            ))}
          </div>
        </div>

        {/* Bottom terminal window decoration */}
        <div className="relative mx-auto mb-[-1px] max-w-3xl px-4 sm:px-6 lg:px-8">
          <div className="card overflow-hidden">
            <div className="flex items-center gap-2 border-b border-[#1a3348] bg-[#101e2c] px-4 py-3">
              <span className="h-3 w-3 rounded-full bg-red-500/70" />
              <span className="h-3 w-3 rounded-full bg-amber-400/70" />
              <span className="h-3 w-3 rounded-full bg-emerald-400/70" />
              <span className="ml-2 font-mono text-[11px] text-[#4d7080]">salar-ai — guidance session</span>
            </div>
            <div className="space-y-2 bg-[#070d14] p-5 font-mono text-sm">
              <p><span className="text-[#00e87e]">user@pk</span><span className="text-[#4d7080]">:~$</span> <span className="text-[#cde4f2]">Mera phone kho gaya hai</span></p>
              <p className="text-[#4d7080]">▸ Detecting domain... <span className="text-[#00e87e]">lost_or_stolen_vehicle_device</span></p>
              <p className="text-[#4d7080]">▸ Loading required fields... <span className="text-[#38b6ff]">11 fields</span></p>
              <p className="text-[#4d7080]">▸ Salar AI: <span className="text-[#cde4f2]">I can help. Please tell me the full incident, phone model, and location...</span></p>
              <p className="text-[#00e87e] cursor-blink"></p>
            </div>
          </div>
        </div>
      </section>

      {/* ── MVP Domains ────────────────────────────────────────── */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mb-12 grid gap-6 lg:grid-cols-[1fr_2fr]">
          <div>
            <p className="chip chip-green mb-3">
              <Zap className="h-3 w-3" />
              MVP domains
            </p>
            <h2 className="font-heading text-3xl font-bold text-civic-text">Three high-need civic flows</h2>
            <p className="mt-4 text-civic-muted leading-7">
              Modular architecture — category rules, RAG sources, maps lookup, and prompts are all decoupled so new Pakistani civic domains can be added without reshaping the app.
            </p>
          </div>
          <QuickIssueCards />
        </div>
      </section>

      {/* ── How it works ───────────────────────────────────────── */}
      <section className="border-y border-civic-border bg-civic-surface/40">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
          <div className="mb-12 flex items-center gap-4">
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-civic-border bg-civic-elevated">
              <Terminal className="h-5 w-5 text-civic-blue" aria-hidden="true" />
            </span>
            <div>
              <p className="chip chip-muted mb-1">Process</p>
              <h2 className="font-heading text-3xl font-bold text-civic-text">From issue to usable draft</h2>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((step) => (
              <div key={step.num} className="card card-hover relative overflow-hidden p-6">
                <div className="mb-4 font-mono text-4xl font-bold text-civic-green/15 select-none">{step.num}</div>
                <div className="absolute right-4 top-4 font-mono text-[10px] text-civic-muted">{step.num}</div>
                <h3 className="mb-2 font-heading text-base font-bold text-civic-text">{step.title}</h3>
                <p className="text-sm leading-6 text-civic-muted">{step.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ────────────────────────────────────────────────── */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="card card-hover relative overflow-hidden p-8">
          <div className="pointer-events-none absolute right-0 top-0 h-64 w-64 rounded-full bg-civic-blue/5 blur-2xl" />
          <div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="chip chip-muted mb-3">
                <FileText className="h-3 w-3" />
                Demo prompt
              </p>
              <p className="font-mono text-2xl font-bold text-civic-text">
                <span className="text-civic-green">&gt;</span>{" "}
                <span className="text-civic-text">&quot;Mera phone kho gaya hai&quot;</span>
              </p>
              <p className="mt-2 font-mono text-sm text-civic-muted">Try this in the chat — Salar AI will guide you through the complaint process.</p>
            </div>
            <Link
              href="/chat"
              className="focus-ring inline-flex shrink-0 items-center justify-center gap-2 rounded-lg bg-civic-blue px-6 py-3.5 font-mono text-sm font-bold uppercase tracking-wider text-white shadow-glow-blue transition hover:brightness-110"
            >
              <MessageSquareText className="h-4 w-4" aria-hidden="true" />
              Open chat
            </Link>
          </div>
        </div>
      </section>

    </main>
  );
}
