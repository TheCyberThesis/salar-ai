import { MapPin } from "lucide-react";

export function MapsCard({ mapsLink }: { mapsLink: string }) {
  return (
    <section className="rounded-lg border border-civic-line bg-white p-5">
      <div className="mb-3 flex items-center gap-2">
        <MapPin className="h-5 w-5 text-civic-blue" aria-hidden="true" />
        <h2 className="font-heading text-lg font-bold text-civic-ink">Location Search</h2>
      </div>
      <p className="mb-4 text-sm leading-6 text-civic-muted">Use this as a starting point and confirm the correct office before visiting.</p>
      <a className="focus-ring inline-flex rounded-md bg-civic-blue px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800" href={mapsLink} target="_blank" rel="noreferrer">
        Open Maps
      </a>
    </section>
  );
}
