import { CircleHelp } from "lucide-react";

export function FollowUpQuestions({ questions }: { questions: string[] }) {
  if (!questions.length) return null;
  return (
    <div className="rounded-lg border border-civic-line bg-civic-mint p-4">
      <div className="mb-3 flex items-center gap-2 font-heading font-bold text-civic-ink">
        <CircleHelp className="h-5 w-5 text-civic-green" aria-hidden="true" />
        Follow-up details
      </div>
      <ul className="space-y-2 text-sm leading-6 text-civic-muted">
        {questions.map((question) => (
          <li key={question}>{question}</li>
        ))}
      </ul>
    </div>
  );
}
