import clsx from "clsx";

import type { ChatMessage } from "@/lib/types";

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={clsx("flex", isUser ? "justify-end" : "justify-start")}>
      <div
        className={clsx(
          "max-w-[88%] rounded-lg px-4 py-3 text-sm leading-6 shadow-sm sm:max-w-[74%]",
          isUser ? "bg-civic-blue text-white" : "border border-civic-line bg-white text-civic-ink"
        )}
      >
        <div className={clsx("mb-1 font-mono text-[10px] uppercase tracking-normal", isUser ? "text-blue-100" : "text-civic-muted")}>
          {isUser ? "You" : "Salaar AI"}
        </div>
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}
