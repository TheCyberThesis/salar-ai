import { DashboardClient } from "@/components/DashboardClient";

export default function DashboardPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-7">
        <p className="font-mono text-[11px] uppercase tracking-widest text-civic-green">Reports</p>
        <h1 className="mt-2 font-heading text-3xl font-bold text-civic-text">Your Guidance Dashboard</h1>
        <p className="mt-2 text-sm leading-6 text-civic-muted">
          View and manage all generated civic guidance reports for this session.
        </p>
      </div>
      <DashboardClient />
    </main>
  );
}
