"use client";

import { FormEvent, useState } from "react";
import { SendHorizonal } from "lucide-react";

export function MessageInput({ disabled, onSend }: { disabled?: boolean; onSend: (message: string) => void }) {
  const [value, setValue] = useState("");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = value.trim();
    if (!message) return;
    onSend(message);
    setValue("");
  }

  return (
    <form onSubmit={submit} className="flex gap-2 border-t border-civic-line bg-white p-3">
      <label className="sr-only" htmlFor="message">
        Message
      </label>
      <textarea
        id="message"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        disabled={disabled}
        rows={2}
        placeholder="Write in English, Urdu, or Roman Urdu..."
        className="focus-ring min-h-12 flex-1 resize-none rounded-md border border-civic-line px-3 py-2 text-sm text-civic-ink placeholder:text-civic-muted"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="focus-ring grid h-12 w-12 shrink-0 place-items-center rounded-md bg-civic-green text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        title="Send message"
      >
        <SendHorizonal className="h-5 w-5" aria-hidden="true" />
      </button>
    </form>
  );
}
