import type { ChatResponse, ReportResponse, UserLocation, VoiceChatResponse } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function readErrorMessage(response: Response): Promise<string> {
  const fallback = `API request failed with ${response.status}`;
  const contentType = response.headers.get("content-type") ?? "";
  try {
    if (contentType.includes("application/json")) {
      const payload = (await response.json()) as { detail?: unknown; message?: unknown };
      const detail = payload.detail ?? payload.message;
      if (typeof detail === "string") return detail;
      if (detail && typeof detail === "object" && "message" in detail) {
        const nestedMessage = (detail as { message?: unknown }).message;
        if (typeof nestedMessage === "string") return nestedMessage;
      }
      return JSON.stringify(payload);
    }
    const message = await response.text();
    return message || fallback;
  } catch {
    return fallback;
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {})
      }
    });
  } catch (err) {
    throw new Error(
      `Could not reach Salar AI API at ${API_BASE_URL}. Make sure the FastAPI server is running, NEXT_PUBLIC_API_BASE_URL is correct, and your browser is not blocking the request.`
    );
  }
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json() as Promise<T>;
}

export async function sendChatMessage(input: {
  sessionId?: string;
  message: string;
  userLocation?: UserLocation;
  userId?: string;
}): Promise<ChatResponse> {
  return apiFetch<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({
      session_id: input.sessionId,
      message: input.message,
      user_location: input.userLocation,
      user_id: input.userId
    })
  });
}

export async function sendVoiceMessage(input: {
  sessionId?: string;
  audioBase64: string;
  mimeType: string;
  userLocation?: UserLocation;
  userId?: string;
}): Promise<VoiceChatResponse> {
  return apiFetch<VoiceChatResponse>("/api/voice-message", {
    method: "POST",
    body: JSON.stringify({
      session_id: input.sessionId,
      audio_base64: input.audioBase64,
      mime_type: input.mimeType,
      user_location: input.userLocation,
      user_id: input.userId
    })
  });
}

export async function generateReport(sessionId: string, userId?: string): Promise<ReportResponse> {
  return apiFetch<ReportResponse>("/api/generate-report", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId, user_id: userId })
  });
}

export async function fetchReport(reportId: string): Promise<ReportResponse> {
  return apiFetch<ReportResponse>(`/api/reports/${reportId}`);
}
