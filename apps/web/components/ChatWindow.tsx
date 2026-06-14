"use client";

import { useEffect, useRef } from "react";
import { RotateCcw, ScrollText } from "lucide-react";

import { ChatBubble } from "@/components/ChatBubble";
import { FollowUpQuestions } from "@/components/FollowUpQuestions";
import { LoadingState } from "@/components/LoadingState";
import { MessageInput } from "@/components/MessageInput";
import { QuickIssueCards } from "@/components/QuickIssueCards";
import { ReportPreview } from "@/components/ReportPreview";
import { SafetyNotice } from "@/components/SafetyNotice";
import { VerifiedSourcesCard } from "@/components/VerifiedSourcesCard";
import { useChat } from "@/hooks/useChat";

export function ChatWindow() {
  const chat = useChat();
  const sensitive = chat.lastResponse?.category === "workplace_harassment_women";
  const chatboxRef = useRef<HTMLDivElement | null>(null);
  const latestMessageRef = useRef<HTMLDivElement | null>(null);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!chat.messages.length) return;
    const frame = window.requestAnimationFrame(() => {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
      latestMessageRef.current?.focus({ preventScroll: true });
    });
    return () => window.cancelAnimationFrame(frame);
  }, [chat.messages, chat.isLoading]);

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_22rem]">

      {/* ── Chat panel ──────────────────────────────────────── */}
      <section className="overflow-hidden rounded-xl border border-civic-border bg-civic-surface shadow-card">

        {/* Header bar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-civic-border bg-civic-elevated px-4 py-3">
          <div className="flex items-center gap-3">
            {/* traffic lights */}
            <div className="flex gap-1.5">
              <span className="h-3 w-3 rounded-full bg-red-500/50" />
              <span className="h-3 w-3 rounded-full bg-civic-amber/50" />
              <span className="h-3 w-3 rounded-full bg-civic-green/50" />
            </div>
            <div>
              <p className="font-mono text-[10px] uppercase tracking-widest text-civic-muted">terminal</p>
              <h1 className="font-heading text-lg font-bold text-civic-text">Civic Guidance Chat</h1>
            </div>
          </div>
          <button
            type="button"
            onClick={chat.clearChat}
            className="focus-ring inline-flex items-center gap-2 rounded-lg border border-civic-border bg-civic-surface px-3 py-2 font-mono text-xs text-civic-muted transition hover:border-civic-muted/40 hover:text-civic-text"
          >
            <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
            Clear
          </button>
        </div>

        {/* Messages */}
        <div
          ref={chatboxRef}
          className="civic-grid max-h-[36rem] min-h-[28rem] space-y-4 overflow-y-auto p-4"
        >
          {chat.messages.length === 0 && (
            <div className="flex h-full min-h-[24rem] items-center justify-center">
              <div className="text-center">
                <p className="font-mono text-3xl font-bold text-civic-green/20">&gt;_</p>
                <p className="mt-2 font-mono text-xs uppercase tracking-widest text-civic-muted/50">
                  Start by describing your issue
                </p>
              </div>
            </div>
          )}
          {chat.messages.map((message, index) => (
            <div
              key={message.id}
              ref={index === chat.messages.length - 1 ? latestMessageRef : undefined}
              tabIndex={-1}
              className="scroll-mt-4 outline-none"
            >
              <ChatBubble message={message} />
            </div>
          ))}
          {chat.isLoading ? <LoadingState /> : null}
          <div ref={chatEndRef} aria-hidden="true" />
        </div>

        <MessageInput disabled={chat.isLoading} onSend={chat.send} onVoice={chat.sendVoice} />
      </section>

      {/* ── Sidebar ─────────────────────────────────────────── */}
      <aside className="space-y-4">
        <SafetyNotice sensitive={sensitive} />

        <section className="card p-4">
          <h2 className="mb-3 font-mono text-[11px] uppercase tracking-widest text-civic-muted">Quick start</h2>
          <QuickIssueCards onSelect={chat.send} />
        </section>

        <FollowUpQuestions questions={chat.lastResponse?.follow_up_questions ?? []} />

        {chat.lastResponse?.sources?.length ? (
          <VerifiedSourcesCard sources={chat.lastResponse.sources} />
        ) : null}

        {chat.error ? (
          <div className="rounded-xl border border-red-500/25 bg-red-500/8 p-4 font-mono text-sm text-red-400">
            {chat.error}
          </div>
        ) : null}

        {/* Generate report button */}
        <button
          type="button"
          disabled={!chat.canGenerateReport || chat.isLoading}
          onClick={chat.createReport}
          className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-xl bg-civic-green px-4 py-3.5 font-mono text-sm font-bold uppercase tracking-wider text-white shadow-glow-sm transition hover:brightness-110 disabled:cursor-not-allowed disabled:bg-civic-muted/20 disabled:text-civic-muted disabled:shadow-none"
        >
          <ScrollText className="h-4 w-4" aria-hidden="true" />
          Generate guidance report
        </button>
      </aside>

      {/* ── Report preview ───────────────────────────────────── */}
      {chat.report ? (
        <section className="lg:col-span-2">
          <ReportPreview report={chat.report} compact />
        </section>
      ) : null}
    </div>
  );
}
