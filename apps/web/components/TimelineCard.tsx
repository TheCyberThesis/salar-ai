import { Clock3 } from "lucide-react";

export function TimelineCard({ timeline }: { timeline: string }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-3 flex items-center gap-2">
        <Clock3 className="h-5 w-5 text-civic-green" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">Expected Timeline</h2>
      </div>
      <p className="text-sm leading-6 text-civic-muted">{timeline}</p>
    </section>
  );
}
