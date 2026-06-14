import { ChatWindow } from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-7">
        <p className="font-mono text-[11px] uppercase tracking-widest text-civic-green">
          English · Urdu · Roman Urdu
        </p>
        <h1 className="mt-2 font-heading text-3xl font-bold text-civic-text">
          Tell Salar AI what happened
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-civic-muted">
          Write in any language. Salar AI will identify the category, collect missing details, and generate a complete complaint draft and guidance report.
        </p>
      </div>
      <ChatWindow />
    </main>
  );
}
