import client from "./client";

export interface Metrics {
  api_id: number;
  total_checks: number;
  successful_checks: number;
  failed_checks: number;
  uptime_percentage: number;
  error_rate: number;
  average_response_time: number | null;
  min_response_time: number | null;
  max_response_time: number | null;
}

export interface Check {
  id: number;
  status_code: number | null;
  response_time: number | null;
  success: boolean;
  checked_at: string;
}

export const getMetrics = (id: number) =>
  client.get<Metrics>(`/api/monitored-apis/${id}/metrics`).then((r) => r.data);

export const getChecks = (id: number) =>
  client.get<Check[]>(`/api/monitored-apis/${id}/checks`).then((r) => r.data);