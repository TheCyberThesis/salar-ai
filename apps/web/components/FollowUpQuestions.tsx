import { CircleHelp } from "lucide-react";

export function FollowUpQuestions({ questions }: { questions: string[] }) {
  if (!questions.length) return null;
  return (
    <div className="rounded-xl border border-civic-green/15 bg-civic-green-glow p-4">
      <div className="mb-3 flex items-center gap-2">
        <CircleHelp className="h-4 w-4 text-civic-green" aria-hidden="true" />
        <span className="font-mono text-[11px] uppercase tracking-widest text-civic-green">
          Follow-up details
        </span>
      </div>
      <ul className="space-y-2">
        {questions.map((q) => (
          <li key={q} className="flex gap-2 text-sm leading-5 text-civic-muted">
            <span className="mt-0.5 shrink-0 font-mono text-[10px] text-civic-green/50">▸</span>
            {q}
          </li>
        ))}
      </ul>
    </div>
  );
}
