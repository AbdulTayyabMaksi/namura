"use client";

import { ExternalLink, Landmark } from "lucide-react";

interface SchemeChipsProps {
  schemes: Array<Record<string, unknown> | { id: string; name: string; application_link?: string }>;
}

export default function SchemeChips({ schemes }: SchemeChipsProps) {
  if (!schemes?.length) return null;

  return (
    <div className="mt-3 border-t border-white/10 pt-3" role="region" aria-label="Matched government schemes">
      <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-amber-400">
        <Landmark size={12} /> {schemes.length} Eligible Schemes Found
      </p>
      <div className="flex flex-wrap gap-2">
        {schemes.slice(0, 6).map((s) => (
          <a
            key={String(s.id)}
            href={String(s.application_link || "#")}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 rounded-lg border border-amber-500/20 bg-amber-500/5 px-2.5 py-1.5 text-[11px] text-amber-200 hover:bg-amber-500/10"
          >
            {String(s.name)}
            <ExternalLink size={10} />
          </a>
        ))}
      </div>
    </div>
  );
}
