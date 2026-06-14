import clsx from "clsx";

import { FormattedMessage } from "@/components/FormattedMessage";
import type { ChatMessage } from "@/lib/types";

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={clsx("flex gap-3", isUser ? "justify-end" : "justify-start")}>
      {/* Avatar dot */}
      {!isUser && (
        <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-civic-green/10 ring-1 ring-civic-green/25">
          <span className="font-mono text-[9px] font-bold text-civic-green">&gt;_</span>
        </div>
      )}

      <div
        className={clsx(
          "max-w-[88%] rounded-xl px-4 py-3 sm:max-w-[76%]",
          isUser
            ? "bg-civic-blue text-white shadow-[0_4px_16px_rgba(24,100,171,0.22)]"
            : "border border-civic-border bg-civic-surface shadow-[0_2px_12px_rgba(12,29,44,0.08)]"
        )}
      >
        <div
          className={clsx(
            "mb-1.5 font-mono text-[10px] uppercase tracking-widest",
            isUser ? "text-white/60" : "text-civic-green"
          )}
        >
          {isUser ? "you" : "salar·ai"}
        </div>
        <FormattedMessage content={message.content} isUser={isUser} />
      </div>

      {isUser && (
        <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-civic-blue/10 ring-1 ring-civic-blue/20">
          <span className="font-mono text-[9px] font-bold text-civic-blue">U</span>
        </div>
      )}
    </div>
  );
}
