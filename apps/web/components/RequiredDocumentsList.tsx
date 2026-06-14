import { FileText } from "lucide-react";

export function RequiredDocumentsList({ documents }: { documents: string[] }) {
  return (
    <section className="card p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-blue/10 ring-1 ring-civic-blue/20">
          <FileText className="h-4 w-4 text-civic-blue" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">Required Documents</h2>
      </div>
      <ul className="space-y-2 text-sm leading-6 text-civic-muted">
        {documents.map((doc) => (
          <li key={doc} className="flex items-start gap-2.5">
            <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-civic-blue/60" />
            {doc}
          </li>
        ))}
      </ul>
    </section>
  );
}
