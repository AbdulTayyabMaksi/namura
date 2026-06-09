"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Check } from "lucide-react";
import { api } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { LANGUAGES } from "@/types";

const STEPS = ["Welcome", "Profile", "Income", "Ready"];

interface OnboardingWizardProps {
  onComplete: () => void;
}

export default function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const { setTwin, setUserId } = useAppStore();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: "",
    occupation: "",
    location: "",
    language: "en",
    income_min: 15000,
    income_max: 35000,
    income_frequency: "monthly",
    persona_id: "" as string,
  });

  const update = (key: string, value: string | number) =>
    setForm((f) => ({ ...f, [key]: value }));

  const finish = async () => {
    setLoading(true);
    try {
      const twin = await api.onboarding({
        ...form,
        persona_id: form.persona_id || undefined,
      });
      setTwin(twin);
      setUserId(twin.user_id);
      onComplete();
    } catch {
      setStep(0);
    } finally {
      setLoading(false);
    }
  };

  const selectDemoPersona = (id: string) => {
    update("persona_id", id);
    finish();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass mx-4 w-full max-w-lg rounded-3xl p-8"
        role="dialog"
        aria-label="Onboarding wizard"
      >
        <div className="mb-6 flex justify-center gap-2">
          {STEPS.map((s, i) => (
            <div
              key={s}
              className={`h-1.5 flex-1 rounded-full transition-all ${
                i <= step ? "bg-emerald-500" : "bg-white/10"
              }`}
              aria-hidden="true"
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div
              key="welcome"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="text-center"
            >
              <h2 className="text-2xl font-bold gradient-text">Welcome to ArthSaathi 2.0</h2>
              <p className="mt-3 text-sm text-slate-400">
                Your AI Financial Digital Twin — simulating your future in your language.
              </p>
              <div className="mt-6 space-y-2">
                <p className="text-xs text-slate-500">Quick start with a demo persona:</p>
                {[
                  { id: "priya", label: "Priya — Teacher, Thane" },
                  { id: "rajesh", label: "Rajesh — Gig Worker, Mumbai" },
                  { id: "kisan", label: "Kisan — Farmer, Karnataka" },
                  { id: "divya", label: "Divya — Visual Impairment, Pune" },
                ].map((p) => (
                  <button
                    key={p.id}
                    onClick={() => selectDemoPersona(p.id)}
                    disabled={loading}
                    className="flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm hover:border-emerald-500/30 hover:bg-emerald-500/5"
                  >
                    {p.label}
                    <ArrowRight size={16} className="text-emerald-400" />
                  </button>
                ))}
              </div>
              <button
                onClick={() => setStep(1)}
                className="mt-4 text-xs text-slate-500 underline hover:text-white"
              >
                Or create your own profile →
              </button>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div key="profile" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <h2 className="mb-4 text-xl font-bold">Your Profile</h2>
              <div className="space-y-3">
                <input
                  placeholder="Full name"
                  value={form.name}
                  onChange={(e) => update("name", e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                  aria-label="Full name"
                />
                <input
                  placeholder="Occupation"
                  value={form.occupation}
                  onChange={(e) => update("occupation", e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                  aria-label="Occupation"
                />
                <input
                  placeholder="Location (City, State)"
                  value={form.location}
                  onChange={(e) => update("location", e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                  aria-label="Location"
                />
                <select
                  value={form.language}
                  onChange={(e) => update("language", e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                  aria-label="Preferred language"
                >
                  {LANGUAGES.map((l) => (
                    <option key={l.code} value={l.code}>
                      {l.label}
                    </option>
                  ))}
                </select>
              </div>
              <button
                onClick={() => setStep(2)}
                disabled={!form.name || !form.occupation}
                className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-3 font-medium text-white hover:bg-emerald-400 disabled:opacity-40"
              >
                Continue <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="income" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
              <h2 className="mb-4 text-xl font-bold">Income Details</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-slate-400">Monthly income range (₹)</label>
                  <div className="mt-1 flex gap-2">
                    <input
                      type="number"
                      value={form.income_min}
                      onChange={(e) => update("income_min", Number(e.target.value))}
                      className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                      aria-label="Minimum income"
                    />
                    <span className="self-center text-slate-500">to</span>
                    <input
                      type="number"
                      value={form.income_max}
                      onChange={(e) => update("income_max", Number(e.target.value))}
                      className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                      aria-label="Maximum income"
                    />
                  </div>
                </div>
                <select
                  value={form.income_frequency}
                  onChange={(e) => update("income_frequency", e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none"
                  aria-label="Income frequency"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="seasonal">Seasonal</option>
                </select>
              </div>
              <button
                onClick={() => setStep(3)}
                className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-3 font-medium text-white hover:bg-emerald-400"
              >
                Continue <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="ready" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/20">
                <Check size={32} className="text-emerald-400" />
              </div>
              <h2 className="text-xl font-bold">Your Digital Twin is Ready!</h2>
              <p className="mt-2 text-sm text-slate-400">
                6 AI agents will analyze your financial life and simulate your future.
              </p>
              <button
                onClick={finish}
                disabled={loading}
                className="mt-6 w-full rounded-xl bg-emerald-500 py-3 font-medium text-white hover:bg-emerald-400 glow-emerald disabled:opacity-40"
              >
                {loading ? "Creating Twin..." : "Launch ArthSaathi"}
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
