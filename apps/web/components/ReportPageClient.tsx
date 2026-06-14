"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { ReportPreview } from "@/components/ReportPreview";
import { fetchReport } from "@/lib/api";
import { isReportResponse } from "@/lib/reports";
import { getReportFromBrowser } from "@/lib/storage";
import { supabase } from "@/lib/supabase";
import type { ReportResponse } from "@/lib/types";

export function ReportPageClient({ reportId }: { reportId: string }) {
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    Promise.resolve().then(() => {
      if (!mounted) return;
      const cached = getReportFromBrowser(reportId);
      if (cached) { setReport(cached); return; }
      Promise.resolve()
        .then(async () => {
          if (supabase) {
            const { data } = await supabase
              .from("user_complaints")
              .select("generated_report")
              .eq("id", reportId)
              .maybeSingle();
            if (isReportResponse(data?.generated_report)) return data.generated_report;
          }
          return fetchReport(reportId);
        })
        .then((loaded) => { if (mounted) setReport(loaded); })
        .catch((err) => { if (mounted) setError(err instanceof Error ? err.message : "Report not found."); });
    });
    return () => { mounted = false; };
  }, [reportId]);

  if (error) {
    return (
      <div className="card border-red-500/25 p-6">
        <p className="font-heading text-xl font-bold text-civic-text">Report unavailable</p>
        <p className="mt-2 text-sm text-civic-muted">{error}</p>
        <Link
          className="focus-ring mt-5 inline-flex items-center gap-2 rounded-lg bg-civic-blue px-4 py-2.5 font-mono text-xs font-bold uppercase tracking-wider text-white transition hover:brightness-110"
          href="/chat"
        >
          Return to chat
        </Link>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="card p-6">
        <div className="flex items-center gap-3">
          <div className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="block h-1.5 w-1.5 rounded-full bg-civic-green"
                style={{ animation: `pulse3 1.4s ease-in-out ${i * 0.18}s infinite` }}
              />
            ))}
          </div>
          <span className="font-mono text-xs uppercase tracking-widest text-civic-muted">Loading report…</span>
        </div>
      </div>
    );
  }

  return <ReportPreview report={report} />;
}
