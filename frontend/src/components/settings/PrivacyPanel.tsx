"use client";

import { useState } from "react";
import { Trash2, Shield, Download } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";

export default function PrivacyPanel() {
  const { userId, twin, resetSession } = useAppStore();
  const [status, setStatus] = useState("");

  const handleDelete = async () => {
    if (!userId || !confirm("Delete your Digital Twin and all data? This cannot be undone (DPDPA right to erasure).")) return;
    try {
      await api.deleteTwin(userId);
      resetSession();
      setStatus("Your data has been permanently deleted.");
    } catch {
      setStatus("Failed to delete data. Please try again.");
    }
  };

  const handleExport = async () => {
    if (!userId) return;
    try {
      const [t, history] = await Promise.all([
        api.getTwin(userId),
        api.getChatHistory(userId),
      ]);
      const blob = new Blob([JSON.stringify({ twin: t, chat_history: history }, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `arthsaathi-data-${userId}.json`;
      a.click();
      setStatus("Data exported successfully.");
    } catch {
      setStatus("Export failed.");
    }
  };

  if (!userId) return null;

  return (
    <div className="h-full overflow-y-auto p-6" role="region" aria-label="Privacy and data settings">
      <h2 className="mb-2 text-xl font-bold gradient-text">Privacy & Data (DPDPA 2023)</h2>
      <p className="mb-6 text-sm text-slate-400">
        You have full control over your Digital Twin data per India&apos;s Digital Personal Data Protection Act.
      </p>

      <div className="space-y-4">
        <div className="glass rounded-2xl p-5">
          <div className="mb-3 flex items-center gap-2">
            <Shield size={18} className="text-emerald-400" />
            <h3 className="font-semibold">Your Data</h3>
          </div>
          <p className="text-sm text-slate-400">
            Name: {twin?.name} · Twin v{twin?.version} · Stored in PostgreSQL (encrypted at rest)
          </p>
        </div>

        <button
          onClick={handleExport}
          className="flex w-full items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm hover:bg-white/10"
        >
          <Download size={16} className="text-blue-400" />
          Export My Data (JSON download)
        </button>

        <button
          onClick={handleDelete}
          className="flex w-full items-center gap-3 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-400 hover:bg-red-500/10"
        >
          <Trash2 size={16} />
          Delete All My Data (Right to Erasure)
        </button>

        {status && <p className="text-xs text-slate-400">{status}</p>}
      </div>
    </div>
  );
}
