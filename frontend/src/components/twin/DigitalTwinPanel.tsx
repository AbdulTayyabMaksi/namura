"use client";

import { motion } from "framer-motion";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import dynamic from "next/dynamic";
import { useAppStore } from "@/lib/store";
import { formatCurrency, formatPercent } from "@/lib/utils";
import { TrendingUp, Shield, Target, Wallet, AlertTriangle, MapPin } from "lucide-react";
import HealthScoreCard from "@/components/twin/HealthScoreCard";

const DigitalTwinScene = dynamic(() => import("@/components/3d/DigitalTwinScene"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center text-slate-500">Loading 3D Twin...</div>
  ),
});

const DIMENSIONS = [
  { key: "income", label: "Income", icon: Wallet },
  { key: "expenditure", label: "Spending", icon: TrendingUp },
  { key: "debt", label: "Debt Health", icon: AlertTriangle },
  { key: "goals", label: "Goals", icon: Target },
  { key: "risk", label: "Risk", icon: Shield },
  { key: "context", label: "Context", icon: MapPin },
];

export default function DigitalTwinPanel() {
  const { twin } = useAppStore();

  if (!twin) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        Select a persona to view their Digital Twin
      </div>
    );
  }

  const avgIncome = (twin.income.range_min + twin.income.range_max) / 2;
  const debtHealth = Math.max(0, 1 - twin.debt.total_debt / (avgIncome * 12));
  const goalCount =
    twin.goals.short_term.length + twin.goals.medium_term.length + twin.goals.long_term.length;

  const radarData = [
    { dimension: "Income", value: Math.min(100, (avgIncome / 50000) * 100), fullMark: 100 },
    {
      dimension: "Spending",
      value: Math.max(0, 100 - (twin.expenditure.discretionary_spend / avgIncome) * 100),
      fullMark: 100,
    },
    { dimension: "Debt", value: debtHealth * 100, fullMark: 100 },
    { dimension: "Goals", value: Math.min(100, goalCount * 33), fullMark: 100 },
    { dimension: "Risk", value: twin.risk.shock_resilience * 100, fullMark: 100 },
    { dimension: "Behavior", value: twin.behavioral_score * 100, fullMark: 100 },
  ];

  return (
    <div className="h-full overflow-y-auto p-6" role="region" aria-label="Digital Twin profile">
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative h-72 overflow-hidden rounded-2xl border border-white/10 lg:h-96"
        >
          <DigitalTwinScene accentColor="#10b981" />
          <div className="absolute bottom-4 left-4 glass rounded-xl px-4 py-2">
            <p className="text-xs text-slate-400">Live Digital Twin</p>
            <p className="font-semibold">{twin.name}</p>
            <p className="text-xs text-emerald-400">v{twin.version} · {twin.behavioral_archetype}</p>
          </div>
        </motion.div>

        <div className="space-y-4">
          <div className="glass rounded-2xl p-4">
            <h3 className="mb-4 text-sm font-semibold text-emerald-400">6-Dimension Twin Radar</h3>
            <div className="h-56" role="img" aria-label="Radar chart of financial twin dimensions">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="dimension" tick={{ fill: "#94a3b8", fontSize: 11 }} />
                  <Radar
                    name="Twin Score"
                    dataKey="value"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#111827",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: 8,
                    }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {DIMENSIONS.map(({ key, label, icon: Icon }) => (
              <motion.div
                key={key}
                whileHover={{ scale: 1.02 }}
                className="glass rounded-xl p-3"
              >
                <div className="mb-1 flex items-center gap-2">
                  <Icon size={14} className="text-emerald-400" />
                  <span className="text-xs font-medium">{label}</span>
                </div>
                <p className="text-lg font-bold">
                  {key === "income" && formatCurrency(avgIncome)}
                  {key === "expenditure" && formatCurrency(twin.expenditure.recurring_commitments)}
                  {key === "debt" && formatCurrency(twin.debt.total_debt)}
                  {key === "goals" && `${goalCount} active`}
                  {key === "risk" && formatPercent(twin.risk.shock_resilience)}
                  {key === "context" && twin.context.location.split(",")[0]}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6">
        <HealthScoreCard />
      </div>

      <div className="mt-6 glass rounded-2xl p-4">
        <h3 className="mb-3 text-sm font-semibold">Income Profile</h3>
        <div className="grid gap-2 text-sm md:grid-cols-3">
          <div>
            <span className="text-slate-500">Range</span>
            <p>{formatCurrency(twin.income.range_min)} – {formatCurrency(twin.income.range_max)}</p>
          </div>
          <div>
            <span className="text-slate-500">Frequency</span>
            <p className="capitalize">{twin.income.frequency}</p>
          </div>
          <div>
            <span className="text-slate-500">Variability</span>
            <p>{formatPercent(twin.income.variability_index)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
