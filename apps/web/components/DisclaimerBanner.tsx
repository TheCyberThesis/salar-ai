import { AlertTriangle } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <section className="rounded-xl border border-civic-amber/20 bg-civic-amber-glow p-4">
      <div className="flex gap-3">
        <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-civic-amber" aria-hidden="true" />
        <p className="text-sm leading-6 text-civic-muted">
          <span className="font-semibold text-civic-amber">Disclaimer: </span>
          Salar AI provides AI-powered public guidance for civic and social issues. It is not a substitute
          for professional legal advice. For serious legal matters, please consult a qualified lawyer or
          relevant authority.
        </p>
      </div>
    </section>
  );
}
