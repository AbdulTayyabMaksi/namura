"use client";

import { cn } from "@/lib/utils";
import { useAppStore } from "@/lib/store";
import {
  Brain,
  ChevronLeft,
  ChevronRight,
  Landmark,
  MessageSquare,
  Shield,
  Sparkles,
  User,
} from "lucide-react";

const NAV_ITEMS = [
  { id: "chat" as const, label: "Saathi Chat", icon: MessageSquare },
  { id: "twin" as const, label: "Digital Twin", icon: Brain },
  { id: "simulate" as const, label: "Future Simulator", icon: Sparkles },
  { id: "schemes" as const, label: "Govt Schemes", icon: Landmark },
  { id: "privacy" as const, label: "Privacy & Data", icon: Shield },
];

export default function Sidebar() {
  const { sidebarOpen, setSidebarOpen, activeTab, setActiveTab, twin, personas, setUserId, setTwin } =
    useAppStore();

  const selectPersona = async (id: string) => {
    setUserId(id);
    try {
      const { api } = await import("@/lib/api");
      const t = await api.getTwin(id);
      setTwin(t);
    } catch {
      /* handled in dashboard */
    }
  };

  return (
    <aside
      className={cn(
        "glass flex h-full flex-col border-r border-white/5 transition-all duration-300",
        sidebarOpen ? "w-72" : "w-16"
      )}
      aria-label="Main navigation"
    >
      <div className="flex items-center justify-between border-b border-white/5 p-4">
        {sidebarOpen && (
          <div>
            <h1 className="text-lg font-bold gradient-text">ArthSaathi 2.0</h1>
            <p className="text-xs text-slate-400">Financial Digital Twin</p>
          </div>
        )}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="rounded-lg p-2 hover:bg-white/5"
          aria-label={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
        >
          {sidebarOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
        </button>
      </div>

      <nav className="flex-1 space-y-1 p-3" role="navigation">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={cn(
              "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all",
              activeTab === id
                ? "bg-emerald-500/20 text-emerald-400 glow-emerald"
                : "text-slate-400 hover:bg-white/5 hover:text-white"
            )}
            aria-current={activeTab === id ? "page" : undefined}
            aria-label={label}
          >
            <Icon size={18} />
            {sidebarOpen && <span>{label}</span>}
          </button>
        ))}
      </nav>

      {sidebarOpen && (
        <div className="border-t border-white/5 p-3">
          <p className="mb-2 px-2 text-xs font-medium uppercase tracking-wider text-slate-500">
            Demo Personas
          </p>
          <div className="space-y-1">
            {personas.map((p) => (
              <button
                key={p.id}
                onClick={() => selectPersona(p.id)}
                className={cn(
                  "flex w-full items-center gap-2 rounded-lg px-2 py-2 text-left text-xs transition-all hover:bg-white/5",
                  twin?.user_id === p.id && "bg-violet-500/20 text-violet-300"
                )}
                aria-label={`Select persona ${p.name}`}
              >
                <User size={14} />
                <div className="min-w-0 flex-1">
                  <p className="truncate font-medium">{p.name}</p>
                  <p className="truncate text-slate-500">{p.occupation}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </aside>
  );
}
