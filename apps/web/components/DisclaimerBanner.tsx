import { AlertTriangle } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <section className="rounded-lg border border-amber-200 bg-civic-warning p-4 text-sm leading-6 text-civic-ink">
      <div className="flex gap-3">
        <AlertTriangle className="mt-1 h-5 w-5 shrink-0 text-amber-700" aria-hidden="true" />
        <p>
          <strong>Disclaimer:</strong> Salaar AI provides AI-powered public guidance for civic and social issues. It is not a substitute for
          professional legal advice. For serious legal matters, please consult a qualified lawyer or relevant authority.
        </p>
      </div>
    </section>
  );
}
