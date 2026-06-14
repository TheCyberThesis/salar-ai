"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { LogIn, LogOut, UserRound } from "lucide-react";
import type { Session } from "@supabase/supabase-js";

import { getReportsFromBrowser } from "@/lib/storage";
import { supabase } from "@/lib/supabase";
import type { ReportResponse } from "@/lib/types";

export function DashboardClient() {
  const [reports, setReports] = useState<ReportResponse[]>([]);
  const [session, setSession] = useState<Session | null>(null);
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    Promise.resolve().then(() => {
      if (mounted) setReports(getReportsFromBrowser());
    });
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => setSession(data.session));
    const { data: subscription } = supabase.auth.onAuthStateChange((_event, current) => setSession(current));
    return () => {
      mounted = false;
      subscription.subscription.unsubscribe();
    };
  }, []);

  async function signIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!supabase) {
      setMessage("Supabase is not configured yet. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY.");
      return;
    }
    const { error } = await supabase.auth.signInWithOtp({ email });
    setMessage(error ? error.message : "Magic link sent. Check your email.");
  }

  async function signOut() {
    await supabase?.auth.signOut();
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[22rem_minmax(0,1fr)]">
      <aside className="space-y-4">
        <section className="rounded-lg border border-civic-line bg-white p-5">
          <div className="mb-4 flex items-center gap-2">
            <UserRound className="h-5 w-5 text-civic-blue" aria-hidden="true" />
            <h2 className="font-heading text-lg font-bold text-civic-ink">Account</h2>
          </div>
          {session ? (
            <div className="space-y-3">
              <p className="text-sm text-civic-muted">{session.user.email}</p>
              <button className="focus-ring inline-flex items-center gap-2 rounded-md border border-civic-line px-3 py-2 text-sm font-semibold hover:bg-civic-mint" onClick={signOut}>
                <LogOut className="h-4 w-4" aria-hidden="true" />
                Sign out
              </button>
            </div>
          ) : (
            <form onSubmit={signIn} className="space-y-3">
              <label className="block text-sm font-semibold text-civic-ink" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                className="focus-ring w-full rounded-md border border-civic-line px-3 py-2 text-sm"
              />
              <button className="focus-ring inline-flex items-center gap-2 rounded-md bg-civic-blue px-3 py-2 text-sm font-semibold text-white hover:bg-blue-800">
                <LogIn className="h-4 w-4" aria-hidden="true" />
                Send magic link
              </button>
              <p className="text-xs leading-5 text-civic-muted">Guest reports are stored in this browser. Supabase Auth is used when configured.</p>
            </form>
          )}
          {message ? <p className="mt-3 rounded-md bg-civic-warning p-3 text-sm text-civic-ink">{message}</p> : null}
        </section>
      </aside>

      <section className="rounded-lg border border-civic-line bg-white p-5">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-normal text-civic-muted">Previous complaints</p>
            <h1 className="font-heading text-2xl font-bold text-civic-ink">Guidance reports</h1>
          </div>
          <Link className="focus-ring rounded-md bg-civic-green px-4 py-2 text-sm font-bold text-white hover:bg-emerald-800" href="/chat">
            New chat
          </Link>
        </div>
        {reports.length ? (
          <div className="space-y-3">
            {reports.map((report) => (
              <Link key={report.report_id} href={`/report/${report.report_id}`} className="block rounded-lg border border-civic-line bg-slate-50 p-4 hover:border-civic-green">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <h2 className="font-heading text-lg font-bold text-civic-ink">{report.subcategory?.replaceAll("_", " ") || report.category}</h2>
                    <p className="mt-1 text-sm text-civic-muted">{report.department}</p>
                  </div>
                  <span className="rounded-md bg-civic-mint px-3 py-1 font-mono text-[11px] uppercase text-civic-green">Guidance Generated</span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed border-civic-line p-8 text-center">
            <p className="font-heading text-xl font-bold text-civic-ink">No saved reports yet</p>
            <p className="mt-2 text-sm text-civic-muted">Generate a report from chat and it will appear here for this browser session.</p>
          </div>
        )}
      </section>
    </div>
  );
}
