import { ExternalLink, ShieldCheck } from "lucide-react";

import type { SourceNote } from "@/lib/types";

export function VerifiedSourcesCard({ sources }: { sources: SourceNote[] }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-4 flex items-center gap-2">
        <ShieldCheck className="h-5 w-5 text-civic-green" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">Verified Guidance Sources</h2>
      </div>
      {sources.length ? (
        <div className="space-y-3">
          {sources.map((source) => (
            <div key={`${source.source_name}-${source.title}`} className="rounded-md border border-civic-line bg-slate-50 p-3">
              <div className="font-heading text-sm font-bold text-civic-ink">{source.source_name}</div>
              <div className="mt-1 font-mono text-[11px] text-civic-muted">
                {source.authority_type || "official source"} · {source.jurisdiction} · verified {source.verified_at || "not dated"}
              </div>
              {source.source_url ? (
                <a className="mt-2 inline-flex items-center gap-1 text-sm font-semibold text-civic-blue hover:underline" href={source.source_url} target="_blank" rel="noreferrer">
                  Source link
                  <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
                </a>
              ) : null}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm leading-6 text-civic-muted">
          I could not verify this from an official Pakistani source in the current knowledge base. Please confirm with the relevant department.
        </p>
      )}
      <p className="mt-4 rounded-md bg-civic-warning p-3 text-sm leading-6 text-civic-ink">
        Procedures and department requirements can change. Always verify final requirements with the relevant Pakistani authority before submission.
      </p>
    </section>
  );
}
