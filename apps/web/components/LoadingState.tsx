export function LoadingState({ label = "processing guidance flow" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 px-4 py-3">
      <div className="flex gap-1">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="block h-1.5 w-1.5 rounded-full bg-civic-green"
            style={{ animation: `pulse3 1.4s ease-in-out ${i * 0.18}s infinite` }}
          />
        ))}
      </div>
      <span className="font-mono text-[11px] uppercase tracking-widest text-civic-muted">
        {label}
      </span>
    </div>
  );
}
