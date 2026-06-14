import { ShieldCheck } from "lucide-react";

export function SafetyNotice({ sensitive = false }: { sensitive?: boolean }) {
  return (
    <div className={`rounded-xl border p-4 ${sensitive ? "border-civic-amber/25 bg-civic-amber-glow" : "border-civic-border bg-civic-elevated"}`}>
      <div className="flex items-start gap-3">
        <ShieldCheck className={`mt-0.5 h-4 w-4 shrink-0 ${sensitive ? "text-civic-amber" : "text-civic-blue"}`} aria-hidden="true" />
        <p className="text-sm leading-6 text-civic-muted">
          {sensitive
            ? "For harassment-related issues, avoid graphic details and do not share private evidence publicly. If you are in immediate danger, contact emergency services or trusted local support first."
            : "Avoid sharing CNIC, phone number, IMEI, address, or private evidence unless the relevant authority requires it."}
        </p>
      </div>
    </div>
  );
}
