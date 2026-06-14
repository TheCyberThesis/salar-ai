import { LockKeyhole } from "lucide-react";

export function SafetyNotice({ sensitive = false }: { sensitive?: boolean }) {
  return (
    <div className="rounded-lg border border-civic-line bg-white p-4 text-sm text-civic-muted">
      <div className="flex items-start gap-3">
        <LockKeyhole className="mt-0.5 h-5 w-5 shrink-0 text-civic-blue" aria-hidden="true" />
        <p>
          {sensitive
            ? "For harassment-related issues, avoid graphic details and do not share private evidence publicly. If you are in immediate danger, contact emergency services or trusted local support first."
            : "Avoid sharing CNIC, phone number, IMEI, address, or private evidence unless the relevant authority requires it."}
        </p>
      </div>
    </div>
  );
}
