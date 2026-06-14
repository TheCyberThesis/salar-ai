"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { ReportPreview } from "@/components/ReportPreview";
import { fetchReport } from "@/lib/api";
import { getReportFromBrowser } from "@/lib/storage";
import type { ReportResponse } from "@/lib/types";

export function ReportPageClient({ reportId }: { reportId: string }) {
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    Promise.resolve().then(() => {
      if (!mounted) return;
      const cached = getReportFromBrowser(reportId);
      if (cached) {
        setReport(cached);
        return;
      }
      fetchReport(reportId)
        .then((loaded) => {
          if (mounted) setReport(loaded);
        })
        .catch((err) => {
          if (mounted) setError(err instanceof Error ? err.message : "Report not found.");
        });
    });
    return () => {
      mounted = false;
    };
  }, [reportId]);

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
        <p className="font-heading text-xl font-bold">Report unavailable</p>
        <p className="mt-2 text-sm">{error}</p>
        <Link className="mt-4 inline-flex rounded-md bg-civic-blue px-4 py-2 text-sm font-semibold text-white" href="/chat">
          Return to chat
        </Link>
      </div>
    );
  }

  if (!report) {
    return <div className="rounded-lg border border-civic-line bg-white p-6 font-mono text-sm text-civic-muted">Loading report...</div>;
  }

  return <ReportPreview report={report} />;
}
