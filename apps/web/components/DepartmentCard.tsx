import { Building2 } from "lucide-react";

export function DepartmentCard({ department, whereToSubmit }: { department: string; whereToSubmit?: string }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-3 flex items-center gap-2">
        <Building2 className="h-5 w-5 text-civic-green" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">Relevant Department</h2>
      </div>
      <p className="text-sm leading-6 text-civic-muted">{department}</p>
      {whereToSubmit ? <p className="mt-3 font-mono text-xs text-civic-muted">Submit: {whereToSubmit}</p> : null}
    </section>
  );
}
