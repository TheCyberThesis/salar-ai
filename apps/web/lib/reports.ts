import type { ReportResponse } from "@/lib/types";

export function isReportResponse(value: unknown): value is ReportResponse {
  if (!value || typeof value !== "object") return false;
  const report = value as Partial<ReportResponse>;
  return typeof report.report_id === "string" && typeof report.session_id === "string" && typeof report.summary === "string";
}

export function mergeReports(primary: ReportResponse[], secondary: ReportResponse[]): ReportResponse[] {
  const seen = new Set<string>();
  return [...primary, ...secondary].filter((report) => {
    if (seen.has(report.report_id)) return false;
    seen.add(report.report_id);
    return true;
  });
}
