const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `API error ${res.status}`);
  }
  return res.json();
}

export const api = {
  health: () => fetchAPI<{ status: string }>("/health"),

  getPersonas: () => fetchAPI<import("@/types").Persona[]>("/api/v1/personas"),

  getTwin: (userId: string) =>
    fetchAPI<import("@/types").DigitalTwin>(`/api/v1/twin/${userId}`),

  chat: (userId: string, message: string, voiceMode = false, lowDataMode = false) =>
    fetchAPI<{
      message: string;
      agents_used: string[];
      scenarios?: import("@/types").ScenarioBranch[];
      nudge?: Record<string, unknown>;
      schemes?: Record<string, unknown>[];
      disclaimer: string;
      audio_summary?: string;
    }>("/api/v1/chat", {
      method: "POST",
      body: JSON.stringify({
        user_id: userId,
        message,
        voice_mode: voiceMode,
        low_data_mode: lowDataMode,
      }),
    }),

  simulate: (userId: string, question: string) =>
    fetchAPI<{ scenarios: import("@/types").ScenarioBranch[]; computation_ms: number }>(
      "/api/v1/simulate",
      {
        method: "POST",
        body: JSON.stringify({ user_id: userId, question }),
      }
    ),

  getSchemes: (userId: string) =>
    fetchAPI<import("@/types").Scheme[]>(`/api/v1/schemes/${userId}`),

  onboarding: (data: {
    name: string;
    occupation: string;
    location: string;
    language: string;
    income_min: number;
    income_max: number;
    income_frequency: string;
    persona_id?: string;
  }) =>
    fetchAPI<import("@/types").DigitalTwin>("/api/v1/onboarding", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  nudgeFeedback: (userId: string, nudgeId: string, action: string) =>
    fetchAPI<{ received: boolean }>("/api/v1/nudge/feedback", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, nudge_id: nudgeId, action }),
    }),

  getChatHistory: (userId: string) =>
    fetchAPI<{ role: string; content: string; created_at: string }[]>(
      `/api/v1/chat/${userId}/history`
    ),

  getHealthScore: (userId: string) =>
    fetchAPI<{
      score: number;
      grade: string;
      label: string;
      breakdown: Record<string, number>;
      top_action: string;
    }>(`/api/v1/twin/${userId}/health-score`),

  deleteTwin: (userId: string) =>
    fetchAPI<{ deleted: boolean }>(`/api/v1/twin/${userId}`, { method: "DELETE" }),
};
