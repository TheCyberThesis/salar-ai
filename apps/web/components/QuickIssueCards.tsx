"use client";

import Link from "next/link";
import { Car, Lightbulb, ShieldAlert, Smartphone } from "lucide-react";

const issues = [
  {
    title: "Lost/Stolen Phone",
    body: "Police report, IMEI/SIM reminders, PTA and telecom verification notes.",
    prompt: "Mera phone kho gaya hai",
    icon: Smartphone
  },
  {
    title: "Lost/Stolen Bike or Car",
    body: "Vehicle details, registration documents, police report proof reminders.",
    prompt: "Meri bike chori ho gayi hai",
    icon: Car
  },
  {
    title: "Utility Bill Overcharging",
    body: "Bill reference, meter proof, provider complaint and regulator escalation notes.",
    prompt: "Mera bijli ka bill bohat zyada aa gaya hai",
    icon: Lightbulb
  },
  {
    title: "Workplace Harassment",
    body: "Safety-first guidance, complaint draft, confidentiality and FOSPAH source notes.",
    prompt: "Mujhe office mein harassment face karni par rahi hai",
    icon: ShieldAlert
  }
];

export function QuickIssueCards({ onSelect }: { onSelect?: (prompt: string) => void }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {issues.map((issue) => {
        const Icon = issue.icon;
        const content = (
          <>
            <div className="mb-3 flex items-center gap-3">
              <span className="grid h-9 w-9 place-items-center rounded-md bg-civic-mint text-civic-green">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
              <h3 className="font-heading text-base font-bold text-civic-ink">{issue.title}</h3>
            </div>
            <p className="text-sm leading-6 text-civic-muted">{issue.body}</p>
          </>
        );
        const className =
          "focus-ring min-h-32 rounded-lg border border-civic-line bg-white p-4 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-civic-green hover:shadow-soft";
        return onSelect ? (
          <button key={issue.title} type="button" onClick={() => onSelect(issue.prompt)} className={className}>
            {content}
          </button>
        ) : (
          <Link key={issue.title} href="/chat" className={className}>
            {content}
          </Link>
        );
      })}
    </div>
  );
}
