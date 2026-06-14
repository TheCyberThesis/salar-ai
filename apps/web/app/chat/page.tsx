import { ChatWindow } from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6">
        <p className="font-mono text-xs uppercase tracking-normal text-civic-green">English · Urdu · Roman Urdu</p>
        <h1 className="mt-2 font-heading text-3xl font-bold text-civic-ink">Tell Salaar AI what happened</h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-civic-muted">
          You can write in English, Urdu, or Roman Urdu. Guest chat works; saving reports later can be connected to Supabase Auth.
        </p>
      </div>
      <ChatWindow />
    </main>
  );
}
