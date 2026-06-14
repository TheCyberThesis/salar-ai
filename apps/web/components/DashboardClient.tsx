"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, LogIn, LogOut, Plus, UserRound } from "lucide-react";
import type { Session } from "@supabase/supabase-js";

import { isReportResponse, mergeReports } from "@/lib/reports";
import { getReportsFromBrowser } from "@/lib/storage";
import { supabase } from "@/lib/supabase";
import type { ReportResponse } from "@/lib/types";

export function DashboardClient() {
  const [reports, setReports] = useState<ReportResponse[]>([]);
  const [session, setSession] = useState<Session | null>(null);
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  const getSupabaseReports = useCallback(async (): Promise<ReportResponse[]> => {
    if (!supabase) return [];
    const { data, error } = await supabase
      .from("user_complaints")
      .select("generated_report")
      .order("created_at", { ascending: false })
      .limit(20);
    if (error) { setMessage(error.message); return []; }
    return (data ?? []).map((row) => row.generated_report).filter(isReportResponse);
  }, []);

  const refreshReports = useCallback(async (cur: Session | null) => {
    const local = getReportsFromBrowser();
    if (!cur) { setReports(local); return; }
    const remote = await getSupabaseReports();
    setReports(mergeReports(remote, local));
  }, [getSupabaseReports]);

  useEffect(() => {
    let mounted = true;
    Promise.resolve().then(() => { if (mounted) setReports(getReportsFromBrowser()); });
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => {
      if (!mounted) return;
      setSession(data.session);
      refreshReports(data.session);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_e, cur) => {
      setSession(cur);
      refreshReports(cur);
    });
    return () => { mounted = false; sub.subscription.unsubscribe(); };
  }, [refreshReports]);

  async function signIn(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!supabase) { setMessage("Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY."); return; }
    const { error } = await supabase.auth.signInWithOtp({ email });
    setMessage(error ? error.message : "Magic link sent. Check your email.");
  }

  async function signOut() { await supabase?.auth.signOut(); }

  const subcategoryLabel = (r: ReportResponse) =>
    r.subcategory?.replaceAll("_", " ") || r.category;

  return (
    <div className="grid gap-5 lg:grid-cols-[20rem_minmax(0,1fr)]">

      {/* ── Account panel ───────────────────────────────────── */}
      <aside className="space-y-4">
        <section className="card p-5">
          <div className="mb-4 flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-blue/10 ring-1 ring-civic-blue/20">
              <UserRound className="h-4 w-4 text-civic-blue" aria-hidden="true" />
            </span>
            <h2 className="font-heading text-base font-bold text-civic-text">Account</h2>
          </div>

          {session ? (
            <div className="space-y-3">
              <p className="font-mono text-xs text-civic-muted">{session.user.email}</p>
              <button
                onClick={signOut}
                className="focus-ring inline-flex items-center gap-2 rounded-lg border border-civic-border bg-civic-elevated px-3 py-2 font-mono text-xs text-civic-muted transition hover:border-civic-muted/40 hover:text-civic-text"
              >
                <LogOut className="h-3.5 w-3.5" aria-hidden="true" />
                Sign out
              </button>
            </div>
          ) : (
            <form onSubmit={signIn} className="space-y-3">
              <label className="block font-mono text-[11px] uppercase tracking-widest text-civic-muted" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="focus-ring w-full rounded-lg border border-civic-border bg-civic-bg px-3 py-2.5 font-mono text-sm text-civic-text placeholder:text-civic-muted/40 transition focus:border-civic-blue/40"
              />
              <button
                type="submit"
                className="focus-ring inline-flex items-center gap-2 rounded-lg bg-civic-blue px-3 py-2.5 font-mono text-xs font-bold uppercase tracking-wider text-white transition hover:brightness-110"
              >
                <LogIn className="h-3.5 w-3.5" aria-hidden="true" />
                Send magic link
              </button>
              <p className="font-mono text-[10px] leading-5 text-civic-muted">
                Guest reports are stored in this browser. Supabase Auth is used when configured.
              </p>
            </form>
          )}

          {message ? (
            <div className="mt-3 rounded-lg border border-civic-amber/25 bg-civic-amber-glow p-3 font-mono text-xs text-civic-amber">
              {message}
            </div>
          ) : null}
        </section>
      </aside>

      {/* ── Reports panel ───────────────────────────────────── */}
      <section className="card p-5">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">Previous complaints</p>
            <h1 className="font-heading text-2xl font-bold text-civic-text">Guidance Reports</h1>
          </div>
          <Link
            href="/chat"
            className="focus-ring inline-flex items-center gap-2 rounded-lg bg-civic-green px-4 py-2.5 font-mono text-xs font-bold uppercase tracking-wider text-white shadow-glow-sm transition hover:brightness-110"
          >
            <Plus className="h-3.5 w-3.5" aria-hidden="true" />
            New chat
          </Link>
        </div>

        {reports.length ? (
          <div className="space-y-3">
            {reports.map((report) => (
              <Link
                key={report.report_id}
                href={`/report/${report.report_id}`}
                className="group flex items-center justify-between gap-4 rounded-xl border border-civic-border bg-civic-elevated p-4 transition-all hover:border-civic-green/30 hover:shadow-[0_0_20px_rgba(0,232,126,0.05)]"
              >
                <div className="min-w-0">
                  <h2 className="font-heading text-sm font-bold capitalize text-civic-text">
                    {subcategoryLabel(report)}
                  </h2>
                  <p className="mt-0.5 truncate font-mono text-[11px] text-civic-muted">{report.department}</p>
                </div>
                <div className="flex shrink-0 items-center gap-3">
                  <span className="chip chip-green">Generated</span>
                  <ArrowRight className="h-4 w-4 text-civic-muted transition group-hover:text-civic-green" aria-hidden="true" />
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-civic-border py-16 text-center">
            <div className="mb-3 font-mono text-4xl font-bold text-civic-muted/20">&gt;_</div>
            <p className="font-heading text-lg font-bold text-civic-text">No saved reports yet</p>
            <p className="mt-2 max-w-xs text-sm text-civic-muted">
              Generate a report from a chat session and it will appear here.
            </p>
            <Link
              href="/chat"
              className="focus-ring mt-5 inline-flex items-center gap-2 rounded-lg bg-civic-green px-5 py-2.5 font-mono text-xs font-bold uppercase tracking-wider text-white shadow-glow-sm transition hover:brightness-110"
            >
              Start guidance
              <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
            </Link>
          </div>
        )}
      </section>
    </div>
  );
}
