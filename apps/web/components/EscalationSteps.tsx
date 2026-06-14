import { ArrowUpRight } from "lucide-react";

export function EscalationSteps({ steps }: { steps: string[] }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-4 flex items-center gap-2">
        <ArrowUpRight className="h-5 w-5 text-civic-blue" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">If No Action Is Taken</h2>
      </div>
      <ol className="space-y-3 text-sm leading-6 text-civic-muted">
        {steps.map((step, index) => (
          <li key={step} className="flex gap-3">
            <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md bg-civic-mint font-mono text-[11px] font-bold text-civic-green">
              {index + 1}
            </span>
            {step}
          </li>
        ))}
      </ol>
    </section>
  );
}
