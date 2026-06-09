"use client";

import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { api } from "@/lib/api";
import { useAppStore } from "@/lib/store";

export default function HealthScoreCard() {
  const { userId } = useAppStore();

  const { data, isLoading } = useQuery({
    queryKey: ["health-score", userId],
    queryFn: () => api.getHealthScore(userId!),
    enabled: !!userId,
  });

  if (!userId || isLoading || !data) return null;

  const color =
    data.grade === "A" ? "#22c55e" :
    data.grade === "B" ? "#3b82f6" :
    data.grade === "C" ? "#eab308" : "#ef4444";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-5"
      role="region"
      aria-label={`Financial health score ${data.score} out of 100`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-400">Financial Health Score</p>
          <p className="text-2xl font-bold" style={{ color }}>{data.score}/100</p>
          <p className="text-sm text-slate-300">Grade {data.grade} — {data.label}</p>
        </div>
        <div
          className="flex h-20 w-20 items-center justify-center rounded-full text-2xl font-bold"
          style={{ backgroundColor: `${color}20`, color, border: `2px solid ${color}40` }}
        >
          {data.grade}
        </div>
      </div>
      <p className="mt-3 text-xs text-emerald-400">💡 {data.top_action}</p>
      <div className="mt-3 grid grid-cols-5 gap-1">
        {Object.entries(data.breakdown).map(([k, v]) => (
          <div key={k} className="text-center">
            <div className="mx-auto h-1.5 w-full overflow-hidden rounded-full bg-white/10">
              <div className="h-full rounded-full bg-emerald-500" style={{ width: `${Math.min(100, v)}%` }} />
            </div>
            <p className="mt-1 text-[9px] capitalize text-slate-500">{k.replace("_", " ")}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
