import { ExternalLink, ShieldCheck } from "lucide-react";

import type { SourceNote } from "@/lib/types";

export function VerifiedSourcesCard({ sources }: { sources: SourceNote[] }) {
  return (
    <section className="card p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-green/10 ring-1 ring-civic-green/20">
          <ShieldCheck className="h-4 w-4 text-civic-green" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">Verified Sources</h2>
      </div>

      {sources.length ? (
        <div className="space-y-3">
          {sources.map((source) => (
            <div
              key={`${source.source_name}-${source.title}`}
              className="rounded-lg border border-civic-border bg-civic-elevated p-3"
            >
              <div className="font-heading text-sm font-semibold text-civic-text">{source.source_name}</div>
              <div className="mt-1 font-mono text-[10px] uppercase tracking-wide text-civic-muted">
                {source.authority_type || "official"} · {source.jurisdiction} · {source.verified_at || "not dated"}
              </div>
              {source.source_url ? (
                <a
                  className="mt-2 inline-flex items-center gap-1 font-mono text-[11px] text-civic-blue hover:underline"
                  href={source.source_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Source link
                  <ExternalLink className="h-3 w-3" aria-hidden="true" />
                </a>
              ) : null}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm leading-6 text-civic-muted">
          No official Pakistani source verified in the current knowledge base. Confirm with the relevant department.
        </p>
      )}

      <div className="mt-4 rounded-lg border border-civic-amber/20 bg-civic-amber-glow p-3">
        <p className="font-mono text-[11px] leading-5 text-civic-amber/90">
          ⚠ Procedures may change. Verify requirements with the relevant Pakistani authority before submitting.
        </p>
      </div>
    </section>
  );
}
