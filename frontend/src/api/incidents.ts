import client from "./client";

export interface Incident {
  id: number;
  api_id: number;
  status: string;
  severity: string;
  failure_count: number;
  started_at: string;
  resolved_at: string | null;
  last_error: string | null;
  resolution_time: number | null;
}

export interface AiAnalysis {
  severity: string;
  probable_cause: string;
  evidence: string[];
  recommendation: string[];
  summary: string;
}

export const listIncidents = () =>
  client.get<Incident[]>("/api/incidents").then((r) => r.data);

export const analyzeIncident = (id: number) =>
  client.post<AiAnalysis>(`/api/incidents/${id}/analyze`).then((r) => r.data);

export const getAnalysis = (id: number) =>
  client.get<AiAnalysis>(`/api/incidents/${id}/analysis`).then((r) => r.data);