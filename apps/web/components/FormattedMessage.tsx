import clsx from "clsx";
import type { ReactNode } from "react";

function InlineText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <strong key={`${part}-${i}`} className="font-semibold text-inherit">
            {part.slice(2, -2)}
          </strong>
        ) : (
          <span key={`${part}-${i}`}>{part}</span>
        )
      )}
    </>
  );
}

const isHeading  = (l: string) => /^#{1,4}\s+/.test(l);
const isBullet   = (l: string) => /^[-*]\s+/.test(l.trim());
const isNumbered = (l: string) => /^\d+[.)]\s+/.test(l.trim());

export function FormattedMessage({ content, isUser }: { content: string; isUser?: boolean }) {
  const lines = content.split(/\r?\n/);
  const blocks: ReactNode[] = [];
  let idx = 0;

  while (idx < lines.length) {
    const line = lines[idx];
    const trimmed = line.trim();
    if (!trimmed) { idx++; continue; }

    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      blocks.push(
        <h3
          key={`h-${idx}`}
          className={clsx(
            "mt-4 first:mt-0 font-heading font-bold leading-snug",
            isUser ? "text-white" : "text-civic-text",
            level <= 2 ? "text-sm" : "text-[13px]"
          )}
        >
          <InlineText text={heading[2]} />
        </h3>
      );
      idx++;
      continue;
    }

    if (isNumbered(trimmed)) {
      const items: string[] = [];
      while (idx < lines.length && isNumbered(lines[idx])) {
        items.push(lines[idx].trim().replace(/^\d+[.)]\s+/, ""));
        idx++;
      }
      blocks.push(
        <ol key={`ol-${idx}`} className="my-3 space-y-1.5 pl-5 text-sm leading-6">
          {items.map((item, i) => (
            <li key={`${item}-${i}`} className="list-decimal pl-1">
              <InlineText text={item} />
            </li>
          ))}
        </ol>
      );
      continue;
    }

    if (isBullet(trimmed)) {
      const items: string[] = [];
      while (idx < lines.length && isBullet(lines[idx])) {
        items.push(lines[idx].trim().replace(/^[-*]\s+/, ""));
        idx++;
      }
      blocks.push(
        <ul key={`ul-${idx}`} className="my-3 space-y-1.5 pl-1 text-sm leading-6">
          {items.map((item, i) => (
            <li key={`${item}-${i}`} className="flex gap-2">
              <span className={clsx("mt-1 shrink-0 font-mono text-[10px]", isUser ? "text-blue-300/60" : "text-civic-green/60")}>▸</span>
              <InlineText text={item} />
            </li>
          ))}
        </ul>
      );
      continue;
    }

    const paraLines = [trimmed];
    idx++;
    while (idx < lines.length) {
      const next = lines[idx].trim();
      if (!next || isHeading(next) || isBullet(next) || isNumbered(next)) break;
      paraLines.push(next);
      idx++;
    }
    blocks.push(
      <p key={`p-${idx}`} className="my-2 first:mt-0 last:mb-0">
        <InlineText text={paraLines.join(" ")} />
      </p>
    );
  }

  return (
    <div
      className={clsx(
        "message-rich text-sm leading-6",
        isUser ? "text-white" : "text-civic-text"
      )}
    >
      {blocks}
    </div>
  );
}
