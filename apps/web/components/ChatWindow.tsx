"use client";

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

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_24rem]">
      <section className="overflow-hidden rounded-lg border border-civic-line bg-white shadow-soft">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-civic-line bg-slate-50 p-4">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-normal text-civic-muted">Assistant</p>
            <h1 className="font-heading text-xl font-bold text-civic-ink">Civic guidance chat</h1>
          </div>
          <button
            type="button"
            onClick={chat.clearChat}
            className="focus-ring inline-flex items-center gap-2 rounded-md border border-civic-line bg-white px-3 py-2 text-sm font-semibold text-civic-ink hover:bg-civic-mint"
          >
            <RotateCcw className="h-4 w-4" aria-hidden="true" />
            Clear
          </button>
        </div>

        <div className="civic-grid max-h-[34rem] min-h-[28rem] space-y-4 overflow-y-auto p-4">
          {chat.messages.map((message) => (
            <ChatBubble key={message.id} message={message} />
          ))}
          {chat.isLoading ? <LoadingState /> : null}
        </div>

        <MessageInput disabled={chat.isLoading} onSend={chat.send} />
      </section>

      <aside className="space-y-4">
        <SafetyNotice sensitive={sensitive} />
        <section className="rounded-lg border border-civic-line bg-white p-4">
          <h2 className="mb-3 font-heading text-lg font-bold text-civic-ink">Quick start</h2>
          <QuickIssueCards onSelect={chat.send} />
        </section>
        <FollowUpQuestions questions={chat.lastResponse?.follow_up_questions ?? []} />
        {chat.lastResponse?.sources?.length ? <VerifiedSourcesCard sources={chat.lastResponse.sources} /> : null}
        {chat.error ? <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{chat.error}</div> : null}
        <button
          type="button"
          disabled={!chat.canGenerateReport || chat.isLoading}
          onClick={chat.createReport}
          className="focus-ring inline-flex w-full items-center justify-center gap-2 rounded-md bg-civic-green px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          <ScrollText className="h-4 w-4" aria-hidden="true" />
          Generate guidance report
        </button>
      </aside>

      {chat.report ? (
        <section className="lg:col-span-2">
          <ReportPreview report={chat.report} compact />
        </section>
      ) : null}
    </div>
  );
}
