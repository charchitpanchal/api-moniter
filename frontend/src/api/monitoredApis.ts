import client from "./client";

export interface MonitoredApi {
  id: number;
  user_id: number;
  name: string;
  url: string;
  method: string;
  expected_status_code: number;
  monitoring_interval: number;
  timeout: number;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface MonitoredApiCreate {
  name: string;
  url: string;
  method: string;
  expected_status_code: number;
  monitoring_interval: number;
  timeout: number;
}

export const listMonitoredApis = () =>
  client.get<MonitoredApi[]>("/api/monitored-apis").then((r) => r.data);

export const createMonitoredApi = (payload: MonitoredApiCreate) =>
  client.post<MonitoredApi>("/api/monitored-apis", payload).then((r) => r.data);

export const deleteMonitoredApi = (id: number) =>
  client.delete(`/api/monitored-apis/${id}`);

export const toggleMonitoredApi = (id: number, enable: boolean) =>
  client.patch<MonitoredApi>(`/api/monitored-apis/${id}/${enable ? "enable" : "disable"}`);