"use client";

import { motion } from "framer-motion";
import {
  AreaChart,
  Area,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
import type { ScenarioBranch } from "@/types";
import { formatCurrency, formatPercent } from "@/lib/utils";

interface ScenarioCardsProps {
  scenarios: ScenarioBranch[];
}

export default function ScenarioCards({ scenarios }: ScenarioCardsProps) {
  return (
    <div
      className="grid gap-3 md:grid-cols-3"
      role="region"
      aria-label="Future scenario comparison"
    >
      {scenarios.map((s, i) => {
        const chartData = s.savings_trajectory.map((v, idx) => ({
          month: `M${idx + 1}`,
          savings: Math.max(0, v),
        }));

        return (
          <motion.div
            key={s.path_type}
            initial={{ opacity: 0, y: 20, rotateX: -10 }}
            animate={{ opacity: 1, y: 0, rotateX: 0 }}
            transition={{ delay: i * 0.15, type: "spring" }}
            className="rounded-xl border border-white/10 bg-black/30 p-4 backdrop-blur-sm"
            style={{
              borderColor: `${s.color}33`,
              boxShadow: `0 8px 32px ${s.color}15`,
            }}
          >
            <div className="mb-3 flex items-center gap-2">
              <span
                className="h-3 w-3 rounded-full"
                style={{ backgroundColor: s.color }}
                aria-hidden="true"
              />
              <h4 className="text-xs font-semibold" style={{ color: s.color }}>
                {s.label}
              </h4>
            </div>
            <p className="mb-3 text-[11px] text-slate-400">{s.description}</p>

            <div className="mb-3 space-y-1.5 text-[11px]">
              <div className="flex justify-between">
                <span className="text-slate-500">6 months</span>
                <span>
                  Savings: {formatCurrency(s.month_6.savings || 0)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">12 months</span>
                <span className="font-medium" style={{ color: s.color }}>
                  Debt trap: {formatPercent(s.month_12.debt_trap_probability || s.debt_trap_probability)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">36 months</span>
                <span>
                  Savings: {formatCurrency(s.month_36.savings || 0)}
                </span>
              </div>
            </div>

            <div className="h-16" aria-hidden="true">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id={`grad-${i}`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={s.color} stopOpacity={0.4} />
                      <stop offset="100%" stopColor={s.color} stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="month" hide />
                  <YAxis hide />
                  <Tooltip
                    contentStyle={{
                      background: "#111827",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: 8,
                      fontSize: 11,
                    }}
                    formatter={(v) => [formatCurrency(Number(v ?? 0)), "Savings"]}
                  />
                  <Area
                    type="monotone"
                    dataKey="savings"
                    stroke={s.color}
                    fill={`url(#grad-${i})`}
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <p className="mt-2 text-[10px] text-slate-500">{s.goal_impact}</p>
            <p className="mt-1 text-[11px] font-medium" style={{ color: s.color }}>
              💡 {s.nudge_action}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}
