"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Mic, Loader2, Bot, User } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { api } from "@/lib/api";
import ScenarioCards from "@/components/scenario/ScenarioCards";
import NudgeCard from "@/components/nudge/NudgeCard";
import MarkdownMessage from "@/components/chat/MarkdownMessage";
import SchemeChips from "@/components/chat/SchemeChips";
import { cn } from "@/lib/utils";

const SUGGESTIONS = [
  "What is Reliance Industries stock price today?",
  "Compare TCS vs Infosys for long-term investing",
  "Should I take a ₹50,000 personal loan?",
  "Explain SIP vs lump sum investing in simple terms",
  "What government schemes am I eligible for?",
  "How does inflation affect my savings?",
];

export default function ChatInterface() {
  const { userId, messages, addMessage, voiceMode, lowDataMode, twin } = useAppStore();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (typeof window !== "undefined" && ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)) {
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SR();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.onresult = (e) => {
        const text = e.results[0][0].transcript;
        setInput(text);
        setListening(false);
      };
      recognitionRef.current.onerror = () => setListening(false);
    }
  }, []);

  const speak = (text: string) => {
    if (!voiceMode || typeof window === "undefined") return;
    const utterance = new SpeechSynthesisUtterance(text.replace(/[*_#]/g, ""));
    utterance.lang = twin?.context.language === "hi" ? "hi-IN" : "en-IN";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  };

  const sendMessage = async (text: string) => {
    if (!text.trim() || !userId || loading) return;

    const userMsg = {
      id: crypto.randomUUID(),
      role: "user" as const,
      content: text.trim(),
      timestamp: new Date(),
    };
    addMessage(userMsg);
    setInput("");
    setLoading(true);

    try {
      const res = await api.chat(userId, text.trim(), voiceMode, lowDataMode);
      const assistantMsg = {
        id: crypto.randomUUID(),
        role: "assistant" as const,
        content: res.message,
        scenarios: lowDataMode ? undefined : res.scenarios,
        nudge: res.nudge,
        schemes: res.schemes as Record<string, unknown>[] | undefined,
        timestamp: new Date(),
      };
      addMessage(assistantMsg);

      if (voiceMode) {
        speak(res.audio_summary || res.message.slice(0, 500));
      }
    } catch {
      addMessage({
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Sorry, I couldn't process that. Please ensure the backend is running on port 8000.",
        timestamp: new Date(),
      });
    } finally {
      setLoading(false);
    }
  };

  const startListening = () => {
    if (!recognitionRef.current) return;
    setListening(true);
    recognitionRef.current.start();
  };

  return (
    <div
      className={cn(
        "flex h-full flex-col",
        voiceMode && twin?.context.disability_flags?.includes("visual_impairment") && "voice-only-mode"
      )}
      role="region"
      aria-label="Chat with Saathi AI"
    >
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center py-12 text-center"
          >
            <div className="mb-4 rounded-2xl bg-emerald-500/10 p-4">
              <Bot size={40} className="text-emerald-400" />
            </div>
            <h3 className="text-xl font-semibold">Ask your Financial Saathi anything</h3>
            <p className="mt-2 max-w-md text-sm text-slate-400">
              Ask any financial question — stocks, companies, loans, taxes, mutual funds,
              government schemes, or personal finance. Powered by 6 AI agents + live market data.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs hover:bg-emerald-500/10 hover:border-emerald-500/30 transition-all"
                  aria-label={`Ask: ${s}`}
                >
                  {s}
                </button>
              ))}
            </div>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={cn("flex gap-3", msg.role === "user" ? "justify-end" : "justify-start")}
            >
              {msg.role === "assistant" && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500/20">
                  <Bot size={16} className="text-emerald-400" />
                </div>
              )}
              <div
                className={cn(
                  "max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
                  msg.role === "user"
                    ? "bg-violet-500/20 text-violet-100"
                    : "glass"
                )}
              >
                {msg.role === "assistant" ? (
                  <MarkdownMessage content={msg.content} />
                ) : (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                )}
                {msg.schemes && <SchemeChips schemes={msg.schemes} />}
                {msg.scenarios && !lowDataMode && (
                  <div className="mt-4" aria-label="Scenario comparison charts">
                    <ScenarioCards scenarios={msg.scenarios} />
                  </div>
                )}
                {msg.nudge && <NudgeCard nudge={msg.nudge} />}
              </div>
              {msg.role === "user" && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-violet-500/20">
                  <User size={16} className="text-violet-400" />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <div className="flex items-center gap-2 text-sm text-slate-400" aria-live="polite">
            <Loader2 size={16} className="animate-spin" />
            Analyzing with 6 AI agents and generating your personalized answer...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="border-t border-white/5 p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage(input);
          }}
          className="flex items-center gap-2"
        >
          <button
            type="button"
            onClick={startListening}
            disabled={listening}
            className={cn(
              "rounded-xl p-3 transition-all",
              listening ? "bg-red-500/20 text-red-400" : "bg-white/5 text-slate-400 hover:bg-white/10"
            )}
            aria-label="Voice input"
          >
            <Mic size={18} className={listening ? "animate-pulse" : ""} />
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={voiceMode ? "Speak or type any financial question..." : "Ask about stocks, companies, loans, taxes, anything..."}
            className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none focus:border-emerald-500/50"
            aria-label="Chat message input"
            disabled={!userId}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading || !userId}
            className="rounded-xl bg-emerald-500 p-3 text-white transition-all hover:bg-emerald-400 disabled:opacity-40 glow-emerald"
            aria-label="Send message"
          >
            <Send size={18} />
          </button>
        </form>
        <p className="mt-2 text-center text-[10px] text-slate-500">
          Educational information only — not regulated financial advice (SEBI compliant)
        </p>
      </div>
    </div>
  );
}
