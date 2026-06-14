import Link from "next/link";
import { CheckSquare2, FileText } from "lucide-react";

import { CopyButton } from "@/components/CopyButton";
import { DepartmentCard } from "@/components/DepartmentCard";
import { EscalationSteps } from "@/components/EscalationSteps";
import { MapsCard } from "@/components/MapsCard";
import { RequiredDocumentsList } from "@/components/RequiredDocumentsList";
import { TimelineCard } from "@/components/TimelineCard";
import { VerifiedSourcesCard } from "@/components/VerifiedSourcesCard";
import type { ReportResponse } from "@/lib/types";

function reportAsText(report: ReportResponse) {
  const loc = report.department_location;
  const issueType = report.issue_type || report.subcategory?.replaceAll("_", " ") || report.category;
  const recipient = report.report_recipient || "Relevant Officer";
  const office = report.reporting_office || report.where_to_submit || report.department;
  const coords =
    typeof loc?.latitude === "number" && typeof loc.longitude === "number"
      ? `${loc.latitude}, ${loc.longitude}`
      : "Not available";
  return `Salar AI Civic Guidance Report

1. Issue Summary
${report.summary}

2. Category / Subcategory
${report.category} / ${report.subcategory || "not specified"}

3. Issue Type
${issueType}

4. Department
${report.department}

5. Reporting Office / Recipient
Office: ${office}
Recipient: ${recipient}

6. User-Provided Details
${JSON.stringify(report.user_provided_details, null, 2)}

7. Missing Information
${report.missing_information.join(", ") || "None listed"}

8. Required Documents
${report.required_documents.map((d) => `- ${d}`).join("\n")}

9. Step-by-Step Procedure
${report.step_by_step_procedure.map((s, i) => `${i + 1}. ${s}`).join("\n")}

10. Complaint / Application Draft
${report.complaint_draft}

11. Where to Submit
${report.where_to_submit}

12. Location
${loc?.place_name ? `Place: ${loc.place_name}\n` : ""}${loc?.address ? `Address: ${loc.address}\n` : ""}${loc?.phone_number ? `Phone: ${loc.phone_number}\n` : ""}Coordinates: ${coords}
Maps: ${loc?.maps_link || report.maps_link}

13. Proof to Collect
${report.proof_to_collect.map((p) => `- ${p}`).join("\n")}

14. Expected Timeline
${report.timeline}

15. If No Action Is Taken
${report.escalation_steps.map((s) => `- ${s}`).join("\n")}

16. Safety / Privacy Notes
${report.safety_privacy_notes.map((n) => `- ${n}`).join("\n")}

17. Sources Used
${report.sources_used.map((s) => `- ${s.source_name}: ${s.source_url || "no link"}`).join("\n")}

18. Disclaimer
${report.disclaimer}`;
}

export function ReportPreview({ report, compact = false }: { report: ReportResponse; compact?: boolean }) {
  const text = reportAsText(report);
  const issueType = report.issue_type || report.subcategory?.replaceAll("_", " ") || report.category;
  const recipient = report.report_recipient || "Relevant Officer";
  const office = report.reporting_office || report.where_to_submit || report.department;

  return (
    <article className="space-y-4">

      {/* ── Header card ─────────────────────────────────────── */}
      <div className="card p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="flex-1">
            <div className="mb-2 flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-md bg-civic-green/10 ring-1 ring-civic-green/20">
                <FileText className="h-3.5 w-3.5 text-civic-green" aria-hidden="true" />
              </span>
              <span className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">
                Salar AI · Civic Guidance Report
              </span>
            </div>
            <h1 className="font-heading text-2xl font-bold text-civic-text">
              {report.subcategory?.replaceAll("_", " ") || report.category}
            </h1>
            <p className="mt-2 text-sm leading-6 text-civic-muted">{report.summary}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="chip chip-green">{issueType}</span>
              <span className="chip chip-blue">To: {recipient}</span>
              <span className="chip chip-muted">{office}</span>
            </div>
          </div>
          <div className="flex gap-2">
            <CopyButton text={text} label="Copy report" />
            {compact && (
              <Link
                className="focus-ring inline-flex items-center gap-1.5 rounded-lg bg-civic-blue px-3 py-2 font-mono text-xs font-bold uppercase tracking-wider text-white transition hover:brightness-110"
                href={`/report/${report.report_id}`}
              >
                Full report
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* ── Info grid ───────────────────────────────────────── */}
      <div className="grid gap-4 lg:grid-cols-2">
        <DepartmentCard
          department={report.department}
          whereToSubmit={report.where_to_submit}
          recipient={recipient}
          reportingOffice={office}
        />
        <MapsCard mapsLink={report.maps_link} location={report.department_location} />
        <RequiredDocumentsList documents={report.required_documents} />
        <TimelineCard timeline={report.timeline} />
      </div>

      {/* ── Procedure ───────────────────────────────────────── */}
      <section className="card p-5">
        <h2 className="mb-4 font-heading text-base font-bold text-civic-text">Step-by-Step Procedure</h2>
        <ol className="space-y-3 text-sm leading-6 text-civic-muted">
          {report.step_by_step_procedure.map((step, i) => (
            <li key={step} className="flex gap-3">
              <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md bg-civic-green/10 font-mono text-[11px] font-bold text-civic-green ring-1 ring-civic-green/20">
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
      </section>

      {/* ── Complaint draft ─────────────────────────────────── */}
      <section className="card p-5">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="font-heading text-base font-bold text-civic-text">Complaint / Application Draft</h2>
          <CopyButton text={report.complaint_draft} label="Copy draft" />
        </div>
        {/* Terminal-style code block */}
        <div className="overflow-hidden rounded-lg border border-civic-border">
          <div className="flex items-center gap-2 border-b border-civic-border bg-civic-elevated px-4 py-2.5">
            <span className="h-2.5 w-2.5 rounded-full bg-red-500/50" />
            <span className="h-2.5 w-2.5 rounded-full bg-civic-amber/50" />
            <span className="h-2.5 w-2.5 rounded-full bg-civic-green/50" />
            <span className="ml-2 font-mono text-[10px] text-civic-muted">complaint-draft.txt</span>
          </div>
          <pre className="max-h-[32rem] overflow-auto bg-civic-bg p-4 font-mono text-xs leading-6 text-civic-text/80">
            {report.complaint_draft}
          </pre>
        </div>
      </section>

      {/* ── Proof to collect ───────────────────────────────── */}
      <section className="card p-5">
        <div className="mb-4 flex items-center gap-2">
          <CheckSquare2 className="h-4 w-4 text-civic-green" aria-hidden="true" />
          <h2 className="font-heading text-base font-bold text-civic-text">Proof to Collect</h2>
        </div>
        <ul className="grid gap-2 text-sm sm:grid-cols-2">
          {report.proof_to_collect.map((item) => (
            <li
              key={item}
              className="flex items-center gap-2 rounded-lg border border-civic-green/15 bg-civic-green-glow px-3 py-2.5 font-semibold text-civic-text"
            >
              <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-civic-green" />
              {item}
            </li>
          ))}
        </ul>
      </section>

      <EscalationSteps steps={report.escalation_steps} />
      <VerifiedSourcesCard sources={report.sources_used} />

      {/* ── Disclaimer ─────────────────────────────────────── */}
      <section className="card border-civic-amber/20 p-5">
        <div className="mb-2 font-mono text-[10px] uppercase tracking-widest text-civic-amber/70">Disclaimer</div>
        <p className="text-sm leading-6 text-civic-muted">{report.disclaimer}</p>
      </section>
    </article>
  );
}
