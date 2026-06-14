import type { ReportResponse } from "@/lib/types";

const REPORTS_KEY = "salar-ai-reports";

export function saveReportToBrowser(report: ReportResponse): void {
  if (typeof window === "undefined") return;
  const current = getReportsFromBrowser();
  const deduped = current.filter((item) => item.report_id !== report.report_id);
  window.localStorage.setItem(REPORTS_KEY, JSON.stringify([report, ...deduped].slice(0, 20)));
}

export function getReportsFromBrowser(): ReportResponse[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(window.localStorage.getItem(REPORTS_KEY) || "[]") as ReportResponse[];
  } catch {
    return [];
  }
}

export function getReportFromBrowser(reportId: string): ReportResponse | null {
  return getReportsFromBrowser().find((report) => report.report_id === reportId) ?? null;
}
