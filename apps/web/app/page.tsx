import Image from "next/image";
import Link from "next/link";
import { ArrowRight, CheckCircle2, FileQuestion, Landmark, MessageSquareText } from "lucide-react";

import { DisclaimerBanner } from "@/components/DisclaimerBanner";
import { QuickIssueCards } from "@/components/QuickIssueCards";

const steps = [
  "Tell us your issue",
  "Salaar AI asks missing details",
  "Get department guidance and complaint draft",
  "Submit complaint and collect proof/token/report number"
];

export default function HomePage() {
  return (
    <main>
      <section className="relative min-h-[calc(100vh-7rem)] overflow-hidden bg-civic-ink text-white">
        <Image
          src="/civic-guidance-hero.png"
          alt="Civic service desk and mobile guidance interface"
          fill
          priority
          className="object-cover object-center opacity-70"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-civic-ink via-civic-ink/72 to-civic-ink/15" />
        <div className="relative mx-auto flex min-h-[calc(100vh-7rem)] max-w-7xl flex-col justify-center px-4 pb-24 pt-14 sm:px-6 lg:px-8">
          <div className="max-w-2xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-2 font-mono text-xs uppercase tracking-normal text-white/90 backdrop-blur">
              <Landmark className="h-4 w-4" aria-hidden="true" />
              Pakistan civic guidance MVP
            </div>
            <h1 className="font-heading text-5xl font-bold tracking-normal sm:text-6xl lg:text-7xl">Salaar AI</h1>
            <p className="mt-5 max-w-xl text-xl leading-8 text-white/90">AI-powered civic guidance for Pakistani citizens.</p>
            <p className="mt-4 max-w-xl text-base leading-7 text-white/78">
              Get help identifying the relevant department, required information, documents, proof to collect, escalation path, and a complaint/application draft.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link className="focus-ring inline-flex items-center gap-2 rounded-md bg-white px-5 py-3 font-bold text-civic-ink shadow-soft hover:bg-civic-mint" href="/chat">
                Start guidance
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Link>
              <Link className="focus-ring inline-flex items-center gap-2 rounded-md border border-white/30 px-5 py-3 font-bold text-white hover:bg-white/10" href="/dashboard">
                Dashboard
              </Link>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 bg-white/94 px-4 py-5 text-civic-ink backdrop-blur">
          <div className="mx-auto grid max-w-7xl gap-3 sm:grid-cols-3">
            {["Lost/stolen phone, bike, or car", "Utility bill overcharging", "Workplace harassment against women"].map((item) => (
              <div key={item} className="flex items-center gap-2 font-mono text-xs">
                <CheckCircle2 className="h-4 w-4 text-civic-green" aria-hidden="true" />
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <DisclaimerBanner />
      </section>

      <section className="mx-auto grid max-w-7xl gap-8 px-4 pb-14 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:px-8">
        <div>
          <p className="font-mono text-xs uppercase tracking-normal text-civic-green">MVP domains</p>
          <h2 className="mt-2 font-heading text-3xl font-bold text-civic-ink">Focused on three high-need civic flows</h2>
          <p className="mt-4 text-base leading-7 text-civic-muted">
            The architecture keeps category rules, required fields, RAG sources, maps lookup, and prompts modular so future Pakistani civic domains can be added without reshaping the app.
          </p>
        </div>
        <QuickIssueCards />
      </section>

      <section className="border-y border-civic-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-center gap-3">
            <span className="grid h-11 w-11 place-items-center rounded-lg bg-civic-sky text-civic-blue">
              <FileQuestion className="h-5 w-5" aria-hidden="true" />
            </span>
            <div>
              <p className="font-mono text-xs uppercase tracking-normal text-civic-muted">How it works</p>
              <h2 className="font-heading text-3xl font-bold text-civic-ink">From issue to usable complaint draft</h2>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-4">
            {steps.map((step, index) => (
              <div key={step} className="rounded-lg border border-civic-line bg-slate-50 p-5">
                <div className="mb-5 grid h-9 w-9 place-items-center rounded-md bg-civic-green font-mono text-sm font-bold text-white">{index + 1}</div>
                <h3 className="font-heading text-lg font-bold text-civic-ink">{step}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-lg border border-civic-line bg-civic-ink p-6 text-white">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-mono text-xs uppercase tracking-normal text-white/70">Demo prompt</p>
              <p className="mt-2 font-heading text-2xl font-bold">“Mera phone kho gaya hai”</p>
            </div>
            <Link className="focus-ring inline-flex items-center justify-center gap-2 rounded-md bg-white px-5 py-3 font-bold text-civic-ink hover:bg-civic-mint" href="/chat">
              Open chat
              <MessageSquareText className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
