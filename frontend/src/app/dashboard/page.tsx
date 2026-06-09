"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import ChatInterface from "@/components/chat/ChatInterface";
import DigitalTwinPanel from "@/components/twin/DigitalTwinPanel";
import SchemeDiscovery from "@/components/schemes/SchemeDiscovery";
import SimulatorPanel from "@/components/simulate/SimulatorPanel";
import PrivacyPanel from "@/components/settings/PrivacyPanel";
import OnboardingWizard from "@/components/onboarding/OnboardingWizard";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const { userId, activeTab, setPersonas, setTwin, setMessages } = useAppStore();
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        const personas = await api.getPersonas();
        setPersonas(personas);

        if (userId) {
          const [t, history] = await Promise.all([
            api.getTwin(userId),
            api.getChatHistory(userId).catch(() => []),
          ]);
          setTwin(t);
          if (history.length > 0) {
            setMessages(
              history.map((h) => ({
                id: crypto.randomUUID(),
                role: h.role as "user" | "assistant",
                content: h.content,
                timestamp: new Date(h.created_at),
              }))
            );
          }
        } else {
          setShowOnboarding(true);
        }
      } catch {
        setShowOnboarding(true);
      } finally {
        setReady(true);
      }
    }
    init();
  }, [userId, setPersonas, setTwin, setMessages]);

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
  };

  if (!ready) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0a0f1c]">
        <div className="text-center">
          <div className="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-sm text-slate-400">Initializing Digital Twin...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#0a0f1c]">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-hidden" role="main">
          {activeTab === "chat" && <ChatInterface />}
          {activeTab === "twin" && <DigitalTwinPanel />}
          {activeTab === "simulate" && <SimulatorPanel />}
          {activeTab === "schemes" && <SchemeDiscovery />}
          {activeTab === "privacy" && <PrivacyPanel />}
        </main>
      </div>
      {showOnboarding && <OnboardingWizard onComplete={handleOnboardingComplete} />}
    </div>
  );
}
