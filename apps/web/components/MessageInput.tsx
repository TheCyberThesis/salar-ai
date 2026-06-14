"use client";

import { FormEvent, KeyboardEvent, useRef, useState } from "react";
import { Mic, SendHorizonal, Square } from "lucide-react";

type VoicePayload = {
  audioBase64: string;
  mimeType: string;
};

function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result;
      if (typeof result !== "string") {
        reject(new Error("Could not read audio."));
        return;
      }
      resolve(result.split(",")[1] ?? "");
    };
    reader.onerror = () => reject(new Error("Could not read audio."));
    reader.readAsDataURL(blob);
  });
}

export function MessageInput({
  disabled,
  onSend,
  onVoice,
}: {
  disabled?: boolean;
  onSend: (message: string) => void;
  onVoice: (payload: VoicePayload) => void;
}) {
  const [value, setValue] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  function resetHeight() {
    const el = textareaRef.current;
    if (el) { el.style.height = "auto"; }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = value.trim();
    if (!message) return;
    onSend(message);
    setValue("");
    resetHeight();
  }

  function handleChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setValue(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      const form = e.currentTarget.form;
      if (form) form.requestSubmit();
    }
  }

  async function toggleRecording() {
    setVoiceError(null);
    if (isRecording && recorderRef.current) {
      recorderRef.current.stop();
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
      setVoiceError("Voice recording is not supported in this browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : "audio/webm";
      const recorder = new MediaRecorder(stream, { mimeType });
      chunksRef.current = [];
      recorderRef.current = recorder;

      recorder.ondataavailable = (e) => { if (e.data.size > 0) chunksRef.current.push(e.data); };
      recorder.onstop = async () => {
        setIsRecording(false);
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || "audio/webm" });
        chunksRef.current = [];
        recorderRef.current = null;
        if (!blob.size) return;
        try {
          const audioBase64 = await blobToBase64(blob);
          onVoice({ audioBase64, mimeType: blob.type || "audio/webm" });
        } catch (err) {
          setVoiceError(err instanceof Error ? err.message : "Could not process recorded audio.");
        }
      };

      recorder.start();
      setIsRecording(true);
    } catch {
      setVoiceError("Microphone access was blocked or unavailable.");
    }
  }

  return (
    <div className="border-t border-civic-border bg-civic-surface/80 p-3 backdrop-blur">
      <form onSubmit={submit} className="flex gap-2">
        <label className="sr-only" htmlFor="message">Message</label>
        <textarea
          ref={textareaRef}
          id="message"
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={3}
          placeholder="Describe your incident in detail… (Enter for new line · Ctrl+Enter to send)"
          className="focus-ring min-h-[4.5rem] max-h-[200px] flex-1 resize-none overflow-y-auto rounded-lg border border-civic-border bg-civic-bg px-3 py-2.5 font-mono text-sm text-civic-text shadow-inner placeholder:text-civic-muted/40 transition focus:border-civic-green/40 focus:bg-civic-elevated disabled:opacity-50"
        />
        <button
          type="button"
          disabled={disabled}
          onClick={toggleRecording}
          className={`focus-ring grid h-12 w-12 shrink-0 place-items-center rounded-lg border transition ${
            isRecording
              ? "border-red-500/40 bg-red-500/10 text-red-400 shadow-[0_0_12px_rgba(255,80,80,0.20)]"
              : "border-civic-border bg-civic-elevated text-civic-muted hover:border-civic-blue/30 hover:text-civic-blue disabled:opacity-40"
          }`}
          title={isRecording ? "Stop recording" : "Record voice message"}
        >
          {isRecording
            ? <Square className="h-4 w-4" aria-hidden="true" />
            : <Mic className="h-4 w-4" aria-hidden="true" />}
        </button>
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="focus-ring grid h-12 w-12 shrink-0 place-items-center rounded-lg bg-civic-green text-civic-bg shadow-glow-sm transition hover:brightness-110 disabled:cursor-not-allowed disabled:bg-civic-muted/20 disabled:shadow-none disabled:text-civic-muted"
          title="Send message"
        >
          <SendHorizonal className="h-4 w-4" aria-hidden="true" />
        </button>
      </form>
      {voiceError ? (
        <p className="mt-2 font-mono text-[11px] text-red-400">{voiceError}</p>
      ) : null}
    </div>
  );
}
