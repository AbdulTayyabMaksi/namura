import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { ChatMessage, DigitalTwin, Persona } from "@/types";

interface AppState {
  userId: string | null;
  twin: DigitalTwin | null;
  personas: Persona[];
  messages: ChatMessage[];
  voiceMode: boolean;
  lowDataMode: boolean;
  sidebarOpen: boolean;
  activeTab: "chat" | "twin" | "schemes" | "simulate" | "privacy";

  setUserId: (id: string | null) => void;
  setTwin: (twin: DigitalTwin | null) => void;
  setPersonas: (personas: Persona[]) => void;
  setMessages: (messages: ChatMessage[]) => void;
  addMessage: (msg: ChatMessage) => void;
  clearMessages: () => void;
  resetSession: () => void;
  setVoiceMode: (v: boolean) => void;
  setLowDataMode: (v: boolean) => void;
  setSidebarOpen: (v: boolean) => void;
  setActiveTab: (tab: AppState["activeTab"]) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      userId: null,
      twin: null,
      personas: [],
      messages: [],
      voiceMode: false,
      lowDataMode: false,
      sidebarOpen: true,
      activeTab: "chat",

      setUserId: (id) => set({ userId: id }),
      setTwin: (twin) => set({ twin, userId: twin?.user_id ?? null }),
      setPersonas: (personas) => set({ personas }),
      setMessages: (messages) => set({ messages }),
      addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
      clearMessages: () => set({ messages: [] }),
      resetSession: () => set({ userId: null, twin: null, messages: [] }),
      setVoiceMode: (v) => set({ voiceMode: v }),
      setLowDataMode: (v) => set({ lowDataMode: v }),
      setSidebarOpen: (v) => set({ sidebarOpen: v }),
      setActiveTab: (tab) => set({ activeTab: tab }),
    }),
    { name: "arthsaathi-store", partialize: (s) => ({ userId: s.userId, voiceMode: s.voiceMode, lowDataMode: s.lowDataMode }) }
  )
);
