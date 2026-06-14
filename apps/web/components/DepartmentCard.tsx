import { Building2 } from "lucide-react";

export function DepartmentCard({
  department,
  whereToSubmit,
  recipient,
  reportingOffice,
}: {
  department: string;
  whereToSubmit?: string;
  recipient?: string;
  reportingOffice?: string;
}) {
  return (
    <section className="card p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-green/10 ring-1 ring-civic-green/20">
          <Building2 className="h-4 w-4 text-civic-green" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">Relevant Department</h2>
      </div>
      <p className="text-sm leading-6 text-civic-muted">{department}</p>
      <dl className="mt-4 space-y-3 text-sm">
        {reportingOffice ? (
          <div className="rounded-lg border border-civic-border bg-civic-elevated px-3 py-2.5">
            <dt className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">Submit at</dt>
            <dd className="mt-1 font-semibold text-civic-text">{reportingOffice}</dd>
          </div>
        ) : null}
        {recipient ? (
          <div className="rounded-lg border border-civic-border bg-civic-elevated px-3 py-2.5">
            <dt className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">Addressed to</dt>
            <dd className="mt-1 font-semibold text-civic-text">{recipient}</dd>
          </div>
        ) : null}
        {whereToSubmit && whereToSubmit !== reportingOffice ? (
          <div>
            <dt className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">Where to submit</dt>
            <dd className="mt-1 text-civic-muted">{whereToSubmit}</dd>
          </div>
        ) : null}
      </dl>
    </section>
  );
}
