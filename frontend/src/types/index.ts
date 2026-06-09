export type Language =
  | "en" | "hi" | "mr" | "kn" | "ta" | "te" | "bn" | "gu" | "pa" | "ml";

export interface Persona {
  id: string;
  name: string;
  occupation: string;
  location: string;
  language: Language;
  persona_id: string | null;
  archetype: string;
}

export interface DigitalTwin {
  user_id: string;
  persona_id?: string;
  name: string;
  income: {
    sources: string[];
    frequency: string;
    range_min: number;
    range_max: number;
    variability_index: number;
    historical: number[];
  };
  expenditure: {
    categories: Record<string, number>;
    recurring_commitments: number;
    discretionary_spend: number;
    impulse_triggers: string[];
  };
  debt: {
    loans: Record<string, unknown>[];
    total_debt: number;
    predatory_risk_score: number;
    monthly_emi: number;
  };
  goals: {
    short_term: Record<string, unknown>[];
    medium_term: Record<string, unknown>[];
    long_term: Record<string, unknown>[];
  };
  risk: {
    risk_appetite: string;
    fraud_vulnerability: number;
    insurance_gaps: string[];
    shock_resilience: number;
  };
  context: {
    location: string;
    language: Language;
    literacy_level: string;
    disability_flags: string[];
    occupation: string;
    seasonal_calendar: string[];
  };
  behavioral_archetype: string;
  behavioral_score: number;
  version: number;
  updated_at: string;
}

export interface ScenarioBranch {
  label: string;
  path_type: string;
  description: string;
  month_6: Record<string, number>;
  month_12: Record<string, number>;
  month_36: Record<string, number>;
  debt_trap_probability: number;
  savings_trajectory: number[];
  goal_impact: string;
  nudge_action: string;
  color: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  scenarios?: ScenarioBranch[];
  nudge?: Record<string, unknown>;
  schemes?: Record<string, unknown>[] | Scheme[];
  timestamp: Date;
}

export interface Scheme {
  id: string;
  name: string;
  benefit_amount: string;
  eligibility: string;
  application_link: string;
  difficulty: number;
  steps: string[];
  estimated_value: number;
}

export const LANGUAGES: { code: Language; label: string }[] = [
  { code: "en", label: "English" },
  { code: "hi", label: "हिंदी" },
  { code: "mr", label: "मराठी" },
  { code: "kn", label: "ಕನ್ನಡ" },
  { code: "ta", label: "தமிழ்" },
  { code: "te", label: "తెలుగు" },
  { code: "bn", label: "বাংলা" },
  { code: "gu", label: "ગુજરાતી" },
  { code: "pa", label: "ਪੰਜਾਬੀ" },
  { code: "ml", label: "മലയാളം" },
];
