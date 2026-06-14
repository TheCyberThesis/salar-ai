export type SupportedDomain =
  | "lost_or_stolen_vehicle_device"
  | "utility_bill_overcharging"
  | "workplace_harassment_women"
  | "unsupported";

export type Stage = "unsupported" | "collecting_missing_info" | "ready_to_generate";

export type SourceNote = {
  title: string;
  source_name: string;
  authority_type?: string | null;
  jurisdiction: string;
  source_url?: string | null;
  verified_at?: string | null;
  confidence_level: string;
};

export type ChatResponse = {
  session_id: string;
  reply: string;
  stage: Stage;
  missing_fields: string[];
  category: SupportedDomain;
  subcategory?: string | null;
  detected_language: string;
  follow_up_questions: string[];
  sources: SourceNote[];
};

export type ChatMessage = {
  id: string;
  role: "assistant" | "user";
  content: string;
  createdAt: string;
};

export type ReportResponse = {
  report_id: string;
  session_id: string;
  summary: string;
  category: SupportedDomain;
  subcategory?: string | null;
  department: string;
  user_provided_details: Record<string, unknown>;
  missing_information: string[];
  required_documents: string[];
  step_by_step_procedure: string[];
  complaint_draft: string;
  where_to_submit: string;
  maps_link: string;
  proof_to_collect: string[];
  timeline: string;
  escalation_steps: string[];
  safety_privacy_notes: string[];
  sources_used: SourceNote[];
  disclaimer: string;
};

export type UserLocation = {
  city?: string;
  area?: string;
  province?: string;
};
