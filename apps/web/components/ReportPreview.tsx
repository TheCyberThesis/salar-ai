import Link from "next/link";

import { CopyButton } from "@/components/CopyButton";
import { DepartmentCard } from "@/components/DepartmentCard";
import { EscalationSteps } from "@/components/EscalationSteps";
import { MapsCard } from "@/components/MapsCard";
import { RequiredDocumentsList } from "@/components/RequiredDocumentsList";
import { TimelineCard } from "@/components/TimelineCard";
import { VerifiedSourcesCard } from "@/components/VerifiedSourcesCard";
import type { ReportResponse } from "@/lib/types";

function reportAsText(report: ReportResponse) {
  return `Salaar AI Civic Guidance Report

1. Issue Summary
${report.summary}

2. Identified Category
${report.category} / ${report.subcategory || "not specified"}

3. Relevant Department/Institution
${report.department}

4. Information Provided by User
${JSON.stringify(report.user_provided_details, null, 2)}

5. Missing Information Still Needed
${report.missing_information.join(", ") || "None listed"}

6. Required Documents
${report.required_documents.map((item) => `- ${item}`).join("\n")}

7. Step-by-Step Procedure
${report.step_by_step_procedure.map((item, index) => `${index + 1}. ${item}`).join("\n")}

8. Complaint/Application Draft
${report.complaint_draft}

9. Where to Submit
${report.where_to_submit}

10. Google Maps Location/Search Link
${report.maps_link}

11. What Proof to Collect
${report.proof_to_collect.map((item) => `- ${item}`).join("\n")}

12. Expected Timeline
${report.timeline}

13. What To Do If No Action Is Taken
${report.escalation_steps.map((item) => `- ${item}`).join("\n")}

14. Important Safety/Privacy Notes
${report.safety_privacy_notes.map((item) => `- ${item}`).join("\n")}

15. Sources Used / Verification Notes
${report.sources_used.map((source) => `- ${source.source_name}: ${source.source_url || "no link"}`).join("\n")}

16. Disclaimer
${report.disclaimer}`;
}

export function ReportPreview({ report, compact = false }: { report: ReportResponse; compact?: boolean }) {
  const text = reportAsText(report);
  return (
    <article className="space-y-4">
      <div className="rounded-lg border border-civic-line bg-white p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-normal text-civic-muted">Salaar AI Civic Guidance Report</p>
            <h1 className="mt-2 font-heading text-2xl font-bold text-civic-ink">{report.subcategory?.replaceAll("_", " ") || report.category}</h1>
            <p className="mt-2 text-sm leading-6 text-civic-muted">{report.summary}</p>
          </div>
          <div className="flex gap-2">
            <CopyButton text={text} label="Copy report" />
            {!compact ? null : (
              <Link className="focus-ring rounded-md bg-civic-blue px-3 py-2 text-sm font-semibold text-white hover:bg-blue-800" href={`/report/${report.report_id}`}>
                Open
              </Link>
            )}
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <DepartmentCard department={report.department} whereToSubmit={report.where_to_submit} />
        <MapsCard mapsLink={report.maps_link} />
        <RequiredDocumentsList documents={report.required_documents} />
        <TimelineCard timeline={report.timeline} />
      </div>

      <section className="rounded-lg border border-civic-line bg-white p-5">
        <h2 className="mb-4 font-heading text-lg font-bold text-civic-ink">Step-by-Step Procedure</h2>
        <ol className="space-y-3 text-sm leading-6 text-civic-muted">
          {report.step_by_step_procedure.map((step, index) => (
            <li key={step} className="flex gap-3">
              <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md bg-civic-mint font-mono text-[11px] font-bold text-civic-green">{index + 1}</span>
              {step}
            </li>
          ))}
        </ol>
      </section>

      <section className="rounded-lg border border-civic-line bg-white p-5">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="font-heading text-lg font-bold text-civic-ink">Complaint/Application Draft</h2>
          <CopyButton text={report.complaint_draft} label="Copy draft" />
        </div>
        <pre className="max-h-[32rem] overflow-auto whitespace-pre-wrap rounded-md bg-slate-950 p-4 font-mono text-xs leading-6 text-slate-100">
          {report.complaint_draft}
        </pre>
      </section>

      <section className="rounded-lg border border-civic-line bg-white p-5">
        <h2 className="mb-4 font-heading text-lg font-bold text-civic-ink">What Proof to Collect</h2>
        <ul className="grid gap-2 text-sm leading-6 text-civic-muted sm:grid-cols-2">
          {report.proof_to_collect.map((item) => (
            <li key={item} className="rounded-md bg-civic-mint px-3 py-2 font-semibold text-civic-ink">
              {item}
            </li>
          ))}
        </ul>
      </section>

      <EscalationSteps steps={report.escalation_steps} />
      <VerifiedSourcesCard sources={report.sources_used} />

      <section className="rounded-lg border border-amber-200 bg-civic-warning p-5 text-sm leading-6 text-civic-ink">
        <h2 className="mb-2 font-heading text-lg font-bold">Disclaimer</h2>
        <p>{report.disclaimer}</p>
      </section>
    </article>
  );
}
