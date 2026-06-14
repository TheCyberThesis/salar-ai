import { Clock3 } from "lucide-react";

export function TimelineCard({ timeline }: { timeline: string }) {
  return (
    <section className="card p-5">
      <div className="mb-3 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-green/10 ring-1 ring-civic-green/20">
          <Clock3 className="h-4 w-4 text-civic-green" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">Expected Timeline</h2>
      </div>
      <p className="text-sm leading-6 text-civic-muted">{timeline}</p>
    </section>
  );
}
