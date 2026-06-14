"use client";

import { useMemo, useState } from "react";

import { generateReport, sendChatMessage } from "@/lib/api";
import { saveReportToBrowser } from "@/lib/storage";
import { supabase } from "@/lib/supabase";
import type { ChatMessage, ChatResponse, ReportResponse, UserLocation } from "@/lib/types";

const greeting =
  "Assalam-o-Alaikum. I’m Salaar AI. Tell me your civic issue in English, Urdu, or Roman Urdu, and I’ll guide you step by step.";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: "greeting", role: "assistant", content: greeting, createdAt: new Date().toISOString() }
  ]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [location, setLocation] = useState<UserLocation>({ city: "Islamabad", area: "G-10" });

  const canGenerateReport = useMemo(() => Boolean(sessionId && lastResponse?.category !== "unsupported"), [sessionId, lastResponse]);

  async function send(message: string) {
    const trimmed = message.trim();
    if (!trimmed) return;
    setError(null);
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", content: trimmed, createdAt: new Date().toISOString() }
    ]);
    setIsLoading(true);
    try {
      const response = await sendChatMessage({ sessionId, message: trimmed, userLocation: location });
      setSessionId(response.session_id);
      setLastResponse(response);
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", content: response.reply, createdAt: new Date().toISOString() }
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not reach Salaar AI backend.");
    } finally {
      setIsLoading(false);
    }
  }

  async function createReport() {
    if (!sessionId) return;
    setIsLoading(true);
    setError(null);
    try {
      const auth = supabase ? await supabase.auth.getSession() : null;
      const userId = auth?.data.session?.user.id;
      const generated = await generateReport(sessionId, userId);
      setReport(generated);
      saveReportToBrowser(generated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not generate report.");
    } finally {
      setIsLoading(false);
    }
  }

  function clearChat() {
    setMessages([{ id: "greeting", role: "assistant", content: greeting, createdAt: new Date().toISOString() }]);
    setSessionId(undefined);
    setLastResponse(null);
    setReport(null);
    setError(null);
  }

  return {
    messages,
    sessionId,
    lastResponse,
    report,
    isLoading,
    error,
    location,
    setLocation,
    send,
    createReport,
    clearChat,
    canGenerateReport
  };
}
