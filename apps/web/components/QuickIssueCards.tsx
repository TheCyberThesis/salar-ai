"use client";

import Link from "next/link";
import { Car, Lightbulb, ShieldAlert, Smartphone } from "lucide-react";

const issues = [
  {
    title: "Lost / Stolen Phone",
    body: "Police report, IMEI/SIM reminders, PTA and telecom verification.",
    prompt: "Mera phone kho gaya hai",
    icon: Smartphone,
    tag: "phone",
  },
  {
    title: "Lost / Stolen Bike or Car",
    body: "Vehicle details, registration docs, police report proof reminders.",
    prompt: "Meri bike chori ho gayi hai",
    icon: Car,
    tag: "vehicle",
  },
  {
    title: "Utility Bill Overcharging",
    body: "Bill reference, meter proof, provider complaint and regulator notes.",
    prompt: "Mera bijli ka bill bohat zyada aa gaya hai",
    icon: Lightbulb,
    tag: "utility",
  },
  {
    title: "Workplace Harassment",
    body: "Safety-first guidance, complaint draft, confidentiality and FOSPAH notes.",
    prompt: "Mujhe office mein harassment face karni par rahi hai",
    icon: ShieldAlert,
    tag: "legal",
  },
];

const accentMap: Record<string, string> = {
  phone: "border-civic-green/20 hover:border-civic-green/40 group-hover:text-civic-green",
  vehicle: "border-civic-blue/20 hover:border-civic-blue/40 group-hover:text-civic-blue",
  utility: "border-civic-amber/20 hover:border-civic-amber/40 group-hover:text-civic-amber",
  legal: "border-red-500/20 hover:border-red-500/40 group-hover:text-red-400",
};

const iconBgMap: Record<string, string> = {
  phone:   "bg-civic-green/10 text-civic-green",
  vehicle: "bg-civic-blue/10 text-civic-blue",
  utility: "bg-civic-amber/10 text-civic-amber",
  legal:   "bg-red-500/10 text-red-400",
};

export function QuickIssueCards({ onSelect }: { onSelect?: (prompt: string) => void }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {issues.map((issue) => {
        const Icon = issue.icon;
        const accent = accentMap[issue.tag] ?? accentMap["phone"];
        const iconBg = iconBgMap[issue.tag] ?? iconBgMap["phone"];

        const inner = (
          <>
            <div className={`mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg ${iconBg}`}>
              <Icon className="h-5 w-5" aria-hidden="true" />
            </div>
            <h3 className="mb-1.5 font-heading text-sm font-bold text-civic-text">{issue.title}</h3>
            <p className="text-xs leading-5 text-civic-muted">{issue.body}</p>
            <div className="mt-3 font-mono text-[10px] uppercase tracking-widest text-civic-muted/50">
              #{issue.tag}
            </div>
          </>
        );

        const cls = `group focus-ring block rounded-xl border bg-civic-surface p-4 text-left card-hover transition-all ${accent}`;

        return onSelect ? (
          <button key={issue.title} type="button" onClick={() => onSelect(issue.prompt)} className={cls}>
            {inner}
          </button>
        ) : (
          <Link key={issue.title} href="/chat" className={cls}>
            {inner}
          </Link>
        );
      })}
    </div>
  );
}
