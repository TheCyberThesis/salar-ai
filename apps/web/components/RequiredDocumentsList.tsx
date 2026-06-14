import { FileText } from "lucide-react";

export function RequiredDocumentsList({ documents }: { documents: string[] }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-4 flex items-center gap-2">
        <FileText className="h-5 w-5 text-civic-blue" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">Required Documents</h2>
      </div>
      <ul className="space-y-2 text-sm leading-6 text-civic-muted">
        {documents.map((document) => (
          <li key={document} className="flex gap-2">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-civic-green" />
            {document}
          </li>
        ))}
      </ul>
    </section>
  );
}
