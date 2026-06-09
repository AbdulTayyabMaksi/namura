"use client";

import { useAppStore } from "@/lib/store";
import { Mic, MicOff, Wifi, WifiOff } from "lucide-react";

export default function Header() {
  const { twin, voiceMode, setVoiceMode, lowDataMode, setLowDataMode } = useAppStore();

  return (
    <header className="glass flex items-center justify-between border-b border-white/5 px-6 py-3">
      <div>
        <h2 className="text-lg font-semibold">
          {twin ? `Welcome, ${twin.name.split(" ")[0]}` : "ArthSaathi Dashboard"}
        </h2>
        {twin && (
          <p className="text-xs text-slate-400">
            {twin.context.occupation} · {twin.context.location} · Archetype:{" "}
            <span className="text-emerald-400">{twin.behavioral_archetype}</span>
          </p>
        )}
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => setLowDataMode(!lowDataMode)}
          className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs transition-all ${
            lowDataMode
              ? "bg-amber-500/20 text-amber-400"
              : "bg-white/5 text-slate-400 hover:bg-white/10"
          }`}
          aria-label={lowDataMode ? "Disable low data mode" : "Enable low data mode"}
          aria-pressed={lowDataMode}
        >
          {lowDataMode ? <WifiOff size={14} /> : <Wifi size={14} />}
          Low Data
        </button>

        <button
          onClick={() => setVoiceMode(!voiceMode)}
          className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs transition-all ${
            voiceMode
              ? "bg-violet-500/20 text-violet-400 glow-violet"
              : "bg-white/5 text-slate-400 hover:bg-white/10"
          }`}
          aria-label={voiceMode ? "Disable voice mode" : "Enable voice mode"}
          aria-pressed={voiceMode}
        >
          {voiceMode ? <Mic size={14} /> : <MicOff size={14} />}
          Voice {voiceMode ? "ON" : "OFF"}
        </button>

        <div className="hidden items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400 sm:flex">
          <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
          6 Agents Active
        </div>
      </div>
    </header>
  );
}
