"use client";

import { Bell, Check, Clock, X } from "lucide-react";
import { api } from "@/lib/api";
import { useAppStore } from "@/lib/store";

interface NudgeCardProps {
  nudge: Record<string, unknown>;
}

export default function NudgeCard({ nudge }: NudgeCardProps) {
  const { userId } = useAppStore();

  const handleFeedback = async (action: string) => {
    if (!userId || !nudge.id) return;
    try {
      await api.nudgeFeedback(userId, String(nudge.id), action);
    } catch {
      /* silent */
    }
  };

  return (
    <div
      className="mt-3 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3"
      role="alert"
      aria-label="Daily financial nudge"
    >
      <div className="mb-2 flex items-center gap-2">
        <Bell size={14} className="text-amber-400" />
        <span className="text-xs font-semibold text-amber-400">Today&apos;s Nudge</span>
      </div>
      <p className="text-xs">{String(nudge.message)}</p>
      {nudge.action != null && (
        <p className="mt-1 text-[11px] text-slate-400">Action: {String(nudge.action)}</p>
      )}
      <div className="mt-2 flex gap-2">
        <button
          onClick={() => handleFeedback("acted")}
          className="flex items-center gap-1 rounded-lg bg-emerald-500/10 px-2 py-1 text-[10px] text-emerald-400 hover:bg-emerald-500/20"
          aria-label="Mark nudge as done"
        >
          <Check size={10} /> Done
        </button>
        <button
          onClick={() => handleFeedback("snoozed")}
          className="flex items-center gap-1 rounded-lg bg-white/5 px-2 py-1 text-[10px] text-slate-400 hover:bg-white/10"
          aria-label="Snooze nudge"
        >
          <Clock size={10} /> Snooze
        </button>
        <button
          onClick={() => handleFeedback("dismissed")}
          className="flex items-center gap-1 rounded-lg bg-white/5 px-2 py-1 text-[10px] text-slate-400 hover:bg-white/10"
          aria-label="Dismiss nudge"
        >
          <X size={10} /> Dismiss
        </button>
      </div>
    </div>
  );
}
