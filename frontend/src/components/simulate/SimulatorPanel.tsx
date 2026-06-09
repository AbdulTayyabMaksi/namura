"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2, Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import ScenarioCards from "@/components/scenario/ScenarioCards";
import type { ScenarioBranch } from "@/types";

const DEMO_QUESTIONS = [
  "Should I take a ₹50,000 personal loan?",
  "What if I start saving ₹120 per day?",
  "Can I afford a home loan in 5 years?",
];

export default function SimulatorPanel() {
  const { userId } = useAppStore();
  const [question, setQuestion] = useState("");
  const [scenarios, setScenarios] = useState<ScenarioBranch[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [computeMs, setComputeMs] = useState(0);

  const runSimulation = async (q: string) => {
    if (!userId || !q.trim()) return;
    setLoading(true);
    setScenarios(null);
    try {
      const res = await api.simulate(userId, q);
      setScenarios(res.scenarios);
      setComputeMs(res.computation_ms);
    } catch {
      /* handled */
    } finally {
      setLoading(false);
    }
  };

  if (!userId) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        Select a persona to run Future Self Simulator
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-6" role="region" aria-label="Future Self Simulator">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 text-center"
      >
        <div className="mb-3 inline-flex rounded-2xl bg-violet-500/10 p-3">
          <Sparkles size={32} className="text-violet-400" />
        </div>
        <h2 className="text-2xl font-bold gradient-text">Future Self Simulator</h2>
        <p className="mt-2 text-sm text-slate-400">
          1,000 Monte Carlo simulations × 3 parallel timelines
        </p>
      </motion.div>

      <div className="mx-auto mb-6 max-w-xl">
        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a major financial decision..."
            className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none focus:border-violet-500/50"
            aria-label="Simulation question"
          />
          <button
            onClick={() => runSimulation(question)}
            disabled={loading || !question.trim()}
            className="rounded-xl bg-violet-500 px-6 py-3 text-sm font-medium text-white hover:bg-violet-400 disabled:opacity-40 glow-violet"
            aria-label="Run simulation"
          >
            {loading ? <Loader2 size={18} className="animate-spin" /> : "Simulate"}
          </button>
        </div>

        <div className="mt-3 flex flex-wrap justify-center gap-2">
          {DEMO_QUESTIONS.map((q) => (
            <button
              key={q}
              onClick={() => {
                setQuestion(q);
                runSimulation(q);
              }}
              className="rounded-full border border-white/10 px-3 py-1.5 text-xs text-slate-400 hover:border-violet-500/30 hover:text-violet-300"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="text-center" aria-live="polite">
          <Loader2 size={24} className="mx-auto animate-spin text-violet-400" />
          <p className="mt-2 text-sm text-slate-400">
            Running 1,000 Monte Carlo simulations across 6 agents...
          </p>
          <div className="mx-auto mt-4 h-1.5 max-w-xs overflow-hidden rounded-full bg-white/5">
            <motion.div
              className="h-full bg-violet-500"
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{ duration: 3, ease: "easeInOut" }}
            />
          </div>
        </div>
      )}

      {scenarios && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <p className="mb-4 text-center text-xs text-slate-500">
            Computed in {computeMs}ms · Informed choice, not paternalistic advice
          </p>
          <ScenarioCards scenarios={scenarios} />
        </motion.div>
      )}
    </div>
  );
}
