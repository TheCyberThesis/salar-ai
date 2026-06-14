"use client";

import { useMemo, useState } from "react";

import { generateReport, sendChatMessage, sendVoiceMessage } from "@/lib/api";
import { saveReportToBrowser } from "@/lib/storage";
import { supabase } from "@/lib/supabase";
import type { ChatMessage, ChatResponse, ReportResponse, UserLocation } from "@/lib/types";

const greeting =
  "Assalam-o-Alaikum. I’m Salar AI. Tell me your civic issue in English, Urdu, or Roman Urdu, and I’ll guide you step by step.";

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

  const canGenerateReport = useMemo(
    () => Boolean(sessionId && lastResponse?.category !== "unsupported" && lastResponse?.stage === "ready_to_generate"),
    [sessionId, lastResponse]
  );

  async function getCurrentUserId() {
    const auth = supabase ? await supabase.auth.getSession() : null;
    return auth?.data.session?.user.id;
  }

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
      const userId = await getCurrentUserId();
      const response = await sendChatMessage({ sessionId, message: trimmed, userLocation: location, userId });
      setSessionId(response.session_id);
      setLastResponse(response);
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", content: response.reply, createdAt: new Date().toISOString() }
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not reach Salar AI backend.");
    } finally {
      setIsLoading(false);
    }
  }

  async function sendVoice(audio: { audioBase64: string; mimeType: string }) {
    setError(null);
    setIsLoading(true);
    try {
      const userId = await getCurrentUserId();
      const response = await sendVoiceMessage({
        sessionId,
        audioBase64: audio.audioBase64,
        mimeType: audio.mimeType,
        userLocation: location,
        userId
      });
      setSessionId(response.chat.session_id);
      setLastResponse(response.chat);
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "user", content: response.transcript, createdAt: new Date().toISOString() },
        { id: crypto.randomUUID(), role: "assistant", content: response.chat.reply, createdAt: new Date().toISOString() }
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not process voice message.");
    } finally {
      setIsLoading(false);
    }
  }

  async function createReport() {
    if (!sessionId) return;
    setIsLoading(true);
    setError(null);
    try {
      const userId = await getCurrentUserId();
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
    sendVoice,
    createReport,
    clearChat,
    canGenerateReport
  };
}
