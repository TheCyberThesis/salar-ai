import { MapPin, Navigation, Phone } from "lucide-react";

import type { DepartmentLocation } from "@/lib/types";

export function MapsCard({ mapsLink, location }: { mapsLink: string; location?: DepartmentLocation | null }) {
  const lat = location?.latitude;
  const lng = location?.longitude;
  return (
    <section className="card p-5">
      <div className="mb-4 flex items-center gap-2">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-civic-blue/10 ring-1 ring-civic-blue/20">
          <MapPin className="h-4 w-4 text-civic-blue" aria-hidden="true" />
        </span>
        <h2 className="font-heading text-base font-bold text-civic-text">Nearest Office</h2>
      </div>

      {location?.place_name ? (
        <p className="font-heading text-base font-bold text-civic-text">{location.place_name}</p>
      ) : null}
      {location?.address ? (
        <p className="mt-1.5 text-sm leading-6 text-civic-muted">{location.address}</p>
      ) : null}

      {typeof lat === "number" && typeof lng === "number" ? (
        <div className="mt-3 rounded-lg border border-civic-blue/15 bg-civic-blue-glow px-3 py-2">
          <span className="font-mono text-xs text-civic-blue">
            {lat.toFixed(6)}, {lng.toFixed(6)}
          </span>
        </div>
      ) : null}

      {location?.phone_number ? (
        <p className="mt-3 flex items-center gap-2 font-mono text-sm font-semibold text-civic-text">
          <Phone className="h-4 w-4 text-civic-green" aria-hidden="true" />
          {location.phone_number}
        </p>
      ) : null}

      {location?.notes ? (
        <p className="mt-3 text-xs leading-5 text-civic-muted">{location.notes}</p>
      ) : null}

      <a
        className="focus-ring mt-4 inline-flex items-center gap-2 rounded-lg bg-civic-blue px-4 py-2.5 font-mono text-xs font-bold uppercase tracking-wider text-white shadow-glow-blue transition hover:brightness-110"
        href={location?.maps_link || mapsLink}
        target="_blank"
        rel="noreferrer"
      >
        <Navigation className="h-3.5 w-3.5" aria-hidden="true" />
        Open Google Maps
      </a>
    </section>
  );
}
