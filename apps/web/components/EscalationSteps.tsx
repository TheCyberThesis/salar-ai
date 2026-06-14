import { ArrowUpRight } from "lucide-react";

export function EscalationSteps({ steps }: { steps: string[] }) {
  return (
    <section className="card p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-blue/10 ring-1 ring-civic-blue/20">
          <ArrowUpRight className="h-4 w-4 text-civic-blue" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">If No Action Is Taken</h2>
      </div>
      <ol className="space-y-3 text-sm leading-6 text-civic-muted">
        {steps.map((step, index) => (
          <li key={step} className="flex gap-3">
            <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md bg-civic-green/10 font-mono text-[11px] font-bold text-civic-green ring-1 ring-civic-green/20">
              {index + 1}
            </span>
            {step}
          </li>
        ))}
      </ol>
    </section>
  );
}
