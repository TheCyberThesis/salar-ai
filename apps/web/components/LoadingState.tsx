export function LoadingState({ label = "Salaar AI is checking the guidance flow" }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 px-4 py-3 font-mono text-xs text-civic-muted">
      <span className="h-2 w-2 animate-pulse rounded-full bg-civic-green" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-civic-blue [animation-delay:120ms]" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-civic-green [animation-delay:240ms]" />
      <span className="ml-2">{label}</span>
    </div>
  );
}
