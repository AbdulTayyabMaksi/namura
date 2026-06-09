"use client";

import { motion } from "framer-motion";
import dynamic from "next/dynamic";
import Link from "next/link";
import {
  ArrowRight,
  Brain,
  Globe,
  Mic,
  Shield,
  Sparkles,
  Users,
} from "lucide-react";

const DigitalTwinScene = dynamic(() => import("@/components/3d/DigitalTwinScene"), {
  ssr: false,
  loading: () => <div className="h-full w-full bg-[#0a0f1c]" />,
});

const FEATURES = [
  {
    icon: Brain,
    title: "Living Digital Twin",
    desc: "6-dimensional AI model of your financial life that evolves with every interaction",
  },
  {
    icon: Sparkles,
    title: "Future Self Simulator",
    desc: "1,000 Monte Carlo simulations across 3 parallel timelines for every major decision",
  },
  {
    icon: Users,
    title: "6-Agent Architecture",
    desc: "Behavior, Risk, Goal, Nudge, Scheme & Guard agents coordinated by LangGraph",
  },
  {
    icon: Globe,
    title: "10 Indian Languages",
    desc: "Voice-first UI with Bhashini STT/TTS for Hindi, Marathi, Kannada and more",
  },
  {
    icon: Mic,
    title: "Voice-Only Mode",
    desc: "WCAG AAA accessible — complete financial flows without touching the screen",
  },
  {
    icon: Shield,
    title: "SEBI Compliant",
    desc: "Guard Agent filters investment advice; educational information only",
  },
];

const PERSONAS = [
  { name: "Priya", role: "Teacher, Thane", income: "₹35K/mo", color: "#3b82f6" },
  { name: "Rajesh", role: "Gig Worker, Mumbai", income: "₹15-40K/mo", color: "#ef4444" },
  { name: "Kisan", role: "Farmer, Karnataka", income: "Seasonal", color: "#22c55e" },
  { name: "Divya", role: "Visual Impairment, Pune", income: "₹25K/mo", color: "#8b5cf6" },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0a0f1c]">
      <div className="absolute inset-0 z-0 opacity-60">
        <DigitalTwinScene interactive />
      </div>

      <div className="relative z-10">
        <nav className="flex items-center justify-between px-6 py-4 md:px-12">
          <div>
            <h1 className="text-2xl font-bold gradient-text">ArthSaathi 2.0</h1>
            <p className="text-xs text-slate-400">Nomura KakushIN 10.0 · 2027 Batch</p>
          </div>
          <Link
            href="/dashboard"
            className="flex items-center gap-2 rounded-full bg-emerald-500 px-5 py-2.5 text-sm font-medium text-white transition-all hover:bg-emerald-400 glow-emerald"
          >
            Launch App <ArrowRight size={16} />
          </Link>
        </nav>

        <section className="px-6 py-20 text-center md:px-12 md:py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="mb-4 inline-block rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-1.5 text-xs text-emerald-400">
              Agentic AI · Financial Digital Twin
            </span>
            <h2 className="mx-auto max-w-4xl text-4xl font-bold leading-tight md:text-6xl">
              Your Financial Future,{" "}
              <span className="gradient-text">Simulated in 3D</span>
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
              ArthSaathi 2.0 creates a living AI model of your financial life — simulating
              thousands of future scenarios in your language, for gig workers, farmers,
              teachers, and every underserved Indian.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link
                href="/dashboard"
                className="flex items-center gap-2 rounded-full bg-emerald-500 px-8 py-3.5 font-semibold text-white transition-all hover:scale-105 hover:bg-emerald-400 glow-emerald"
              >
                Start Your Digital Twin <ArrowRight size={18} />
              </Link>
              <a
                href="#features"
                className="rounded-full border border-white/10 bg-white/5 px-8 py-3.5 font-medium text-slate-300 transition-all hover:bg-white/10"
              >
                Explore Features
              </a>
            </div>
          </motion.div>
        </section>

        <section id="personas" className="px-6 py-16 md:px-12">
          <h3 className="mb-8 text-center text-2xl font-bold">Built for Real India</h3>
          <div className="mx-auto grid max-w-4xl gap-4 md:grid-cols-4">
            {PERSONAS.map((p, i) => (
              <motion.div
                key={p.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                className="glass rounded-2xl p-5 text-center transition-all hover:scale-105"
                style={{ borderColor: `${p.color}33` }}
              >
                <div
                  className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full text-lg font-bold"
                  style={{ backgroundColor: `${p.color}20`, color: p.color }}
                >
                  {p.name[0]}
                </div>
                <p className="font-semibold">{p.name}</p>
                <p className="text-xs text-slate-400">{p.role}</p>
                <p className="mt-1 text-xs" style={{ color: p.color }}>
                  {p.income}
                </p>
              </motion.div>
            ))}
          </div>
        </section>

        <section id="features" className="px-6 py-16 md:px-12">
          <h3 className="mb-12 text-center text-2xl font-bold">Complete Feature Set</h3>
          <div className="mx-auto grid max-w-5xl gap-6 md:grid-cols-2 lg:grid-cols-3">
            {FEATURES.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                viewport={{ once: true }}
                className="glass rounded-2xl p-6 transition-all hover:border-emerald-500/20"
              >
                <div className="mb-4 inline-flex rounded-xl bg-emerald-500/10 p-3">
                  <f.icon size={22} className="text-emerald-400" />
                </div>
                <h4 className="mb-2 font-semibold">{f.title}</h4>
                <p className="text-sm text-slate-400">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        <footer className="border-t border-white/5 px-6 py-8 text-center text-xs text-slate-500">
          <p>ArthSaathi 2.0 — Educational information only, not regulated financial advice.</p>
          <p className="mt-1">DPDPA 2023 Compliant · WCAG AAA Accessible · SEBI Guard Agent Active</p>
        </footer>
      </div>
    </div>
  );
}
